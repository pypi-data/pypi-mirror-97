# -*- coding: utf-8 -*-
__version__ = '1.3'
__author__  = 'Olivier DUFAILLY'
__license__ = 'BSD'

import os
import os.path
import gzip

# Usual and common return codes
C_CANCEL  = 0x100
C_WARNING = 0x010
C_OK      = 0
C_FAIL    = -3
C_FILE_NOT_FOUND = -4
C_UNKNOWN        = -5
C_ERROR   = -1000 # Should be a very wrong case

def GetLowExt(fn):
  ''' Return the file extension in lower char '''
  lfn = fn.lower()
  p = lfn.rfind('.')
  return lfn[p+1:] if p>0 else ''

def cmp(a, b):
  return (a > b) - (a < b) 

#-----------------------------------------------------------------------#
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


#
# Binary Search in an ordered table (ascending order)
#
# def Arrays_binarySearch(t, key):
#   ''' Locate the leftmost value exactly equal to x '''
#   i = bisect_left(t, key)
#   if i != len(t) and t[i] == key:
#     return i
#   return -1

# def getDirectory(path): --> use os.path.dirname

def RemoveExt(filename):
  posext = -1 if (filename == None) else filename.rfind('.')
  return filename[0:posext] if posext>0 else filename


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

  
