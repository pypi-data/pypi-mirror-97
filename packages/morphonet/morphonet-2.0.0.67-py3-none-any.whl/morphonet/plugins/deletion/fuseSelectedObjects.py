# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class FuseSelectedObjects(MorphoPlugin):
    """ This plugin fuse opbjects in the segmented image
   
    Parameters
    ----------
    Objects: 
        It can be apply either on selected objects or on colored objects where fusion will done by selection id
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Fuse")
        self.set_parent("Remove objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        import numpy as np
        times=[]
        for cid in objects: #List all time points
            o=dataset.get_object(cid)
            if o is not None and o.t not in times:
                times.append(o.t)
        times.sort() #Order Times


        for t in times:
            tofuse={}
            for cid in objects:
                o=dataset.get_object(cid)
                if o is not None and o.t==t: 
                    if o.s not in tofuse:
                        tofuse[o.s]=[]
                    tofuse[o.s].append(o.id)
            for s in tofuse:
                if len(tofuse[s])>1 : #More than one object to fuse..
                    data=dataset.get_seg(t)
                    minFuse=np.array(tofuse[s]).min()
                    cells_updated=[minFuse]
                    self.print_mn(" --> fuse objects "+str(tofuse[s])+" at "+str(t) + " in "+str(minFuse))
                    for tof in tofuse[s]:
                        if tof!=minFuse:
                            cells_updated.append(tof)
                            data[np.where(data==tof)]=minFuse
                            dataset.del_link(dataset.get_object(t,tof)) 
                    dataset.set_seg(t,data,cells_updated)


        self.restart()



