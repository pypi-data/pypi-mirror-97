# -*- coding: utf-8 -*-
# package: pypos3d.wftk
import sys
import os
import copy
import logging
import traceback
import gzip
import bisect

import numpy as np
from scipy import spatial

from langutil import C_OK, C_FAIL, C_ERROR, GetLowExt
from pypos3d.wftk import WFBasic 
from pypos3d.wftk.WFBasic import C_MISSING_FACEMAT, C_MISSING_MAT, FEPSILON, CoordSyst, FaceNormalOrder
from pypos3d.wftk.WFBasic import LowestIdxPos, findCommonPoints, CreateLoop, FaceVisibility
from pypos3d.wftk.WFBasic import TexCoord2f, Point3d, Vector3d, calcMLS, getOBJFile, Edge, IndexAdd, FaceCut, FaceSplit, CuttingData

from pypos3d.wftk.PoserFileParser import OBJ_FNAT, PoserFileParser
from pypos3d.wftk.Repere import Repere
from pypos3d.wftk.GeomGroup import GeomGroup


class WFMat:
  ''' Simple WaveFront Material.
  Only diffuse color, diffuse map and transparency are managed.
  '''
  
  def __init__(self, name, kd=(0.9, 0.9, 0.9), map_kd=None):
    self.name = name
    self.d = 1.0 # Opacity
    self.kd = kd if len(kd)==4 else kd + (self.d, )
    self.map_kd = map_kd
    # self.ka = (0.0, 0.0, 0.0)
    # self.ks = (0.0, 0.0, 0.0)
    # self.ke = (0.0, 0.0, 0.0)
    # self.illum = 2.0
    

  @classmethod
  def readMtl(cls, libMaterialName):
    logging.info("Loading Material file:%s", libMaterialName)

    rin = open(libMaterialName, 'rt', errors='replace') 

    parser = PoserFileParser(rin)
    matDict = {}
    curMat = None
    
    while True:
      code,lw,rw = parser.getLine()
      lw = lw.lower()
      
      if code==PoserFileParser.TT_WORD:
        if lw=="newmtl": # New material
          curMat = WFMat(rw)
          matDict[rw] = curMat

        elif (lw=="ka") or (lw=="ks") or (lw=='ke') or (lw=='illum'):
          #tv = rw.split()
          #curMat.ka = ( float(tv[0]), float(tv[1]), float(tv[2]), float(tv[3]) )
          pass
        
        elif lw=="kd":
          tv = rw.split()
          curMat.kd = (float(tv[0]), float(tv[1]), float(tv[2]), curMat.d)

        elif lw=="d":
          curMat.d = float(rw)
          curMat.kd = (curMat.kd[0], curMat.kd[1], curMat.kd[2], curMat.d)

        elif lw=="map_kd":
          curMat.map_kd = rw
      elif code==PoserFileParser.TT_EOF:
        break
      else:
        raise Exception("L[%d] - Not Accepted : %s", parser.lineno(), lw)

    rin.close()

    return matDict

  


# =====================================================================================
class WaveGeom(object):
  '''WaveGeom class represent a WaveFront file and a geometric container for 3D objects
  This class represents a Geometry as it can be stored in a WaveFront file or
  embedded in Poser files.


  Design: (memory efficient)

    o-----------------------------------o
    | WaveGeom                          |
    +-----------------------------------+
    | coordList = list of Point3d       |
    |             Shared between groups |
    |                                   |
    | idem for texList and normList     |
    |                                   |     o--------------------------------------------------------o
    | groups = list of GeomGroup  ------|---> | GeomGroup                                              |
    |                                   |     +--------------------------------------------------------+
    o-----------------------------------o     | coordList, texList, normList point to WaveGeom ones    |
                                              |                                                        |
                                              | stripCount = list of int [ Nbface + 1 ]                |
                                              | o------------------------------------------------o     |
                                              | | 0  | 4  | ......                                     |
                                              | o------------------------------------------------o     |
                                              |   f0   f1                                              |
                                              |                                                        |
                                              | vertIdx = list of int[] : Index of Vertex in coordList |
                                              | o------------------------------------------------o     |
                                              | | f0.0 | f0.1 | f0.2 | f0.3 | f1.0 | ....              |
                                              | o------------------------------------------------o     |
                                              |   Here: f0 has 4 vertex - Vertex order determines the  |
                                              |         face normal (ie direct order).                 |
                                              |                                                        |
                                              | tvertIdx and normIdx follow the same organization.     |
                                              | (They shall have the same length as vertIdx, or empty  |
                                              |  if the GeomGroup has no texture or no normal)         |
                                              |                                                        |
                                              o--------------------------------------------------------o

  '''
  # Comparison constants
  VERTEX_EPS = 1e-6
  NORMAL_EPS = 1e-6
  TEX_EPS = 1e-6

  VERTEX_COUNT = 0x0001
  VERTEX_COORD = 0x0002
  TEXCOORD_COUNT = 0x0004
  TEXCOORD_COORD = 0x0008
  NORMAL_COUNT = 0x0010
  NORMAL_COORD = 0x0020
  GROUP_COUNT = 0x0040
  GROUP_NAME = 0x0080
  GROUP_NBFACE = 0x0100
  GROUP_STRIPIDX = 0x0200
  GROUP_NORMPRES = 0x0400
  GROUP_VERTIDX = 0x0800
  GROUP_TVERTIDX = 0x1000
  GROUP_NORMIDX = 0x2000
  MAT_COUNT = 0x4000
  MAT_NAMES = 0x8000


  def _selfInit(self):
    self._name= ''

    #  The vertex list shared between groups
    self.coordList = []

    # The texture coordinates list
    self.texList = [ ] # public TexCoord2f[] 

    #   the normal list
    self.normList = []

    self.lstMat = [ ] # public List<String> ; // List of Material names

    self.curMatIdx = 0

    # Each face's & line's Geometry Group membership is kept here. . .
    # public List<GeomGroup> groups; // key = name of Group, value =
    self.groups = [ ]

    # Current group
    self.curGroup = None # protected AbsGeomGroup 

    self._curWriteMatIdx = 0

    # Name of file
    self._libMaterialName = ''
    self.libMat = {}

  def __init__(self, st=None, filename=None, usemtl=False, imgdirpath='.'):
    ''' Create a Wavefront geometry.
    Initialize temporaly lists for reading operations.
    Parameters
    ----------
    st : optional input file 
      if None, Create an empty WaveGeom with a first default internal group 
      named "default".
      
    usemtl : optional, bool, default is False
      Indicate if material files (*.mtl) shall be read
      
    imgdirpath : optional, str, default is None
      list of directories separated by os.pathsep where to search
      texture files. (for usemtl = True)
      
    '''
    self._selfInit()
    self.setName(filename)
    
    self.curGroup = GeomGroup("default")
    self.curGroup.linkCoordList(self)
    self.usemtl = False
    self.imgdirpath = imgdirpath

    if st:
      self.usemtl = usemtl
      
      self.readInternal(st)
      
      if self.usemtl and self._libMaterialName:
        # Load the given .mtl File
        try:
          filedir = os.path.dirname(filename)
          
          self.libMat = WFMat.readMtl(os.path.join(filedir, self._libMaterialName))
          
          # TODO: Check Material usage in groups
        except FileNotFoundError:
          logging.warning("Material file read Error:%s", self._libMaterialName)
          
    else:
      # When the WaveGeom is not created from a file 
      # a default material is required
      self.addMaterial("default") 
      
    #except Exception as e: # Should
    #  logging.error("Error:%s", str(e))

  def setName(self, n):
    self._name = n

  def getName(self): return self._name
  def getGroups(self): return self.groups
  def getMaterialList(self): return self.lstMat
  def getMaterialLibName(self): return self._libMaterialName  

  def setTexList(self, ntextab):
    self.texList = ntextab

  def compareTo(self, wg): # WaveGeom wg)
    res = 0

    if self.getCoordListLength() != wg.getCoordListLength():
      return WaveGeom.VERTEX_COUNT

    if self.getTexListLength() != wg.getTexListLength():
      return WaveGeom.TEXCOORD_COUNT

    if len(self.getGroups()) != len(wg.getGroups()):
      return WaveGeom.GROUP_COUNT

    if len(self.getMaterialList()) != len(wg.getMaterialList()):
      return WaveGeom.MAT_COUNT

    # Compare Vertex
    vertex_dist = self.compareVertexList(wg, WaveGeom.VERTEX_EPS, False)
    if vertex_dist > WaveGeom.VERTEX_EPS:
      return WaveGeom.VERTEX_COORD

    # Compare Texture Coordinates
    tex_dist = self.compareTextureList(wg, WaveGeom.TEX_EPS, False)
    if tex_dist > WaveGeom.TEX_EPS:
      return WaveGeom.TEXCOORD_COORD

    # Compare Materials
    #for (int i = 0; i < getMaterialList().size(); i++)
      #{
    if self.getMaterialList() != wg.getMaterialList():
      return WaveGeom.MAT_NAMES

    #  Compare Groups
