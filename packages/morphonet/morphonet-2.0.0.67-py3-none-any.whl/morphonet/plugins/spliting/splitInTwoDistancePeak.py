# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from .functions import *

class SplitInTwoDistancePeak(MorphoPlugin):
    """ This plugin split opbjects based on distance between two Peaks in the segmented image 

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects

    """
    
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Split In 2")
        self.set_parent("Split objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
            
        from scipy import ndimage as ndi 
        from skimage.segmentation import watershed
        from skimage.feature import peak_local_max
        import numpy as np
        for cid in objects:
            o=dataset.get_object(cid)
            if o is not None:
                data=dataset.get_seg(o.t)
                cellCoords=np.where(data==o.id)
                self.print_mn('     ----->>>  Split object '+str(o.getName()) + " with "+str(len(cellCoords[0]))+ " voxels ")
                xmin,xmax,ymin,ymax,zmin,zmax=get_borders(data,cellCoords)
                cellShape=[1+xmax-xmin,1+ymax-ymin,1+zmax-zmin]
                mask=np.zeros(cellShape,dtype=np.bool)
                mask[cellCoords[0]-xmin,cellCoords[1]-ymin,cellCoords[2]-zmin]=True
                distance = ndi.distance_transform_edt(mask)
                peak_idx = peak_local_max(distance,  footprint=np.ones((3, 3, 3)),num_peaks=2)
                local_maxi = np.zeros_like(mask, dtype=bool)
                local_maxi[tuple(peak_idx.T)] = True
                markers = ndi.label(local_maxi)[0]
                labelw = watershed(-distance, markers, mask=mask)
                data,newIds=apply_new_label(data,xmin,ymin,zmin,labelw)
                if len(newIds)>0:
                    dataset.del_link(o)
                    newIds.append(o.id)
                    dataset.set_seg(t,data,newIds)
                
        self.restart()
