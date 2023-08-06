# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class DelTemporalLink(MorphoPlugin):
    """This plugin delete any temporal links between objects

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Delete Links")
        self.set_parent("Temporal Relation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        for cid in objects:
             o=dataset.get_object(cid)
             if o is not None:
                dataset.del_link(o)
                self.print_mn(" ----> remove link for object "+str(o.id)+" at "+str(o.t))
        self.restart()
        
