# -*- coding: utf-8 -*-
#
#  
import sys
import logging

from langutil import C_OK, C_FAIL, C_ERROR, C_FILE_NOT_FOUND
from langutil.File import File

from pypos3d.pftk.PoserBasic import PoserToken, PoserConst, index, LowerLangName
from pypos3d.pftk.StructuredAttribut import ValueOpDelta


def parseOrNull(s):
  return float(s) if s else 0.0 


class ChannelColumnDescriptor(object):
  ''' Internal Column descriptor '''
  def __init__(self, nc):
    self.nocol = nc
    self.isSet = False
    self.act = None
    self.gt = None
    self.chanType = None
    self.initValue = 0.0
    self.min = -10000.0
    self.max =  10000.0
    self.trackingScale = 0.1
    self.lstAltFiles = [ ]
    self.lstOps = [ ]



class ChannelImportAnalysis: # implements PoserConst
  ''' Result of a XLS/XLSX/ODS file import for channel creation
   
   When using alternateGeom on Victoria4, Victoria4.2 with Poser7 :
   - The alternateGeom channel starts at 1!!! (even if it should not)
   - It's probably a Poser7 bug
  '''
  # Operation keywords : Op, OpKey.Dep, valueKey.key, valueKey.val
  C_CMD_OP = "Op"
  C_CMD_OPKEY_DEP = "OpKey.Dep"
  C_CMD_OPKEY_KEY = "valueKey.key"
  C_CMD_OPKEY_VAL = "valueKey.val"

  # public ChannelImportAnalysis(Figure f, String baseDir, String tabChannel[][])
  def __init__(self, f, baseDir, tabChannel):
    self.fig = f
    self.tabChan = tabChannel
    self.nblgn = len(self.tabChan)
    self.nbcol = len(self.tabChan[0])
    self.ts = [ [0]*self.nbcol for l in range(0, self.nblgn) ]
    self.lstChan = [ ]
    self.baseDir = baseDir
  

  def checkVocab(self):
    ret = C_OK

    # Check col #0 key words
    self.ts[0][0] = C_OK if self.tabChan[0][0].lower()==LowerLangName[PoserToken.E_actor] else C_FAIL
    self.ts[1][0] = C_OK if self.tabChan[1][0].lower()=="channel" else C_FAIL
    self.ts[2][0] = C_OK if self.tabChan[2][0].lower()=="type" else C_FAIL
    self.ts[3][0] = C_OK if self.tabChan[3][0].lower()==LowerLangName[PoserToken.E_initValue] else C_FAIL
    self.ts[4][0] = C_OK if self.tabChan[4][0].lower()==LowerLangName[PoserToken.E_min] else C_FAIL
    self.ts[5][0] = C_OK if self.tabChan[5][0].lower()==LowerLangName[PoserToken.E_max] else C_FAIL
    self.ts[6][0] = C_OK if self.tabChan[6][0].lower()==LowerLangName[PoserToken.E_trackingScale] else C_FAIL
    self.ts[7][0] = C_OK if self.tabChan[7][0].lower()==LowerLangName[PoserToken.E_alternateGeom] else C_FAIL

    # Operation keywords : Op, OpKey.Dep, valueKey.key, valueKey.val
    for nolgn in range( 8, self.nblgn):
      val = self.tabChan[nolgn][0]

      if val:
        if (val.lower()==self.C_CMD_OP.lower()) and (val.lower()==self.C_CMD_OPKEY_DEP.lower()) \
            and (val.lower()==self.C_CMD_OPKEY_KEY.lower()) and (val.lower()==self.C_CMD_OPKEY_VAL.lower()):
          logging.info("Unknown key word[" + self.tabChan[nolgn][0] + "] at line :" + nolgn)
          self.ts[nolgn][0] = C_FAIL
      else:
        logging.info("Missing Ligne Title[] at line :%d", nolgn)
        self.ts[nolgn][0] = C_FAIL

    return ret

  def checkColumns(self):
    cd = None
    ret = C_OK

    for nocol in range(1, self.nbcol):
      # Check actor presence
      if self.tabChan[0][nocol].endswith(".*"):
        actorBaseName = self.tabChan[0][nocol][0:len(self.tabChan[0][nocol]) - 2]

        # Search for actorBaseName descendant
        lstDescName = self.fig.getDescendant(actorBaseName)

        for i in range(0,  len(lstDescName)): # Avoid first name!!
          cd = self.create(lstDescName[i], nocol)
          cd.isSet = True
          self.lstChan.append(cd)
      else:
        actorName = self.tabChan[0][nocol] + ":" + str(self.fig.getBodyIndex())
        cd = self.create(actorName, nocol)
        self.lstChan.append(cd)

    return ret

  def create(self, actorName, nocol):
    cd = ChannelColumnDescriptor(nocol)

    cd.act = self.fig.findActor(actorName)
    if cd.act==None:
      self.ts[0][nocol] = PoserConst.C_ACTOR_NOTFOUND
      logging.info("Unknown actor[%s] at column %d", actorName, nocol)
    else:
      # Check Channel Name (if the actor exists)
      cd.gt = cd.act.getChannel(self.tabChan[1][nocol])
      if cd.gt:
        # The channel already exists
        self.ts[1][nocol] = PoserConst.C_EXISTS
        logging.info("Channel [%s] exists for actor[%s] at column %d", self.tabChan[1][nocol], actorName, nocol)

      # Check channel type : valueParm, visibility, geomChan
      if self.tabChan[2][nocol].lower()==LowerLangName[PoserToken.E_valueParm]:
        cd.chanType = PoserToken.E_valueParm
      elif self.tabChan[2][nocol].lower()==LowerLangName[PoserToken.E_geomChan]:
        cd.chanType = PoserToken.E_geomChan
      elif self.tabChan[2][nocol].lower()==LowerLangName[PoserToken.E_visibility]:
        cd.chanType = PoserToken.E_visibility
      else:
        # Incorrect channel type  ... But will work for 'upgrade'
        self.ts[2][nocol] = C_FAIL
        # Keep existing channel data
        if cd.gt:
          cd.min = cd.gt.getMin()
          cd.max = cd.gt.getMax()
          cd.trackingScale = cd.gt.getTrackingScale()
        logging.info("Incorrect Channel Type [%s] for actor[%s] at column %d", self.tabChan[2][nocol], actorName, nocol)

      try:
        if cd.chanType==PoserToken.E_valueParm: # // Read min/max values
          cd.initValue = parseOrNull(self.tabChan[3][nocol])
          cd.min = parseOrNull(self.tabChan[4][nocol])
          cd.max = parseOrNull(self.tabChan[5][nocol])
          cd.trackingScale = parseOrNull(self.tabChan[6][nocol])

        elif cd.chanType==PoserToken.E_geomChan:
          cd.initValue = 0
          cd.min = 0
          # cd.max = 1 : To be computed later
          cd.trackingScale = 1

          # Check alternate presence
          strAltNames = self.tabChan[7][nocol]

          tabAltNames = strAltNames.split("\n") if strAltNames else None

          if tabAltNames == None:
            logging.info("No alternate geometries exists for actor[%s] at column %d", actorName, nocol)
            cd.max = 0
          else:
            # Check geometries filenames
            for altgeomName in tabAltNames:
              filename = self.baseDir + altgeomName
              altGeomFile1 = File(filename + "." + PoserConst.PFT_EXT[PoserConst.PFT_OBJ])
              if altGeomFile1.exists() and altGeomFile1.isFile():
                cd.lstAltFiles.append(altGeomFile1)
              else:
                altGeomFile2 = File(filename + "." + PoserConst.PFT_EXT[PoserConst.PFT_OBZ])
                if altGeomFile2.exists() and altGeomFile2.isFile():
                  cd.lstAltFiles.append(altGeomFile1)
                else:
                  logging.info("AlternateGeom File[%s] does not exist at column %d", filename, nocol)
                  self.ts[7][nocol] = C_FILE_NOT_FOUND

            cd.max = len(cd.lstAltFiles)

        elif cd.chanType==PoserToken.E_visibility:
          cd.initValue = float(self.tabChan[3][nocol]) if self.tabChan[3][nocol] else 1.0
          cd.min = 0
          cd.max = 1
          cd.trackingScale = 1

        else: # Nothing to do with other channel types
          pass

        self.analyseOps(cd)

      except ValueError:
        logging.info("Numeric Conversion error at column %d Avoid calculated cells", nocol)
        self.ts[2][nocol] = C_ERROR

    return cd

  def analyseOps(self, cd):
    # Check operations descriptions until the bottom of the column
    nolgn = 8
    while nolgn < self.nblgn:
      if (self.ts[nolgn][0] == C_OK) and self.tabChan[nolgn][0] and self.tabChan[nolgn][cd.nocol]:
        if self.tabChan[nolgn][0].lower()==self.C_CMD_OP.lower():
          # Current tabChan[nolgn][nocol] is a simple expression
          op = ValueOpDelta(pfigure=self.fig, pactor=cd.act, channelExpr=self.tabChan[nolgn][cd.nocol])
        else:
          # Current tabChan identifies the beginning of en OptKey definition
          # We suppose that key / val are well organised
          qualifiedName = self.tabChan[nolgn][cd.nocol]

          figName, actName, gtName = None, None, None

          ptind = qualifiedName.find('.')
          if ptind < 0:
            figName = "Figure " + str(self.fig.getBodyIndex())
            actName = cd.act.getName()
            gtName = qualifiedName
          else:
            actName = qualifiedName[0:ptind]

            ptdp = qualifiedName.find(':')
            if (ptdp < 0):
              actName = actName + ':' + str(self.fig.getBodyIndex())

            figName = "Figure " + str(index(actName))
            gtName = qualifiedName[ptind + 1:]

          op = ValueOpDelta(PoserToken.E_valueOpKey, figName, actName, gtName, 0.0)
          nolgn+=1

          while (nolgn < self.nblgn - 1) and self.tabChan[nolgn][0].lower()==self.C_CMD_OPKEY_KEY.lower():
            if self.tabChan[nolgn][cd.nocol]:
              key = self.tabChan[nolgn][cd.nocol]
              val = self.tabChan[nolgn + 1][cd.nocol]
              op.addValueKey(parseOrNull(key), parseOrNull(val))
            nolgn += 2
            
          nolgn-=1 # Push Back one line

        cd.lstOps.append(op)

      nolgn+=1
      #End While

  def getWorstStatus(self, ligne=None):
    return min(self.ts[ligne]) if ligne else min( v for lgn in self.ts for v in lgn)