#   for (int nogrp = 0; nogrp < getGroups().size(); nogrp++)
#      {
#      AbsGeomGroup g1 = (AbsGeomGroup) getGroups().get(nogrp)
#      AbsGeomGroup g2 = (AbsGeomGroup) wg.getGroups().get(nogrp)
#
#      if (!g1.getName().equals(g2.getName()))
#        {
#        return GROUP_NAME
#        }
#
#      if (g1.getNbFace() != g2.getNbFace())
#        {
#        return GROUP_NBFACE
#        }
#
#      for (int faceno = 0; faceno < g1.getNbFace(); faceno++)
#        {
#        int startIdx1 = g1.stripCount[faceno]
#        int lastIdx1 = g1.stripCount[faceno + 1]
#        int startIdx2 = g2.stripCount[faceno]
#        int lastIdx2 = g2.stripCount[faceno + 1]
#
#        if ((startIdx1 != startIdx2) || (lastIdx1 != lastIdx2))
#          {
#          return GROUP_STRIPIDX
#          }
#
#        boolean w2 = (g1.normIdx == null) || (g1.normIdx.length == 0)
#        boolean w3 = (g2.normIdx == null) || (g2.normIdx.length == 0)
#        if (w2 != w3)
#          {
#          return GROUP_NORMPRES
#          }
#
#        for (int i = startIdx1; i < lastIdx1; i++)
#          {
#          if (g1.vertIdx[i] != g2.vertIdx[i])
#            {
#            return GROUP_VERTIDX
#            }
#          if (g1.tvertIdx[i] != g2.tvertIdx[i])
#            {
#            return GROUP_TVERTIDX
#            }
#
#          if (!w2)
#            {
#            if (g1.normIdx[i] != g2.normIdx[i])
#              {
#              return GROUP_NORMIDX
#              }
#            }
#          }
#        }
#      }
#
#    if (getNormListLength() != wg.getNormListLength())
#      {
#      return NORMAL_COUNT
#      }
#
#    // Compare Normals
#    double normal_dist = compareNormalList(wg, NORMAL_EPS, false)
#    if (normal_dist > NORMAL_EPS)
#      {
#      return NORMAL_COORD
#      }
#
    return res

  def copy(self): # return WaveGeom wg
    ''' Return a deep copy of self '''
    wg = self.copyData()

    wg.setName(self._name)

    wg.texList = [ TexCoord2f(t) for t in self.texList ]

    wg.lstMat = [ s for s in self.lstMat ]
    wg._libMaterialName = self._libMaterialName

    # Each face's Geometry Group membership is kept here. . .
    wg.groups = [ GeomGroup(src=ggd, inCoordList=wg.coordList) for ggd in self.groups ]

    # Link correctly groups
    # FIX a major error
    wg.optimizeGroups()

    return wg

  def addMaterial(self, matName):
    ''' Add a material name to the list of materials.
    Search for existing material, if it already exists return the found index, 
    else add it at the end of the list.
    Set .curMatIdx to the new material index

    Parameters
    ----------
    matName : str
       Name of the material to add.
    Returns:
    int : The index of the material name in the list.
    '''
    try:
      i = self.lstMat.index(matName)
      self.curMatIdx = i

    except ValueError:
      self.lstMat.append(matName)
      self.curMatIdx = len(self.lstMat) - 1
      
    self.curGroup.setMaterialName(self.curMatIdx)

    return self.curMatIdx

  def selectMaterial(self, matName):
    ''' Select a material name as default current value (for read operation)
    Set .curMatIdx to the new material index

    Parameters
    ----------
    matName : str
       Name of the material to add.
    Returns:
    int : The index of the material name in the list.
    '''
    try:
      self.curMatIdx = self.lstMat.index(matName)

    except ValueError:
      self.curMatIdx = - 1
      
    self.curGroup.setMaterialName(self.curMatIdx)

    return self.curMatIdx


  def sanityCheck(self):
    ''' Check the consistency of a WaveGeom. '''
    
    gret = C_OK
    
    for grp in self.groups:
      print('Checking Group[{:s}]:'.format(grp.getName()))
      ret = grp.sanityCheck()
      if ret!=C_OK:
        print('Group has errors')
        gret = min(gret, ret)
        
    return gret


  # TODO Accelerate with KDTree and PaveList2D
  def optimizeGroups(self, cleaning=False):
    ''' Optimize the groups of this WaveGeom.
    After Vertex and texture coordinates are uniq.
    O(n2) long algorythm.
    '''
    if cleaning:
      hasTexture = (self.texList!=None) and (len(self.texList) > 0)
      nbInit = len(self.coordList)
      mapVert = [-1] * nbInit
      mapTVert = [-1] * len(self.texList) if hasTexture else None
      
      nCoordList = [ ]
      nTexList = []
      
      for grp in self.groups:
        for i,vi in enumerate(grp.vertIdx):
          nvi = mapVert[vi]
          if nvi<0:
            nvi = IndexAdd(nCoordList, self.coordList[vi])
            mapVert[vi] = nvi
          
          grp.vertIdx[i] = nvi
        
        if hasTexture:          
          for i,vti in enumerate(grp.tvertIdx):
            nvti = mapTVert[vti]
            if nvti<0:
              nvti = IndexAdd(nTexList, self.texList[vti])
              mapTVert[vti] = nvti
          
            grp.tvertIdx[i] = nvti

      self.coordList = nCoordList
      self.texList = nTexList
      
      logging.info("Vertex Optimization=%d/%d", len(self.coordList), nbInit)
    
    for gg in self.groups:
      gg.linkCoordList(self)

  #
  #    * @see deyme.v3d.wf.WaveGeom#createGeomGroup(java.lang.String)
  #    
  def createGeomGroup(self, name):
    ''' Create a new GeomGroup in the WaveGeom.
    Return the already existing one if the same name exists.
    Parameters
    ----------
    name : str
      Name of the new GeomGroup
    '''
    gg = None
    #  Very rare : need to create a group with a name
    if name:
      gg = self.getGroup(name)
    else:
      name = "default"
      no = 0
      while True:
        name = name + str(no)
        gg = self.getGroup(name)
        no += 1
        if not gg:
          break

    if not gg:
      gg = GeomGroup(name)
      gg.linkCoordList(self)
      #  Bug found : 10FEV2008
      self.groups.append(gg)

    return gg

  # public void readInternal(PoserFileParser st)
  def readInternal(self, st): # PoserFileParser st)
    ''' Internal WaveGeom reader '''
    numbVerts, numbTVerts, numbTSets, numbElems, numbSets = -1, -1, -1, -1, -1

    fin = False
    while not fin:
      code,lw,rw = st.getLine()
      
      if code == PoserFileParser.TT_WORD:
        if lw=="v":
          self.coordList.append(st.readVertex())
          continue

        if lw=="vt":
          self.texList.append(st.readTexture())
          continue

        if lw=="vn":
          # Ignore normals
          self.normList.append(st.readNormal())
          continue

        if lw=="f":
          self.readFace(st)
          continue

        if lw=="l":
          self.readLine(st)
          continue

        if lw=="numbVerts":
          numbVerts = int(rw)
          continue

        if lw=="numbTVerts":
          numbTVerts = int(rw)
          continue

        if lw=="numbTSets":
          numbTSets = int(rw)
          continue

        if lw=="numbElems":
          numbElems = int(rw)
          continue

        if lw=="numbSets":
          numbSets = int(rw)
          continue

        if lw=='usemtl':
          # FIX 20110314-ODY: Material names could contain white chars and others (like #)
          self.addMaterial(rw)
          continue

        if lw=="s":
          continue

        if lw=="g":
          self.curGroup = self.createGeomGroup(rw)
          self.curGroup.setMaterialName(self.curMatIdx)
          continue

        # Record mtllibs that could be read and resolved later
        if lw=='mtllib': # rw should read a FILENAME
          if st.getFileNature()==OBJ_FNAT:
            self._libMaterialName = rw
          continue

        if (lw[0]=="g") and (len(st.sval) > 1):
          # Strange case where there's no space after 'g' (OBJ regular ??)
          self.curGroup = self.createGeomGroup(lw[1:])
          self.curGroup.setMaterialName(self.curMatIdx)
          continue

      elif (code==PoserFileParser.TT_RIGHTBRACKET) or (code==code==PoserFileParser.TT_EOF):
        fin = True
      else:
        # log.warning("L[" + st.lineno() + "] - Not Accepted :" + lw)
        raise Exception("L[%d] - Not Accepted : %s", st.lineno(), lw)

    # Ensure that the default group is kept (may append)
    if ((st.getFileNature() != OBJ_FNAT) and not self.groups) or \
        (not self.curGroup in self.groups):
      self.groups.append(self.curGroup)      

    # Close Groups
    self.optimizeGroups()

    # return a tuple of values (for Poser usage)
    return (numbVerts, numbTVerts, numbTSets, numbElems, numbSets)

    

  def readFace(self, st): # throws ParsingErrorException
    ''' Adds the indices of the current face to the arrays.
     
    ViewPoint files can have up to three arrays: Vertex Positions, Texture
    Coordinates, and Vertex Normals. Each vertex can contain indices into all
    three arrays.
    '''
    vertIndex = 0
    texIndex = 0
    normIndex = 0

    coordIdxList = [ ]
    texIdxList = [ ]
    normIdxList = [ ]
     
    #   There are n vertices on each line. Each vertex is comprised
    #   of 1-3 numbers separated by slashes ('/'). The slashes may
    #   be omitted if there's only one number.

    line = st.rval

    tabVert = line.split(" ")

    if tabVert:
      for i in range( 0, len(tabVert)):
        sana = tabVert[i]
        posS1 = sana.find('/')
        vertIndex = int(sana[0:posS1] if (posS1 > 0) else sana) - 1

        if vertIndex < 0:
          # FIX 20081231 : when reading a file, the real coord list is unknown 
          # ==> Use the temporary list
          vertIndex += len(self.coordList) + 1

        coordIdxList.append(vertIndex)

        if posS1 > 0:
          posS2 = sana.find('/', posS1 + 1)

          if posS2 > 0:
            if (posS2 > posS1 + 1):
              texIndex = int(sana[posS1+1:posS2]) - 1
              if (texIndex < 0):
                # FIX 20081231 : when reading a file, the real coord list is unknown 
                texIndex += len(self.texList) + 1

              texIdxList.append(texIndex)

            if (posS2 < len(sana) - 1):
              normIndex = int(sana[posS2 + 1:]) - 1
              if (normIndex < 0):
                # FIX 20081231 : when reading a file, the real coord list is unknown 
                normIndex += len(self.normList) + 1

              normIdxList.append(normIndex)
          else:
            texIndex = int(sana[posS1 + 1:]) - 1
            if (texIndex < 0):
              # FIX 20081231 : when reading a file, the real coord list is unknown 
              texIndex += len(self.texList) + 1

            texIdxList.append(texIndex)

      # Add face to current groups
      self.curGroup.addFace(coordIdxList, texIdxList, normIdxList)
    # // End of readFace

  def readLine(self, st):
    ''' Adds the indices of the current line to the arrays.
    ViewPoint files can have up to two arrays: Vertex Positions, Texture
    Coordinates. Each vertex can contain indices into all two arrays.
    '''
  
    vertIndex = 0
    texIndex = 0

    coordIdxList = [ ] # .clear()
    texIdxList = [ ] # .clear()
    # There are n vertices on each line. Each vertex is comprised
    # of 1-2 numbers separated by slashes ('/'). The slashes may
    # be omitted if there's only one number.
    # st.getToken()
    line = st.rval
    tabVert = line.split(" ")

    if tabVert:
      for i in range( 0, len(tabVert)):
        sana = tabVert[i]
        posS1 = sana.find('/')
        vertIndex = int(sana[0:posS1] if (posS1 > 0) else sana) - 1

        if vertIndex < 0: # Relative Index
          vertIndex += len(self.coordList) + 1

        coordIdxList.append(vertIndex)

        if posS1 > 0:
          posS2 = sana.find('/', posS1 + 1)

          if posS2 > 0:
            if (posS2 > posS1 + 1):
              texIndex = int(sana[posS1+1:posS2]) - 1
              if (texIndex < 0):
                texIndex += len(self.texList) + 1

              texIdxList.append(texIndex)
      # End Of for

      # Add face to current groups
      self.curGroup.addLine(coordIdxList, texIdxList)
    # End of readLine

  # FIXME: 20200713 def getTexListLength(self): return self.numbTVerts

  def getGroupName(self): 
    return self.groups[0]._name if len(self.groups) else None

  # public int getNbGroup() { return groups.size() } 

  # public GeomGroup getGroup(String name)
  def getGroup(self, name):
    ''' Retrieve a group by its name.
    For compatibility reason with Poser files, this function also searchs
    the name + ':1'
    Parameters
    ----------
    name : str
      Name of the GeomGroup
    ''' 
    idx = name.rfind(':')
    altname = name[0:idx] if idx >= 0 else name + ":1"

    lg = [ g for g in self.groups if (name==g._name) or (altname==g._name) ]

    return lg[0] if lg else None

  def getNbFace(self):
    nf = 0

    for grp in self.groups:
      nf += grp.getNbFace()

    return nf

  # public TexCoord2f getTexCoord(int idx) { return texList[idx] }


  # abstract public void writeFormattedVertex(PrintWriter fw, String nPfx, DecimalFormat fmt)
  # abstract public void writeFormattedNormal(PrintWriter fw, String nPfx, DecimalFormat fmt)
  # abstract public boolean hasNormals()
  def writeFormattedVertex(self, fw, nPfx):
      pfx = nPfx + "v {0: 11.8f} {1: 11.8f} {2: 11.8f}\n"
      for p in self.coordList:
        fw.write(pfx.format(p.x, p.y, p.z))
          
      fw.write('\n')

  def writeFormattedNormal(self, fw, nPfx):
      if self.hasNormals():
        pfx = nPfx + "vn {0: 11.8f} {1: 11.8f} {2: 11.8f}\n"
        for vn in self.normList:
          fw.write(pfx.format(vn.x, vn.y, vn.z))
  

  def hasNormals(self):
    return self.normList != None and len(self.normList)



