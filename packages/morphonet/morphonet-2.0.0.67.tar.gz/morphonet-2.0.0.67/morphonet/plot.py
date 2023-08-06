# -*- coding: latin-1 -*-
import os,sys,errno
import numpy as np
from datetime import datetime
from morphonet.tools import _save_seg_thread,imread,imsave,isfile,copy,get_id_t,get_name,_get_param,_add_line_in_file,_read_last_line_in_file
from os.path import isdir,join,dirname,basename
from morphonet.tools import convert_to_OBJ,write_XML_properties,read_XML_properties,get_longid,_check_version
from threading import Thread
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from io import BytesIO
import signal


class MorphoObject():
    """ Object
    """
    def __init__(self,tid):
        tids=tid.split(",")
        if len(tids)<=1:
            self.t=0
            self.id=int(tids[0])
        else:
            self.t =int(tids[0])
            self.id= int(tids[1])
        if len(tids)>2:
            self.s= int(tids[2]) #Selections
    def get_name(self):
        return get_name(self.t,self.id)



class MorphoInfo():
    """ Information that can be added in the Infos menu on the MorphoNet windows

    Parameters
    ----------
    name : string
        the name of the info
    info_type : string
        the type of the info as definied in the MorphoNet format  https://morphonet.org/help_format

    """
    def __init__(self,name,info_type):
        self.name=name
        self.info_type=info_type
        self.data={}
        self.updated=True
       
    def clear(self):
        self.data.clear()

    def _get_object(self,o):
        for oo in self.data:
            if oo.id==o.id and oo.t==o.t:
                return oo
        return o

    def set(self,mo,value):
        '''
        Associated a value to the info
        with the currente date and time

        Parameters
        ----------
        mo : MorphoObject
            the cell object
        value : string
            the value
        Examples
        --------
        >>> info.set(mo,"a7.8")
        '''
        self.set_curation(mo,value,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def get_last(self,mo):
        '''
        Return the last value to the object

        Parameters
        ----------
        mo : MorphoObject
            the cell object

        Examples
        --------
        >>> value=info.get_last(mo)
        '''

        if mo not in self.data:
            return None
        ks=sorted(self.data[mo],reverse=True)
        return self.data[mo][ks[0]]

    def get_curation(self,mo):
        '''
        Return all the curation corresponding to the object

        Parameters
        ----------
        mo : MorphoObject
            the cell object

        Examples
        --------
        >>> currations=info.get_curation(mo)
        '''

        if mo not in self.data:
            return []
        if len(self.data)==1:
            return []
        ks=sorted(self.data[mo])
        curated=[]
        for k in ks[:len(ks)-1]:
            curated.append( (self.data[mo][k],k) )
        return curated

    def set_curation(self,mo,value,d):
        '''
        Add a new curration value to the info

        Parameters
        ----------
        mo : MorphoObject
            the cell object
        value : string
            the value
        d: string
            the date of the curration
        Examples
        --------
        >>> info.set_curation(mo,"a7.8","2020-02-02 12:23:34")
        '''

        if mo not in self.data:
            self.data[mo]={}
        if self.info_type == "time" and type(value) == str:
            self.data[mo][d]=[MorphoObject(value)]
        else:
            self.data[mo][d]=value
        self.updated=True

    def del_curation(self,mo,value,d):
        if mo not in self.data:
            return False

        if d not in self.data[mo]:
            return False

        if self.data[mo][d]==value:
            del self.data[mo][d]
            self.updated=True
            return True
            

        return False

    def del_curation_using_value(self,mo,value):
        if mo not in self.data:
            return False

        for d in self.data[mo]:
            if self.data[mo][d][0].get_name() == value:
                del self.data[mo][d]
                self.updated=True
                return True

        return False

    def del_selection(self,select):
        if not self.info_type == "selection":
            print("You can't delete a selection from a non selection type info")
            return False
        if select is None:
            print("No selection to remove")
            return False

        for cell_id in self.data:
            if self.data[cell_id] is not None and self.data[cell_id] == select:
                print(self.data[cell_id])
        return True

    def get_txt(self,time_begin=-1,time_end=-1):
        Text="#MorphoPlot"+'\n'
        Text+='#'+self.name+'\n'
        Text+="type:"+self.info_type+"\n"
        for o in self.data:
            if ( time_begin==-1 or (time_begin>=0 and o.t>=time_begin) ) and (time_end==-1 or (time_end>=time_begin and o.t<=time_end) ):
                if self.info_type=="time" :
                    daughters=self.get_last(o)
                    for d in daughters:
                        Text+=o.get_name()+':'+d.get_name()+'\n'
                else:
                    Text+=o.get_name()+':'+str(self.get_last(o))+'\n' #TODO GROUP ETC...
        return Text

    def is_curated(self,time_begin=-1,time_end=-1):
        for o in self.data:
            if ( time_begin==-1 or (time_begin>=0 and o.t>=time_begin) ) and (time_end==-1 or (time_end>=time_begin and o.t<=time_end) ):
                if len(self.get_curation(o))>=1:
                    return True
        return False

    def get_curation_txt(self,time_begin=-1,time_end=-1):
        Text="#MorphoPlot"+'\n'
        Text+='#Curation for '+self.name+'\n'
        Text+="type:"+self.info_type+"\n"
        for o in self.data:
            if ( time_begin==-1 or (time_begin>=0 and o.t>=time_begin) ) and (time_end==-1 or (time_end>=time_begin and o.t<=time_end) ):
                listCurated=self.get_curation(o)
                for vd in listCurated:
                    (v,da)=vd
                    if self.info_type=="time":
                        for d in v:
                            Text+=o.get_name()+':'+d.get_name()+'#'+str(da)+'\n'
                    else:
                        Text+=o.get_name()+':'+str(v)+'#'+str(da)+'\n'
        return Text

    def get_dict(self):
        prop={}
        for o in self.data:
            cv=o.t*10**4+o.id
            val=self.get_last(o)
            if self.info_type=='time': #Cell Lineage
                for m in val:
                    mother=m.t*10**4+m.id
                    if m.t<o.t:
                        if mother not in prop:
                            prop[mother]=[]
                        prop[mother].append(cv)
                    else: #Inverse
                        if cv not in prop:
                            prop[cv]=[]
                        prop[cv].append(mother)
            else:
                prop[cv]=val
        return prop

    def write_curation(self,txt_filename):
        print(" --> save "+txt_filename)
        f=open(txt_filename,'w')
        f.write("#Curation for "+self.name+'\n')
        f.write("type:"+self.info_type+"\n")
        for o in self.data:
            listCurated=self.get_curation(o)
            for vd in listCurated:
                (v,d)=vd
                if self.info_type=="time":
                    for ds in v:
                        f.write(o.get_name()+':'+ds.get_name()+"#"+str(d)+'\n')
                else:
                    f.write(o.get_name()+':'+str(v)+"#"+str(d)+'\n')
        f.close()

    def read_curation(self,txt_filename):
        if os.path.isfile(txt_filename):
            f=open(txt_filename,'r')
            for line in f:
                if line.find("#")!=0 and line.find("type")==-1: 
                    p=line.find(":")
                    d=line.find("#")
                    o=self._get_object(MorphoObject(line[:p]))
                    if self.info_type=="time":
                        od=self._get_object(MorphoObject(line[p+1:d]))
                        self.set_curation(o,[od],line[d+1:].strip()) #TODO GROUP ETC...
                    else:
                        self.set_curation(o,line[p+1:d],line[d+1:].strip()) #TODO GROUP ETC...
            f.close()



class Dataset():
    """Dataset class automatically created when you specify your dataset path in the seDataset function from Plot()

    Parameters
    ----------
    begin : int
        minimal time point
    end : int 
        maximal time point
    raw : string
        path to raw data file where time digits are in standard format (ex: (:03d) for 3 digits  )(accept .gz)
    segment : string
        path to segmented data file  where time digits are in standard format  (accept .gz)
    log : bool
        keep the log
    background : int
        the pixel value of the background inside the segmented image 
    xml_file : string
        path to the xml propertie files (.xml)
    memory : int
        number of time step keep in memory durig curation (if you have memeory issue, decrease this number)
    """

    def __init__(self,parent,begin=0,end=0,raw=None,segment=None,log=True,background=0,xml_file=None,memory=20):
        self.parent=parent
        self.begin=begin
        self.end=end
        self.log=log

        
    
        #raw data
        self.raw=False
        self.show_raw=None
        self.raw_datas={}  #list of each rawdata time point  
        if raw is not None:
            self.raw=True
            self.raw_path=dirname(raw)+"/"
            if dirname(raw)=="":
                self.raw_path=""
            self.raw_files=basename(raw)

        #Segmentation
        self.seg_datas={}  #list of each segmented time point 
        self.segment_path=""
        self.segment_files="curated_t{:03d}.inr.gz"
        if segment is not None:
            self.segment_path=dirname(segment)+"/"
            if dirname(segment)=="":
                self.segment_path=""
            self.segment_files=basename(segment)
            if self.segment_path!="" and not isdir(self.segment_path):
                os.mkdir(self.segment_path)

        #LOG
        self.log_file = "morpho_log.txt"

        self.background=background #Background Color
            
        #DATA Management
        self.memory=memory #Memory to store dataset in Gibabytes
        self.lasT=[] #List of last time step
        self.times=[] #List of modified time point 
        
        #INFOS
        self.infos={} #For all infos Infos
        self.xml_file = xml_file #Xml Properties
        self._read_properties(self.xml_file)  #Lineage Initialisation

        self.seeds=None #To Send Centers to Unity

        #Cell to update
        self.cells_updated={}

    def print_mn(self,msg):
        """Print a string on the 3D viewer

        Parameters
        ----------
        msg : string
            your message to print 
       
        """
        self.parent.print_mn(msg)

    def save_log(self,command,exec_time):
        """Save the specitic command in the log file 

        Parameters
        ----------
        command : string
            Executed Command
        exec_time : float
            time of execution 

        Examples
        --------
        >>> dataset.save_log("fuse",date)
        """

        if self.log :
            _add_line_in_file(self.log_file,str(command)+str(exec_time.strftime("%Y-%m-%d-%H-%M-%S"))+"\n")


    def restart(self,plug):  #Apply and Restart a Curation 
        """Restart the curation mode after execution of a specific plugin

        Parameters
        ----------
        plug : MorphoPlug
            the plugin just executed

        Examples
        --------
        >>> dataset.restart(fuse)
        """

        if plug is not None:
            print(" --> Done " +str(plug.name))
            for t in self.times:
                self._save_seg(t,plug.exec_time)
        
        self.parent.restart(self.times)

    def backup(self,command,t,objects):
        '''
        Backup XML files and Image before performing an action
        '''
        if not isdir(".backup_morphonet"):
            os.mkdir(".backup_morphonet")
        backup_folder=join(".backup_morphonet",str(datetime.timestamp(datetime.now())))
        os.mkdir(backup_folder)

        #SAVE ACTION
        _add_line_in_file(join(backup_folder,"action.txt"), command)

        # BACKUP XML
        os.system('cp '+self.xml_file+" "+backup_folder+" &")

        #BACKUP IMAGE
        times = []
        for cid in objects:  # List all time points
            o = self.get_object(cid)
            if o is not None and o.t not in times:
                times.append(o.t)
        times.sort()  # Order Times
        for t in times:
            filename = join(self.segment_path, self.segment_files.format(t))
            os.system('cp '+filename+" "+backup_folder+" &")


    def cancel(self):
        '''
        Cancel the last action (by put the backup back)
        '''
        #Look for the last backup
        backups=[]
        for back in os.listdir(".backup_morphonet"):
            if isdir(join(".backup_morphonet",back)):
                backups.append(back)
        backups.sort()  # Order Times
        if len(backups)==0:
            print(" --> no backup found")
            return False

        last_backup=backups[len(backups)-1]
        backup_folder=join(".backup_morphonet",last_backup)

        #READ COMMAND
        selection = ""
        if isfile(join(backup_folder,"action.txt")):
            action=_read_last_line_in_file(join(backup_folder,"action.txt"))
            print(">> Cancel " + action)
            self.print_mn("Cancel "+action)
            self.save_log("CANCEL "+action,datetime.now())

            #Retrieve the list of cells
            for a in action.split(";"):
                if a.strip().startswith("ID:"):
                    objts=a[a.find('[')+1:a.find(']')].split("',")
                    for o in a[a.find('[')+1:a.find(']')].split("',"):
                        selection+=o.replace("'","")+";"



        #RESTORE XML
        if isfile(join(backup_folder,os.path.basename(self.xml_file))):
            self._read_properties(join(backup_folder,os.path.basename(self.xml_file)),reload=True)

        #RESTORE Images
        times=[]
        for t in range(self.begin,self.end+1):
            filename = join(backup_folder, self.segment_files.format(t))
            if isfile(filename):
                times.append(t)
                os.system('cp -f ' + filename + " " + self.segment_path)
                self.cells_updated[t]=None #Recompute all cells
                data=self.get_seg(t,reload=True)
                self._set_volume(data, t)

        #REMOVE BACKUP
        os.system('rm -rf '+backup_folder)

        self.parent.restart(self.times,selection=selection)


    #OBJECT ACCESS
    def get_object(*args):
        """Get an MorphoObject from a list of arguments (times, id, ... )

        Parameters
        ----------
        *args : list of arugemnts 
            the arguments which define the object, with at least 1 argument (object id with time =0 )

        Return 
        ----------
        MorphoObject class 

        Examples
        --------
        >>> dataset.get_object(1,2)
        """
        if len(args) == 2:
            if args[1]=="":
                return None
            return MorphoObject(args[1])
        elif len(args) == 3:
            return MorphoObject(get_name(args[1],args[2]))
        return None
        

    ##### DATA ACCESS 
    def _set_last(self,t):
        if t in self.lasT:
            self.lasT.remove(t)
        self.lasT.append(t)
        if t not in self.seg_datas:
            if self._get_data_size()>self.memory*10**9:
                remove_t=self.lasT.pop(0)
                if remove_t in self.seg_datas:
                    del self.seg_datas[remove_t]
                if remove_t in self.raw_datas:
                    del self.raw_datas[remove_t] 

    def _get_data_size(self):
        sif=0
        for t in self.seg_datas:
            if self.seg_datas[t] is not None:
                sif+=self.seg_datas[t].nbytes
        return sif

    def _set_volume(self,data,t):
        #Compute new Volumes
        inf=self._get_info('cell_volume',info_type="float")
        factor=4 #Computational Factor to reduce time computation
        dataResize=data[::factor,::factor,::factor]
        cells=np.unique(dataResize)
        cells=cells[cells!=self.background]
        for c in cells:
            prevV=inf.get_last(c)
            newV=len(np.where(dataResize==c)[0])*(factor*factor*factor) 
            if prevV!=newV:
                inf.set(MorphoObject(get_name(t,c)),newV)
        del dataResize

    def set_seg(self,t,data,cells_updated=None):
        """Define the segmented data at a specitic time point

        Parameters
        ----------
        t : int
            the time point 
        data : numpy matrix
            the segmented image
        cells_updated (optional): list
            list of cell just udpated by the plugin (in order to compute faster)

        Examples
        --------
        >>> dataset.set_seg(1,data)
        """

        self.seg_datas[t]=data
        if t not in self.times:
            self.times.append(t)

        self.update_cells(t,cells_updated)

    def update_cells(self,t,cells_updated):
        """Updated list of modified cells given a specific time step

        Parameters
        ----------
        t : int
            the time point 
        cells_updated : list or MorphoObject
            list of cell just udpated by the plugin (in order to compute faster)

        Examples
        --------
        >>> dataset.update_cells(1,[o,d])
        """

        if t not in self.cells_updated:
            self.cells_updated[t]=[]

        if cells_updated is not None:
            for c in cells_updated:
                if c not in self.cells_updated[t]:
                    self.cells_updated[t].append(c)

    def _save_seg(self,t,exec_time,data=None):
        if data is None:
            data=self.seg_datas[t]
        else:
            self.seg_datas[t]=data
        self._set_volume(data,t)

        sst=_save_seg_thread(self.segment_path,self.segment_files,data,t,exec_time)
        sst.start()

    def get_raw(self,t):
        """Get the rawdata data at a specitic time point

        Parameters
        ----------
        t : int
            the time point 
        Return
        ----------
        numpy matrix
            the raw data

        Examples
        --------
        >>> dataset.get_raw(1)
        """
        filename=join(self.raw_path,self.raw_files.format(t))
        if not os.path.isfile(filename):
            print(" Miss raw file "+filename)
            return None
        if t not in self.raw_datas:
            self.raw_datas[t]=imread(join(self.raw_path,self.raw_files.format(t)))
        self._set_last(t)  # Define the time step as used
        return self.raw_datas[t]

    def get_seg(self,t,reload=False):
        """Get the segmented data at a specitic time point

        Parameters
        ----------
        t : int
            the time point 

        Return
        ----------
        numpy matrix
            the segmented image

        Examples
        --------
        >>> dataset.get_seg(1)
        """
        self._set_last(t) #Define the time step as used
        if t not in self.seg_datas or reload:
            self.seg_datas[t]=None
            if isfile(join(self.segment_path,self.segment_files.format(t))):
                self.seg_datas[t]=imread(join(self.segment_path,self.segment_files.format(t)))
        return self.seg_datas[t]

    def get_center(self,data): #Calculate the center of a dataset
        """Get the barycnetr of an matrix passed in argument 

        Parameters
        ----------
        data : numpy matrix
            the 3D image (could be segmented or rawdata) 

        Return
        ----------
        list of coordinates 
            the barycenter of the image 

        Examples
        --------
        >>> center=dataset.get_center(seg)
        """

        return [np.round(data.shape[0]/2),np.round(data.shape[1]/2),np.round(data.shape[2]/2)]

    def add_seed(self,seed):
        """Add a seed in the seed list

        Parameters
        ----------
        seed : numpy array
            the coordinate of a seed 


        Examples
        --------
        >>> dataset.add_seed(np.int32([23,34,45]))
        """

        if self.seeds is None:
            self.seeds=[]
        self.seeds.append(seed)

    def get_seeds(self):
        """Return the list of seeds as string

        Examples
        --------
        >>> seeds=mc.get_seeds()
        """

        if self.seeds is None or len(self.seeds)==0:
            return None
        strseed=""
        for s in self.seeds:
            strseed+=str(s[0])+","+str(s[1])+","+str(s[2])+";"
        self.seeds=None #Reinitializeation
        return strseed[0:-1]

    ##### LINEAGE FUNCTIONS
    def _read_properties(self,filename,reload=False):
        if filename is not None :
            prop_path=os.path.dirname(filename)
            properties=read_XML_properties(filename)
            if properties is not None:
                for info_name in properties:
                    prop=properties[info_name]
                    if prop is not None:
                        if info_name!="all_cells":
                            info_type=None
                            if info_name.startswith("selection_"):
                                info_type = "selection"
                                info_name=info_name.replace("selection_","")

                            inf=self._get_info(info_name,info_type=info_type,reload=reload)
                            for idl in prop:
                                t,c=get_id_t(idl) 
                                mo=MorphoObject(get_name(t,c))
                                if info_name=='cell_lineage':
                                    daughters=[]
                                    for daughter in prop[idl]:
                                        td,d=get_id_t(daughter)
                                        daughters.append(MorphoObject(get_name(td,d)))
                                    inf.set(mo,daughters)
                                else:
                                    inf.set(mo , prop[idl] )

                            inf.read_curation(join(prop_path,info_name+".log")) #READ CURATION FILE

    def _write_properties(self,filename):
        if filename is not None:
            properties={}
            for info_name in self.infos:
                inf=self.infos[info_name]
                if inf.info_type=="selection":
                    properties["selection_"+info_name] = inf.get_dict()
                else:
                    properties[info_name]=inf.get_dict()
            properties["all_cells"]=[] #Add ALL CELLS
            inf=self._get_info("cell_volume")
            for o in inf.data:
                properties["all_cells"].append(get_longid(o.t,o.id))
            write_XML_properties(properties,filename)

    def _get_info(self,info_name,info_type=None,reload=False):
        if info_type is None:
            if info_name in self.infos:
                info_type = self.infos[info_name].info_type
            elif info_name=="cell_lineage":
                info_type = "time"
            elif info_name=="cell_volume":
                info_type = "float"
            else:
                info_type="string"

        if reload and info_name in self.infos: #Clear Info
            self.infos[info_name].clear()

        if info_name not in self.infos:  #Create a new one
            self.infos[info_name]=MorphoInfo(info_name,info_type)
        return self.infos[info_name]

    ################## TEMPORAL FUNCTIONS 
    def _get_at(self,objects,t):
        cells=[]
        for cid in objects:
            o=self.get_object(cid)
            if o is not None and o.t==t:
                    cells.append(o)
        return cells
    
    def add_link(self,da,mo):
        """Create a temporal link in the lineage

        Parameters
        ----------
        da : MorphoObject
            the daughter cell 
        mo : MorphoObject
            the mother cell 


        Examples
        --------
        >>> mc.add_link(da,mo)
        """
        inf=self._get_info("cell_lineage",info_type="time")
        listCells=inf.get_last(da)
        if listCells is None:
            listCells=[]
        listCells.append(mo)
        inf.set(da,listCells)

    def del_link(self,o): #We remove all links correspond to a cells
        """Remove all temporal relations for a sepcific in the lineage

        Parameters
        ----------
        o : MorphoObject
            the cell 

        Examples
        --------
        >>> mc.del_link(o)
        """
        inf=self._get_info("cell_lineage",info_type="time")
        for a in inf.data:
            if a.t==o.t and a.id==o.id:
                inf.set(a,[])
                #print("Set null to "+str(o.id))
            else:
                listCells=inf.get_last(a)
                if listCells is not None:
                    listCellsB=[]
                    remove=False
                    for c in listCells:
                        if c.t==o.t and c.id==o.id:
                            remove=True
                        else:
                            listCellsB.append(c)                    
                    if remove:
                        #print("Remove links for "+str(a.id))
                        inf.set(a,listCellsB)


#****************************************************************** MORPHONET SERVER


class _MorphoServer(Thread):
    def __init__(self,ploti,todo,host="",port=9875):
        Thread.__init__(self) 
        self.ploti=ploti
        self.todo=todo
        self.host=host
        self.port=port
        self.server_address = (self.host, self.port)
        self.available = threading.Event() #For Post Waiting function
        self.lock = threading.Event()
        self.lock.set()
        

    def run(self): #START FUNCTION
        #print("Run server Localhost on the port ", self.port)
        if self.todo=="send":
            handler = _MorphoSendHandler(self.ploti,self)
        else: #recieve
            handler = _MorphoRecieveHandler(self.ploti,self)

        self.httpd = HTTPServer(self.server_address, handler)
        self.httpd.serve_forever()

    def reset(self):
        self.obj = None  
        self.cmd=None  
        self.available = threading.Event() #Create a new watiing process for the next post request
        self.lock.set() #Free the possibility to have a new command

    def wait(self):  #Wait free request to plot (endd of others requests)
        self.lock.wait()

    def post(self,cmd,obj): #Prepare a command to post
        self.lock = threading.Event() #LOCK THE OTHER COMMAND
        self.available.set() 
        self.cmd=cmd
        self.obj=obj
        
    def stop(self):
        self.lock.set()
        self.available.set()
        self.httpd.shutdown()

class _MorphoSendHandler(BaseHTTPRequestHandler):
 
    def __init__(self, ploti,ms):
        self.ploti = ploti
        self.ms=ms
     
    def __call__(self, *args, **kwargs): #Handle a request 
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") #To accept request from morphonet
        self.end_headers()


    def do_GET(self): #NOT USED
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self.ms.available.wait() #Wait the commnand available
        self._set_headers()
        #print("-> SEND for "+self.ms.cmd)#+"->"+str(self.ms.obj))
        content_length = int(self.headers['Content-Length']) 
        command =self.rfile.read(content_length)
        response = BytesIO()
        #print(command)
        response.write(bytes(self.ms.cmd, 'utf-8'))
        response.write(b';') #ALWAYS ADD A SEPARATOR
        if self.ms.obj is not None:
            if  self.ms.cmd.find("RAW")==0:
                response.write(self.ms.obj)
            else :
                response.write(bytes(self.ms.obj, 'utf-8'))
        self.wfile.write(response.getvalue())
        self.ms.cmd=""
        self.ms.obj=None
        self.ms.reset() #FREE FOR OTHERS COMMAND
        

    def log_message(self, format, *args):
        return

class _MorphoRecieveHandler(BaseHTTPRequestHandler):
 
    def __init__(self, ploti,ms):
        self.ploti = ploti
        self.ms=ms
     
    def __call__(self, *args, **kwargs): #Handle a request 
        super().__init__(*args, **kwargs)


    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") #To accept request from morphonet
        self.end_headers()


    def do_GET(self): #NOT USED
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self._set_headers()
        response = BytesIO() #Read 
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        command =self.rfile.read(content_length)
        action=_get_param(command,"action")
        current_time=int(_get_param(command,"time"))
        objects=_get_param(command,"objects").split(";")
        #print("action="+action)
        if action=="showraw":
            self.ploti.plot_raws(current_time)
        elif action=="upload":
            self.ploti.upload(objects[0],2)
        elif action == "cancel":
            self.ploti.cancel()
        elif action=="reload_infos":
            self.ploti.reload_infos()
        elif action=="create_curation":
            self.ploti.curate_info(_get_param(command,"info"),_get_param(command,"objects"),_get_param(command,"value"),_get_param(command,"date"))
        elif action=="delete_curation":
            self.ploti.delete_curate_info(_get_param(command,"info"),_get_param(command,"objects"),_get_param(command,"value"),_get_param(command,"date"))
        elif action=="delete_curation_value":
            self.ploti.delete_curate_info_using_value(_get_param(command,"info"),_get_param(command,"objects"),_get_param(command,"value")) 
        elif action=="create_info_unity":
            self.ploti.create_info_from_unity(_get_param(command,"name"),_get_param(command,"datatype"),_get_param(command,"infos"))
        elif action=="delete_info_unity":
            self.ploti.delete_info_from_unity(_get_param(command,"info"))
        elif action=="delete_selection":
            self.ploti.delete_selection_from_unity(_get_param(command,"info"),_get_param(command,"selection"))
        else:
            actions=unquote(str(command.decode('utf-8'))).split("&")
            for plug in self.ploti.plugins:
                if plug._cmd()==action: #print(" Found Plugin "+plug().cmd())
                    ifo=0 
                    for tf in plug.inputfields:
                        plug._set_inputfield(tf,actions[3+ifo][actions[3+ifo].index("=")+1:])
                        ifo+=1
 
                    for dd in plug.dropdowns:
                        plug._set_dropdown(dd,actions[3+ifo][actions[3+ifo].index("=")+1:])
                        ifo+=1
                    for cd in plug.coordinates:
                        plug._set_coordinates(cd,actions[3+ifo][actions[3+ifo].index("=")+1:])
                        ifo+=1

                    plug.process(current_time,self.ploti.dataset,objects)

        response.write(bytes("DONE", 'utf-8'))
        self.wfile.write(response.getvalue())
        

    def log_message(self, format, *args):
        return
    
class Plot:#Main function to initalize the plot mode
    """Plot data onto the 3D viewer of the MorphoNet Window.

    Parameters (mostly for debuging )
    ----------
    log : bool
        keep the log
    start_browser : bool
        automatically start the browser when plot initliaze
    port : int
        port number to communicate with the MorphoNet Window. 
    
    Returns
    -------
    MorphoPlot
        return an object of morphonet which will allow you to send data to the MorphoNet Window.


    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.Plot()

    """

    def __init__(self,log=True,clear_backup=True,start_browser=True,port_send=9875,port_recieve=9876):
        
        _check_version()

        self.server_send=_MorphoServer(self,"send",port=port_send) #Instantiate the local MorphoNet server
        self.server_send.start() #

        self.server_recieve=_MorphoServer(self,"recieve",port=port_recieve) #Instantiate the local MorphoNet server 
        self.server_recieve.start() 
    

        if start_browser :
            self.show_browser()
        self.plugins=[]
        self.log=log        

        signal.signal(signal.SIGINT, self._receive_signal)

        self._clear_temp()

        if clear_backup:
            self._clear_backup()

    #########################################  SERVER COMMUNICATION

    def write_info(self,txt_filename,data):
        print(" --> save "+txt_filename)
        f=open(txt_filename,'w')
        f.write(data)
        f.close()

    def connect(self, login,passwd): #Need to be connected to be upload on MorphoNet 
        """Connect to the MorphoNet server

        In order to directly upload data to the MorphoNet server, you have to enter your MorphoNet credentials

        Parameters
        ----------
        login : string
            your login in MorphoNet
        passwd : string
            your password in MorphoNet

        Examples
        --------
        >>> import morphonet
        >>> mc=morphonet.Plot()
        >>> mc.connect("mylogin","mypassword")
        """
        import morphonet 
        self.mn=morphonet.Net(login,passwd)
     
    def print_mn(self,msg):
        """Print a string on the 3D viewer

        Parameters
        ----------
        msg : string
            your message to print 
       
        Examples
        --------
        >>> mc=print_mn("Hello")
        """
        if msg!="DONE":
            print(msg)
        self.send("MSG",msg)

    def send(self,cmd,obj=None):
        """ Send a command to the 3D viewer

        Examples
        --------
        >>> mc.send("hello")
        """
        self.server_send.wait() #Wait the commnand available
        if cmd is not None:
            cmd=cmd.replace(" ","%20")
        if obj is not None:
            if type(obj)==str:
                obj=obj.replace(" ","%20")
        self.server_send.post(cmd,obj)

    def quit(self):
        """ Stop communication between the browser 3D viewer and python

        Examples
        --------
        >>> mc.quit()
        """
        self.server_send.stop() #Shut down the server
        self.server_recieve.stop() #Shut down the server

    def upload(self,dataname,upload_factor=2):
        """Create the dataset on MorphoNet server and upload data

        Parameters
        ----------
        dataname : string
            Name of the new dataset on the server
        upload_factor : float
            the scaling attached to the dataset to match the raw data

        Examples
        --------
        >>> ...after starting MorphoPlot and curating the data
        >>> mc.upload("new dataset name",1)
        """
        print("---->>> Upload dataset "+dataname)
        self.mn.create_dataset(dataname,minTime=self.dataset.begin,maxTime=self.dataset.end)
        for t in range(self.dataset.begin,self.dataset.end+1):
            data=self.dataset.get_seg(t)
            if data is not None:
                obj=convert_to_OBJ(data,t,background=self.dataset.background,factor=upload_factor,cells_updated=None,path_write=self.temp_path)
                self.mn.upload_mesh(t,obj)
        #TODO add Infos
        print("---->>>  Uploading done")

   
    def show_browser(self): 
        """ Start Mozilla Firefox browser and open morphoplot page
        
        Examples
        --------
        >>> mc.show_browser()
        """
        import webbrowser
        from morphonet import url
        print("open "+url)
        try:
            webbrowser.get('firefox').open_new_tab("http://"+url+'/morphoplot')
        except Exception as e:
            print("Firefox error: " % e)
            quit()

    def curate(self): #START UPLOAD AND WAIT FOR ANNOTATION
        """ Start sending data to the browser 3D viewer, then wait for annotation from the browser

        Examples
        --------
        >>> mc=morphonet.Plot(start_browser=False)
        >>> mc.set_dataset(...)
        >>> mc.curate()
        """
        self.print_mn("Wait for the MorphoNet Windows")
        self.send("START_"+str(self.dataset.begin)+"_"+str(self.dataset.end))
        self.set_default_plugins()  #Initialise Default set of plugins
        self.plot_meshes()
        self.plot_infos()
        self.plot_infos_currated()
        self._reset_infos()
        self.print_mn("DONE")

    def restart(self,times,selection=None):

        self.dataset._write_properties(self.dataset.xml_file)

        if times is not None: #PLOT MESHES
            self.plot_meshes(times)

        if self.dataset.show_raw is not None: #PLOT RAWDATAS
            self.plot_raw(self.dataset.show_raw)

        self.plot_seeds(self.dataset.get_seeds()) #PLOT SEEDS
 
        self.plot_infos() #PLOT ALL INFOS

        self.plot_selection(selection) #PLOT SELECTION

        self._reset_infos()
        self.print_mn("DONE")

    def cancel(self):
        '''
        Cancel last action -> retrieve last backup
        '''
        self.dataset.cancel()
    #########################################  DATASET 

    def set_dataset(self,begin=0,end=0,raw=None,segment=None,background=0,xml_file=None,factor=4,raw_factor=4,memory=20):
        """ Define a dataset to curate
        
        Parameters
        ----------
        begin : int
            minimal time point
        end : int 
            maximal time point
        raw : string
            path to raw data file where time digits are in standard format (ex: (:03d) for 3 digits  )(accept .gz)
        segment : string
            path to segmented data file  where time digits are in standard format  (accept .gz)
        background : int
            the pixel value of the background inside the segmented image 
        xml_file : string
            path to the xml propertie files (.xml)
        factor : int
            reduction factor when meshes are calculated and send to the MorphoNet window
        raw_factor : int
            raw data reduction factor
        memory : int
            number of time step keep in memory durig curation (if you have memeory issue, decrease this number)

        Examples
        --------
        >>> ...after connection
        >>> mc.set_dataset(self,begin=0,end=10,raw=path/to/name_t(:03d).inr.gz,segment=path/to/segmenteddata_t(:03d).inr.gz,xml_file=path/to/properties_file.xml)
        """
        self.dataset=Dataset(self,begin,end,raw=raw,segment=segment,log=self.log,background=background,xml_file=xml_file,memory=memory)
        self.center=None
        self.factor=factor #Reduce factor to compute the obj
        self.raw_factor=raw_factor #Reduction factor

        #Temporary folder
        self.temp_path=".temp_morphonet_"+str(os.path.basename(segment))
        if self.temp_path!="" and not isdir(self.temp_path):
            os.mkdir(self.temp_path)

    ######################################### PLUGINS

    def add_plugin(self,plug):
        """ Add a python plugin to be import in the MorphoNet Window
        
        Parameters
        ----------
        plugin : MorphoPlugin
            A plugin instance

        Examples
        --------
        >>> from plugins.MARS import MARS
        >>> mc.add_plugin(MARS())
        """
        if plug not in self.plugins:
            self.plugins.append(plug)
            self._create_plugin(plug)

    def _create_plugin(self,plug):
        """ Create the plugin in the MorphoNet Window
        
        Parameters
        ----------
        plugin : MorphoPlugin
            A plugin instance
    
        """
        print(" --> create Plugin "+plug.name)
        self.send("BTN",plug._get_btn())
        
    def set_default_plugins(self):
        """ Load the default plugins to the 3D viewer

        Examples
        --------
        >>> mc.set_default_plugins()
        """
        from morphonet.plugins import defaultPlugins
        for plug in defaultPlugins:
            self.add_plugin(plug)


    ######################################### RAWIMAGES 
   
    def plot_raws(self,t):
        """ Enable the possibility to plot raw images to the browser for a specified time point ? 
        
        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        >>> mc.plot_raws(1)
        """
        if self.dataset.raw:
            if self.dataset.show_raw is None or self.dataset.show_raw!=t:
                self.dataset.show_raw=t
                self.restart(None)         

    def plot_raw(self,t):
        """ Compute and send raw images to the browser for a specified time point
        
        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        >>> mc.plot_raw(1)
        """
        if self.dataset.raw:
            print(" --> Send rawdatas at "+str(t))
            rawdata=self.dataset.get_raw(t)
            if rawdata is not None:
                new_shape=np.uint16(np.floor(np.array(rawdata.shape)/self.raw_factor)*self.raw_factor) #To avoid shifting issue
                rawdata=rawdata[0:new_shape[0],0:new_shape[1],0:new_shape[2]]
                factor_data=rawdata[::self.raw_factor,::self.raw_factor,::self.raw_factor]
                bdata=np.uint8(np.float32(np.iinfo(np.uint8).max)*factor_data/factor_data.max()).tobytes(order="F")
                if self.center is None:
                    self.center=self.dataset.get_center(rawdata)
                cmd="RAW_"+str(t)+"_"+str(rawdata.shape[0])+"_"+str(rawdata.shape[1])+"_"+str(rawdata.shape[2])+"_"+str(self.raw_factor)+"_"+self._get_centerText()
                self.send(cmd,bdata)

    ######################################### ADDD CENTERS
    
    def plot_seeds(self,seeds):
        """ Plot the cell centers to the browser
        
        Parameters
        ----------
        seeds : string
            the centers of the cells

        Examples
        --------
        >>> mc.plot_seeds(seed_info)
        """
        if seeds is not None and seeds!="":
            self.send("SEEDS",seeds)

    def _get_centerText(self):
        if self.center is not None:
            return str(int(round(self.center[0])))+"_"+str(int(round(self.center[1])))+"_"+str(int(round(self.center[2])))
        return "0_0_0"

    ######################################### PRIMITIVES  
    
    def add_primitive(self,name,obj): 
        """ Add a primitive using specified content with the specified name to the browser
        
        Parameters
        ----------
        name : string
            the name of the primitive
        obj : bytes
            content of the primitive (3D data)

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mc.add_primitive("primitive name",content)
        >>> f.close()
        """
        self.send("PRIM_"+str(name),obj)

    ######################################### INFOS 
    
    def _reset_infos(self):
        """
            Reset the updated of all infos 
        """
        if self.dataset.infos is not None:
            for info_name in self.dataset.infos: 
                inf=self.get_info(info_name)
                inf.updated=False

    def plot_infos(self):

        """ Plot all the infos of the datasset
        """

        if self.dataset.infos is not None:
            for info_name in self.dataset.infos: 
                self.plot_info(self.get_info(info_name))

    def plot_info(self,info): #PLOT INFO (CORRESPONDENCAE)
        """ Send the specified informations with the specified name to browser
        
        Parameters
        ----------
        info : Info Class
           the info to plot   

        Examples
        --------
        >>> my_info=mc.get_info("Cell Name")
        >>> mc.plot_infos(my_info)
        """

        
        if info is None:
            return 
        if info.updated:
            print(" --> plot "+info.name)
            info_text=info.get_txt(time_begin=self.dataset.begin,time_end=self.dataset.end) 
            self.send("INFO_"+info.name,info_text)

            
    def plot_infos_currated(self):

        """ Plot all the curation for all the infos of the datasset
        """

        if self.dataset.infos is not None:
            for info_name in self.dataset.infos: 
                self.plot_info_currated(self.get_info(info_name))

    def plot_info_currated(self,info): 
        """ Send the specified currattion for the informations with the specified name to browser
        
        Parameters
        ----------
        info : Info Class
           the info to plot   
        """

        
        if info is None:
            return 
        if info.is_curated():
            curation_txt=info.get_curation_txt(time_begin=self.dataset.begin,time_end=self.dataset.end)
            self.send("CUR_"+info.name,curation_txt)

    def get_infos(self):
        """ Return all the informations associated to the dataset
        """
        return self.dataset.infos

    def get_info(self,info_name):
        """ Return the info associated to the dataset
        
        Parameters
        ----------
        info_name : string
           the name of the info

        return info : Class info 
            return an object of info 

       
        Examples
        --------  
        >>> my_info=mc.get_info("Cell Name")
        >>> my_info.get_txt() #return the text file
        """
        if info_name in self.dataset.infos:
            return self.dataset.infos[info_name]
        return None

    def create_info(self,info_name,info_type,data=None):
        """ Create an info associated to the dataset
        
        Parameters
        ----------
        info_name : string
           the name of the info
        info_type
            the type of the info (float,string, etc.. ) in string
        data (optional) : List<string> or info as in MorphoNet
            information content as a list of all lines 

        Examples
        --------  
        >>> info=mc.create_info("Cell Name","string")
        >>> info.set(el,"a7.8")
        """
        inf=self.dataset._get_info(info_name,info_type=info_type,reload=True)
        if data is not None:
            if type(data) == str: #From Text Info as in MorphoNet
                for d in data.split('\n'):
                    if not d.startswith("#") and not d.startswith(("type")):
                        dos=d.split(":")
                        if len(dos)==2:
                            mo=MorphoObject(dos[0].strip())
                            inf.set(mo, dos[1].strip())
            else:
                inf.data=data

    def delete_info(self,info_name):
        """ delete an info associated to the dataset
        
        Parameters
        ----------
        info_name : string
           the name of the info

        Examples
        --------  
        >>> info=mc.delete_info("Cell Name")
        >>> info.set(el,"a7.8")
        """
        inf=self.dataset._get(info_name,info_type=info_type,reload=True)
        if data is not None:
            if type(data) == str: #From Text Info as in MorphoNet
                for d in data.split('\n'):
                    if not d.startswith("#") and not d.startswith(("type")):
                        dos=d.split(":")
                        if len(dos)==2:
                            mo=MorphoObject(dos[0].strip())
                            inf.set(mo, dos[1].strip())
            else:
                inf.data=data

    def set_info_type(self,info_name,info_type):
        """ Change or specify the type of an info associated to the dataset
            The info can be created directly in python or load in the XML file

        Parameters
        ----------
        info_name : string
          the name of the info
        info_type
           the type of the info (float,string, etc.. )  in string

        Return True if the changement is affected

        Examples
        --------
        >>> mc.set_info_type("ThisField","selection")
        """
        infor=self.get_info(info_name)
        if infor is None:
            return False
        infor.info_type=info_type
        return True


    def reload_infos(self):
        self.plot_infos()
        self.plot_infos_currated()

    def curate_info(self,info_name,k,v,d):
        """ Apply the curration value of a specific object for the info name 
        
        Parameters
        ----------
        info_name : string
           the name of the info
        k : string
            object to curate
        v : string
            value of curation
        d : string
            date of curation  
        """

        info=self.get_info(info_name)
        o=info._get_object(MorphoObject(k))
        info.set_curation(o,v,d)
        self.restart(None)

    def delete_curate_info(self,info_name,k,v,d):
        """ Delete the curration value of a specific object for the info name 
        
        Parameters
        ----------
        info_name : string
           the name of the info
        k : string
            object to curate
        v : string
            value of curation
        d : string
            date of curation  
        """
        info=self.get_info(info_name)
        o=info._get_object(MorphoObject(k))
        if not info.del_curation(o,v,d):
            print(" Error during the deletion of the curation ")
        self.restart(None)

    def delete_curate_info_using_value(self,info_name,k,v):
        """ Delete the curration value of a specific object for the info name using the value
        
        Parameters
        ----------
        info_name : string
           the name of the info
        k : string
            object to curate
        v : string
            value of curation
        """
        info=self.get_info(info_name)
        o=info._get_object(MorphoObject(k))
        if not info.del_curation_using_value(o,v):
            print(" Error during the deletion of the curation ")
        self.restart(None)

    def create_info_from_unity(self,info_name,datatype,data):
        """ Create or Update info when receiving data from unity
        
        Parameters
        ----------
        info_name : string
           the name of the info
        datatype : string
            info type
        data : string
            data to write in info file
        """

        self.create_info(info_name,datatype,data)
        self.dataset._write_properties(self.dataset.xml_file)
        self.restart(None)

    def delete_info_from_unity(self,info_name):
        """ Create or Update info when receiving data from unity
        
        Parameters
        ----------
        info_name : string
           the name of the info
        datatype : string
            info type
        data : string
            data to write in info file
        """
        print(" --> delete info "+info_name)
        info=self.get_info(info_name)
        print(info)
        if info is not None:
            print("got info : "+info_name)
            info.clear()
            print(self.dataset.infos[info_name])
            del self.dataset.infos[info_name]
            self.dataset._write_properties(self.dataset.xml_file)
            self.restart(None)

    def delete_selection_from_unity(self,info_name,selection_number):
        """ Create or Update info when receiving data from unity
        
        Parameters
        ----------
        info_name : string
           the name of the info
        datatype : string
            info type
        data : string
            data to write in info file
        """
        info=self.get_info(info_name)
        if info is not None:
            info.del_selection(selection_number)
            self.dataset._write_properties(self.dataset.xml_file)
            self.restart(None)

    #########################################  SELECTION
    def plot_selection(self,selection):
        '''
        Plot selection (list of objects separated by ;)
        '''
        if selection is not None:
            print(" --> plot selection "+selection)
            self.send("SELECT",str(selection))

    #########################################  MESH
    def _get_mesh(self,t,data):
        if self.center is None:
            self.center=self.dataset.get_center(data)
        if t not in self.dataset.cells_updated:
            self.dataset.cells_updated[t]=[]
        obj=convert_to_OBJ(data,t,background=self.dataset.background,factor=self.factor,center=self.center,cells_updated=self.dataset.cells_updated[t],path_write=self.temp_path) #Create the OBJ
        self.dataset.cells_updated[t]=[]
        return obj  
    
    def plot_mesh(self,t): #UPLOAD DITECLTY THE OBJ TIME POINT IN UNITY
        """ Send the 3D files for the specified time point to browser and display the mesh 
        
        Parameters
        ----------
        t : int
            the time point to display in browser

        Examples
        --------
        >>> mc.plot_mesh(1)
        """
        obj=""
        data=self.dataset.get_seg(t)
        if data is not None:
            print(" --> Send mesh at "+str(t))
            self.dataset._set_volume(data,t) #Update Volumes
            obj=self._get_mesh(t,data)
        self.send("LOAD_"+str(t),obj)

    def plot_at(self,t,obj):#PLOT DIRECTLY THE OBJ PASS IN ARGUMENT
        """ Plot the specified 3D data to the specified time point inside the browser
        
        Parameters
        ----------
        t : int
            the time point to display in browser
        obj : bytes
            the 3d data

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mc.plot_at(1,content)
        >>> f.close()
        """
        self.send("LOAD_"+str(t),obj)

    def plot_meshes(self,times=None):  # PLOT ALL THE TIMES STEP EMBRYO IN MORPHONET
        """ Plot all data inside the browser

        Examples
        --------
        >>> mc.plot_meshes()
        """
        if times is None:
            times=range(self.dataset.begin,self.dataset.end+1)
        for t in times:
            self.plot_mesh(t)
           
    def del_mesh(self,t): #DELETE DITECLTY THE OBJ TIME POINT IN UNITY
        """ Delete the specified time point in the browser
        
        Parameters
        ----------
        t : int
            the time point to delete

        Examples
        --------
        >>> mc.del_mesh(1)
        """
        self.send("DEL_"+str(t))


    ################ TO QUIT PROPERLY

    def _clear_temp(self):
        #print(" --> clear temporary path ")
        os.system('rm -rf .temp_morphonet*')

    def _clear_backup(self):
        # print(" --> clear morphonet backup ")
        os.system('rm -rf .backup_morphonet')

    def _receive_signal(self,signalNumber, frame):
        if signalNumber==2:
            try:
                self._clear_temp()
                self.quit()
                quit()
            except:
                print(" --> quit MorphoPlot")
        return



