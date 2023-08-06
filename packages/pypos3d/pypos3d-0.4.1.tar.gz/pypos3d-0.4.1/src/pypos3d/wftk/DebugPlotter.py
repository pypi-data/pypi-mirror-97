'''
Created on 2 sept. 2020
Convenience module for debug plotting using 
@author: olivier
'''
# For plotting debug
import matplotlib
matplotlib.use('Agg') # MUST BE CALLED BEFORE IMPORTING plt
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation

from pypos3d.wftk.WFBasic import Edge


class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)


def annotate3D(ax, s, *args, **kwargs):
    '''add anotation text s to to Axes3d ax'''

    tag = Annotation3D(s, *args, **kwargs)
    ax.add_artist(tag)

def Plot(l0,l1=None):
  
  if not l0: return
  
  if isinstance(l0[0], Edge):
    X0 = [ e.p0.x for e in l0 ]
    Y0 = [ e.p0.y for e in l0 ]        
    Z0 = [ e.p0.z for e in l0 ]
  else: # List of (Point 3d, Point3d)
    X0 = [ e[0].x for e in l0 ]
    Y0 = [ e[0].y for e in l0 ]        
    Z0 = [ e[0].z for e in l0 ]
    
  if l1:
    X1 = [ e.p0.x for e in l1 ]
    Y1 = [ e.p0.y for e in l1 ]
    Z1 = [ e.p0.z for e in l1 ]
  
  fig = plt.figure()
  ax = fig.gca(projection='3d')
  
  ax.plot(X0,Y0,Z0,'g',label='l0', linewidth=1, marker='x')
 
  for j, e in enumerate(l0): 
    annotate3D(ax, s=str(j), xyz=(X0[j],Y0[j],Z0[j]), fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')    
  if l1:
    ax.plot(X1,Y1,Z1,'r',label='l1',linewidth=1, marker='o')
  
    for j, e in enumerate(l1): 
      annotate3D(ax, s=str(j), xyz=(X1[j],Y1[j],Z1[j]), fontsize=8, xytext=(-3,3),
                 textcoords='offset points', ha='right',va='bottom')    

  plt.show()
  return plt
  
def PlotTexture(l0):
  
  if not l0: return
  
  # List of (TexCoord, Point3d)
  X0 = [ e.x for e in l0 ]
  Y0 = [ e.y for e in l0 ]        
  
  fig = plt.figure()
  ax = fig.gca()#projection='3d')
  
  ax.plot(X0,Y0,'g',label='l0', linewidth=1, marker='x')
 
#   for j, e in enumerate(l0): 
#     annotate3D(ax, s=str(j), xyz=(X0[j],Y0[j],Z0[j]), fontsize=10, xytext=(-3,3),
#                textcoords='offset points', ha='right',va='bottom')    
#   if l1:
#     ax.plot(X1,Y1,Z1,'r',label='l1',linewidth=1, marker='o')
#   
#     for j, e in enumerate(l1): 
#       annotate3D(ax, s=str(j), xyz=(X1[j],Y1[j],Z1[j]), fontsize=8, xytext=(-3,3),
#                  textcoords='offset points', ha='right',va='bottom')    

  plt.show()


def PlotFaces(lstFaces):
  fig = plt.figure()
  ax = fig.gca(projection='3d')
  
  colors = [ 'r', 'g', 'b']
  markers = [ 'x', 'o', '=']
  for noface, f in enumerate(lstFaces):
    X0 = [ e.p0.x for e in f ] + [ f[-1].p1.x,  ]
    Y0 = [ e.p0.y for e in f ] + [ f[-1].p1.y,  ]
    Z0 = [ e.p0.z for e in f ] + [ f[-1].p1.z,  ]
    ax.plot(X0,Y0,Z0,colors[noface],label='l'+str(noface), linewidth=1, marker=markers[noface])
    
    for j, e in enumerate(f): 
      annotate3D(ax, s=str(j), xyz=(X0[j],Y0[j],Z0[j]), fontsize=10, xytext=(-3,3),
                 textcoords='offset points', ha='right',va='bottom')    
  plt.show()