# TODO: Compute Normals if none and required
#     if self.hasNormal and not geom.normList:
#       nidx = 0 
#       for grp in geom.getGroups():
#         vertIdxTbl = grp.vertIdx
#         
#         for noface in range(0, grp.getNbFace()):
#           startIdx = grp.getFaceStartIdx(noface)
#           lastIdx = grp.getFaceLastIdx(noface)
#           argc = lastIdx - startIdx
#   
#           v0 = vertIdxTbl[startIdx]
#           v1 = vertIdxTbl[startIdx+1]
#           v2 = vertIdxTbl[startIdx+2]
# 
#           lv1 = geom.coordList[v0]     
#           a = Point3d(geom.coordList[v1]).sub(lv1)
#           b = Point3d(geom.coordList[v2]).sub(lv1)
#           n = a.cross(b)
#           n.normalize()
#           
#           geom.normList.append(n)
#           
#           # Give the same normal to each vertex (Ugly)
#           grp.normIdx.extend( [nidx] * argc )
# 
#           nidx += 1

  # public void writeVertex(PrintWriter fw, String nPfx, boolean writeNormals)
  def writeVertex(self, fw, nPfx, writeNormals): # PrintWriter fw, String nPfx, boolean writeNormals)
    # Print Vertex
    self.writeFormattedVertex(fw, nPfx)

    # Print Texture Vertex
    for tex in self.texList:
      fw.write(nPfx + "vt {0: 11.8f} {1: 11.8f}\n".format(tex.x, tex.y))

    fw.write('\n')

    if writeNormals:
      self.writeFormattedNormal(fw, nPfx)

  # private void writeFace(PrintWriter fw, String nPfx, String gn, AbsGeomGroup gg, boolean writeNormals)
  def writeFace(self, fw, nPfx, gn, gg, writeNormals):
    fw.write(nPfx + "g " + gn + '\n')

    # FIX 20101002 : Take into account files without texture coordinates 
    withoutNormal = (gg.normIdx==None) or (len(gg.normIdx)==0) or (not writeNormals)
    withoutTextur = (gg.tvertIdx==None) or (len(gg.tvertIdx)==0)

    for faceno in range(0, gg.getNbFace()):
      startIdx = gg.stripCount[faceno]
      lastIdx = gg.stripCount[faceno + 1]

      if (self._curWriteMatIdx != gg.matIdx[faceno]):
        self._curWriteMatIdx = gg.matIdx[faceno]
        fw.write(nPfx + "usemtl " + self.lstMat[self._curWriteMatIdx] + '\n')

      fw.write(nPfx + "f")

      if withoutTextur:
        if withoutNormal:
          for i in range(startIdx, lastIdx):
            fw.write(" " + str(gg.vertIdx[i] + 1))
        else:
          for i in range(startIdx, lastIdx):
            fw.write(" " + str(gg.vertIdx[i] + 1) + "//" + str(gg.normIdx[i] + 1))
      else:
        if withoutNormal:
          for i in range(startIdx, lastIdx):
            fw.write(" " + str(gg.vertIdx[i] + 1) + "/" + str(gg.tvertIdx[i] + 1))
        else:
          for i in range(startIdx, lastIdx):
            fw.write(" " + str(gg.vertIdx[i] + 1) + "/" + str(gg.tvertIdx[i] + 1) + "/" + str(gg.normIdx[i] + 1))

      fw.write('\n')

  # private void writeLine(PrintWriter fw, String nPfx, String gn, AbsGeomGroup gg)
  def writeLine(self, fw, nPfx, gn, gg):

    hasTexture = len(self.texList)>0

    for lineno in range(0, gg.getNbLine()):
      startIdx = gg.lineStripCount[lineno]
      lastIdx = gg.lineStripCount[lineno + 1]

      if(self._curWriteMatIdx != gg.matIdx[lineno]):
        self._curWriteMatIdx = gg.matIdx[lineno]
        fw.write(nPfx + "usemtl " + self.lstMat[self._curWriteMatIdx] + '\n')

      fw.write(nPfx + "l")
      # FIX20160910 : Do not write false texture Id (make Poser9 KO)
      if hasTexture:
        for i in range(startIdx, lastIdx):
          fw.write(" " + str(gg.vertLineIdx[i] + 1) + "/" + str(gg.tvertLineIdx[i] + 1))
      else:
        for i in range(startIdx, lastIdx):
          fw.write(" " + str(gg.vertLineIdx[i] + 1))

      fw.write('\n')

  # public void writeGroups(PrintWriter fw, String nPfx, boolean writeNormals)
  def writeGroups(self, fw, nPfx, writeNormals, writeOBJName=False): 
    self._curWriteMatIdx = -1

    for gg in self.groups:
      if writeOBJName: # Should only append in 'real' .obj format
        fw.write("o " + gg._name + '\n')
        
      self.writeFace(fw, nPfx, gg._name, gg, writeNormals)
      self.writeLine(fw, nPfx, gg._name, gg)

  # public void writeInOBJ(PrintWriter fw, String nPfx)
  def writeInOBJ(self, fw, nPfx, writeOBJName=False):
    # self.writeConst(fw, "# " + nPfx, None)
    fw.write(nPfx+ '# Generated by pypos3d\n')
    fw.write(nPfx + "mtllib default.mtl\n")
    self.writeVertex(fw, nPfx, True)
    self.writeGroups(fw, nPfx, True, writeOBJName=writeOBJName)

  def writeOBJ(self, fileName, writeOBJName=False):
    ''' Write the WaveGeom in a WaveFront format file (.obj) 
    Paramters
    ---------
    filename : str
      Path of the file to create.
    writeOBJName : bool, optional, default False
      if True the write operation create one 'o ObjetName' line for each group
      Not correctly supported by Poser
    Returns
    -------
    int : C_OK, C_ERROR
    '''
    ret = C_OK
    fout = None
    try:
      fout = open(fileName, 'w')
      self.writeInOBJ(fout, "", writeOBJName=writeOBJName)
      fout.close()

    except FileNotFoundError:
      if WFBasic.PYPOS3D_TRACE: print('File Not Found Error:' + fileName)
      ret = C_ERROR

    except OSError as e: # (IOException ioex)
      if WFBasic.PYPOS3D_TRACE: 
        traceback.print_last()
        print('Write Error:' + str(e))
      ret = C_ERROR
      
    finally:
      if fout:
        fout.close()

    return ret

  # public int writeOBZ(String fileName)
  def writeOBZ(self, fileName):
    ''' Write the WaveGeom in a compressed WaveFront format file (.obz = .obj + gzip) 
    Paramters
    ---------
    filename : str
      Path of the file to create.
    Returns
    -------
    int : C_OK, C_ERROR
    '''
    ret = C_OK
    fout = None
    try:
      fout = gzip.open(fileName, 'wt')
      self.writeInOBJ(fout, "")
      fout.close()

    except FileNotFoundError:
      if WFBasic.PYPOS3D_TRACE: print('File Not Found Error:' + fileName)
      ret = C_ERROR
      
    except OSError as e: # (IOException ioex)
      if WFBasic.PYPOS3D_TRACE: 
        traceback.print_last()
        print('Write Error:' + str(e))
      ret = C_ERROR
      
    finally:
      if fout:
        fout.close()

    return ret


  def save(self, fn):
    ''' Write a WaveFront file in text mode or in compressed mode.
    Use the extension to find the right mode.

    Parameters
    ----------
    fn : str
      Full path name

    Returns
    -------
    int
      C_OK write without error, C_ERROR a write error has occurred
    '''
    if GetLowExt(fn)== 'obj': 
      ret = self.writeOBJ(fn)
    else:
      ret = self.writeOBZ(fn)

    return ret




  # Find the Egde vextex based on 'findEdges' method.
  # Group is supposed to be alone in the GeomCustom.
  #   
  # @return the table of index of the edge vertex
  #
  #  public int[] findEdgeCoord()
  def findEdgeCoord(self):
    gName = self.getGroupName()
    ng = self.getGroup(gName)
    return ng.findEdgeCoord()

  # Find the common points.
  # 
  # @param pBasName
  #            Name of lower element
  # @param pHautName
  #            Name of high element
  # @return a table of index of Vertex of 'this'.
  # public int[] findJonction(String pBasName, String pHautName)
  def findJonction(self, pBasName, pHautName):
    gBas = self.getGroup(pBasName)
    if not gBas:
      logging.warning("Groupe Bas[%s] NO faces", pBasName )
      return None

    logging.info("Groupe Bas[%s]: %d faces", pBasName, gBas.getNbFace())

    gHaut = self.getGroup(pHautName)
    if not gHaut:
      logging.warning("Groupe Bas[%s] NO faces", pHautName )
      return None

    logging.info("Groupe Haut[%s]: %d faces", pHautName, gHaut.getNbFace()) 

    #    int[] comPtTbl = util.findCommonPoints(gBas.getVertIdxTable(), gHaut.getVertIdxTable())
    comPtTbl = findCommonPoints(gBas.vertIdx, gHaut.vertIdx)
    logging.info("ComPoints[]: %d points", len(comPtTbl))

    return comPtTbl


  #  public int[] extractSortJonction(String pBasName, String pHautName)
  def extractSortJonction(self, pBasName, pHautName):
    ''' Return the list of  ... internal stuff '''
    comCoordOrig = self.findJonction(pBasName, pHautName)
    comCoord = None

    if comCoordOrig:
      logging.info("Extracting Jonction : %s/%s", pBasName, pHautName)
      grp = self.getGroup(pBasName)

      nVertIdx = self.calcGroupVertIndex(grp)
      comCoord = [ nVertIdx.index(comCoordOrig[no]) for no in range(0, len(comCoordOrig)) ]

    return comCoord

  #  public void copyMat(AbsWaveGeom src) : Dangerous because of the default material name
  #def copyMat(self, src):
  #  self.lstMat += src.lstMat


  # Calculate for a Group the mapping table for Vertex 
  # beween group index and global GeomCustom index.
  #
  #@return    the mapping table. 
  #           res[i] is the index in the GeomCustom vertex table.
  #  public int[] calcGroupVertIndex(GeomGroup g)
  def calcGroupVertIndex(self, grp):
    nVertIdx = [ ]

    for faceno in range(0, grp.getNbFace()):
      startIdx = grp.stripCount[faceno]
      lastIdx = grp.stripCount[faceno + 1]
      for i in range(startIdx,lastIdx):
        try:
          nVertIdx.index(grp.vertIdx[i])
        except:
          nVertIdx.append(grp.vertIdx[i])

    nVertIdx.sort()
    return nVertIdx

  # Calculate for a Group the mapping table for Texture Coordinates 
  # between group index and global GeomCustom index.
  #
  # @return    the mapping table. 
  #            res[i] is the index in the GeomCustom vertex table.
  #  public int[] calcGroupTVertIndex(GeomGroup g)
  def calcGroupTVertIndex(self, grp):
    # FIX 20101002 : If geom has no texture - fill the TVertIndex with "0"
    if len(self.texList) == 0:
      nTvertIdx = [ ] # * len(grp.tvertIdx)
    else:
      nTvertIdx = [  ]

      for faceno in range(0, grp.getNbFace()):
        startIdx = grp.stripCount[faceno]
        lastIdx = grp.stripCount[faceno + 1]

        for i in range(startIdx, lastIdx):
          #addToTable(nTvertIdx, grp.tvertIdx[i])
          try:
            nTvertIdx.index(grp.tvertIdx[i])
          except:
            nTvertIdx.append(grp.tvertIdx[i])

      nTvertIdx.sort()

    return nTvertIdx

  #
  #
  #  public int[] calcGroupNormIndex(GeomGroup g)
  def calcGroupNormIndex(self, grp):
    # A group without normals in a global geom that contains some normals 
    if (not self.hasNormals()) or (not grp.normIdx):
      return None

    nNormIdx = [ ]

    for faceno in range(0, grp.getNbFace()):
      startIdx = grp.stripCount[faceno]
      lastIdx = grp.stripCount[faceno + 1]

      for i in range(startIdx, lastIdx):
        try:
          nNormIdx.index(grp.normIdx[i])
        except:
          nNormIdx.append(grp.normIdx[i])

    nNormIdx.sort()
    return nNormIdx

  #----------------------------------------------------------------------
  #  public WaveGeom extractSortGeom(String groupName)
  def extractSortGeom(self, groupName):
    ''' Extract the group of the given name and create a new WaveGeom
    that contains a <u>deep copy</u> of the original data.
    
    Parameters
    ----------
    groupName : str

    Returns
    -------
    WaveGeom : a new optimized WaveGeom
    '''
    logging.info('Extracting :%s', groupName)
    grp = self.getGroup(groupName)
    if not grp:
      return None

    gc = WaveGeom()
    gc.lstMat = copy.copy(self.lstMat)

    ngrp = gc.createGeomGroup(groupName if (grp.getName()==None) else grp.getName())
        
    hasTexture = (grp.tvertIdx!=None) and (len(grp.tvertIdx)>0)  

    nbInit = len(self.coordList)
    
    nTexList = []
    
    # A sort on vertex indexes is required (by Poser Morphs)
    sidx = set(grp.vertIdx)
    lidx = list(sidx)
    lidx.sort()
    ngrp.vertIdx = [ bisect.bisect(lidx, vi)-1 for vi in grp.vertIdx ]
    nCoordList = [ Point3d(self.coordList[vi]) for vi in lidx ]
    
    if hasTexture:          
      mapTVert = [-1] * len(self.texList)
      for vti in grp.tvertIdx:
        nvti = mapTVert[vti]
        if nvti<0:
          nvti = len(nTexList)
          nTexList.append(TexCoord2f(self.texList[vti]))
          mapTVert[vti] = nvti
      
        ngrp.tvertIdx.append(nvti)

    gc.coordList = nCoordList
    gc.texList = nTexList
    
    ngrp.linkCoordList(gc)
    ngrp.setMaterialName(grp.curMatIdx)
    
    
    # Copy the faces 
    ngrp.matIdx = copy.copy(grp.matIdx)
    ngrp.stripCount = copy.copy(grp.stripCount) # [:-1] + [ sc+vertpos for sc in angrp.stripCount ]
    
    logging.info("End Result [%s:%d faces, %d Vx, %d Tx]", ngrp.getName(), ngrp.getNbFace(), len(ngrp.coordList),\
                 len(ngrp.texList) if hasTexture else 0)
    
    logging.info("End with Vertex Optimization=%d/%d", len(ngrp.coordList), nbInit)

    return gc

  

  #  public int findMinDist(Point3d p, int noMax, double treshhold)
  def findMinDist(self, p, noMax, treshhold):
    idx = -1
    minDist = sys.float_info.max

    for i in range(0, noMax):
      pe = self.coordList[i]
      d = p.distance(pe)
      if ((d < treshhold) and (d < minDist)):
        minDist = d
        idx = i

    return idx

  #  (non-Javadoc)
  #    * @see deyme.v3d.wf.WaveGeom#scale(double, double, double)
  #    
  def scale(self, ex, ey, ez):
    ''' Scale all vertex along axis '''
    for p in self.coordList:
      p.x *= ex
      p.y *= ey
      p.z *= ez

  def translate(self, tx, ty, tz):
    ''' Translate all vertex '''
    for p in self.coordList:
      p.x += tx
      p.y += ty
      p.z += tz

  #  def centerGeom(self, tx, ty, tz, rx, ry, rz):
  def centerGeom(self, tx, ty, tz, rx, ry, rz):
    raise RuntimeError('Not Implemented')
