# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


class ExtremeWater(MorphoPlugin):
    """ This plugin perform a watershed algorithm on the full image based on seeds added by a local maximum algorithm 

    Parameters
    ----------
    Gaussian_Sigma : int, default :8
        sigma parameters from the gaussian algorithm (from skimage) applied on the rawdata in otder to perform the local maximum algorithm
    MinOrMax: Dropdown
        To aplly the local minmum or local maximum algorithm (depend on the color of the bacground of the rawdata )
    Gaussian_Sigma_For Watersheed: int, default :2
        sigma parameters from the gaussian algorithm (from skimage) applied on the rawdata used in the watershed algorithm
    threshold_for_mask: int, default : 100
        a threshold parameters in which voxel will be remove on the gaussian image before performing the watershed algorithm
    RemoveBorder: Dropdown
        remove all elements which touch the border ot the segmented image 
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("ExtremeWater")
        self.add_inputfield("gaussian_sigma",default=8)
        self.add_dropdown("MinOrMax",["min","max"])
        self.add_inputfield("gaussian_sigma_for_watershed",default=2)
        self.add_inputfield("threshold_for_mask",default=100)
       
        self.add_dropdown("RemoveBorder",["yes","no"])
        self.set_parent("Perform Segmentation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        s_sigma=int(self.get_inputfield("gaussian_sigma"))
        w_sigma=int(self.get_inputfield("gaussian_sigma_for_watershed"))
        threshold=float(self.get_inputfield("threshold_for_mask"))
        MinOrMax=self.get_dropdown("MinOrMax")
        RemoveBorder=self.get_dropdown("RemoveBorder")

        from skimage.morphology import watershed,extrema
        from skimage.filters import gaussian 
        from skimage.measure import label
        import numpy as np

        membrane_image=dataset.get_raw(t)

        #Smoothing
        if s_sigma > 0.0:
            self.print_mn(" --> Perform gaussian with sigma="+str(s_sigma))
            seed_preimage=gaussian(membrane_image, sigma=s_sigma,preserve_range=True)
        else:
            seed_preimage = membrane_image
        
        #Fin Extrema
        self.print_mn(" --> Find "+MinOrMax+" extrema ")
        if MinOrMax=="min":
            local=extrema.local_minima(seed_preimage) 
        else: 
            local=extrema.local_maxima(seed_preimage) 

        #Labels Seeds
        self.print_mn(" --> Labels seeds")
        label_maxima = label(local) 

        #Perform Gaussian
        if w_sigma > 0.0:
            self.print_mn(" --> Perform gaussian with sigma="+str(w_sigma))
            seed_w_preimage=gaussian(membrane_image, sigma=w_sigma,preserve_range=True)
        else:
            seed_w_preimage = membrane_image

        #Thresholding
        mask=None
        if threshold>0.0:
            self.print_mn(" --> Perform threshold with value="+str(threshold))
            mask=seed_w_preimage>threshold


        self.print_mn(" --> Perform watershed")
        labels=watershed(seed_w_preimage, label_maxima,mask=mask)  #background ?

        #remove the element at the border
        if RemoveBorder=="yes":
            self.print_mn(" --> Remove Borders")
            borders=np.unique(np.concatenate((np.unique(labels[0,:,:]),np.unique(labels[labels.shape[0]-1,:,:]),np.unique(labels[:,0,:]),np.unique(labels[:,labels.shape[1]-1,:]),np.unique(labels[:,:,0]),np.unique(labels[:,:,labels.shape[2]-1])),axis=0))
            st=""
            for b in borders:
                st+="(labels=="+str(b)+') |'
            st=st[0:-1]
            labels[np.where(eval(st))]=0

        new_ids=np.unique(labels)
        new_ids=new_ids[new_ids!=dataset.background]
        self.print_mn(" --> Found  "+str(len(new_ids))+" labels")
       
        dataset.set_seg(t,labels,new_ids)
        self.restart()
