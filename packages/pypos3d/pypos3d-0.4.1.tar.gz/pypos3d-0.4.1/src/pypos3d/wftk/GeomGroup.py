# -*- coding: utf-8 -*-
# package: pypos3d.wftk
import sys, copy
import logging
import math

import numpy as np
from scipy import spatial

from langutil import C_FAIL, C_ERROR , C_OK

from pypos3d.wftk import WFBasic
from pypos3d.wftk.WFBasic import C_VERTEX_NOT_FOUND, COUNT, FEPSILON, TexCoord2f, CoordSyst
from pypos3d.wftk.WFBasic import LowestIdxPos, CreateLoop, FaceNormalOrder
from pypos3d.wftk.WFBasic import Point3d, Vector3d, Edge, Regularity, IndexAdd, CreateTransform
from pypos3d.wftk.PaveList2D import PaveList2D

class GeomGroup(object):
  ''' GeomGroup represents a Geometrical group of faces and lines (3D).  '''

  def __init__(self, name='', src=None, inCoordList=None):
    ''' Create a GeomGroup.
    
    Parameters
    ----------
    name : str
      Name of the GeomGroup

    src : GeomGroup
      Source for the GeomGroup (copy constructor)

    inCoordList : list of Point3d
      List of 3D vertex to initialize the GeomGroup
    '''
    #  Pointer to the coordinate table of the whole object
    self.coordList = src.coordList if src else (inCoordList if inCoordList else [])
    self.texList = src.texList if src else [ ]
    self.normList = src.normList if src else [ ]

    # Pointer to the WaveGeom
    self.geom = src.geom if src else None

    # group name. Multiple group names are not managed as defined in OBJ format
    self._name = src._name if src else name

    # Contains the index of the first element of vertIdx that defines a face
    # Length > 1
    self.stripCount = copy.copy(src.stripCount) if src else [ 0, ]

    # Contains the index of the first element of vertIdx that defines a line
    # Null if no line OR Length > 1
    self.lineStripCount = copy.copy(src.lineStripCount) if src else [ 0, ]

    self.matIdx = copy.copy(src.matIdx) if src else []

    # Indexes of Vertex that compose each face
    self.vertIdx =  copy.copy(src.vertIdx) if src else []

    # Indexes of Texture that compose each face (empty if none)
    self.tvertIdx =  copy.copy(src.tvertIdx) if src else []

    # Indexes of Normal that compose each face (empty if none)
    self.normIdx =  copy.copy(src.normIdx) if src else []

    # Indexes of Vertex that compose each line
    self.vertLineIdx =  copy.copy(src.vertLineIdx) if src else []

    # Indexes of Texture that compose each line
    self.tvertLineIdx =  copy.copy(src.tvertLineIdx) if src else []

    self._bestCrit = src._bestCrit if src else 0.0
    self.curMatIdx = src.curMatIdx if src else 0
    self.lstMat = src.lstMat if src else None

  def __str__(self):
    return 'GeomGroup[{0:s}]: {1:d} faces'.format(self._name, self.getNbFace())


  def getNbFace(self):
    ''' Returns the number of faces '''
    return len(self.stripCount) - 1

  def getNbLine(self):
    ''' Returns the number of lines '''
    return 0 if (self.lineStripCount == None) else len(self.lineStripCount) - 1

  def getName(self):  return self._name

  def setName(self, n):
    self._name = n

  def getFaceStartIdx(self, noface):
    return self.stripCount[noface]

  def getFaceLastIdx(self, noface):
    return self.stripCount[noface + 1]

  def getMatIdx(self, noface):
    return self.matIdx[noface]

  def setMatIdx(self, noface, idx):
    self.matIdx[noface] = idx

  # public int[] getFaceVertIdx(int noface, int[] restab)
  def getFaceVertIdx(self, noface):
    ''' Return the list of index of the Vertex of the given face. '''
    startIdx = self.getFaceStartIdx(noface)
    lastIdx = self.getFaceLastIdx(noface)
    return self.vertIdx[startIdx:lastIdx] 

  # public int[] getFaceTVertIdx(int noface)
  def getFaceTVertIdx(self, noface):
    ''' Return the list of index of the texture coordinates of the given face. '''
    startIdx = self.getFaceStartIdx(noface)
    lastIdx = self.getFaceLastIdx(noface)
    return self.tvertIdx[startIdx:lastIdx] 

  def getFaceNormIdx(self, noface):
    ''' Return the list of index of the normals (Vector3d) of the given face. '''
    startIdx = self.getFaceStartIdx(noface)
    lastIdx = self.getFaceLastIdx(noface)
    return self.normIdx[startIdx:lastIdx] 


  def getFaceVertex(self, noface, copyPoint=False, restab=None):
    ''' Return the list of Vertex of given face.
    Parameters
    ----------
    noface : int
      Face number [0 .. NbFace[
    copyPoint : bool
      if true, new Point3d are created.
      By default, this method return a pointers to the existing Point3d (in CoordList)
    restab : list
      Use restab to populate the result, else create a new list

    Returns
    -------
    list of Point3d
    '''
    startIdx = self.getFaceStartIdx(noface)
    lastIdx = self.getFaceLastIdx(noface)
    
    if restab:
      restab[:] = [ Point3d(self.coordList[self.vertIdx[i]]) for i in range(startIdx, lastIdx) ] if copyPoint else [ self.coordList[self.vertIdx[i]] for i in range(startIdx, lastIdx) ]
      return restab

    return [ Point3d(self.coordList[self.vertIdx[i]]) for i in range(startIdx, lastIdx) ] if copyPoint else [ self.coordList[self.vertIdx[i]] for i in range(startIdx, lastIdx) ]

  #
  #
  def getFaceLoop(self, faceDescr, hasTexture=False, invertNorm=False):
    ''' Returns an (eventually) textured set of Edges
    Point3d are copied from the coordList and muted with a .texture attr

    Parameters
    ----------
    faceDescr : int or str
      if faceDescr is a str, it is considered as a Material Name. The selected face, is the first 
      with this material
      if faceDescr is an int,it should be a valid faceno
    hasTexture : bool
      Indicates that the face as texture coordinates
    invertNorm : bool
      if true the face order is reverted
    
    Returns
    -------
    list of Edge
    '''
    faceno = self.findFace(self.geom.lstMat.index(faceDescr)) if isinstance(faceDescr, str) else int(faceDescr)

    # Create the list of edges with new vertex with potential textures 
    startidx = self.getFaceStartIdx(faceno)
    lastidx = self.getFaceLastIdx(faceno)
    
    # Use new points with previous face definition
    vxtab = [ Point3d(self.coordList[self.vertIdx[i]]) for i in range(startidx, lastidx) ]

    if invertNorm:
      vxtab.reverse()

    if hasTexture: # Mutate the Point3d, so that they contain the associated texture coordinates
      for i, p in enumerate(vxtab):
        p.texture = self.texList[self.tvertIdx[i+startidx]]
  
    # Return the list of face edges
    return [ Edge(vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ Edge(vxtab[-1], vxtab[0]), ]



  def findTVertIdx(self, ptIdx):
    ''' Find the first face that refers to <code>vertIdx</code> and return the associated texture index.
    Parameters
    ----------
    vertIdx : int
      Index of the vertex to look for.

    Returns
    -------
    int
      The texture index, 
       C_VERTEX_NOT_FOUND if vertex not found, 
       C_FAIL if no texture index are available
    '''
    if ((self.tvertIdx == None) or (len(self.tvertIdx) == 0)):
      return C_FAIL

    for faceno in range(0, len(self.stripCount) - 1):
      startIdx = self.stripCount[faceno]
      lastIdx = self.stripCount[faceno + 1]

      for i in range(startIdx, lastIdx):
        if (self.tvertIdx[i] == ptIdx):
          return self.tvertIdx[i]

    return C_VERTEX_NOT_FOUND

  def addFace(self, coordIdx, texIdx, normIdx):
    ''' Add a face defined by indexes of Vertex, Texture Coords and normals if any.
  
    Return the origin coordIdx for convenience
    '''   
    empty = not self.vertIdx
    self.vertIdx += coordIdx
    self.stripCount.append(len(self.vertIdx))
    self.matIdx.append(self.curMatIdx)

    if self.tvertIdx or (empty and texIdx):    
      if texIdx:    
        self.tvertIdx += texIdx
      
      #while (len(self.tvertIdx) < ):
      self.tvertIdx += [0]*(len(self.vertIdx)-len(self.tvertIdx))
    
    if self.normIdx or (empty and normIdx):
      if normIdx:    
        self.normIdx += normIdx
        
      self.normIdx += [0]*(len(self.vertIdx)-len(self.normIdx))
      
    return coordIdx


  def addLine(self, coordIdx, texIdx): # List<Integer> coordIdx, List<Integer> texIdx)
    ''' Add a line defined by indexes of Vertex, Texture Coords and normals if any.
  
    Return the origin coordIdx for convenience
    '''   

    self.vertLineIdx += coordIdx
    self.tvertLineIdx += texIdx

    while (len(self.tvertLineIdx) < len(self.vertLineIdx)):
      self.tvertLineIdx.append(0)

    self.lineStripCount.append(len(self.vertLineIdx))
    self.matIdx.append(self.curMatIdx)
    return coordIdx
    
  def addFaceByEdges(self, lstEdges, hasTexture, materialName, refNorm=None):
    ''' Create the closing face(s) and add it(them) to the list of faces of the group.
    This method uses the CreateLoop function based on a min/max tree search with 
    alpha-beta prune. 

    Parameters
    ----------
    lstEdges : list of Edge(s)
      List of Edges where faces will be search
    hasTexture : bool
      Indicates that the face has texture coordinates
    materialName : str
      Material to assign to the created face(s)
    refNorm : Vector3d
      if not null used to reorganize faces so that their normals are aligned with the reference one

    Returns
    -------
    list of face indexes, number of faces, list of Point3d
    '''
    wg = self.geom
    self.curMatIdx = wg.addMaterial(materialName)
    
    lstFacesIdx = [ ]
  
    FaceLst, coordList, *_ = CreateLoop([ e for e in lstEdges if e])
    logging.info('Loop %d faces created', len(FaceLst))
    # Warning: Face edges' order my be mixed
    for f in FaceLst:
      
      if refNorm and f: # Check face definition : Counter clock shall match refNorm
        FaceNormalOrder(f, refNorm)
      
      coordIdx = [ IndexAdd(wg.coordList, e.p0) for e in f ]
      lstFacesIdx += coordIdx
      texIdx = [ IndexAdd(wg.texList, e.p0.texture) for e in f ] if hasTexture else [ ]
        
      self.addFace(coordIdx, texIdx, [ ])
  
    return lstFacesIdx, len(FaceLst), coordList


  def addFacesByVertexO2(self, nFaceList, nMatList, hasTexture=False):
    ''' Add a list of faces defined by a list of vertex.
    O(n2) algorithm
    '''    
    for faceno, f in enumerate(nFaceList):
      coordIdx = [ ]
      texIdx = [ ]
      
      # Protect from "None" faces with Slice Option
      if not f: continue
      
      for p in f:
        try:
          idx = self.coordList.index(p)
        except:
          idx = len(self.coordList)
          self.coordList.append(p)
          
        coordIdx.append(idx)
        
        if hasTexture:
          try:
            idx = self.texList.index(p.texture)
          except:
            idx = len(self.texList)
            self.texList.append(p.texture)
            
          texIdx.append(idx)  
          
      # Take into account original Material of the face
      self.curMatIdx = nMatList[faceno]
      self.addFace(coordIdx, texIdx, [ ])
  
  def addFacesByVertex(self, nFaceList, nMatList, hasTexture=False):
    ''' Add a list of faces defined by a list of vertex.
    Octree (scipy.spatial.KDTree) algorithm
    '''    
    # List of new points
    tmpCoordList = [ ]
    nbMaxVerts = len(self.coordList)
    nbMaxTVerts = len(self.texList)
    
    if (nbMaxVerts<1000) and (nbMaxTVerts<1000):
      logging.info("Using O(n2) method: %d", nbMaxVerts)
      return self.addFacesByVertexO2(nFaceList, nMatList, hasTexture=hasTexture)
    
    logging.info("Init CoordList/TexList: %d/%d", nbMaxVerts, nbMaxTVerts)
 
    nbsrc = len(self.coordList)
    npTab = np.zeros( (nbsrc, 3) )
    for pNo, p in enumerate(self.coordList):
      npTab[pNo] = [ p.x, p.y, p.z ]
    
    # Create an KDTree with the 'known Vertex' in a "global" np.array
    tree = spatial.KDTree(npTab, leafsize=10 if nbsrc<10000 else 100)
    svect = np.zeros((1,3))
    
    if hasTexture:
      # Create a PaveList with the 'known Texture coords' in a "global" np.array
      pl = PaveList2D(n=32, texList=self.texList)
    
    for faceno, f in enumerate(nFaceList):
      coordIdx = [ ]
      texIdx = [ ]
      
      # Protect from "None" faces with Slice Option
      if not f: continue
      
      for p in f:
        # Search in KDTtree
        svect[0] = [ p.x, p.y, p.z ]
        rest, resIdx = tree.query(svect)

        # if found (not too far) ==> Put it in a tmp table
        if rest[0]<FEPSILON:
          # Use an existing vertex
          idx = resIdx[0]
        else:
          # Add a new vertex to the local list of new Vertex
          try:
            idx = tmpCoordList.index(p)
          except:
            idx = len(tmpCoordList)
            tmpCoordList.append(p)

          # New Points are comming after the existing ones
          idx+=nbsrc          

        coordIdx.append(idx)
        
        if hasTexture:
          idx = pl.IndexAdd(p.texture)
          texIdx.append(idx)  
          
      # Take into account original Material of the face
      self.curMatIdx = nMatList[faceno]
      self.addFace(coordIdx, texIdx, [ ])
    #End for faceno 

    # Update the Global CoordList
    self.coordList += tmpCoordList



  # public int fillDedupFace(int nbFace, int[] tabHshFace, int[][] tabFaceIdx)
  def fillDedupFace(self, nbFace, tabHshFace, tabFaceIdx):
    ''' Copy strip data to deduplication tables '''
    for faceno in range(0, len(self.stripCount) -1):
      startIdx = self.stripCount[faceno]
      lastIdx = self.stripCount[faceno+1]
      idxTab = self.vertIdx[startIdx:lastIdx]
      nbv = lastIdx - startIdx

      # Find lowest index
      lowestIdx = LowestIdxPos(idxTab)
      finalIdxTab = [ idxTab[(i + lowestIdx) % nbv] for i in range(0, nbv) ]
      tabHshFace.append( sum(finalIdxTab) )
      tabFaceIdx.append( finalIdxTab )
      nbFace+=1

    return nbFace

  def extendLoopVicinity(self, edgePtIdx, edgeLoopPtIdx):
    '''Extends edgeLoopPtIdx with vertex of faces that are using vertex of edgePtIdx tab.
     As of 23-May-2020 : edgeLoopPtIdx does not need to be initialized. It'll grow 
     @param edgePtIdx       Initial table of vertex
     @param edgeLoopPtIdx   Table to extends.
    '''

    # For each point of existing loop
    for vi in edgePtIdx:
      # Search for faces that contains the current vertex
      for fno in range(0, self.getNbFace()):
        staIdx = self.stripCount[fno]
        lstIdx = self.stripCount[fno+1]

        if vi in self.vertIdx[staIdx:lstIdx]:
          # Add all vertex of the face to the target Loop if the new vertex is not already in it
          for nvertidx in self.vertIdx[staIdx:lstIdx]:
            if not nvertidx in edgeLoopPtIdx:
              edgeLoopPtIdx.append(nvertidx)


#  /* (non-Javadoc)
#   * @see deyme.v3d.wf.GeomGroup#buildVectors()
#   */
#  public long[] buildVectors()
  def buildVectors(self, geomcond=None):
    vectTbl = [ ]

    hasTexture = (self.tvertIdx!=None) and (len(self.tvertIdx)>0)

    for faceno in range(0, len(self.stripCount) - 1):
      startIdx = self.stripCount[faceno]
      lastIdx = self.stripCount[faceno + 1] - 1
      for i in range(startIdx, lastIdx):
        idx0 = self.vertIdx[i]
        idx1 = self.vertIdx[i + 1]
        p0 = Point3d(self.coordList[idx0])
        p1 = Point3d(self.coordList[idx1])

        if not geomcond or (geomcond(p0) and geomcond(p1)):
          if hasTexture:
            p0.texture = self.texList[self.tvertIdx[i]]
            p1.texture = self.texList[self.tvertIdx[i+1]]
          vectTbl.append(Edge(p0, p1, idx0, idx1))

      # To close the loop
      idx0 = self.vertIdx[lastIdx]
      idx1 = self.vertIdx[startIdx]
      p0 = Point3d(self.coordList[idx0])
      p1 = Point3d(self.coordList[idx1])
      if not geomcond or (geomcond(p0) and geomcond(p1)):
        if hasTexture:
          p0.texture = self.texList[self.tvertIdx[lastIdx]]
          p1.texture = self.texList[self.tvertIdx[startIdx]]
        vectTbl.append(Edge(p0, p1, idx0, idx1))

    # Sort the Vector table to keep only lonely vectors
    return sorted(vectTbl, key=Edge.hashCode)


  def findEdges(self, geomcond=None):
    ''' Find a set of edges (according geomcond on Point3d)
    Edge are containg a copy of each source point (with a .texture attribut if any)
    '''
    logging.info("Group[%s]: %d faces", self._name , self.getNbFace())
    vectTbl = self.buildVectors(geomcond=geomcond) # Edge[] 
    logging.info("Group[%s]: %d vectors", self._name, len(vectTbl))

    vectno = 0

    # Edge[] edgeVect
    edgeVect = [ ]

    lenin = len(vectTbl)
    while vectno < lenin:
      curVect = vectTbl[vectno]
      vectno+=1

      nbocc = 1
      while (vectno < lenin) and (curVect==vectTbl[vectno]):
        vectno+=1
        nbocc+=1

      if nbocc==1:
        edgeVect.append(curVect)

    logging.info("Group[" + self._name + "]: " + str(len(edgeVect)) + " edge vectors deduced")

    return edgeVect

  def findFace(self, matidx):
    ''' Return the first faceno using the given material (by index) '''
    try:
      return self.matIdx.index(matidx)
    except:
      return -1

  def setBestCrit(self, crit):
    self._bestCrit = crit

  def setMaterialName(self, matIdx):
    self.curMatIdx = matIdx

  def invertFaceOrder(self):
    ''' Invert all faces order (ie. revert 'auto' normals)
    '''
    hasTexture = (self.tvertIdx!=None) and (len(self.tvertIdx)>0)  
    hasNormal = (self.normIdx!=None) and (len(self.normIdx)>0)  

    tmpVert = [] 
    tmpTVert = []

    for faceno in range( 0, self.getNbFace()):
      fvi = self.getFaceVertIdx(faceno)
      fvi.reverse()
      tmpVert += fvi
      
      if hasTexture:
        fvti = self.getFaceTVertIdx(faceno)
        fvti.reverse()
        tmpTVert += fvti
        
    self.vertIdx[:] = tmpVert[:]
    
    if hasTexture:
      self.tvertIdx[:] = tmpTVert[:]
      

    

#   */

                         
    
  # -----------------------------------------------------------------------------
  def sanityCheck(self):
    ''' Check the consistency of a group. '''
    res = C_OK
    name = self.getName() if self.getName() else "NoName"
    
    sizeVertexList = len(self.geom.coordList)
    
    # Verify Vertex indexes
    for vi in self.vertIdx:
      if (vi<0) or (vi>=sizeVertexList):
        print('Group[{0:s}] Bad Vertex Index: {1:d}'.format(name, vi))
        res = C_ERROR
    
    if self.tvertIdx:
      if len(self.tvertIdx)!=len(self.vertIdx):
        print('Group[{0:s}] Bad Length for Texture Index: {1:d} instead of {2:d}'.format(name, len(self.tvertIdx),len(self.vertIdx)))
        res = C_ERROR

      sizeTexList = len(self.geom.texList)
        
      for vti in self.tvertIdx:
        if (vti<0) or (vti>=sizeTexList):
          print('Group[{0:s}] Bad Texture Index List: {1:d}'.format(name, vti))
          res = C_ERROR
        
    if self.normIdx:
      if len(self.normIdx)!=len(self.vertIdx):
        print('Group[{0:s}] Bad Length for Normal Index List: {1:d} instead of {2:d}'.format(name, len(self.normIdx),len(self.vertIdx)))

      sizeNormList = len(self.geom.normList)
        
      for vti in self.normIdx:
        if (vti<0) or (vti>=sizeNormList):
          print('Group[{0:s}] Bad Normal Index : {1:d}'.format(name, vti))
          res = C_ERROR
    
    # Check faces counts
    nbf3, nbf4, nbfo = 0,0,0
    for faceno in range(0,self.getNbFace()):
      nbv = self.getFaceLastIdx(faceno) - self.getFaceStartIdx(faceno)
      if nbv==3: 
        nbf3+=1
      elif nbv==4:
        nbf4+=1
      else:
        nbfo+=1

    print('Group[{0:s}] has {1:d} Triangles, {2:d} Quad, {3:d} others'.format(name, nbf3, nbf4, nbfo))
    
    return res
    
  # -----------------------------------------------------------------------------
  def calcXYRadius(self, lstVxIdx):
    ''' Compute the Maximum Radius on Oxy plan of a list of vertex indices fo this group. '''
    rmax = sys.float_info.min
  
    for p in [ self.coordList[i] for i in lstVxIdx ]:
      r = p.x*p.x + p.y*p.y
      if r>rmax:
        rmax = r
  
    return math.sqrt(rmax)
  
  # -----------------------------------------------------------------------------
  def removeFace(self, faceno=-1, materialName=None):
    ''' Remove a face from a group.
    Enhancement: a more pythonic way (instead the copy of the java code)
    
    Parameters
    ----------
    faceno : int
      Face to remove (if >0)

    materialName : str
      Name of the material. Remove the first face with this material

    Returns
    -------
    int
      C_OK : Success
      C_ERROR : faceno==-1 and materialName not found
    '''
    if faceno==-1:
      if materialName:
        try:
          matidx = self.lstMat.index(materialName)
          faceno = self.matIdx.index(matidx)
        except ValueError:
          return C_FAIL
      else:
        return C_ERROR
      
    startidx = self.getFaceStartIdx(faceno)
    lastidx = self.getFaceLastIdx(faceno)
    delta = lastidx - startidx

    del self.matIdx[faceno]
    del self.vertIdx[startidx:lastidx]

    if self.tvertIdx:
      del self.tvertIdx[startidx:lastidx]
      
    if self.normIdx:
      del self.normIdx[startidx:lastidx]
      
    debsc = self.stripCount[:faceno] # if faceno>0 else [ ]
    finsc = [ sc-delta for sc in self.stripCount[faceno+1:] ]
    self.stripCount[:] = debsc + finsc
    
    return C_OK

  # -----------------------------------------------------------------------------
  def removeFaces(self, lstFaceNo=None, materialName=None):
    ''' Remove a set of faces given by their face numbers or a materialName. '''
    nbface = self.getNbFace()
    if not lstFaceNo:
      matidx = self.lstMat.index(materialName)
      lstFaceNo = [ fi for fi in range(0, nbface) if self.matIdx[fi]==matidx ]
      
    nstripcount = [ ]
    nvertidx = [ ]
    nmatIdx = [ ]
    ntvertIdx = [ ]
    nnormIdx = [ ]
    
    hasTexture = (self.tvertIdx!=None) and (len(self.tvertIdx)>0)  
    hasNormal = (self.normIdx!=None) and (len(self.normIdx)>0)  
      
    for fi in range(0,len(self.stripCount)-1):
      stidx = self.stripCount[fi]
      lastidx = self.stripCount[fi+1]
      
      if not fi in lstFaceNo:
        nstripcount.append(len(nvertidx))
        nmatIdx.append(self.matIdx[fi])
  
        for i, vidx in enumerate(self.vertIdx[stidx:lastidx]):
          nvertidx.append(vidx)
          
          if hasTexture:
            ntvertIdx.append(self.tvertIdx[stidx+i])
            
          if hasNormal:
            nnormIdx.append(self.normIdx[stidx+i])
            
    nstripcount.append(len(nvertidx))
    self.stripCount = nstripcount
    self.matIdx = nmatIdx
    self.vertIdx = nvertidx
    
    if hasTexture:
      self.tvertIdx = ntvertIdx
      
    if hasNormal:
      self.normIdx = nnormIdx
  
  def extractFaces(self, destName=None, materialName=None, inGeom=True):
    ''' Extract from the current group, the faces that match the condition
    Create a new group
    if inGeom is False: Create a new geometry
    else add the new group to the geometry of the current group
    '''    
    wg = self.geom if inGeom else self.geom.copy()
      
    try:
      matidx = self.lstMat.index(materialName)
    except ValueError:
      return None
    
    ngrp = wg.createGeomGroup(destName if destName else self.getName()+'_extracted_' + materialName)
    
    hasTexture = (self.tvertIdx!=None) and (len(self.tvertIdx)>0)  
    hasNormal = (self.normIdx!=None) and (len(self.normIdx)>0)  

    if inGeom:
      for faceno in range(0, self.getNbFace()):
        if self.matIdx[faceno]==matidx:
          ngrp.vertIdx += self.getFaceVertIdx(faceno)
          
          if hasTexture:
            ngrp.tvertIdx += self.getFaceTVertIdx(faceno)
          
          if hasNormal:
            ngrp.normIdx += self.getFaceNormIdx(faceno)
          
          ngrp.stripCount.append(len(ngrp.vertIdx))
          ngrp.matIdx.append(matidx)
    else:
      print('extractFaces not inGeom : NOT IMPLEMENTED YET')
      return None
    
    # Remove extracted faces
    self.removeFaces(materialName=materialName)
    
    return ngrp
    
    
      
  
  def FaceFusion(self, prevMatName, newMatName):  
    ''' Fusion of the faces with prevMatName into a single face with newMatName.
    If the faces are not connex, it may generate several faces.
    '''
    #Ensure the new Material exists
    self.geom.addMaterial(newMatName)
    
    lstFacesIdx = []
    nbface = self.getNbFace()
    matidx = self.lstMat.index(prevMatName)
    for faceno in range(0, nbface):
      if self.matIdx[faceno]==matidx:
        lstFacesIdx.append( self.getFaceVertIdx(faceno) )
    
    if len(lstFacesIdx)==1:
      # No Fusion required - Just change Mat name
      self.matIdx[self.matIdx.index(matidx)] = self.lstMat.index(newMatName)
      return
      
    
    # Create a dictionnary of unoriented edges
    #   dict of [ idx0, idx1, List of nextEdgeIdx Ptr=[], used=False, code, count, tidx0, tidx1 ]
    edgeDict = { }
    for f in lstFacesIdx:
      # For Each Edge
      for edge in [ (f[i], f[i+1]) for i in range(0, len(f)-1) ] + [ (f[-1], f[0]), ]:
        code = (min(edge) << 32) | max(edge)
        try:
          edgeDesc = edgeDict[code]
          edgeDesc[COUNT] += 1
        except KeyError:
          edgeDesc = [ edge[0], edge[1], [], False, code, 1, -1, -1 ]
          edgeDict[code] = edgeDesc
          
          
    bigFace = []
    # For Each Face
    for f in lstFacesIdx:
      # For Each Edge
      for edge in [ (f[i], f[i+1]) for i in range(0, len(f)-1) ] + [ (f[-1], f[0]), ]:
        # if Edge is exterior (not shared) Add it to the new edge list
        code = (min(edge) << 32) | max(edge)
        edgeDesc = edgeDict[code]
        if edgeDesc[COUNT]==1:
          # bigFace.append(edgeDesc)
          bigFace.append( (self.coordList[edge[0]], self.coordList[edge[1]]) )
          
    self.addFaceByEdges(bigFace, False, newMatName)
    # Remove old faces
    self.removeFaces(materialName=prevMatName)
  
  


  # -----------------------------------------------------------------------------
  def fusion(self, angrp):
    ''' Fusion 'ngrp' into self group.
    Both groups may belong to different WaveGeom

    Parameters
    ----------
    ngrp : GeomGroup
      Group to add.
    '''
    
    destHasTexture = (self.tvertIdx!=None) and (len(self.tvertIdx)>0)
    destHasNorm =  (self.normIdx!=None) and (len(self.normIdx)>0)
    hasTexture = (angrp.tvertIdx!=None) and (len(angrp.tvertIdx)>0)
    hasNorm =  (angrp.normIdx!=None) and (len(angrp.normIdx)>0)

    logging.info("Start [%s:%d faces, %d Vx, %d Tx] <- [%s:%d faces, %d Vx, %d Tx]", self.getName(), self.getNbFace(), \
                 len(self.coordList), len(self.texList), \
                 angrp.getName(), angrp.getNbFace(), len(angrp.coordList),len(angrp.texList))
    
    if self.geom!=angrp.geom:
      # They belong to different WaveGeom
      # the destination WaveGeom must be upgraded with missing Vertex, TVertex and Norms
      # All indexes must me remapped
      
      # Copy the added group
      ngrp = GeomGroup(src=angrp)
      
      nbInit = len(ngrp.coordList)
      mapVert = [-1] * nbInit      
      nbMaxVerts = len(self.coordList)      
      nbMaxTVerts = len(self.texList)

      if (nbMaxVerts<1000) and (nbMaxTVerts<1000):
        
        # Case of empty dest list (append few times)
        if nbMaxVerts==0: # Vertex Mapping are already copied and correct
          logging.info("Direct Copy of %d vertex", len(ngrp.coordList))
          self.geom.coordList[:] = ngrp.geom.getCoordList()
        else:
          logging.info("Using O(n2) method: %d/%d", nbMaxVerts, nbMaxTVerts)
          #t0 = time.clock()
          #nbhit = 0
          for i,vi in enumerate(ngrp.vertIdx):
            nvi = mapVert[vi]
            if nvi<0:
              nvi = IndexAdd(self.coordList, Point3d(ngrp.coordList[vi]))
              mapVert[vi] = nvi
            #else:
              #nbhit+=1
              
            ngrp.vertIdx[i] = nvi
          
          #dt = time.clock() - t0
          #print('O(n2).Vertex:{0:.1f} pt/s - hit:[{1:d}/{2:d}]'.format( float(len(ngrp.vertIdx))/float(dt), nbhit, len(ngrp.vertIdx)))
        
        if hasTexture:
          # Case of empty dest list (append few times)
          if nbMaxTVerts==0:# TexCoord Mapping are already copied and correct
            logging.info("Direct Copy of %d Texture coords", len(ngrp.texList))
            self.geom.texList[:] = ngrp.geom.getTexList()
          else:          
            #t0 = time.clock()
            mapTVert = [-1] * len(ngrp.texList)
            #nbhit, nbCommon = 0,0
            for i,vti in enumerate(ngrp.tvertIdx):
              nvti = mapTVert[vti]
              if nvti<0:
                nvti = IndexAdd(self.texList, TexCoord2f(ngrp.texList[vti]))
                mapTVert[vti] = nvti
                #nbCommon+=1
              #else:
                #nbhit+=1
            
              ngrp.tvertIdx[i] = nvti
    
            #dt = time.clock() - t0
            #print('O(n2).Text:{0:.1f} pt/s - hit:[{1:d}/{2:d}] - Common={3:d}'.format( float(len(ngrp.tvertIdx))/float(dt), nbhit, len(ngrp.tvertIdx), nbCommon))

  
        if hasNorm:          
          mapNorm = [-1] * len(ngrp.normList)
          for i,vti in enumerate(ngrp.normIdx):
            nvti = mapNorm[vti]
            if nvti<0:
              nvti = IndexAdd(self.normList, Vector3d(ngrp.normList[vti]))
              mapNorm[vti] = nvti
          
            ngrp.normIdx[i] = nvti
      
        # TODO: Proceed with Lines
      else: # Use an octree and a PaveList2D to merge coordList(s)
        logging.info("Using Octree method: %d/%d", nbMaxVerts, nbMaxTVerts)
        
        npTab = np.empty( (nbMaxVerts, 3) )
        for pNo, p in enumerate(self.coordList):
          npTab[pNo] = [ p.x, p.y, p.z ]
    
        # Create an KDTree with the 'known Vertex' in a "global" np.array
        tree = spatial.KDTree(npTab, leafsize=10 if nbMaxVerts<10000 else 100)
        svect = np.zeros((1,3))
        
        #t0 = time.clock()

        for i,vi in enumerate(ngrp.vertIdx):
          nvi = mapVert[vi]
          if nvi<0:
            # Search in KDTtree
            p = Point3d(ngrp.coordList[vi])
            svect[0] = [ p.x, p.y, p.z ]
            rest, resIdx = tree.query(svect)

            # if found (not too far) ==> Put it in a tmp table
            if rest[0]<FEPSILON: # Use an existing vertex
              nvi = int(resIdx[0])
            else: # Add a new vertex to the dest list of Vertex
              nvi = len(self.coordList)
              self.coordList.append(p)

            mapVert[vi] = nvi
          
          ngrp.vertIdx[i] = nvi
          
        #dt = time.clock() - t0
        #print('Octree.Vertex:{0:.1f} pt/s'.format( float(len(ngrp.vertIdx))/float(dt)))

        if hasTexture:
          mapTVert = [-1] * len(ngrp.texList)
          #minx, maxx, miny,maxy = sys.float_info.max, sys.float_info.min, sys.float_info.max, sys.float_info.min
          
          #t0 = time.clock()
          #nbhit, nbCommon = 0,0
          pl = PaveList2D(n=32, texList=self.texList)
          #dt = time.clock() - t0
          #print('PaveList.Create:{0:.1f} pt/s -stat:{1:s}'.format( float(len(ngrp.tvertIdx))/float(dt), pl.statStr()))

          for i,vti in enumerate(ngrp.tvertIdx):
#             dt = time.clock() - t0
#             if (dt>5.0) and (i%100==0): print('PAveList.Text[{0:d}] : {1:.1f} pt/s'.format( i, float(i)/dt))
            nvti = mapTVert[vti]
            if nvti<0:
              texture = TexCoord2f(ngrp.texList[nvti])
              nvti = pl.IndexAdd(texture)
              mapTVert[vti] = nvti
            #else:
              #nbhit+=1
              
            ngrp.tvertIdx[i] = nvti
          
          #dt = time.clock() - t0
          #print('Octree.PaveList:{0:.1f} pt/s - hit:[{1:d}/{2:d}] - Common={3:d}'.format( float(len(ngrp.tvertIdx))/float(dt), nbhit, len(ngrp.tvertIdx), nbCommon))
          
      # Map Material indexes
      mapMatIdx = [ IndexAdd(self.lstMat, matName) for matName in ngrp.lstMat ]
      ngrp.matIdx = [ mapMatIdx[mi] for mi in ngrp.matIdx ]

      # Keep the new group for fusion
      angrp = ngrp
    # else VertIdx Maps are identity
        
    if hasTexture:
      if not destHasTexture:
        self.tvertIdx = [0]*len(self.vertIdx)
    elif destHasTexture:
      angrp.tvertIdx = [0]*len(angrp.vertIdx)
    
    if hasNorm:
      if not destHasNorm:
        self.normIdx = [0]*len(self.vertIdx)
    elif destHasNorm:
      angrp.normIdx = [0]*len(angrp.vertIdx)
    
    destHasTexture = destHasTexture or hasTexture
    destHasNorm =  destHasNorm or hasNorm

    # Copy the faces 
    vertpos = len(self.vertIdx)
    
    self.matIdx += angrp.matIdx
    self.vertIdx += angrp.vertIdx
    self.stripCount = self.stripCount[:-1] + [ sc+vertpos for sc in angrp.stripCount ]
    
    if destHasTexture:
      self.tvertIdx += angrp.tvertIdx
      
    if destHasNorm:
      self.normIdx += angrp.vertIdx

    logging.info("End Result [%s:%d faces, %d Vx, %d Tx]", self.getName(), self.getNbFace(), len(self.coordList),\
                 len(self.texList) if destHasTexture else 0)


  def linkCoordList(self, wg):
    ''' Ensure that the GeomGroup points to WaveGeom common data. '''
    self.coordList = wg.coordList if wg else None
    self.texList = wg.texList if wg else None
    self.normList = wg.normList if wg else None
    self.lstMat = wg.lstMat if wg else None
    self.geom = wg if wg else None


  
  
  #
  # Create a strip of faces with two loops in the geom group
  # l0 >= l1
  #
  #
  #     X---------------------X---------------------X
  #     |\                                    ----- |
  #     | \                               ----      |
  #     |  \                           ---          |
  #     |   x-------------------------x..           |
  #     |   |                         |  ...        |
  #     |   |                         |      ..     |
  #     |   |                         |        ...  |
  #     |   |                         |           ..X
  #     |   |                         |             |
  #     |   x--------e=l1.j0----------x..           |
  #     |  /                             ...        |
  #     | /                                  ..     |
  #     |/                                     .... |
  #     X---------------e0=l0.0---------------------X
  #
  # Return the list of faces defined by a list of vertex indexes
  #
  def createStrip(self, l0, l1, Rep0, Rep1, hasTexture, minAngle=0.7854, minCosinus=0.01):
    ''' Create a strip of faces from two loops in the geom group.

    Parameters
    ----------
    l0 : list of Edge
      First list of egdes

    l1 : list of Edge
      Second list of egdes

    Returns
    -------
    list of faces
        list of faces defined by a list of vertex indexes
    '''
  
    lstFaces = []
    nbl0 = len(l0)
    nbl1 = len(l1)

    if (nbl0==0) or (nbl1==0):
      return C_ERROR

    if nbl0<nbl1: # Swap lists and Coord Systems
      # The faces will be build in the wrong order (wrt normal)
      l0, nbl0, Rep0, l1, nbl1, Rep1 = l1, nbl1, Rep1, l0, nbl0, Rep0
      swaped = True
    else:
      swaped = False
    
    if WFBasic.PYPOS3D_TRACE:
      for i in range(0,nbl0):self.geom.addMaterial('DebugMat'+str(i))
      self.geom.curGroup = self
    
    # Change coordinates to l0 coordinate system
    l0 = Rep0.To(l0, hasTexture=hasTexture)
    l1 = Rep0.To(l1, hasTexture=hasTexture)
      
    # j0 : Edge number in l1 where p0 is the closest to the first point of l0
    dmin = sys.float_info.max
    P0 = l0[0].p0
    j0 = -1
    # New heuristic: Estimate the distance at the Middle of segment
    mide0 = Point3d(P0).add(l0[0].p1).scale(0.5)
    for j,e in enumerate(l1):
      d = mide0.distance(Point3d(e.p0).add(e.p1).scale(0.5))
      if d<dmin:
        j0 = j
        dmin = d
      
    oneAgain = True
    j, jmax = j0, (j0-1)%nbl1
    i, imax = 0, nbl0-1
    e0Consumed, e1Consumed = False, False
      
    # Plot the strips
    #Plot(l0,l1)
    
    nbFaceInit = self.getNbFace()
    
    while oneAgain:
      if WFBasic.PYPOS3D_TRACE:
        self.geom.selectMaterial('DebugMat'+str(i))
          
      e0 = l0[i]
      e1 = l1[j]

      configUtil = 2*e0Consumed + e1Consumed
      if configUtil==0: # 2 New edges
        # Try a Quadrangle
        amin, aidx, cmin, cidx, vn = Regularity(e0.p0, e0.p1, e1.p1, e1.p0)
        if WFBasic.PYPOS3D_TRACE: print('createStrip({0:d},{1:d}) - sin[{2:g}, {3:d}] - cos[{4:g}, {5:d}] - {6:s}'.format(i,j, amin*180.0/math.pi, aidx, cmin, cidx,str(vn)))

        if (cmin>minCosinus) and (amin>minAngle): # Create a QuadAngle
          # Create a quandrangular face          
          texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p1, e1.p0 ] ] if hasTexture else [ ]
          vexIdxs = [e0.idx0, e0.idx1, e1.idx1, e1.idx0]
          e0Consumed = True
          e1Consumed = True
          if WFBasic.PYPOS3D_TRACE: print('  Quad {0:s} {1:s} {2:s} {3:s}'.format(str(e0.p0), str(e0.p1), str(e1.p1), str(e1.p0)))

        elif ((aidx==0) or (aidx==2)) or ((cidx==1) or (cidx==3)): # Create a T1 triangle
          texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p0 ] ] if hasTexture else [ ]
          vexIdxs = [e0.idx0, e0.idx1, e1.idx0]
          e0Consumed = True
          e1Consumed = False
          if WFBasic.PYPOS3D_TRACE: print('  Tri1 {0:s} {1:s} {2:s}'.format(str(e0.p0), str(e0.p1), str(e1.p0)))

        else: # Create a T2 triangle
          texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e1.p1, e1.p0 ] ] if hasTexture else [ ]
          vexIdxs = [e0.idx0, e1.idx1, e1.idx0]
          e0Consumed = False
          e1Consumed = True          
          if WFBasic.PYPOS3D_TRACE: print('  Tri2 {0:s} {1:s} {2:s}'.format(str(e0.p0), str(e1.p1), str(e1.p0)))

      elif configUtil==1: # 1 New edge : e0
        texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p1 ] ] if hasTexture else [ ]
        vexIdxs = [e0.idx0, e0.idx1, e1.idx1 ]
        e0Consumed = True

      elif configUtil==2: # 1 New edge : e1
        texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p1, e1.p1, e1.p0 ] ] if hasTexture else [ ]
        vexIdxs = [e0.idx1, e1.idx1, e1.idx0]
        e1Consumed = True

      #else: print('Impossible') : e0Consumed and e0Consumed can be both false


      # Add the new face taking into accound the reverted loops
      if not swaped:
        vexIdxs.reverse()
        texIdxs.reverse()

      lstFaces += self.addFace( vexIdxs, texIdxs, [ ] )


      # Compute new egdes
      if (i==imax) and (j==jmax):
        if e0Consumed and (i!=imax):
          i+=1
          e0 = l0[i]
          e0Consumed = False
          
        if e1Consumed and (j!=jmax):
          j = (j+1)%nbl1 
          e1 = l1[j]
          e1Consumed = False
          
        oneAgain = False
      else:
        if e0Consumed and (i!=imax): 
          i+=1
          e0Consumed = False
              
        if e1Consumed and (j!=jmax):
          j = (j+1)%nbl1
          e1Consumed = False
    # Wend        
  
    # Final Edges may not be consumed
    # Create a last triangle
    if (not e0Consumed and e1Consumed):
      texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p1 ] ] if hasTexture else [ ]
      vexIdxs = [e0.idx0, e0.idx1, e1.idx1 ]
      if swaped:
        vexIdxs.reverse()
        texIdxs.reverse()
      lstFaces += self.addFace( vexIdxs, texIdxs, [ ] )

    elif not e1Consumed and e0Consumed:
      texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p1, e1.p1, e1.p0 ] ] if hasTexture else [ ]
      vexIdxs = [e0.idx1, e1.idx1, e1.idx0]
      if swaped:
        vexIdxs.reverse()
        texIdxs.reverse()
      lstFaces += self.addFace( vexIdxs, texIdxs, [ ] )

      
    if WFBasic.PYPOS3D_TRACE: print('==> createStrip[{0:s}]: InitFace={1:d} NewFaces={2:d}'.format(self.getName(), nbFaceInit, self.getNbFace()))
      
    return lstFaces    
       
       
  def calcCoordSyst(self, faceno=0, orientation='XZY'):
    ''' Create a coordinate system from the first (default) face of a group.
    The face is supposed to be a square (at least) 4 edges

    (Oy)

     3        2
      +-------+
      ^       |
   eu |   X   |
      |       |
      +------>+          (Ox)
     0   ev    1

    Parameters
    ----------
    faceno : int
        Index of the face to use
    orientation : str
      Orientation of coord (NOT USED - RESERVED FOR FUTURE)

    Returns
    -------
    CoordSyst
      A new 3D Coordinate System at the center of the face (X, eu, ev)
      the third vector of the coordinate system: ew = eu x ev
    '''

    vxtab = self.getFaceVertex(faceno)
    eu = Vector3d( vxtab[3].x - vxtab[0].x, vxtab[3].y - vxtab[0].y, vxtab[3].z - vxtab[0].z).normalize()
    ev = Vector3d( vxtab[1].x - vxtab[0].x, vxtab[1].y - vxtab[0].y, vxtab[1].z - vxtab[0].z).normalize()       
    center = Point3d(vxtab[3].x + vxtab[1].x, vxtab[3].y + vxtab[1].y, vxtab[3].z + vxtab[1].z).scale(0.5)
    
    return CoordSyst(center, eu, ev)
  

  # ---------------------------------------------------------------------------
  # TODO: Move it in WFBasic for a more general usage and wall it the vertex
  # list of the GeomGroup
  #
  def RadialScale(self, center, eu, ev, dh, ds, R, nbLoop=0, topPlaneGrp=None):
    ''' Perform a quadratic Radial Scaling of vertexes.

    - Modified Point are below the top Coord. Syst and z>0.0 in the (center, eu, ev) one
      The top Coord system is either given by topPlaneGrp of computed as follow:
      TopCoord = ( center + (0,0,dh), eu, ev )
    - Modify the impunt vertex
    - The scaling curve is defined by the point [-ds, 0] and [+dh, R] 
      where R is a supposed Radius of the vextex at coordinate z = dh

      The Parabol z = a.r² 
      

      O = the center
   
                                ^ Scale Ratio
                                |                           .....  X (usually 1.0 (100%))
                                |                .....   X
                                |        ..... X
                                |    ..X
                                |  .. 
                               .x..
                             .  |
                           .    |
                          .     |
                         .      |
      ------------------x-------O-----------------------------------|--------------> Oz
                       -ds      |                                   dh
                                |        .....
 

 
    Parameters
    ----------
    center : Point3d
      Center of the bottom Plan

    eu : Vector3d
      First Vector of the bottom Plan

    ev : Vector3d
      Second Vector of the bottom Plan (eu and ev are supposed unitary and orthog)

    dh : float
      Height limit of the Parabol
    ds : float
      Down limit of the Parabol
    R : float
      Radius of the parabol in dh

    Returns
    -------
    GeomGroup
      returns self
  
    '''
    if WFBasic.PYPOS3D_TRACE: print('RadialScale({0:s}) ------------------------ '.format(self.getName()))
  
    # Compute the Cutting axis and the transformation matrix of the reference plan
    ew,M,MT = CreateTransform(eu, ev)
  
    # Compute the 'a' coef of the Parabol z = a.r² - ds
    a = (dh+ds) / R / R
  
    rd2 = R*R
  
    if topPlaneGrp:
      centerTop, euTop, evTop = topPlaneGrp.calcCoordSyst()

      ewTop, Mtop, MTtop = CreateTransform(euTop, evTop)

      # For each point in the upper cylinder and below the topPlane : Do a radial quadratic scaling
      for p in self.geom.coordList:
        
        # In top the Coord Syst
        pInTop = Point3d(p).sub(centerTop).inLin33(Mtop)
        
        if pInTop.z<FEPSILON:
          # Change for Cutting Plan Coordinate System
          p.sub(center).inLin33(M)
          
          # if (p.z>=-FEPSILON) and (p.z <= dh+FEPSILON) and (p.x*p.x+p.y*p.y < rd2): FIX Avoid double z condition
          if (p.z>=-FEPSILON) and (p.x*p.x+p.y*p.y < rd2):
            k = math.sqrt( (p.z + ds) / a) / R
            p.scale(k)
      
          # Change (back) to initial Coordinate System
          p.inLin33(MT).add(center) 
      
    else:
      # For each point in the upper cylinder : Do a radial quadratic scaling
      for p in self.geom.coordList:
        
        # Change for Cutting Plan Coordinate System
        p.sub(center).inLin33(M)
        
        if (p.z>=-FEPSILON) and (p.z <= dh+FEPSILON) and (p.x*p.x+p.y*p.y < rd2):
          k = math.sqrt( (p.z + ds) / a) / R
          p.scale(k)
    
        # Change (back) to initial Coordinate System
        p.inLin33(MT).add(center) 
    
    return self


  def FaceRadialScale(self, center, eu, ev, pc=1.0, lstFaceNo=None, materialName=None):
    ''' Perform a radial scaling of the vertex of a list of faces.
    '''
    if WFBasic.PYPOS3D_TRACE: print('FaceRadialScale({0:s}) ------------------------ '.format(self.getName()))
    
    nbface = self.getNbFace()
    if not lstFaceNo:
      matidx = self.lstMat.index(materialName)
      lstFaceNo = [ fi for fi in range(0, nbface) if self.matIdx[fi]==matidx ]
 
    # Compute the Cutting axis and the transformation matrix of the reference plan
    ew,M,MT = CreateTransform(eu, ev)
    
    ptMap = { vi : self.coordList[vi] for fi in lstFaceNo for vi in self.vertIdx[self.stripCount[fi]:self.stripCount[fi+1]] }
        
    # For each point in the upper cylinder : Do a radial quadratic scaling
    for p in ptMap.values():
      # Change for Cutting Plan Coordinate System
      p.sub(center).inLin33(M)
      
      p.scale(pc)
  
      # Change (back) to initial Coordinate System
      p.inLin33(MT).add(center) 
    
    return self
#