#      self.translate(-tx, -ty, -tz)
#      matRz = Matrix3d([None]*)
#      i = 0
#      while i < getCoordListLength():
#          matRz.transform(getPoint(i))
#          i += 1
#      matRx = Matrix3d([None]*)
#      i = 0
#      while i < getCoordListLength():
#          matRx.transform(getPoint(i))
#          i += 1
#      matRy = Matrix3d([None]*)
#      i = 0
#      while i < getCoordListLength():
#          matRy.transform(getPoint(i))
#          i += 1

  def getCoordListLength(self):
    ''' Return the size of the vertex list. '''
    return len(self.coordList)

  def getCoordList(self):
    ''' Return a deep copy of the vertex list (.coordList) '''
    return [ Point3d(p) for p in self.coordList ]

  # Return a copy of the Texutre List
  def getTexList(self):
    ''' Return a deep copy of the texture list (.texList) '''
    return [ TexCoord2f(p) for p in self.texList ]

  # Return a copy of the normal list
  def getNormList(self):
    ''' Return a deep copy of the normal list (.normList) '''
    return [ Vector3d(p) for p in self.normList ]

  def setCoordList(self, cl):
    self.coordList = cl
    for gg in self.groups:
      gg.linkCoordList(self)

  #
  def applySymZY(self):
    ''' Apply an Oyz symetry. '''
    for p in self.coordList:
      p.x = -p.x

    for gg in self.groups:
      gg.invertFaceOrder()


  #
  # Clean duplicate vertex
  # Not tested, Not Pythonic
  def cleanDupVert(self, radius):
    res = C_OK
    logging.info("Start Cleaning for %s", self.getName())
    nbMaxVerts = len(self.coordList)
    tabNewIdx = [ -1 ]*nbMaxVerts
    i = 0
    j = 0
    curIdx = 0

    while i < nbMaxVerts:
      # Look for first vertex to manage
      while (i < nbMaxVerts) and (tabNewIdx[i] != -1):
        i+=1

      if i < nbMaxVerts:
        tabNewIdx[i] = curIdx
        j = i+1
        while j < nbMaxVerts:
          cd = self.coordList[i].distanceLinf(self.coordList[j])
          if cd < radius:
            tabNewIdx[j] = curIdx
          j += 1
        curIdx += 1
    #End of While

    if curIdx == nbMaxVerts:
      return C_FAIL

    nCoordLst = [None]*curIdx
    j = 0
    i = 0

    while i < nbMaxVerts:
      nCoordLst[j] = self.coordList[i]
      j+=1
      while (i < nbMaxVerts) and (tabNewIdx[i] < j): i+=1

    for gg in self.groups:
      for i,vi in enumerate(gg.vertIdx):
        gg.vertIdx[i] = tabNewIdx[vi]

    self.setCoordList(nCoordLst)
    return res

  def fusion(self, inLst, outMapLst=None):
    ''' Fusion the current WaveGeom with a list of other WaveGeoms.
    Parameters
    ----------
    inLst : list of WaveGeom
      The List of WaveGeom to insert in self. (Not modified)
    outMapLst : None or empty list
      Out data : returns for each WaveGeom the mapping of vertex between it
      and the fusioned WaveGeom (required by morph update) 
    '''
    logging.info("Start Fusion for %s", self.getName())
    nbMaxVerts = len(self.coordList)
    nbMaxTVerts = len(self.texList)
    nbMaxFaces = self.getNbFace()

    # Prepare the temporary list of vertex
    for curGeom in inLst:
      nbMaxVerts += len(curGeom.coordList)
      nbMaxTVerts += len(curGeom.texList)
      nbMaxFaces += curGeom.getNbFace()

    # Copy original data
    tmpCoordList = copy.copy(self.coordList)
    tmpTexList = copy.copy(self.texList)
    logging.info("tmpCoordList created : %d", nbMaxVerts)
    logging.info("tmpTexList created : %d", nbMaxTVerts)

    # Prepare the face deduplication data
    tabHshFace = [ ] # [None]*nbMaxFaces
    tabFaceIdx = [ ] # [None]*nbMaxFaces
    nbTotFace = 0
    for curGrp in self.groups:
      nbTotFace = curGrp.fillDedupFace(nbTotFace, tabHshFace, tabFaceIdx)
    logging.info("Init Dedup Face table with : %d/%d", nbTotFace, nbMaxFaces)

    # For each incomming GeomCustom
    for curGeom in inLst:
      # Create a mapping table for Vertex of that GeomCustom
      mapVert = [ ]
      #prevMax = len(tmpCoordList)

      # Record the mapping table for external usage
      if outMapLst:
        outMapLst.append(mapVert)

      nbsrc = len(tmpCoordList)
      npTab = np.zeros( (nbsrc, 3) )
      for pNo, p in enumerate(tmpCoordList):
        npTab[pNo] = [ p.x, p.y, p.z ]
    
      # Create an KDTree with the 'known Vertex' in a "global" np.array
      tree = spatial.KDTree(npTab, leafsize=10 if nbsrc<10000 else 100)

      svect = np.zeros((1,3))
      prevNbCoord = nbsrc

      # For each Vertex of the current incomming Geom
      for curPt in curGeom.coordList:
        # Search in KDTtree
        svect[0] = [ curPt.x, curPt.y, curPt.z ]
        rest, resIdx = tree.query(svect)

        # if found (not too far) ==> Put it in a tmp table
        if rest[0]<2.0e-6:
          # Use an existing vertex
          newIdx = resIdx[0]
        else:
          # Add a new vertex to the global list
          newIdx = nbsrc
          nbsrc+=1
          tmpCoordList.append(curPt)

        #mapVert[noVert] = newIdx
        mapVert.append(newIdx)

      # Extend the np.array with the new Vertex
      npTabExt = np.zeros( (nbsrc-prevNbCoord, 3) )
      for pNo,p in enumerate(tmpCoordList[prevNbCoord:nbsrc]):
        npTabExt[pNo] = [ p.x, p.y, p.z ]
      npTab = np.vstack((npTab,npTabExt))

      # Create a mapping table for TVertex of that GeomCustom
      nbtv = len(curGeom.texList)
      mapTVert = [ nbtv+i for i in range(0,nbtv) ] # = new int[curGeom.numbTVerts];
      # Add all the Texture vertex to the global list
      tmpTexList += curGeom.texList

      # Copy the faces taking into account the mapping table
      for curGrp in curGeom.groups:
        for i in range(0, len(curGrp.vertIdx)):
          curGrp.vertIdx[i] = mapVert[curGrp.vertIdx[i]]

        if len(curGeom.texList) > 0:
          for i in range(0, len(curGrp.tvertIdx)):
            curGrp.tvertIdx[i] = mapTVert[curGrp.tvertIdx[i]]

        # Deduplicate faces
        tabKeptFace = [ False ] * curGrp.getNbFace()
        nbKeptFace = 0
        idxFirstFace = nbTotFace

        for faceno in range(0, curGrp.getNbFace()):
          startIdx = curGrp.stripCount[faceno]
          lastIdx = curGrp.stripCount[faceno+1]
          idxTab = curGrp.vertIdx[startIdx:lastIdx]
          nbv = lastIdx - startIdx
          # Find lowest index
          lowestIdx = LowestIdxPos(idxTab)
          finalIdxTab = [ idxTab[(i + lowestIdx) % nbv] for i in range(0, nbv) ]

          hashVal = sum(finalIdxTab)
          i = 0
          while i < nbTotFace:
            if (tabHshFace[i]==hashVal) and finalIdxTab==tabFaceIdx[i]:
              # The face already exists in the fusioned geom
              break
            i += 1

          # The face has not been found : add it
          if i==nbTotFace:
            tabHshFace.append(hashVal)
            tabFaceIdx.append(finalIdxTab)
            nbTotFace += 1
            nbKeptFace += 1
            tabKeptFace[faceno] = True
          else:
            tabKeptFace[faceno] = False
        # End for faceno

        # Rebuild the group data
        newStripCount = [0] * (nbKeptFace+1)

        # First : Count the number of vertex of kept faces : Useless in Python
        curGrp_vertIdx = [ ]  # new int[l];
        curGrp_tvertIdx = [ ] # new int[l];
        curGrp_matIdx = [ ]   # new int[nbKeptFace];

        # Copy the vertex indexes of kept faces
        prev_nfn = curGrp.getNbFace()
        nfn = 0
        for faceno in range(0, curGrp.getNbFace()):
          if tabKeptFace[faceno]:
            nbv = len(tabFaceIdx[idxFirstFace + nfn])

            # System.arraycopy(tabFaceIdx[idxFirstFace + nfn], 0, curGrp_vertIdx, nnfn, nbv)
            curGrp_vertIdx += tabFaceIdx[idxFirstFace + nfn]

            # System.arraycopy(tabTVertIdx, 0, curGrp_tvertIdx, nnfn, nbv)
            startIdx = curGrp.stripCount[faceno]
            lastIdx = curGrp.stripCount[faceno+1]
            curGrp_tvertIdx += curGrp.tvertIdx[startIdx:lastIdx] 

            curGrp_matIdx.append(curGrp.matIdx[faceno])

            nfn += 1
            newStripCount[nfn] = newStripCount[nfn - 1] + nbv


        curGrp.stripCount = newStripCount
        curGrp.vertIdx = curGrp_vertIdx
        curGrp.tvertIdx = curGrp_tvertIdx
        curGrp.matIdx = curGrp_matIdx
        self.groups.append(curGrp)
        curGrp.linkCoordList(None)
        logging.info("Group:%s merged with %d faces on %d", curGrp.getName(), nfn, prev_nfn)


    # Finalisation : Convert Lists 
    self.coordList = tmpCoordList
    self.texList = tmpTexList

    # Link Groups
    for gg in self.groups:
      gg.linkCoordList(self)

    # Fusion of material List
    for curGeom in inLst:
      nbmat = len(curGeom.getMaterialList())
      mapMat = [0] * nbmat
      for i,mn in enumerate(curGeom.getMaterialList()):
        mapMat[i] = self.addMaterial(mn)

      # Change material indexes in any groups
      for gg in curGeom.groups:
        for faceno in range(0, gg.getNbFace()):
          gg.setMatIdx(faceno, mapMat[gg.getMatIdx(faceno)])



  def addGroup(self, ngrp):
    ''' Add a group to the current WaveGeom. The group may belong to different WaveGeom

    Parameters
    ----------
    ngrp : GeomGroup
      Group to add
    '''

    # Create an empty new Group in the current WaveGeom
    internGrp = GeomGroup()
    internGrp.setName(ngrp.getName())
    self.groups.append(internGrp)
    internGrp.linkCoordList(self)
    
    # Fusion the incomming group with the new internal empty group
    internGrp.fusion(ngrp)
    return internGrp




  def removeGroup(self, grp, cleaning=False):
    ''' Remove a group from the current WaveGeom '''
    ret = C_OK    
    gg = grp if isinstance(grp, GeomGroup) else self.getGroup(grp)

    try:
      self.groups.remove(gg)
      if cleaning:
        self.optimizeGroups(cleaning=True)
      
    except ValueError:
      logging.info("Group:%s not found", gg.getName() if gg else 'Null group')
      ret = C_FAIL

    return ret
    

