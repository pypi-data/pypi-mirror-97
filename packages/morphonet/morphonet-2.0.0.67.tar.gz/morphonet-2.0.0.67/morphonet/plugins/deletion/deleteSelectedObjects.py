# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class DeleteSelectedObjects(MorphoPlugin):
    """ This plugin completly delete the opbjects from the segmented image
   
    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Delete")
        self.set_parent("Remove objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        import numpy as np
        for cid in objects:
            if cid!="":
                o=dataset.get_object(cid)
                data=dataset.get_seg(o.t)
                self.print_mn(" --> delete object "+str(o.id)+" at "+str(o.t))
                dataset.del_link(o)
                data[np.where(data==o.id)]=dataset.background
                dataset.set_seg(o.t,data)
           
        self.restart()





