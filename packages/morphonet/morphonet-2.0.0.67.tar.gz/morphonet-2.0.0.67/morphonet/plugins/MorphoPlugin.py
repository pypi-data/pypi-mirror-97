# -*- coding: latin-1 -*-
import numpy as np
from datetime import datetime

class MorphoPlugin:
    """Plugin class to be heritate in order to create plugin in MorphoNet  

    Examples
    --------
    >>> class MyFirstPLugin(MorphoPlugin):
    >>>     def __init__(self): 
    >>>         MorphoPlugin.__init__(self) 
    >>>         self.set_name("My First Plugin ")

    """

    def __init__(self):
        self.name="default plugin name"
        self.parent="None"
        self.inputfields={}
        self.dropdowns={}
        self.dropdowns_sel={}
        self.coordinates={}
        self.exec_time=None #Time of Execution
        self.dataset=None


    def set_name(self,text_name):     #PLUGIN NAME 
        """Define the plugin name

        Parameters
        ----------
        name : string
            the plugin name

        Examples
        --------
        >>> mc.set_name("My first Plugin")
        """
        self.name=text_name

 
    def set_parent(self,text_name):     #PARENT GROUP
        """Define the parent name in order to group plugin the in the Morphow Window

        Parameters
        ----------
        name : string
            the parent name

        Examples
        --------
        >>> self.set_parent("Create new objects")
        """

        self.parent=text_name

    
    #INPUT FIELD IN UNITY
    def add_inputfield(self,text_name,default=None): 
        """Define a new variable for the plugin wich will be appear as a Input Field in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 
        default_value : multi-type (optional)
            the default value of the variable

        Examples
        --------
        >>> self.add_inputfield(""gaussian_sigma",8)
        """
        self._set_inputfield(text_name,default)

    def _set_inputfield(self,text_name,value):
        self.inputfields[text_name]=value

    def get_inputfield(self,text_name):
        """Return the value of the variable enter in the Input Field in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> gauss=int(self.get_inputfield("Min gaussian_sigma"))
        """

        return self.inputfields[text_name]

    #DROWDOWN IN UNITY
    def add_dropdown(self,text_name,option):
        """Define a new variable as a list of options for the plugin wich will be appear as a Dropdown in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 
        option : list of string 
            list of options 

        Examples
        --------
        >>> self.add_dropdown("Inverse",["no","yes"])
        """

        self.dropdowns[text_name]=option
        self._set_dropdown(text_name,0)

    def _set_dropdown(self,text_name,value):
        self.dropdowns_sel[text_name]=int(value)

    def get_dropdown(self,text_name):
        """Return the value of the variable enter in the Dropdown in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> isOk=self.get_dropdown("Inverse")=="yes"
        """
        return self.dropdowns[text_name][self.dropdowns_sel[text_name]]

    #ADD COORDINATES IN UNITY
    def add_coordinates(self,text_name):
        """Define a new variable as a list of 3D coordinates wich allow you the get the list of corrdinates entered in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> self.add_coordinates("seeds")
        """
        self.coordinates[text_name]=[]

    def _set_coordinates(self,text_name,coords): #Recieve '(-0.9, 0.2, -3.5); (0.1, -0.2, -3.5); (0.9, -0.6, -3.5)'
        if coords!="":
            self.coordinates[text_name]=[]
            for s in coords.split(";"):
                self.coordinates[text_name].append(np.float32(s[1:-1].split(',')))

    def get_coordinates(self,text_name):
        """Return the list of coordinates defined in the Morphow Window

        Parameters
        ----------
        text_name : string
            the name of the variable 

        Examples
        --------
        >>> seeds=self.get_coordinates("seeds")
        """

        return self.coordinates[text_name]

    #INTERNAL COMMAND
    def _cmd(self):
        return self.name

    def _get_btn(self):
        c=self._cmd()+";"+self.parent
        for tf in self.inputfields:
            c+=";IF_"+str(tf)
            if self.inputfields[tf] is not None:
                c+=";DF_"+str(self.inputfields[tf])
        for dd in self.dropdowns:
            c+=";DD_"+str(dd)+"_"
            for v in self.dropdowns[dd]:
                c+=str(v)+"_"
        for cd in self.coordinates:
            c+=";CD_"+str(cd)
        return c

    def print_mn(self,msg):
        """Print a string on the 3D viewer

        Parameters
        ----------
        msg : string
            your message to print 
        """
        if self.dataset is not None:
            self.dataset.print_mn(msg)
        else:
            print(msg)

    #Start the plugin
    def start(self,t,dataset,objects):
        """Start function which have be to be exectuted at the begining of the process 

        Parameters
        ----------
        t : time
            the specitic time step on the MorphoNet Window
        dataset: dataset
            the dataset variable
        objects :
            the selected objects int the MorphoNet Window

        Examples
        --------
        >>>     def process(self,t,dataset,objects): #PLUGIN EXECUTION
        >>>         if not self.start(t,dataset,objects): 
        >>>             return None

        """

        self.exec_time=datetime.now()
        self.dataset=dataset
        self.t=t
        self.objects=objects
        self.print_mn(">> Process "+self.name)
        isOk=True
        for tf in self.inputfields:
            if self.inputfields[tf] is None or self.inputfields[tf]=="":
                self.print_mn(" --> Please fill the parameter "+str(tf))
                isOk=False
            else:
                self.print_mn(" --> Found "+str(tf)+" = "+str(self.inputfields[tf]))
        if isOk and objects is not None and len(objects)>0 and objects[0]!='':
            self.print_mn(" --> with objects :"+str(objects))
            self.dataset.backup(self.get_log(),t,objects)

        if not isOk:
            self.dataset.restart(self)
        return isOk

    def get_log(self):
        log = "Plugin:" + self.name + "(" + self.parent + "); Time:" + str(self.t) + ";"
        for tf in self.inputfields:
            log += " IF:" + str(tf) + ":" + str(self.get_inputfield(tf)) + ";"
        for dd in self.dropdowns:
            log += " DD:" + str(dd) + ":" + str(self.get_dropdown(dd)) + ";"
        for cd in self.coordinates:
            log += " CD:" + str(cd) + ":" + str(self.get_coordinates(cd)) + ";"
        if self.objects is not None and len(self.objects) > 0 and self.objects[0] != '':
            log += " ID:" + str(self.objects) + ";"
        return log

    #Restart the curation
    def restart(self):
        """Restart function which have be to be exectuted at the end of the process in order to restart properlly the curation

        Examples
        --------
        >>>     def process(self,t,dataset,objects):
        >>>         if not self.start(t,dataset,objects):
        >>>             return None
        >>>         ...
        >>>         ... plugin execution  ...
        >>>         ...
        >>>         self.restart()

        """
        self.dataset.save_log(self.get_log(),self.exec_time)
        self.dataset.restart(self)