#    def compareVertexList(self, wg, accuracy, complete):
#        """ generated source for method compareVertexList """
#        wg3d = wg
#        d = 0.0
#        dmax = 0.0
#        i = 0
#        while i < self.getCoordListLength():
#            d = self.coordList[i].distanceLinf(wg3d.coordList[i])
#            if d > accuracy:
#                dmax = d
#                if not complete:
#                    return dmax
#            i += 1
#        return dmax
#
#    def compareNormalList(self, wg, accuracy, complete):
#        """ generated source for method compareNormalList """
#        wg3d = wg
#        d = 0.0
#        dmax = 0.0
#        dv = Vector3d()
#        i = 0
#        while i < self.getNormListLength():
#            dv.sub(self.normList[i], wg3d.normList[i])
#            d = dv.lengthSquared()
#            if d > accuracy:
#                dmax = d
#                if not complete:
#                    return dmax
#            i += 1
#        return dmax
#
  def copyData(self):
    ng = WaveGeom()
    ng.coordList = self.getCoordList()
    if self.normList:
      ng.normList = self.getNormList()
    return ng




  def fillHole(self, srcGrpOrName, srcMatName, destGrpName, destMatName, mergeGrp, nbLoop, alpha, createCenter=True):
    ''' Fill a hole in the geometry with the MLS method.
    Hole sampling created with a "SPIDER NET" algo of mine.
    AS described by document http://www.inf.ufrgs.br/~oliveira/pubs_files/WangJ_OliveiraM_Hole_Filling.pdf<
    Title : A Hole-Filling Strategy for Reconstruction of Smooth Surfaces in Range Images
    Written by JIANNING WANG &  MANUEL M. OLIVEIRA
    
    The hole is identified by a material and searched in the srcGrpName group.
    A new group named destGrpName is created using a destMaterialName.
    
    Parameters
    ----------
    srcGrpName  : str 
      Group name where hole is located. Default group used if null.
    srcMatName  : str 
      Material name affected to the hole.
    destGrpName : str 
      Group name to be created.
    destMatName : str 
      Material name affected to the new group.
    mergeGrp    : bool 
      Indicate if the new group is to be merged with the initial group.
    nbLoop      : int 
      Number of Edge loops to consider. Default should be 2. 
    alpha       : float 
      Influence of distant point (less than one).
   
    Returns
    -------
    int
       Result Code. C_OK when no problem has occured.
    '''
    res = C_OK
    i,j,k = 0,0,0
    lstmat = self.getMaterialList()
    try:
      matidx = lstmat.index(srcMatName)
    except ValueError:
      logging.warning("Material[%s] is missing", srcMatName )
      return C_MISSING_MAT

    # Get default group
    grp = srcGrpOrName if isinstance(srcGrpOrName, GeomGroup) else self.getGroup(self.getGroupName()) if not srcGrpOrName else self.getGroup(srcGrpOrName)

    # Get the first face with the given material
    holefaceno = grp.findFace(matidx)
    if holefaceno == -1:
      logging.warning("In Group[%s] - No face with Material [%s] is missing", grp.getName(), srcMatName )
      return C_MISSING_FACEMAT

    # Get the vertex that compose the "hole face"
    edgePt = grp.getFaceVertex(holefaceno)
    edgePtIdx = grp.getFaceVertIdx(holefaceno)
    nbEdgePt = len(edgePt)
    logging.info("Edge contains %d points", nbEdgePt)

    # Calculate 'nnLoop' loops Vicinity
    edgeLoopPtIdx =  copy.copy(edgePtIdx)

    # First Loop Vicinity
    grp.extendLoopVicinity(edgePtIdx, edgeLoopPtIdx)
    nbLoopPt = len(edgeLoopPtIdx)
    logging.info("Edge Loop 1 contains %d points", nbLoopPt)

    for i in range(1, nbLoop):
      tmpIdx = edgeLoopPtIdx[0:nbLoopPt]

      grp.extendLoopVicinity(tmpIdx, edgeLoopPtIdx)
      nbLoopPt = len(edgeLoopPtIdx)
      logging.info("Edge Loop %d contains %d points", (i + 1), nbLoopPt)


    # Compute projection Repere with SVD matrix decomposition
    repUVN = Repere(nbLoopPt, edgeLoopPtIdx, self.coordList)
    tabproj = repUVN.project(0, 0, nbLoopPt, edgeLoopPtIdx, self.coordList, None)

    # Determine G the isobarycenter and the average length of edges 
    isoG = Point3d()
    avgEdgeLength = 0.0
    # Limited to the first points that are the edge vertex
    for i in range(0, nbEdgePt):
      isoG.add(tabproj[i])
      avgEdgeLength += tabproj[i].dXY(tabproj[(i + 1) % nbEdgePt])

    isoG.scale(1.0 / float(nbEdgePt))
    isoG.z = 0.0
    avgEdgeLength /= float(nbEdgePt)
    
    # Determine the maximum distance between edges and G
    maxLength2Edges = sys.float_info.min
    for i in range(0, nbEdgePt):
      d = isoG.dXY(tabproj[i])
      if d > maxLength2Edges:
        maxLength2Edges = d

    # Determine the number of segment on a pseudo-radius
    # Each pseudo-radius will contain nbSeg-1 new points
    nbSeg = (1 + int((maxLength2Edges / avgEdgeLength))) >> 1
    if nbSeg < 2:
      nbSeg = 2

    # Number of new created points. +1 for the center isoG
    nbNewPt = nbEdgePt * (nbSeg - 1) + 1
    sampPt = [None]*nbNewPt  # of Vector3d
    v = Vector3d()
    sampPt[0] = isoG
    for i in range(0, nbEdgePt): # Limited to the first points that are the edge vertex
      k = i * (nbSeg - 1) + 1
      for j in range(1, nbSeg):
        v.sub(isoG, tabproj[i])
        v.scale(float(j) / float(nbSeg))
        sampPt[k] = Point3d(tabproj[i])
        sampPt[k].z = 0.0
        sampPt[k].add(v)
        k += 1

    # Calculate Texture Coord of G and Texture Index of edge points
    uvmap = (self.texList) and (len(self.texList)>0)
    edgeSampTextIdx = grp.getFaceTVertIdx(holefaceno)
    if uvmap:
      tx = 0.0
      ty = 0.0

      for i in range(0, nbEdgePt):
        tx += self.texList[edgeSampTextIdx[i]].x
        ty += self.texList[edgeSampTextIdx[i]].y

      texG = TexCoord2f( (tx / float(nbEdgePt)), (ty / float(nbEdgePt)) )

      # Extend texList
      # Allocate new texture index at the end of the current table of the geometry
      lastno = len(self.texList)
      edgeSampTextIdx += [ lastno+i-nbEdgePt for i in range(nbEdgePt, nbEdgePt + nbNewPt) ]

      vtex = TexCoord2f()
      ntexList = copy.copy(self.texList) # [ None ] * (self.getTexListLength() + nbNewPt) # of TexCoord2f
      # System_arraycopy(self.texList, 0, ntexList, 0, self.getTexListLength())

      # ntexList[self.getTexListLength() + 0] = texG 
      ntexList.append( texG )
      for i in range(0, nbEdgePt):
        k = len(self.texList) + i * (nbSeg - 1) + 1
        for j in range(1, nbSeg):
          vtex.sub(texG, self.texList[edgeSampTextIdx[i]])
          vtex.scale(float(j) / float(nbSeg))
          ntexList.append(TexCoord2f(self.texList[edgeSampTextIdx[i]]).add(vtex))
          ntexList[k]

      self.setTexList(ntexList)
    else:
      logging.warning("No UV Map for %s", grp.getName())

    # Create a raster with edge Vertex and Sampled Vertex
    #edgeSamp = [None]*(nbEdgePt + nbNewPt) # of Point3d
    #System_arraycopy(tabproj, 0, edgeSamp, 0, nbEdgePt)
    #System_arraycopy(sampPt, 0, edgeSamp, nbEdgePt, nbNewPt)
    edgeSamp = tabproj[0:nbEdgePt] + sampPt

    # Allocate new vertex index at the end of the current table of the geometry
    #edgeSampIdx = [0]*(nbEdgePt + nbNewPt)
    #System_arraycopy(edgePtIdx, 0, edgeSampIdx, 0, nbEdgePt)
    lastno = self.getCoordListLength()
    edgeSampIdx = edgePtIdx + [ idx+lastno for idx in range(0, nbNewPt) ]
    logging.info("Meshed Size=%d", len(edgeSamp))

    #for i in range(nbEdgePt, nbEdgePt + nbNewPt):
      #edgeSampIdx[i] = lastno
      #lastno += 1

    # Calculate Point Altitudes
    calcMLS(edgeSamp, nbEdgePt, len(edgeSamp), tabproj, alpha)

    # Save Result in a new GeomGroup
    ngrp = self.createGeomGroup(destGrpName)

    ncl = repUVN.reserveProject(nbEdgePt, self.getCoordListLength(), nbNewPt, edgeSamp)
    #System_arraycopy(self.getCoordList(), 0, ncl, 0, self.getCoordListLength())
    ncl[0:self.getCoordListLength()] = self.getCoordList()[0:self.getCoordListLength()]
    self.setCoordList(ncl)
    if destMatName:
      self.addMaterial(destMatName)
      ngrp.setMaterialName(self.curMatIdx)

    lstFacevIdx = []
    lstFacevtIdx = []

    normIdx = [ ]
    for i in range(0, nbEdgePt):
      isuiv = (i + 1) % nbEdgePt
      i1 = nbEdgePt + i * (nbSeg - 1) + 1
      i2 = nbEdgePt + isuiv * (nbSeg - 1) + 1

      # Create first Quad face
      coordIdx = [ edgeSampIdx[i], edgeSampIdx[isuiv], edgeSampIdx[i2], edgeSampIdx[i1] ]
      texIdx = [ edgeSampTextIdx[i], edgeSampTextIdx[isuiv], edgeSampTextIdx[i2], edgeSampTextIdx[i1] ] if uvmap else [ ]
