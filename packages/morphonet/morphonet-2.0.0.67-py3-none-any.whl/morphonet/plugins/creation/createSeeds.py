# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

class CreateSeeds(MorphoPlugin):
    """ This plugin create new seeds from a h min (or max) algorithm on the rawdata image

    Parameters
    ----------
    Gaussian_Sigma : int, default :8
        sigma parameters from the gaussian algorithm (from skimage) applied on the rawdata in otder to perform the h minimum or maximum algorithm
    MinOrMax: Dropdown
        To aplly the h minmum or h maximum algorithm (depend on the color of the bacground of the rawdata )
    h_value : int, default :2
        the h value of h_minima or h_maxumum algorithm (see https://scikit-image.org/docs/stable/api/skimage.morphology.html )
        
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("CreateSeeds")
        self.add_inputfield("gaussian_sigma",default=8)
        self.add_dropdown("MinOrMax",["min","max"])
        self.add_inputfield("h_value",default=2)
        self.set_parent("Create new objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
  
        s_sigma=int(self.get_inputfield("gaussian_sigma"))
        MinOrMax=self.get_dropdown("MinOrMax")
        h_value=float(self.get_inputfield("h_value"))
       
        from skimage.morphology import extrema
        from skimage.filters import gaussian 
        from skimage.measure import label
        import numpy as np

        data=dataset.get_seg(t)
        center=dataset.get_center(data)
        rawdata=dataset.get_raw(t)

        #Smoothing
        if s_sigma > 0.0:
            self.print_mn(" --> Perform gaussian with sigma="+str(s_sigma))
            seed_preimage=gaussian(rawdata, sigma=s_sigma,preserve_range=True)
        else:
            seed_preimage = rawdata

        #Fin Extrema
        self.print_mn(" --> Perform  h "+MinOrMax+ " whith h = "+str(h_value))
        if MinOrMax=="min":
            local=extrema.h_minima(seed_preimage,h_value)
        else: 
            local=extrema.h_maxima(seed_preimage,h_value) 

        self.print_mn(" --> Perform  labelisation")
        label_maxima,nbElts = label(local,return_num=True) 
        nbc=0
        for elt in range(1,nbElts+1):
            coord=np.where(label_maxima==elt)
            v=dataset.background
            if data is not None:
                v=data[coord[0][0],coord[1][0],coord[2][0]]
            if v==dataset.background:
                dataset.add_seed(np.int32([coord[0][0]-center[0],coord[1][0]-center[1],coord[2][0]-center[2]]))
                self.print_mn(" ----> Create a seed at "+str(coord[0][0])+","+str(coord[1][0])+","+str(coord[2][0]))
                nbc+=1
        self.print_mn(" --> Found "+str(nbc)+" peaks with "+MinOrMax+" extrema")

        self.restart()

