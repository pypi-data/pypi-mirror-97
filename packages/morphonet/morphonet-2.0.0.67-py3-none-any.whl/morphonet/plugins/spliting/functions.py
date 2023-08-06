
def get_borders(data,cellCoords,border=4):
    xmin=max(0,cellCoords[0].min()-border)
    xmax=min(data.shape[0],cellCoords[0].max()+border)
    ymin=max(0,cellCoords[1].min()-border)
    ymax=min(data.shape[1],cellCoords[1].max()+border)
    zmin=max(0,cellCoords[2].min()-border)
    zmax=min(data.shape[2],cellCoords[2].max()+border)
    return xmin,xmax,ymin,ymax,zmin,zmax


def apply_new_label(data,xmin,ymin,zmin,labelw,minVol=0):
    import numpy as np
    labels=np.unique(labelw)
    labels=labels[labels!=0] #Remove Background
    #First We check of all coords have the required minimum of size
    #The biggest cell get the same label
    Labelsize={}
    Bigest=0
    BigestL=-1
    for l in labels:
        Labelsize[l]=len(np.where(labelw==l)[0])
        if Labelsize[l]>Bigest:
            Bigest=Labelsize[l]
            BigestL=l

    labels=labels[labels!=BigestL]
    newIds=[]
    lastID=data.max()+1
    for l in labels:
        new_coords=np.where(labelw==l)
        if len(new_coords[0])>=minVol:
            data[new_coords[0]+xmin,new_coords[1]+ymin,new_coords[2]+zmin]=lastID
            print('     ----->>>>>  Create a new object '+str(lastID)+ " with "+str(len(new_coords[0]))+ " voxels")
            lastID+=1
            newIds.append(lastID)
        else:
            print("     ----->>>>>  Do not create with "+str(len(new_coords[0]))+ " voxels")
    return data,newIds