#       coordIdx = [ edgeSampIdx[i], edgeSampIdx[i1], edgeSampIdx[i2], edgeSampIdx[isuiv] ]
#       texIdx = [ edgeSampTextIdx[i], edgeSampTextIdx[i1], edgeSampTextIdx[i2], edgeSampTextIdx[isuiv] ] if uvmap else [ ]
      ngrp.addFace(coordIdx, texIdx, normIdx)
        
      # Create other Quad faces
      for j in range(1, nbSeg - 1):
        coordIdx = [ edgeSampIdx[i1 + j - 1], edgeSampIdx[i2 + j - 1], edgeSampIdx[i2 + j], edgeSampIdx[i1 + j] ]
        texIdx = [ edgeSampTextIdx[i1 + j - 1], edgeSampTextIdx[i2 + j - 1], edgeSampTextIdx[i2 + j], edgeSampTextIdx[i1 + j] ] if uvmap else [ ]
#         coordIdx = [ edgeSampIdx[i1 + j - 1], edgeSampIdx[i1 + j], edgeSampIdx[i2 + j], edgeSampIdx[i2 + j - 1] ]
#         texIdx = [ edgeSampTextIdx[i1 + j - 1], edgeSampTextIdx[i1 + j], edgeSampTextIdx[i2 + j], edgeSampTextIdx[i2 + j - 1] ] if uvmap else [ ]
        ngrp.addFace(coordIdx, texIdx, normIdx)

      # Create last Triangular face
      if createCenter:
        coordIdx = [ edgeSampIdx[i1 + nbSeg - 2], edgeSampIdx[i2 + nbSeg - 2], edgeSampIdx[nbEdgePt] ]
        texIdx = [ edgeSampTextIdx[i1 + nbSeg - 2], edgeSampTextIdx[i2 + nbSeg - 2], edgeSampTextIdx[nbEdgePt] ] if uvmap else [ ]
        ngrp.addFace(coordIdx, texIdx, normIdx)
      else:
        lstFacevIdx.append(edgeSampIdx[i1 + nbSeg - 2])
        if uvmap:
          lstFacevtIdx.append(edgeSampTextIdx[i1 + nbSeg - 2])


    # Create a centrale face (if center triangles have not been inserted)
    if not createCenter:
      ngrp.addFace(lstFacevIdx, lstFacevtIdx, normIdx)
      

    # Merge New group with intial one and Remove the hole face
    if mergeGrp:
      grp.removeFace(holefaceno)
      grp.fusion(ngrp)
      self.groups.remove(ngrp)
    return res
# ==============================================================================
#  End Of WaveGeom
# ==============================================================================





# ------------------------------------------------------------------------------
def readGeom(fn, usemtl=False, imgdirpath=''):
  ''' Read a .OBJ (or .OBZ compressed) file and return a WaveGeom.
  
  Parameters
  ----------
  fn  : str
    Filename of the .OBJ (or.obz) file

  Returns
  -------
  WaveGeom 
    the read geometry (None in case of FileNotFoundError)
  '''
  gm = None

  try:
    # Read full body geometry
    rin = getOBJFile(fn)

    pfr = PoserFileParser(rin, OBJ_FNAT)
    gm = WaveGeom(st=pfr, filename=fn, usemtl=usemtl, imgdirpath=imgdirpath)

    rin.close()

  except FileNotFoundError as e:
    if WFBasic.PYPOS3D_TRACE: print ('File({0:s} - Read Error {1:s}'.format(fn, str(e.args)))

  return gm
 


