# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


# Test if a center is inside the image
def _centerInShape(c,s): 
    if c[0]<0 or c[1]<0 or c[2]<0 or c[0]>=s[0] or c[1]>=s[1] or c[2]>=s[2]:
        return False 
    return True


class WatershedithNewSeeds(MorphoPlugin):
    """ This plugin perform a watershed algorithm on the background of the image based on seeds pass in parameters
   
    Parameters
    ----------
    Gaussian_Sigma : int, default :2
        sigma parameters from the gaussian algorithm (from skimage) aplied on the rawdata
    Volume_Minimum: int, default : 1000
        minimum volume under wichi new object are created
    Inverse: Dropdown
        applied the watershed on inverted rawdata (for image on black or white background)
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Watershed")
        self.add_inputfield("Gaussian_Sigma",default=2)
        self.add_inputfield("Volume_Minimum",default=1000)
        self.add_dropdown("Inverse",["no","yes"])
        self.add_coordinates("Add a Seed")
        self.set_parent("Create new objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        seeds=self.get_coordinates("Add a Seed")
        if len(seeds)==0:
            self.restart()
            return None

        s_sigma=int(self.get_inputfield("gaussian_sigma"))
        Inverse=self.get_dropdown("Inverse")
        min_vol=int(self.get_inputfield("Volume_Minimum"))

        from skimage.morphology import label
        from skimage.segmentation import watershed
        from skimage.filters import gaussian 
        import numpy as np
        data=dataset.get_seg(t)
        rawdata=dataset.get_raw(t)

        if data is None:
            data=np.zeros(rawdata.shape).astype(np.uint16)

        center=dataset.get_center(data)
        if center is None:
            center=[np.round(rawdata.shape[0]/2),np.round(rawdata.shape[1]/2),np.round(rawdata.shape[2]/2)]
        #First we remove seeds which are inside other cell 

        #Smoothing
        if s_sigma > 0.0:
            self.print_mn(" --> Perform gaussian with sigma="+str(s_sigma))
            seed_preimage=gaussian(rawdata, sigma=s_sigma,preserve_range=True)
        else:
            seed_preimage = rawdata

        new_seed=[]
        
        for s in seeds:
            seed=np.int32(s+center)
            if _centerInShape(seed,data.shape):
                olid=data[seed[0],seed[1],seed[2]]
                if olid==dataset.background: 
                    new_seed.append(seed)
                    self.print_mn(" ----> add seed "+str(seed))
                else:
                    self.print_mn(" ----> remove this seed "+str(seed)+ " which already correspond to cell "+str(olid))
            else:
                self.print_mn(" ----> this seed "+str(seed)+ " is out of the image")

                if len(new_seed)==0:
                    self.restart()
                    return None


        markers=np.zeros(data.shape,dtype=np.uint16)
        markers[0,:,:]=1
        markers[:,0,:]=1
        markers[:,:,0]=1
        markers[data.shape[0]-1,:,:]=1
        markers[:,data.shape[1]-1,:]=1
        markers[:,:,data.shape[2]-1]=1
        
        newId=2
        for seed in new_seed: #For Each Seeds ...
            markers[seed[0],seed[1],seed[2]]=newId
            newId+=1
                
        #Create The Mask
        mask=np.ones(data.shape,dtype=np.bool)
        mask[data!=dataset.background]=False
            
        #Inverse the image
        if Inverse=="yes":
            seed_preimage=seed_preimage.max()-seed_preimage

        self.print_mn(" --> Process watershed ")
        labelw=watershed(seed_preimage,markers=markers, mask=mask)

        self.print_mn(" --> Combine new objects")
        cMax=data.max()
        new_ids=np.unique(labelw)
        new_ids=new_ids[new_ids>1]
        nbc=1

        for new_id in new_ids:
            newIdCoord=np.where(labelw==new_id)
            if len(newIdCoord[0])>min_vol:
                data[newIdCoord]=cMax+nbc
                self.print_mn(" ----> add object "+str(nbc+cMax)+' with  '+str(len(newIdCoord[0]))+ " voxels")
                dataset.set_seg(t,data,[new_id])
                nbc+=1
            else:
                self.print_mn(" ----> remove object with  "+str(len(newIdCoord[0]))+ " voxels")
        self.print_mn(" --> Found  "+str(nbc)+" new labels")
        self.restart()