# ----------------------------------------------------------------------------
def PlaneCut(target, centerOrRepOrPlane, eu=None, ev=None, materialName='SectionMat', \
             slicing=False, radialLimit=0.0, radialScale=0.0): 
  ''' Cut target group along the normal vector of the input plan (or the third vector of the Coordinate System).
  Create a new WaveGeom with one group :
    default : the result geometry does not contain cut faces
  Hyp:
  - Cutting plane defined by a point and a set of non co-linear vectors
  - Does not modify the plane nor the input 'target'
  - Create the closing faces if materialName not null
  - By default remove the cut faces (slice=False), else just create the new edges and faces
 
  Perform a Radial Scale on the closing face, if radialScale>0.0
 
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to cut

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system

  materialName : str, optional, default='SectionMat'
    Name of the material of the closing face.
    if None, the closing face is not inserted in the result geometry

  slicing : bool, optional, default=False
    When slicing is True , the result geometry contains all geometries with 'sliced' faces along the plane
    defined by (center, eu, ev)
   

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'
  radialScale : float, optional, default 0.0
    For any positive value, the closing face is scaled with this value (central homothetie)

  Returns
  -------
  WaveGeom, CuttingData :
    a new WaveGeom with a single new GeomGroup
    the CuttingData object
  '''
  logging.info("Start for %s", target.getName())

  nwg = WaveGeom()
  nwg.lstMat = copy.copy(target.lstMat)
  
  if target.tvertIdx:
    hasTexture = True
    nwg.texList = copy.copy(target.texList)
  else:
    hasTexture = False

  # Compute the Cutting axis and the transformation matrix
  if isinstance(centerOrRepOrPlane, Point3d):
    rep = CoordSyst(centerOrRepOrPlane, eu, ev)
  elif isinstance(centerOrRepOrPlane, CoordSyst):
    rep = centerOrRepOrPlane
  else: # Supposed to be a plane
    rep = centerOrRepOrPlane.calcCoordSyst()

  # Convert All input group coordinates in center+(eu,ev,ew) system
  nwg.coordList = rep.To(target.coordList)

  ngrp =  nwg.createGeomGroup(target.getName() + 'cut')

  # Create a new face list (defined by Vertex)
  nFaceList = [ ]
  # List of mat indexes to apply (or restore) to the faces
  nMatList = [ ]
  
  closingFaceVx = [ ]

  # In the cutting plan coord. syst, the cutting vector is Oz
  cuttingVect = Vector3d(0.0,0.0,1.0) 

  radialLimit2 = radialLimit*radialLimit

  # For each target face
  for faceno in range(0, target.getNbFace()):
    startidx = target.getFaceStartIdx(faceno)
    lastidx = target.getFaceLastIdx(faceno)
                        
    if lastidx-startidx<3:
      if WFBasic.PYPOS3D_TRACE: print('  PlaneCut[{0:s}] ignoring face : {1:d}'.format(target.getName(), faceno))
      continue
    
    # Retrieve the material of the face to cut
    matidx = target.matIdx[faceno]
    # Intersect with plane

    # Compute the list of enhanced Vertex, without aligned ones
    # We have at least 3 points
    prevPt = Point3d(nwg.coordList[target.vertIdx[startidx]])
    if hasTexture:
      prevPt.texture = nwg.texList[target.tvertIdx[startidx]]
    vxtab = [ prevPt, ]
    nextPt, e0, e1 = None, None, None

    for i in range(startidx+1, lastidx-1):
      if nextPt:
        np = nextPt
        e0 = e1
      else:
        np = Point3d(nwg.coordList[target.vertIdx[i]]) 
        if hasTexture:
          np.texture = nwg.texList[target.tvertIdx[i]]
        e0 = Edge(prevPt, np)

      nextPt = Point3d(nwg.coordList[target.vertIdx[i+1]]) 
      if hasTexture:
        nextPt.texture = nwg.texList[target.tvertIdx[i+1]]

      e1 = Edge(np, nextPt)
      if e0.isAligned(e1): # Elimintate np and grow e1 segment
        e1 = Edge(prevPt, nextPt)
      else:
        vxtab.append(np)

    # Add the last point
    vxtab.append(nextPt)
 

    # Prepare the list of face edges
    lstEdgeVx = [ (vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ (vxtab[-1], vxtab[0]), ]

    if len(vxtab)<3:
      if WFBasic.PYPOS3D_TRACE: print('  PlaneCut[{0:s}] ignoring cleaned face : {1:d}'.format(target.getName(), faceno))
      
      v = FaceVisibility(lstEdgeVx, cuttingVect)
      if v>FEPSILON:  # Determine if the face shall be kept
        lstNewFaceVx = [ v[0] for v in lstEdgeVx ]

        nFaceList.append(lstNewFaceVx)
        nMatList.append(matidx)
      elif (radialLimit2!=0.0) and (min( v[0].x*v[0].x+v[0].y*v[0].y for v in lstEdgeVx ) > radialLimit2):
          lstNewFaceVx = [ v[0] for v in lstEdgeVx ]
          # return lstNewFaceVx, [ ], False
          nFaceList.append(lstNewFaceVx)
          nMatList.append(matidx)
      continue

    # Now the plan is the origin of the coordinate sytem, the Normal vector is enough to cut
    lstNewFaceVx, lstNewEdges, multiple = FaceCut(lstEdgeVx, cuttingVect, hasTexture, slicing, radialLimit2)
 
    # Add the face to the face list of the new geometry
    if lstNewFaceVx:
        
      if multiple: # In such case, lstNewFaceVx is a list of list of Vertex
        if WFBasic.PYPOS3D_TRACE: 
          print('  PlaneCut[{0:s}].Cutting[{1:d}]: {2:d} faces'.format(target.getName(), faceno, len(lstNewFaceVx)))
        nFaceList += lstNewFaceVx
        nMatList += [ matidx ] * len(lstNewFaceVx)
      else:
        if WFBasic.PYPOS3D_TRACE: print('  PlaneCut[{0:s}].Cutting[{1:d}]: {2:d} vertex'.format(target.getName(), faceno, len(lstNewFaceVx)))
        nFaceList.append(lstNewFaceVx)
        nMatList.append(matidx)
    
      # Add the new Edges to the closing Face
      if lstNewEdges:
        closingFaceVx += lstNewEdges

  
  # Finish the group's creation
  # Add each face to the group
  ngrp.addFacesByVertex(nFaceList, nMatList, hasTexture)
    
  # Add the closing face to the list of faces to keep
  if materialName:
    lstFacesIdx, nbFaces, cl = ngrp.addFaceByEdges(closingFaceVx, hasTexture, materialName)
  else:
    lstFacesIdx, nbFaces, cl = None, 0, []
    # Create a local list of the cut points
    if radialScale>0.0:
      for edge in closingFaceVx:      
        IndexAdd(cl, edge[0])
        IndexAdd(cl, edge[1])

  if radialScale>0.0:
    for p in cl:
      p.x *= radialScale
      p.y *= radialScale

  nwg.coordList = rep.From(nwg.coordList)
  nwg.optimizeGroups() # Just because we've change the coordList pointer!

  cd = CuttingData(ngrp, None, rep, lstFacesIdx, nbFaces, hasTexture)
  
  logging.info("End for %s: Top=[%s with %d faces]", target.getName(), ngrp.getName(), ngrp.getNbFace())

  return nwg, cd

# ----------------------------------------------------------------------------
def PlaneSplit(target, centerOrRepOrPlane, eu=None, ev=None, radialLimit=0.0, materialName='SectionMat'):
  ''' Split target group along the third vector of the input plan. 
  Create a new GeomGroup with the two cut groups.

  Hyp:
  - Cutting plane defined by a point and a set of non co-linear vectors
  - Does not modify the plane nor the input 'target'
  - Create the closing faces if materialName not null in both groups
 
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to cut

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system

  materialName : str, optional, default='SectionMat'
    Name of the material of the closing face.
    if None, the closing face is not inserted in the result geometry

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'

  Returns
  -------
  WaveGeom, CuttingData :
    a new WaveGeom with two new GeomGroup(s)
    the CuttingData object
  ''' 
  logging.info("Start for %s", target.getName())

  nwg = WaveGeom()
  nwg.lstMat = copy.copy(target.lstMat)
  
  if target.tvertIdx:
    hasTexture = True
    nwg.texList = copy.copy(target.texList)
  else:
    hasTexture = False

  # Compute the Cutting axis and the transformation matrix
  if isinstance(centerOrRepOrPlane, Point3d):
    rep = CoordSyst(centerOrRepOrPlane, eu, ev)
  elif isinstance(centerOrRepOrPlane, CoordSyst):
    rep = centerOrRepOrPlane
  else: # Supposed to be a plane
    rep = centerOrRepOrPlane.calcCoordSyst()

  # Convert All input geometry coordinates in center+(eu,ev,ew) system
  nwg.coordList = rep.To(target.coordList)

  # Create a new face list (defined by Vertex)
  nTopFaceList, nBotFaceList = [], []
    
  # List of mat indexes to apply (or restore) to the faces
  nTopMatList, nBotMatList = [ ], [ ]
  
  closingFaceVx = [ ]

  # In the cutting plan coord. syst, the cutting vector is Oz
  cuttingVect = Vector3d(0.0,0.0,1.0) 

  radialLimit2 = radialLimit*radialLimit

  # For each target face
  for faceno in range(0, target.getNbFace()):
    startidx = target.getFaceStartIdx(faceno)
    lastidx = target.getFaceLastIdx(faceno)
                        
    if lastidx-startidx<3:
      if WFBasic.PYPOS3D_TRACE: print('  [{0:s}] ignoring face : {1:d}'.format(target.getName(), faceno))
      continue
    
    # Retrieve the material of the face to cut
    matidx = target.matIdx[faceno]
    # Intersect with plane

    # Compute the list of enhanced Vertex, without aligned ones
    # We have at least 3 points
    prevPt = Point3d(nwg.coordList[target.vertIdx[startidx]])
    if hasTexture:
      prevPt.texture = nwg.texList[target.tvertIdx[startidx]]
    vxtab = [ prevPt, ]
    nextPt, e0, e1 = None, None, None

    for i in range(startidx+1, lastidx-1):
      if nextPt:
        np = nextPt
        e0 = e1
      else:
        np = Point3d(nwg.coordList[target.vertIdx[i]]) 
        if hasTexture:
          np.texture = nwg.texList[target.tvertIdx[i]]
        e0 = Edge(prevPt, np)

      nextPt = Point3d(nwg.coordList[target.vertIdx[i+1]]) 
      if hasTexture:
        nextPt.texture = nwg.texList[target.tvertIdx[i+1]]

      e1 = Edge(np, nextPt)
      if e0.isAligned(e1): # Elimintate np and grow e1 segment
        e1 = Edge(prevPt, nextPt)
      else:
        vxtab.append(np)

    # Add the last point
    vxtab.append(nextPt)
 

    # Prepare the list of face edges
    lstEdgeVx = [ (vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ (vxtab[-1], vxtab[0]), ]

    if len(vxtab)<3:
      if WFBasic.PYPOS3D_TRACE: print('  [{0:s}] ignoring cleaned face : {1:d}'.format(target.getName(), faceno))
      
      lstNewFaceVx = [ v[0] for v in lstEdgeVx ]

      v = FaceVisibility(lstEdgeVx, cuttingVect)
      # Determine in which group the face shall be kept
      if (v>FEPSILON) or \
         ((radialLimit2!=0.0) and (min( v[0].x*v[0].x+v[0].y*v[0].y for v in lstEdgeVx ) > radialLimit2)):
        nTopFaceList.append(lstNewFaceVx)
        nTopMatList.append(matidx)
      else:
        nBotFaceList.append(lstNewFaceVx)
        nBotMatList.append(matidx)

      continue

    # Now the plan is the origin of the coordinate sytem, the Normal vector is enough to cut
    lstTopFacesVx, lstBotFacesVx, lstNewEdges = FaceSplit(lstEdgeVx, cuttingVect, hasTexture, radialLimit2)
 
    # Add the face(s) to the face list of the new geometry
    if lstTopFacesVx: # lstTopFacesVx is a list of list of Vertex
      nTopFaceList += lstTopFacesVx
      nTopMatList += [ matidx ] * len(lstTopFacesVx)
    
    if lstBotFacesVx: # lstTopFacesVx is a list of list of Vertex
      nBotFaceList += lstBotFacesVx
      nBotMatList += [ matidx ] * len(lstBotFacesVx)
    
    # Add the new Edges to the closing Face
    if lstNewEdges:
      closingFaceVx += lstNewEdges

  # Finish the group's creation : Add each face to the group
  topGrp = nwg.createGeomGroup(target.getName() + 'cutTop')
  botGrp = nwg.createGeomGroup(target.getName() + 'cutBot')

  logging.info("Adding Top Faces in %s: [%s with %d faces]", target.getName(), topGrp.getName(), len(nTopFaceList))
  topGrp.addFacesByVertex(nTopFaceList, nTopMatList, hasTexture)

  logging.info("Adding Bottom Faces in %s: [%s with %d faces]", target.getName(), botGrp.getName(), len(nBotFaceList))
  botGrp.addFacesByVertex(nBotFaceList, nBotMatList, hasTexture)
    
  # Add the closing face to the list of faces to keep
  logging.info("Creating ClosingFace in %s:%d edges", topGrp.getName(), len(closingFaceVx))
  #Plot(closingFaceVx,None)
  
  if materialName:    
    lstFacesIdx, nbFaces, _ = topGrp.addFaceByEdges(closingFaceVx, hasTexture, materialName, refNorm=Vector3d(cuttingVect).neg())
  else:
    lstFacesIdx, nbFaces  = None, 0

  nwg.coordList = rep.From(nwg.coordList)
  logging.info("Optimizing PlaneSplit for %s", target.getName())
  nwg.optimizeGroups() # Just because we've change the coordList pointer!

  cd = CuttingData(topGrp, botGrp, rep, lstFacesIdx, nbFaces, hasTexture)

  logging.info("End for %s: Top=[%s with %d faces] Bottom=[%s with %d faces]", target.getName(), topGrp.getName(), topGrp.getNbFace(), botGrp.getName(), botGrp.getNbFace())

  return nwg, cd



  


# ----------------------------------------------------------------------------
# TODO: Output to rethink - Could return all the closing faces (we have them)
#
def PlaneSlice(target, centerOrRepOrPlane, eu=None, ev=None, cutFaceMatLst=None, radialLimit=0.0, radialScale=0.0, minLength=0.0): 
  ''' Compute the slice of a given GeomGroup.
  Hyp:
  - Cutting plane defined by a point and a set of non co-linear vectors
  - Does not modify the plane
 
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to cut

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system

  cutFaceMatLst : list, optional, default=None, out
    When not null, this list is filled with the list of the material indexes of cut faces

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'

  radialScale : float, optional, default 0.0
    For any positive value, the closing face is scaled with this value (central homothetie)

  minLength : float, optional, default 0.0
    When not null, created egdes shall be longuer than minLength

  Returns
  -------
  list of Edge()
    With list of edges that represents the first closing face of the cut.
    Edges are containing new Point3d (carrying texture if any)
  ''' 
  logging.info("Start for %s", target.getName())

  keepMaterial = (cutFaceMatLst!=None)

  if target.tvertIdx:
    hasTexture = True
    texList = copy.copy(target.texList)
  else:
    hasTexture = False

  # Compute the Cutting axis and the transformation matrix
  # Compute the Cutting axis and the transformation matrix
  if isinstance(centerOrRepOrPlane, Point3d):
    rep = CoordSyst(centerOrRepOrPlane, eu, ev)
  elif isinstance(centerOrRepOrPlane, CoordSyst):
    rep = centerOrRepOrPlane
  else: # Supposed to be a plane
    rep = centerOrRepOrPlane.calcCoordSyst()

  # Convert All input group coordinates in center+(eu,ev,ew) system
  coordList = rep.To(target.coordList)

  closingFaceVx = [ ]

  # In the cutting plan coord. syst, the cutting vector is Oz
  cuttingVect = Vector3d(0.0,0.0,1.0) 
  
  radialLimit2 = radialLimit*radialLimit

  # For each target face
  for faceno in range(0, target.getNbFace()):
    startidx = target.getFaceStartIdx(faceno)
    lastidx = target.getFaceLastIdx(faceno)
    
    if lastidx-startidx<3:
      if WFBasic.PYPOS3D_TRACE: print('PlaneSlice[{0:s}] ignoring NON face : {1:d}'.format(target.getName(), faceno))
      continue
    
    # Compute the list of enhanced Vertex, without aligned ones
    # We have at least 3 points
    prevPt = Point3d(coordList[target.vertIdx[startidx]])
    if hasTexture:
      prevPt.texture = texList[target.tvertIdx[startidx]]
    vxtab = [ prevPt, ]
    nextPt, e0, e1 = None, None, None

    for i in range(startidx+1, lastidx-1):
      if nextPt:
        np = nextPt
        e0 = e1
      else:
        np = Point3d(coordList[target.vertIdx[i]]) 
        if hasTexture:
          np.texture = texList[target.tvertIdx[i]]
        e0 = Edge(prevPt, np)

      nextPt = Point3d(coordList[target.vertIdx[i+1]]) 
      if hasTexture:
        nextPt.texture = texList[target.tvertIdx[i+1]]

      e1 = Edge(np, nextPt)
      if e0.isAligned(e1): # Elimintate np and grow e1 segment
        e1 = Edge(prevPt, nextPt)
      else:
        vxtab.append(np)

    # Add the last point
    vxtab.append(nextPt)
 
    if len(vxtab)<3:
      if WFBasic.PYPOS3D_TRACE: print('  PlaneSlice[{0:s}] ignoring cleaned face : {1:d}'.format(target.getName(), faceno))
      continue

    
    # Prepare the list of face edges
    lstEdgeVx = [ (vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ (vxtab[-1], vxtab[0]), ]

    # Now the plan is at the origin - The Normal is enough to cut
    _, lstNewEdges, _ = FaceCut(lstEdgeVx, cuttingVect, hasTexture, True, radialLimit2)
 
    # Add the new Edges to the closing Face
    if lstNewEdges:
      closingFaceVx += lstNewEdges
      if keepMaterial:
        cutFaceMatLst.append(target.matIdx[faceno])
  
  # Compute the closing face(s) and keep the first one
  lstEdgesList, loccl, _  = CreateLoop(closingFaceVx)
  lstEdges = lstEdgesList[0] if lstEdgesList else [ ]

  # Scale if required 
  if radialScale>0.0:
    for p in loccl:
      p.x *= radialScale
      p.y *= radialScale
    
  # Eliminate too short edges, if required
  if minLength>0.0:
    
    for i,e in enumerate(lstEdges):
      if e.norme()<minLength:
        # Remove this edge  
        # Compute the 'mid' point with a bspline cubic algo
        pmid = Point3d(e.p0).add(e.p1).scale(0.5)
        loccl.append(pmid)
        
        # Compute potential texute coordinate
        if hasTexture:
          pmid.texture = TexCoord2f(TexCoord2f(e.p0.texture).add(e.p1.texture).scale(0.5))
        
        l = len(lstEdges)
        # Change points in previous and next edge
        lstEdges[i-1] = Edge(lstEdges[i-1].p0, pmid)
        lstEdges[(i+1)%l] = Edge(pmid, lstEdges[(i+1)%l].p1)
      
        del lstEdges[i]
      
  # Return to initial coordinate system
  rep.inFrom(loccl)
    
  logging.info("End for %s: List of Edges=[%d edges]", target.getName(), len(lstEdges))

  return lstEdges


#
# Compute the vertex indexes (and TexVert) into final coord List indexes
# Change the coordinate system to the 'image' one
# Return a list of loops defined by indexes in the final coord list
#
def __prepareForMeshing(coordList, Loops, botFaceNorm):
  LoopsIdx = [ ]
    
  for loop in Loops:
    loopIdx = [ ]
    
    for noedge, ed in enumerate(loop):
      idx0 = IndexAdd(coordList, Point3d(ed.p0))
      idx1 = IndexAdd(coordList, Point3d(ed.p1))
      loopIdx.append(idx0)
      loop[noedge] = Edge(ed.p0, ed.p1, idx0, idx1)
  
    LoopsIdx.append(loopIdx)
  
  # Check Rotation orders to be aligned with the bottom face normal
  for loop in Loops[1:]:
    FaceNormalOrder(loop, botFaceNorm)

  return LoopsIdx



# -----------------------------------------------------------------------------
# TODO: Rework output (Cutting Data)
# TODO: Add a fillHole to the top part
def RadialScaleRemesh(target, centerOrRepOrPlane, eu=None, ev=None, dh=0.0, ds=0.0, repOrtopPlane=None, \
                      nbSlice=5, radialLimit=0.0, minLength=0.0, tabScale=None, reScale=False, \
                      reMesh=False, cutTop=False, cutBottom=True, \
                      fillHole=True, filledHoleMat='Extremity', \
                      alpha=0.0625):
  ''' RadialScaleRemesh is an high level function to rework a part of a geometry while preserving the extremities.
  - Cut target into 3 groups according to the first coord syst (centerOrRepPlane) 
    and the second coord syst defined eicher by a coord sys or a plane or a distance 
    from the first coord system along Oz axis.
  - Optionaly Remesh the central part
  - Optionaly perform a hole filling on the bottom face
  - Optionaly rescale the centrale part (quadric or spline defined by a tab of scales)
  
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to rework

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system
 
  dh : float, optional, default 0.0
    Distance between the bottom plane and to top plane along the normal vector of the bottom plane.
    When dh=0.0, repOrTopPlane arg shall be given

  ds : float, optional, default 0.0
    Scaling agrument. Distance between the bottom plane and the bottom of the parabol for scaling options.
    Refer to GeomGroup.RadialScale for detailed explanations

  repOrtopPlane : CoordSyst OR GeomGroup
    When this parameter is a CoordSyst, it defines the top cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  nbSlice : int, optional, default 5
    Remesh argument. Number of slices of the remeshed central zone

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'

  minLength : float, optional, default 0.0
    When not null, created egdes shall be longuer than minLength


  tabScale : list of float, optional, default None
    Scaling argument.
    if tabScale not null, it must contain nbSlice+1 float. a Null float value means no radial scaling
      tabScale[0] is at bottom
      tabScale[nbSlice] is at top
    Refer to CoordSyst.RadialSplineScaling for details

   reScale : bool, optional, default False
     Ask for a scaling of the central part

   reMesh : bool, optional, default False
     Ask for a remesh of the central part

   cutTop : bool, optional, default False
     True : The result WaveGeom does not contain any group for the cut part
     False : The result WaveGeom contains a group for the cut part

   cutBottom : bool, optional, default True
     True : The result WaveGeom does not contain any group for the cut part
     False : The result WaveGeom contains a group for the cut part

   fillHole : bool, optional, default True
     Ask for a hole filling operation on the bottom face. Usually with cutBottom=True

   filledHoleMat : str, optional, default='Extremity'
     Material name to give to the faces created by the fill hole option
     or
     Material name to give to the closing face of the bottom
     or
     When set to None : No closing face is created

   alpha : float, optional, default = 0.0625
     fillHole coef (refer to WaveGeom.fillHole


  Returns
  -------
  WaveGeom, CuttingData :
    a new WaveGeom with 1 to 3 GeomGroups
    The cutting data where topGrp is cd.grp and the central part is cd.ogrp 

  '''
  logging.info("Start for %s", target.getName())

  # Validate inputs
  if reScale and dh==0.0 and not tabScale:
    logging.warning('  ({0:s})-dh and tabScale are null: No Scaling allowed'.format(target.getName()))

  if fillHole and not cutBottom:
    logging.warning('  ({0:s})-Hole filling requires to CutBottom=True: ERROR'.format(target.getName()))
    return None, C_ERROR

  # Compute the Cutting axis and the transformation matrix of the reference plan (the bottom Plan)
  if isinstance(centerOrRepOrPlane, Point3d):
    center = centerOrRepOrPlane
    repBottom = CoordSyst(center, eu, ev)
  elif isinstance(centerOrRepOrPlane, CoordSyst):
    repBottom = centerOrRepOrPlane
    center = centerOrRepOrPlane.center
  else: # Supposed to be a plane
    repBottom = centerOrRepOrPlane.calcCoordSyst()
    center = repBottom.center

  # Determine top cutting plane
  # Create a coordinate system for the cut of the top faces
  if isinstance(repOrtopPlane, CoordSyst):
    repTop = repOrtopPlane
  else:
    topPlane = repOrtopPlane
    repTop = topPlane.calcCoordSyst() if topPlane else CoordSyst(Point3d(center).add(Vector3d(0.0, 0.0, dh).inLin33(repBottom.MT)), repBottom.eu, repBottom.ev)

  # Slice the objet in three groups (bottom group is tmpCd.ogrp)
  _, tmpCd = PlaneSplit(target, repBottom, materialName='bottomTmpFace', radialLimit=radialLimit)

  if tmpCd.nbFaces!=1:
    logging.warning('  ({0:s})-Bottom Extremity slice does not contain one face but:{1:d}'.format(target.getName(), tmpCd.nbFaces))
    return None, tmpCd

  # Slice along the top plane : topGrp is cd.grp and the central part is cd.ogrp 
  nwg, cd = PlaneSplit(tmpCd.grp, repTop, materialName='topTmpFace', radialLimit=radialLimit)

  if cd.nbFaces!=1:
    logging.warning('  ({0:s})-Top Extremity slice does not contain one face but:{1:d}'.format(target.getName(), cd.nbFaces))
    return None, cd

  topGrp = cd.grp

  # Add the bottom group to the final WaveGeom
  bottomGrp = nwg.addGroup(tmpCd.ogrp)

  # Create the list of edges with new vertex and potential texture attributes
  bottomLoop = tmpCd.grp.getFaceLoop('bottomTmpFace', hasTexture=tmpCd.hasTexture) #, invertNorm=True)

  # Create the list of edges with new vertex and potential texture attributes
  topLoop = topGrp.getFaceLoop('topTmpFace', hasTexture=cd.hasTexture)
    
  # The working group
  target = cd.ogrp

  # Remesh if required
  if reMesh:
    # Create loop of edges for each slicing position (along Oz)
    Loops = [ bottomLoop, ] if bottomLoop  else [ ]
    Reps = [ repBottom, ] if bottomLoop  else [ ]
    
    faceMatLst = []
    c0cn = Point3d(repTop.center).sub(center)

    logging.info("ReMesh [%s]: %d loops", target.getName(), len(Loops))    
    
    # For each slice
    for islice in range(1, nbSlice):
      k = float(islice)/float(nbSlice)
      centers = Point3d(center).add(Vector3d(c0cn).scale(k))
      evk = Vector3d(repBottom.ev).scale(1.0-k).add(Vector3d(repTop.ev).scale(k)).normalize()
      euk = Vector3d(repBottom.eu).scale(1.0-k).add(Vector3d(repTop.eu).scale(k)).normalize()
      repk = CoordSyst(centers, euk, evk)
      Reps.append(repk)

      # Loops[islice] = Plane Slice 'only' 
      nLoop = PlaneSlice(target, centers, euk, evk, cutFaceMatLst=faceMatLst, \
                         radialLimit=radialLimit, minLength=minLength)
      Loops.append(nLoop)
    
    #if topLoop:
    Loops.append(topLoop)
    Reps.append(repTop)
    
    # Create a regular Mesh with the loops
    ngrp = nwg.createGeomGroup(target.getName() + '_remeshed')    
    ngrp.curMatIdx = faceMatLst[0]  
    hasTexture = cd.hasTexture
  
    # Record Vertex and Texture in the WaveGeom (new Point3d(s)) - Compute Final indexes
    # Convert Edges' points into the repBottom coordinate system
    LoopsIdx = __prepareForMeshing(ngrp.coordList, Loops, Vector3d(repBottom.ew).neg())
  
    for noloop, loop in enumerate(Loops[:-1]):
      ngrp.createStrip(loop, Loops[noloop+1], Reps[noloop], Reps[noloop+1], hasTexture)

    logging.info("ReMesh-finish [%s]: %d loops", target.getName(), len(Loops))    

    # Perform the scaling, Only available with reMesh
    if reScale and tabScale:
      for noloop, loop in enumerate(Loops):
        Reps[noloop].RadialScalePoint([ nwg.coordList[idx] for idx in LoopsIdx[noloop] ], tabScale[noloop])
      # FIX: Avoid a double scaling in case of parameter mix
      reScale = False

    # Put back the top group (they belong the same WaveGeom)
    # So Vertex Indexes have not been changed
    if not cutTop:
      ngrp.fusion(topGrp)

    # Rebuild the bottom face if fillHole required
    if fillHole or filledHoleMat:
      # Rebuild the bottomLoop 
      vxtab = [ nwg.coordList[idx] for idx in LoopsIdx[0] ]
      if hasTexture: # Texture Coord were kept in the original copy of the bottom loop
        for i,p in enumerate(vxtab):
          p.texture = Loops[0][i].p0.texture
      
      # Create this face by changing its order
      Loop0 = [ Edge(vxtab[i], vxtab[(i+1)%len(vxtab)]) for i in range(0, len(vxtab)) ] # + [ Edge(vxtab[0], vxtab[-1]), ]
      ngrp.addFaceByEdges(Loop0, hasTexture, 'bottomTmpFace')

    # Remove the old middle part
    nwg.removeGroup(target)

  else: # No meshing : Must retrieve the central part
    logging.info("Finish [%s]", target.getName())    

    ngrp = target
    if not cutTop:
      ngrp.fusion(topGrp)

  if not cutBottom:
    ngrp.fusion(bottomGrp)

  # Remove Useless groups
  nwg.removeGroup(topGrp)
  nwg.removeGroup(bottomGrp)

  # Remove the topTmpFace
  ngrp.removeFace(materialName='topTmpFace')

  # Do Quadratic Radial scaling, if not already done by the tabScale param
  # With dh<>0, tabScale should be null
  if reScale and dh>0.0 and not tabScale:
    R = repTop.calcXYRadius( [ e.p0 for e in topLoop ] )
    repBottom.RadialQuadraticScaling(nwg.coordList, R, dh, ds, repTop, radialLimit)
  elif reScale and dh>0.0 and tabScale:
    R = repTop.calcXYRadius( [ e.p0 for e in topLoop ] )
    repBottom.RadialSplineScaling(nwg.coordList, R, dh, ds, repTop, radialLimit, tabScale)
    
  # Do a hole filling on the fusioned face
  if fillHole:
    # Fusion (if needed) the Cutting face
    ngrp.FaceFusion(prevMatName='bottomTmpFace', newMatName='Hole')    
    nwg.fillHole(ngrp, 'Hole', 'embout', filledHoleMat, True, 2, alpha, createCenter=False)
  elif filledHoleMat:
    ngrp.FaceFusion(prevMatName='bottomTmpFace', newMatName=filledHoleMat)    

  # Optimze final WaveGeom and clean unused vertex
  nwg.optimizeGroups(cleaning=True)
 
  return nwg, cd





