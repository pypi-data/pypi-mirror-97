import os
import re
import numpy as np
import math
import csv
from datetime import datetime
from datetime import timedelta
from itertools import product
from skimage import io
from skimage.transform import downscale_local_mean

from scipy.ndimage import gaussian_filter

from skimage.transform import resize
from skimage.morphology import disk
from scipy.ndimage.filters import generic_filter
import cv2 as cv

import tifffile

from . import generalFunctions as genF
from .zProj import maxProj,avProj,minProj,signalProj
from .FindCentres import findCentres
from .noMergeStitch import noMergeStitch,noMergeStitch2,cenList2Size
from .LabelVideo import moment2Str,addTimeLabel
from .AlignExtract import findRegion,extractRegion
from .AlignExtract import rotCoord_NoCrop,rotate_image
from .exceptions import UnknownTifMeta
from . import findMeta as fMeta
from . import errorMessages as EM



class XFold:
    """
    This class represents an 'experiment folder'. That is a folder where you 
    put all the data that you want the code to analyse and consider as one 
    experiment. The object therefore holds all information that is globally 
    the same for all data.
    
    Attributes
    ----------
    XPath : str
        The path of the experiment folder.
    FieldIDMapList : list or str
        If list, each element represents a session and is a list of IDs (str), 
        one for each field in that session. If str, then it should be a file 
        path to a txt file containing this info. If path is one level then it 
        is interpreted as being in the parent directory of XPath. The format 
        is new line for each session and each field ID separated by commas.
    Filters : list of str
        Files/directories including any of these terms in their name 
        are excluded from all analysis.
    StartTimes : dict
        The dictionary keys are the field IDs and the values are the datetime 
        object of when that experiment started.
    sizeDic : 
        Is a dictionary of {fieldID:[maxYSize,maxXSize]}
    """
    
    UINT16MAX = 65535
    OutDirSig = 'XFoldAnalysis_'
    FieldDir = 'Exp'
    chanOrder = {'BF':0,
                 'YFP':1,
                 'GFP':2,
                 'RFP':3,
                 'CFP':4,
                 'FR':5,
                 'Label':6,
                 'DAPI':7}
    
    def __init__(
        self,
        XPath,
        FieldIDMapList=None,
        Filters=[],
        StartTimes=None,
        makeTFiles = True
    ):
        """
        Parameters
        ----------
        FieldIDMapList : None or str or list of list of str
            User provided source to build the FieldIDMapList from.
            If None then the Nth field of easch session if given ID 'N'.
            If str then it must be a filepath to a .txt file containing the 
            information in format:
            A,B,C,D
            D,E
            C,F
            where each line represents a session and each comma-separated 
            string is the ID for each field.
            Filepaths which are just one level deep are interpreted to just be 
            the name of the file in the XFold parent directory.
        Filters : list of str
            Any files containing any of the strings in this list will be 
            excluded from all analysis.
        StartTimes : None or str or dict
            User provided source to build StartTimes dictionary from.
            If None then each field will be assigned the time it first appears 
            in the data.
            If str then it must be a path to a .txt with the information. 
            Filepaths which are just one level deep are interpreted to just be 
            the name of the file in the XFold parent directory. The file must 
            be in one of 2 formats:
            Format1:
            fieldID1: dd/mm/yyyy hh:mm:ss
            fieldID2: dd/mm/yyyy hh:mm:ss
            Where there is a line for every fieldID.
            Format2:
            dd/mm/yyyy hh:mm:ss
            Meaning every field started at the same time.
            If dict then we assume you have made the whole dictionary yourself.
        makeTFiles : bool
            Making the TFiles requires more processing since it looks into the 
            files to see what is stored. You need to make them if you want to 
            make a TData but otherwise you can set to False to save time.
        """ 
        
        self.XPath = XPath
        assert os.path.exists(XPath), 'The XPath you provided doesn\'t exist'
        assert os.path.split(self.XPath)[0]!='',EM.xf1
        assert os.listdir(XPath)!=[],EM.xf2
        self.XPathP = os.path.split(self.XPath)[0]
        
        self.Filters = Filters
        self.Warnings = []
        
        self._seshData = None
        self.FieldIDMapList = self.buildFieldIDMapList(FieldIDMapList)
        
        self.StartTimes = self.buildStartTimes(StartTimes)
        self.SessionsList = []
        self.makeSessions(makeTFiles)
        
        self.HomogFiltDic = {} # see XFold.buildHomogFilts()
        self.AlignDic = {} # see XFold.buildStoredAlignments()
        self.TemplateDic = {} # see XFold.buildTemplateDic()
        self.WindowDic = {} # see XFold.buildWindowDic()
        self.MaskDic = {} # see XFold.buildMaskDic()
        
        self.SavedFilePaths = []
        self.StitchCounts = [0,0]
        self.HomogOverflow = [0,0] #[no. of ims overf'ed,no. of ims treated]
        
        self.Assertions()
    
    
    def Assertions(self):
        """Put any final checks during XFold initiation here."""
        assert isinstance(self.Filters,list),'Filters must be a list.'
        
        
    def buildFieldIDMapList(self,FieldIDMapList):
        """
        Interprets user input for FieldIDMapList source to build the true list.
        """
        
        if type(FieldIDMapList)==list:
            pass
        elif isinstance(FieldIDMapList,str) and FieldIDMapList != '':
            if not os.path.split(FieldIDMapList)[0]:
                FieldIDMapList = os.path.join(self.XPathP,FieldIDMapList)
            with open(FieldIDMapList,'rt') as theFile:  
                FM = theFile.read()
            FieldIDMapList = [sesh.split(',') for sesh in FM.split('\n')]
        elif not FieldIDMapList:
            FieldIDMapList = []
            if not self._seshData:
                self.buildSessionData()
            for sesh in self._seshData:
                NF = sesh[1]['NF']
                FieldIDMapList.append([str(x+1) for x in range(NF)])
        else:
            raise Exception('FieldIDMapList format not recognised.')
        return FieldIDMapList
        
        
    def buildStartTimes(self,StartTimes):
        """
        Interprets user input for StartTimes to create StartTimes dictionary.
        """
        if isinstance(StartTimes,dict):
            pass
        elif isinstance(StartTimes,str):
            if os.path.split(StartTimes)[0] == '':
                StartTimes = os.path.join(self.XPathP,StartTimes)
            assert os.path.exists(StartTimes),EM.st1%StartTimes
                
            with open(StartTimes,'rt') as theFile:
                labData = theFile.read()
            # this gets rid of any spurious whitespace at end of the .txt file
            endWSpaceReg = r'(\s*)$'
            labData = re.sub(endWSpaceReg,'',labData)
            labData = labData.split('\n')
            # get rid of spurious white spaces at the end of lines:
            labData = [re.sub(endWSpaceReg,'',s) for s in labData]
            
            StartTimes = [line.split(': ') for line in labData]
            XVFields = set([y for x in self.FieldIDMapList for y in x])
            
            if len(StartTimes)==1 and len(StartTimes[0])==1:
                # format2 (see __init__):
                StartTimes = {k:labData[0] for k in XVFields}
            elif len(StartTimes)>1 and all([len(s)==2 for s in StartTimes]):
                # format1 (see __init__):
                StartTimes = {k:v for k,v in StartTimes}
            else:
                raise Exception(EM.st2)
            
            # now just do checks that everything is good:
            labRegs = set(list(StartTimes.keys()))
            regMom = r'\d{2}/\d{2}/\d{4} \d\d:\d\d:\d\d'
            matchQ = all([re.match(regMom,x) for x in StartTimes.values()])
            TX = '%d/%m/%Y %H:%M:%S'

            if labRegs==XVFields and matchQ:
                StartTimes = {k:datetime.strptime(v,TX) 
                              for k,v in StartTimes.items()}
            elif not matchQ: 
                raise Exception(EM.st2)
            else:
                raise Exception(EM.st3)
            
        elif not StartTimes:
            self.Warnings.append(EM.stW)
            XVFields = set([y for x in self.FieldIDMapList for y in x])
            StartTimes = {}
            for field in XVFields:
                for i,XV in enumerate(self.FieldIDMapList):
                    if field in XV:
                        StartTimes.update({field:i})
                        break
            # for now we don't know the metadata of the sessions so we just 
            # leave it like this and update during makeSessions()           
        else: 
            raise Exception('StartTimes not in recognised format.')
        return StartTimes
            

    def buildSessionData(self):
        """
        This looks in XPath and retrieves all data required to make sessions.
        i.e it groups image file paths into sessions and extracts metadata.
        """
        # get all the image file paths you can find and process them
        walk = [x for x in os.walk(self.XPath)]
        fps = sorted([os.path.join(x[0],fn) for x in walk for fn in x[2]])
        fps = [fp for fp in fps if not any(fl in fp for fl in self.Filters)]
        tps = [t for t in fps if '.tif' in t]
        
        tps2 = tps.copy()

        # for each session make: [all sesh paths,sesh metadata dictionary]
        sesh = []
        for tp in tps:
            if tp not in tps2:
                continue
            meta =  fMeta.allSeshMeta(tp)
            mb = meta['madeBy']
            strippedPath = genF.stripTags(tp,mb)
            tps2b = [genF.stripTags(T,mb) for T in tps2]
            seshTPs = [T for T,Tb in zip(tps2,tps2b) if Tb==strippedPath]
            for T in seshTPs:
                tps2.remove(T)
            sesh.append([seshTPs,meta])
        
        # order the sessions by their startMom
        seshSM = [s[1]['startMom'] for s in sesh]
        self._seshData = [S for _,S in sorted(zip(seshSM,sesh))]        
        
        
    def makeSessions(self,makeTFs=True):
        """ 
        Makes all the sessions found in the XPath.
        It applies the Filters, to filter out unwanted files.
        All Sessions are saved within the XFold.SessionsList and also are 
        returned in a list so you could save them separately if you want.
        """
        
        self.SessionsList = []
        if not self._seshData:
            self.buildSessionData()
        assert len(self._seshData)==len(self.FieldIDMapList),EM.fm1
        
        # make the sessions
        allSesh = []
        for i,s in enumerate(self._seshData):
            allSesh.append(
                Session(
                    self,
                    i,
                    self.FieldIDMapList[i],
                    s[1]['metadata'],
                    s[0],
                    allMeta = s[1],
                    makeTFiles = makeTFs
                ))
            
        # update StartTimes if we didn't complete it before 
        # (i.e. if there wasn't a txt file provided we use metadata to guess)
        for k,v in self.StartTimes.items():
            if isinstance(v,int):
                self.StartTimes.update({k:allSesh[v].StartMom})
        self.SessionsList = allSesh
        return allSesh

    
    def buildHomogFilts(self,HomogFilts):
        """
        This loads homogenisation filters (see TData.Homogensise) that are 
        saved to the XFold so they don't have to be loaded multiple times.
        They are saved to XFold.HomogFiltDic which is a dict of channel names 
        for keys and filters for values.
        
        Parameters
        ----------
        HomogFilts : str or dict
            If str then it is a path to a directory containing the filters. 
            They must be named chan_XX.tif where chan is the channel name and 
            XX if FF or DF for flat/dark field (see TData.Homogenise). Path 
            with one level is taken to be in the XFold parent folder. If 
            dict then keys are channel names and values are dicts with key = 
            FF or DF (for flat field or dark field) and values are path to 
            filter or the image itself.
        """
        
        if isinstance(HomogFilts,str):
            if not os.path.split(HomogFilts)[0]:
                HomogFilts = os.path.join(self.XPathP,HomogFilts)
            fps = os.listdir(HomogFilts)
            HF = ['_FF.tif','_DF.tif']
            hNames = [c+f for c in XFold.chanOrder.keys() for f in HF]
            for h in hNames:
                if h in fps:
                    im = io.imread(os.path.join(HomogFilts,h)).astype('float32')
                    if h[:-7] not in self.HomogFiltDic.keys():
                        self.HomogFiltDic[h[:-7]] = {}
                    self.HomogFiltDic[h[:-7]][h[-6:-4]] = im#/im.max()
        elif isinstance(HomogFilts,dict):
            for k,v in HomogFilts.items():
                if k not in self.HomogFiltDic.keys():
                    self.HomogFiltDic[k] = {}
                for k2,v2 in HomogFilts[k].items():
                    if isinstance(v2,str):
                        im = io.imread(HomogFilts[k][k2]).astype('float32')
                        self.HomogFiltDic[k][k2] = im#/im.max()
                    elif isinstance(v2,np.ndarray):
                        self.HomogFiltDic[k][k2] = v2#/v2.max()
                    else:
                        raise Exception('HomogFilts format not correct.')
        else:
            raise Exception('HomogFilts must be a str or dict')
    
    
    def buildStoredAlignments(self,storedAlignments,refresh=False):
        """
        Stored alignments is a .txt file that can be created when you run 
        TData.AlignExtract and stores the alignments found so that they can be 
        used again later to save time. This function loads a given .txt file 
        to the XFold so it is ready to use.
        
        Parameters
        ---------
        storedAlignments : str
            The path to the stored alignments. If it is a path of one level 
            then it assumes this is in the parent directory of the XFold.
        refresh : bool
            Whether to reload the provided storedAlignments if XFold.AlignDic 
            already contains a dictionary under the key 'storedAlignments'.
        
        Builds
        ------
        XFold.AlignDic : dict
            Each key is the str storedAlignments (so that multiple 
            storedAlignments can be stored) and each value is another 
            dictionary. That 2nd dictionary have keys that are the codes 
            that identify each session-time-field and the values are (ang,
            [shifty,shiftx], see TData.AlignExtract).
        """
        assert isinstance(storedAlignments,str),EM.ae7
        if storedAlignments in self.AlignDic.keys() and not refresh:
            return
        else:
            self.AlignDic[storedAlignments] = {}
        storedAlignmentsP = storedAlignments
        if os.path.split(storedAlignmentsP)[0]=='':
            storedAlignmentsP = os.path.join(self.XPathP,storedAlignmentsP)
        if not os.path.exists(storedAlignmentsP):
            open(storedAlignmentsP,'w').close()
        with open(storedAlignmentsP,'r') as file:
            aligns = file.read()
        aligns = aligns.split('\n')
        codeReg = r'(S\d+T\d+F\d+) : '
        codeReg += r'([+-]?\d*.?\d*) ([+-]?\d*.?\d*) ([+-]?\d*.?\d*)'
        for a in aligns:
            search = re.search(codeReg,a)
            if search:
                kk = search.group(1)
                ang = float(search.group(2))
                shift = [float(search.group(3)),float(search.group(4))]
                self.AlignDic[storedAlignments].update({kk:(ang,shift)})        
    
    
    def buildTemplates(self,templates,refresh=False):
        """
        The templates are the images, resized and rotated to the good 
        orientation, that you want to match and extract from the data using 
        e.g. TData.AlignExtract. This function loads them into a dictionary so 
        that they don't have to be loaded each time.
        
        Parameters
        ---------
        templates : str
            A path to a folder containing the template images saved as tifs. 
            String with only one level of path is interpreted as a directory 
            within the parent of XPath. The images must be in subdirectories 
            for each field with name 'Exp'+fieldID. 
        refresh : bool
            Whether to reload the provided templates if XFold.TemplateDic 
            already contains a dict under the key 'templates'.
        
        Builds
        ------
        XFold.TemplateDic : dict
            Each key is the str templates (so that multiple sets of 
            templates can be stored) and each value is another 
            dictionary. That 2nd dictionary have keys that are the field IDs 
            and the values are the images.
        """
        assert isinstance(templates,str),'Templates must be a string.'
        if templates in self.TemplateDic.keys() and not refresh:
            return
        else:
            self.TemplateDic[templates] = {}        
        templatesP = templates
        if os.path.split(templatesP)[0]=='':
            templatesP = os.path.join(self.XPathP,templatesP)
        assert os.path.exists(templatesP),EM.ae1
        
        # now make the dictionary from FieldIDMapList
        temps = [os.path.join(templatesP,d) for d in os.listdir(templatesP)]
        temps = [t for t in temps if os.path.isdir(t)]
        assert all([len(os.listdir(t))==1 for t in temps]),EM.ae2
        fs = [os.path.split(t)[1][len(XFold.FieldDir):] for t in temps]
        temps = [os.path.join(t,os.listdir(t)[0]) for t in temps]
        
        for i,temp in enumerate(temps):
            with tifffile.TiffFile(temp) as tif:
                temps[i] = tif.asarray().astype('float32')
        
        self.TemplateDic[templates].update({k:v for k,v in zip(fs,temps)})
 

    def buildWindows(self,windows,refresh=False):
        """
        The windows are a .txt file with the four corners of a rectangle 
        defining where on a template image you find the region you want to 
        extract data with using TData.ExtractProfileRectangle(). This loads 
        them for all fields so they don't have to be built each time.
        
        Parameters
        ---------
        windows : str
            A path to a folder containing the window files saved as .txt. 
            String with only one level of path is interpreted as a directory 
            within the parent of XPath. The files must be in subdirectories 
            for each field with name 'Exp'+fieldID. 
        refresh : bool
            Whether to reload the provided windows if XFold.WindowDic
            already contains a dict under the key 'windows'.
        
        Builds
        ------
        XFold.WindowDic : dict
            Each key is the str windows (so that multiple sets of 
            windows can be stored) and each value is another 
            dictionary. That 2nd dictionary have keys that are the field IDs 
            and the values are the window data.
        """
            
        if windows in self.WindowDic.keys() and not refresh:
            return
        else:
            self.WindowDic[windows] = {}        
        windowsP = windows
        if os.path.split(windowsP)[0]=='':
            windowsP = os.path.join(self.XPathP,windowsP)
        assert os.path.exists(windowsP),'Windows file not found.'
        
        # now make the dictionary from FieldIDMapList
        ws = [os.path.join(windowsP,w) for w in os.listdir(windowsP)]
        ws = [w for w in ws if os.path.isdir(w)]
        fs = [os.path.split(w)[1][len(XFold.FieldDir):] for w in ws]
        
        ws = [[os.path.join(w,f) for f in os.listdir(w)] for w in ws]
        ws = [[t for t in w if '.txt' in t] for w in ws]
        assert all([len(w)==1 for w in ws]),EM.bw1
        ws = [w[0] for w in ws]
        
        for f,w in zip(fs,ws):
            with open(w,'rt') as roi:
                w = roi.read()
            w = [p.split('\t') for p in w.split('\n') if p!='']
            w = [[int(float(p[1])),int(float(p[0]))] for p in w]
            # you can give it trapezium window and we convert to rectangle
            w = genF.trap2rect(w)
            self.WindowDic[windows].update({f:w})
 

    def buildMasks(self,masks,refresh=False):
        """
        The masks are .tif files the same as the templates (see 
        XFold.buildTemplates()) but with a white line drawn around a region 
        that you want to take values from using TData.ExtractProfileRectangle. 
        Pixels outside this region will be ignored. This loads them for all 
        fields so they don't have to be imported and processed each time.
        
        Parameters
        ---------
        masks : str
            A path to a folder containing the mask tifs. String with only one 
            level of path is interpreted as a directory within the parent of 
            XPath. The files must be in subdirectories for each field with 
            name 'Exp'+fieldID. 
        refresh : bool
            Whether to reload the provided masks if XFold.MaskDic
            already contains a dict under the key 'masks'.
        
        Builds
        ------
        XFold.MaskDic : dict
            Each key is the str masks (so that multiple sets of 
            masks can be stored) and each value is another 
            dictionary. That 2nd dictionary have keys that are the field IDs 
            and the values are the processed masks as numpy arrays.
        """
            
        if masks in self.MaskDic.keys() and not refresh:
            return
        else:
            self.MaskDic[masks] = {}        
        masksP = masks
        if os.path.split(masksP)[0]=='':
            masksP = os.path.join(self.XPathP,masksP)
        assert os.path.exists(masksP),'Masks directory not found.'
        
        # now make the dictionary from FieldIDMapList
        ms = [os.path.join(masksP,m) for m in os.listdir(masksP)]
        ms = [m for m in ms if os.path.isdir(m)]
        fs = [os.path.split(m)[1][len(XFold.FieldDir):] for m in ms]
        
        ms = [[os.path.join(m,f) for f in os.listdir(m)] for m in ms]
        ms = [[t for t in m if '.tif' in t] for m in ms]
        assert all([len(m)==1 for m in ms]),EM.bm1
        ms = [m[0] for m in ms]
        for f,m in zip(fs,ms):
            m = genF.maskFromOutlinePath(m)
            self.MaskDic[masks].update({f:m})


    def BuildSummary(self):
        """This method builds a string containing global information about 
        the xfold. Stuff like what channels, how much data etc... print it to
        see for yourself!"""
        
        summary = ''
        
        if not self.SessionsList:
            self.makeSessions()
        allSesh = self.SessionsList
        allTFiles = [TP for sesh in allSesh for TP in sesh.tFilePaths]
        
        summary += 'Total no. of sessions: ' + str(len(allSesh)) + '\n'
        summary += 'Total no. of tiff files: ' + str(len(allTFiles)) + '\n'
        
        # size in memory
        totSize = sum([os.stat(tp).st_size for tp in allTFiles])/1000000
        summary += 'Total memory of tiff files: ' + str(totSize) + ' MB\n'
        
        totalNT = str(sum([s.NT for s in allSesh]))
        summary += 'Total no. of time points (according to metadata): ' 
        summary += totalNT + '\n'
        uniqueF = str(len(set([y for x in self.FieldIDMapList for y in x])))
        summary += 'Total no. of fields (no. of unique ID): ' + uniqueF + '\n'
        
        # total duration of experiment
        firstStart = allSesh[0].StartMom
        lastStart = allSesh[-1].StartMom
        timeDelta = allSesh[-1].TStep
        totT = lastStart - firstStart + timeDelta*allSesh[-1].NT
        totD = str(totT.days)
        totH = str(totT.seconds//3600)
        totM = str(totT.seconds%3600//60)
        totT = totD + ' days, ' + totH + ' hours, ' + totM + ' minutes.'
        summary += 'Total time span: ' + totT + '\n'
        
        # NM,NZ and NC in 'set-like' form:
        summary += '\nThe following shows only the value of the given '\
                'attribute \nwhen it changes from one session to the next: \n'
        setF = str(genF.onlyKeepChanges([s.NF for s in allSesh]))
        setM = str(genF.onlyKeepChanges([s.NM for s in allSesh]))
        setZ = str(genF.onlyKeepChanges([s.NZ for s in allSesh]))
        setC = str(genF.onlyKeepChanges([s.NC for s in allSesh]))
        summary += 'Fields: ' + setF + '\n'
        summary += 'Montage tiles: ' + setM + '\n'  
        summary += 'z-Slices: ' + setZ + '\n'  
        summary += 'number of channels: ' + setC + '\n'  
        
        # channel names
        setCNames = str(genF.onlyKeepChanges([s.Chan for s in allSesh]))
        summary += 'names of channels: ' + setCNames + '\n'  
        
        # session names:
        sNames = ''.join([s.Name+'\n' for s in allSesh])
        summary += '\nThe names of the sessions: \n' + str(sNames) + '\n'
        return summary
    
    
    def Summarise(self):
        summary = self.BuildSummary()
        print(summary)
    
    
    def printProcessingStats(self):
        """ Some of the methods of other classes (especially TData) will 
        report statistics on the things they have done which get saved 
        into the parent xfold's attributes. This method prints them, 
        typically to give a report at the end of a processing session.
        """
        # saved files
        print('Files saved from analysis of your xfold:')
        [print(e) for e in self.SavedFilePaths]
        # blank time points removed
        print('Removed blank time points in (session : session time point):\n')
        for s in self.SessionsList:
            if s.BlankTimePoints:
                print(s.Name,' : ',set(s.BlankTimePoints))
        print('Number of auto-alinments during stitching '\
              'due to low signal: ',self.StitchCounts[0])
        print('Number of auto-alignments during stitching due '\
              'to large calculated shifts: ',self.StitchCounts[1])
        if self.HomogOverflow[0]>0:
            print('Fraction of images that had unit16 overflow during '\
                  'division by filter during field of view homogensiation: ',
                  self.HomogOverflow[1]/self.HomogOverflow[0])
        warnings = set(self.Warnings)
        for w in warnings:
            print(w)
            
    def checkTFiles(self,verbose=False):
        """ 
        This checks whether the number of images in the TFiles corresponds to 
        the dimensions that it thinks it has. I.e. whether the file is 
        corrupted somehow. It returns the paths of all corrupted files.
        """
        badFiles = []
        for s in self.SessionsList:
            for tf in s.TFilesList:
                if verbose:
                    print('Checking ',os.path.split(tf.TPath)[1])
                try:
                    fMeta.file2Dims(tf.TPath)
                except AssertionError:
                    badFiles.append(tf.TPath)
        return badFiles
        
            
class Session:
    """ A Session object represents one imaging session, i.e. one run of an 
    imaging protocol with your microscope software. 
    It holds all details on what that protocol was and where files are stored.
    
    Attributes
    ----------
    Name : str - A name for the session. Taken from its files ('tags' removed).
    MadeBy : {'Andor','MicroManager'} - the software that made the session.
    TFilesList : list - all TFile objects for that session.
    etc etc
    
    Methods
    -------
    makeTData - this is the most important method. It extracts specified image 
                data from the session.
    """
    
    def __init__(
        self,
        ParentXFold,
        SessionN,
        FieldIDMap,
        Metadata,
        tFilePaths,
        allMeta = None,
        makeTFiles = True
    ):
        """
        We extract all metadata during intialisation to save in attributes.
        
        Parameters
        -----------
        ParentXFold : XFold object
            The parent XFold of the Session.
        SessionN : int
            The position where you'll find this Session in the parent 
            XFold.SessionsList.
        FieldIDMap : list
            The list of the parent XFold.FieldIDMapList that corresponds to this
            Session. Element i if this list is the name we give to the ith 
            field of the image data of this session.
        Metadata : str
            Any metadata that isn't in the image files. Extracted as a raw 
            string.
        tFilePaths : list
            List of file paths of all image files associated with this session.
        makeTFiles : bool
            Whether to make the TFiles for the Session now.
        """
        
        self.ParentXFold = ParentXFold
        self.SessionN = SessionN
        self.FieldIDMap = FieldIDMap
        self.Metadata = Metadata
        self.tFilePaths = tFilePaths
        
        if allMeta:
            self.allMeta = allMeta
        else:
            self.allMeta = fMeta.allSeshMeta(self.tFilePaths[0])
        
        self.Name = self.allMeta['Name']
        self.MadeBy = self.allMeta['madeBy']
        
        self.imType = self.allMeta['imType']
        
        self.Chan = self.allMeta['Chan']
        self.Chan2 = [genF.chanDic(c) for c in self.Chan]
        self.NF = self.allMeta['NF']
        self.NT = self.allMeta['NT']
        self.NM = self.allMeta['NM']
        self.NZ = self.allMeta['NZ']
        self.NC = self.allMeta['NC']
        self.NY = self.allMeta['NY']
        self.NX = self.allMeta['NX']
        self.Shape = self.allMeta['Shape']
        
        self.StartMom = self.allMeta['startMom']
        self.TStep = self.allMeta['TStep']
        
        self.MOlap = self.allMeta['MOlap']
        self.NMY = self.allMeta['NMY']
        self.NMX = self.allMeta['NMX']
        self.FieldNMYs = self.allMeta['FieldNMYs']
        self.FieldNMXs = self.allMeta['FieldNMXs']
        
        self.MontageOrder = self.allMeta['MontageOrder']
        self.pixSizeY = self.allMeta['pixSizeY']
        self.pixSizeX = self.allMeta['pixSizeX']
        self.pixUnit = self.allMeta['pixUnit']
        
        # when the data along a certain dimension Q is split between different 
        # TFiles we assume there is an ordering and the position ith TFile 
        # will always contain L data points along Q. The ith element of the 
        # lists in this dictionary give L.
        self.FileTag2Len = {'T':{},'F':{},'M':{},'Z':{},'C':{}}
     
        self.BlankTimePoints = []
        
        self.tFilesMadeFlag = False
        if makeTFiles:
            self.makeTFiles()
        else:
            self.TFilesList = []   
    
    
    def makeTFiles(self,setTFileList=True,checkTF=False):
        """
        This creates all TFiles in tFilePaths of the Session. It returns them 
        in a list and saves them to the session in self.TFilesList. Unless you 
        set setTFileList=False.
        
        Parameters
        ----------
        setTFileList : bool
            Whether to set the Session's TFileList with the results.
        checkTF : bool
            Whether to raise exception if any TF is corrupt.
        """ 
        
        if setTFileList:
            self.TFilesList = []
        
        allTFiles = []
        
        for i,tf in enumerate(self.tFilePaths):
            
            nt,nf,nm,nz,nc,ny,nx = fMeta.file2Dims(tf,checkCorrupt=checkTF)
            lensDic = {'T':nt,'F':nf,'M':nm,'Z':nz,'C':nc}
            
            tagDic = genF.getTagDic(tf,self.MadeBy)
            
            # update self.FileTag2Len
            for k,v in tagDic.items():
                if v not in self.FileTag2Len[k].keys():
                    self.FileTag2Len[k].update({v:lensDic[k]})
            
            # find TFile position in session from self.FileTag2Len
            seshQ = []
            for k,v in lensDic.items():
                if k in tagDic.keys():
                    start = 0
                    # adds dimension length to start until you reach your tag
                    for k2,v2 in self.FileTag2Len[k].items():
                        if tagDic[k]==k2:
                            break
                        else:
                            start += v2
                    seshQ.append([i+start for i in range(v)])
                else:
                    seshQ.append(list(range(v)))
            allTFiles.append(TFile(self,i,tf,*seshQ,nt,nf,nm,nz,nc,ny,nx))
        
        if setTFileList:
            self.TFilesList = allTFiles
        
        # Andor leaves wrong NT in session metadata .txt file if session is 
        # stopped before end. So check if this is the case and update to what 
        # the files actually contain if needed.
        if self.FileTag2Len['T']:
            self.NT = sum(self.FileTag2Len['T'].values())
            self.Shape = tuple([self.NT,*self.Shape[1:]])
        
        self.tFilesMadeFlag = True
        
        return allTFiles
    
    
    def makeTData(self,T='all',F='all',M='all',Z='all',C='all'):
        """
        This builds a user specified TData from a session.
        
        Parameters
        ----------
        T,F,M,Z,C : {'all',int,list,str}
            The indices of the data points wrt to the session data. 
            'all' for all, int for one index, list for list of indices 
            or for C you can request one channel or a list of channels by 
            name(s) and for F you can request one field or list of fields by 
            its ID(s).
        
        Returns
        --------
        tdata : TData
            A TData containing the requested data points.
        
        Notes
        ------
        Your request must be ordered, you can't change ordering here. This 
        ultimately is because allowing that would require data from all the 
        different TFiles to be put back together with a much slower and more 
        complex numpy method.
        This is related to an implicit assumption that data extracted from a 
        TFile will form a continuous sequence in the output data along any Q. 
        (Note the data may not, however, originate from continuous sequences 
        of data points within the TFile).
        """

        assert self.tFilesMadeFlag,EM.mt5
        
        # interpret the user input of index selections
        if isinstance(F,str) and F != 'all':
            assert F in self.FieldIDMap,EM.mt0
            F = self.FieldIDMap.index(F)
        if isinstance(C,str) and C != 'all':
            C = genF.chanDic(C)
            _cs = [genF.chanDic(c) for c in self.Chan]
            assert C in _cs,EM.mt1
            C = _cs.index(C)
        if isinstance(F,list):
            for i,f in enumerate(F):
                if isinstance(f,str):
                    assert f in self.FieldIDMap,EM.mt0
                    F[i] = self.FieldIDMap.index(f)
        if isinstance(C,list):
            _cs = [genF.chanDic(c) for c in self.Chan]
            for i,c in enumerate(C):
                if isinstance(c,str):
                    assert c in _cs,EM.mt1
                    C[i] = _cs.index(c)
            
        userSel = [T,F,M,Z,C]
        userSel = [[x] if isinstance(x,int) else x for x in userSel]
        all2Range = lambda p: list(range(p[1])) if p[0]=='all' else p[0]
        userSel = list(map(all2Range, zip(userSel,self.Shape[0:5])))
        dimsU = tuple([len(x) for x in userSel]+[self.NY]+[self.NX])
        
        assert all([Q==sorted(Q) for Q in userSel]),EM.mt2
        
        # from each file load the required data
        dataList = []
        pTFs = []
        for tf in self.TFilesList:
            seshQ = [tf.SeshT,tf.SeshF,tf.SeshM,tf.SeshZ,tf.SeshC]
            # what of user's selection are in this file:
            tfSel = [[q for q in Q if q in S] for Q,S in zip(userSel,seshQ)]
            if not all(tfSel):
                continue
            pTFs.append(tf)
            # where along each seshQ of this file are these user selections:
            tfSelInd = [[S.index(q) for q in Q] for Q,S in zip(tfSel,seshQ)]
            dimsTF = tuple([len(x) for x in tfSel]+[self.NY]+[self.NX])
            prod = product(*tfSelInd)
            with tifffile.TiffFile(tf.TPath) as tif:
                pageIndices = [genF.unravel(*X,*tf.Shape[0:5]) for X in prod]
                _data = tif.asarray(key=pageIndices).reshape(dimsTF)
            dataList.append([_data,tfSel])
        
        # check all the user selection has been retrieved
        # this is probably quite a weak check, just checking the right no. of 
        # images have been loaded
        lenU = np.prod([len(q) for q in userSel])
        lenTFs = sum([np.prod([len(q) for q in d[1]]) for d in dataList])
        # add padding tiles for unequal montage sizes
        # since those obv haven't been retrieved
        lenNonFM = [len(q) for i,q in enumerate(userSel) if i not in [1,2]]
        lenNonFM = np.prod(lenNonFM)
        for f in userSel[1]:
            ny = self.FieldNMYs[f]
            nx = self.FieldNMXs[f]
            lenTFs += lenNonFM*((self.NMX-nx)*self.NMY + (self.NMY-ny)*nx)
        assert lenU==lenTFs,EM.mt3
            
        # now fill in fullData with the bits from different files
        fullData = np.zeros(dimsU,dtype='uint16')
        for d in dataList:
            starts = [UQ.index(Q[0]) for Q,UQ in zip(d[1],userSel)]
            starts = tuple([slice(s,s+len(Q)) for s,Q in zip(starts,d[1])])
            fullData[starts] = d[0]
        return TData(pTFs,fullData,*userSel)
    
     
    def BuildSummary(self):
        
        summary = ''
        summary += 'Name of session: ' + self.Name + '\n'
        summary += 'No. of TFiles in session: '+str(len(self.TFilesList))+'\n'
        summary += 'TFiles in session: \n'
        [os.path.split(TF.TPath)[1]+'\n' for TF in self.TFilesList]
        
        summary += '\nSession channels: '+str(self.Chan)+'\n'
        summary += 'No. of time points: '+str(self.NT)+'\n'
        summary += 'No. of fields: '+str(self.NF)+'\n'
        summary += 'No. of montage tiles: '+str(self.NM)+'\n'
        summary += 'No. of z-slices: '+str(self.NZ)+'\n'
        summary += 'No. of channels: '+str(self.NC)+'\n'
        summary += 'Size in Y: '+str(self.NY)+'\n'
        summary += 'Size in X: '+str(self.NX)+'\n'
        return summary
        
        
    def Summarise(self):
        summary = self.BuildSummary()
        print(summary)
    
    
        
class TFile:
    """ 
    This class represents a tiff file but doesn't contain the image data of 
    the file. It holds information about what the file has inside and what 
    parts of the Session it relates to.
    
    Parameters
    ----------
    ParentSession : Session
        The Session which this tiff file belongs to.
    TFileN : int
        Where in the ParentSession's TFileList you will find this TFile.
    TPath : str
        The file's path.
    SeshQ with Q=T,F,M,Z,C : list of int
        Each is a list of indices which give the positions within the 
        parent Session where the data in the file comes from (along each axis 
        T,F,M,Z and C). I.e. SeshT = [2,3] mean the file contains the 3rd and 
        4th timepoint of the Session.
    NT,NF,NM,NZ,NC,NY,NX : int
        The sizes of each dimensions of the image data inside the file.
    Chan : list of str
        The names of the channels in your TFile.
    FieldIDs : list of str
        The IDs of each field in the file.
        
    Note
    ----
    You generally need to look at all files in a Session to figure out the 
    SeshQ. So TFiles are currently only created by Session.makeTFiles() which 
    does all that search and hands the SeshQ to the __init__. Perhaps in the 
    future it would be useful to be able to hand just the ParentSession and 
    TPath and then the __init__ could calculate SeshQs.
    """
    
    def __init__(
        self,
        ParentSession,
        TFileN,
        TPath,
        SeshT,
        SeshF,
        SeshM,
        SeshZ,
        SeshC,
        NT = None,
        NF = None,
        NM = None,
        NZ = None,
        NC = None,
        NY = None,
        NX = None
    ):
        
        self.ParentSession = ParentSession
        self.TFileN = TFileN 
        self.TPath = TPath 
        self.Chan = [c for i,c in enumerate(ParentSession.Chan) if i in SeshC]
        
        if not all([NT,NF,NM,NZ,NC,NY,NX]):
            nt,nf,nm,nz,nc,ny,nx = fMeta.file2Dims(self.TPath,checkCorrupt=False)
            self.NT = nt
            self.NF = nf
            self.NM = nm
            self.NZ = nz
            self.NC = nc
            self.NY = ny
            self.NX = nx
            self.Shape = (nt,nf,nm,nz,nc,ny,nx)
        else:
            self.NT = NT
            self.NF = NF
            self.NM = NM
            self.NZ = NZ
            self.NC = NC
            self.NY = NY
            self.NX = NX
            self.Shape = (NT,NF,NM,NZ,NC,NY,NX)            
        
        # lists of indices which locate the TFile data within parent session
        self.SeshT = SeshT
        self.SeshF = SeshF
        self.SeshM = SeshM
        self.SeshZ = SeshZ
        self.SeshC = SeshC
        
        self.FieldIDs = [self.ParentSession.FieldIDMap[f] for f in SeshF]
    
    
    def makeTData(self,T='all',F='all',M='all',Z='all',C='all'):
        """ This method creates a specific TData from the TFile.
        
        Parameters
        -----------
        Q : list or int or 'all' or str
            For Q = T,F,M,Z,C, these are the indices of the images you want to 
            take from the TFile along each axis. Either a single index (int) 
            or a list or just 'all' data points. With the channel axis you can 
            name the channel you want with a 'str'.
        """
                  
        # first interpret the user input of index selections
        if isinstance(F,str) and F != 'all':
            assert F in self.FieldIDMap,EM.mt0
            F = self.FieldIDMap.index(F)        
        if isinstance(C,str) and C != 'all':
            C = genF.chanDic(C)
            _cs = [genF.chanDic(c) for c in self.Chan]
            assert C in _cs,EM.mt1
            C = _cs.index(C)
        userSel = [T,F,M,Z,C]
        userSel = [[x] if isinstance(x,int) else x for x in userSel]
        # an f() to replace occurences of 'all' with a list of all indices
        all2Range = lambda p: list(range(p[1])) if p[0]=='all' else p[0]        
        # convert occurences of 'all' -> list of all indices
        userSel = list(map(all2Range, zip(userSel,self.Shape[0:5])))
        
        NQ = [self.NT,self.NF,self.NM,self.NZ,self.NC]
        for Q,n in zip(userSel,NQ):
            for q in Q:
                assert q in range(n),EM.mt4
        
        # make an itertools product of the user selected indices
        prod = product(*userSel)
        with tifffile.TiffFile(self.TPath) as tif:        
            pageIndices = [genF.unravel(*X,*self.Shape[0:5]) for X in prod]
            data = tif.asarray(key=pageIndices)
        
        dims = tuple([len(x) for x in userSel]+[self.NY]+[self.NX])
        data.shape = dims
        
        allSQ = [self.SeshT,self.SeshF,self.SeshM,self.SeshZ,self.SeshC]
        seshQ = [[SQ[q] for q in Q] for Q,SQ in zip(userSel,allSQ)]
        
        return TData([self],data,*seshQ)
        
        
    def BuildSummary(self):
        mb = self.ParentSession.MadeBy
        summary = ''
        summary += 'TFile name: '
        summary += genF.stripTags(os.path.split(self.TPath)[1],mb)+'\n'
        summary += 'From session: ' + self.ParentSession.Name + '\n'
        summary += 'TFile path: '+ self.TPath+'\n\n'
        summary += 'No. of time points: '+str(self.NT)+'\n'
        summary += 'No. of fields: '+str(self.NF)+'\n'
        summary += 'No. of montage tiles: '+str(self.NM)+'\n'
        summary += 'No. of z-slices: '+str(self.NZ)+'\n'
        summary += 'No. of channels: '+str(self.NC)+'\n'
        summary += 'Size in Y: '+str(self.NY)+'\n'
        summary += 'Size in X: '+str(self.NX)+'\n'
        return summary
        
        
    def Summarise(self):
        summary = self.BuildSummary()
        print(summary)
    

class TData:
    """ This class holds the actual image data numpy array of dtype uint16.
    So these are the only objects in this package which take a lot of memory.
    The dimension ordering is always: 
    (times,fields,montages,zslices,channels,ypixels,xpixels)
    Generally a TData is made by TFile.makeTData() or Session.makeTData()
    
    Parameters
    ----------
    ParentTFiles : list of TFiles
        The TFiles used to derive this TData.
    ParentSession : xfold.Session object
        The Session that the TData is derived from.
    data : 7D numpy array
        The image data as uint16 numpy array.
    SeshQ : list 
        For Q=T,F,M,Z and C. These are the indices in the Session that the 
        data corresponds to. They are lists containing all the indices.
    FieldIDs : list of str
        The ID for each field in the data.
    """
    
    def __init__(
        self,
        ParentTFiles,
        data,
        SeshT,
        SeshF,
        SeshM,
        SeshZ,
        SeshC
    ):
        
        self.ParentTFiles = ParentTFiles
        self.ParentSession = ParentTFiles[0].ParentSession
        self.ParentXFold = self.ParentSession.ParentXFold
        self.data = data
        self.Shape = None
        self.updateDimensions() # sets NT,NF,NM,NZ,NC,NY,NX,Shape
        self.pixSizeY = self.ParentSession.pixSizeY
        self.pixSizeX = self.ParentSession.pixSizeX
        self.pixUnit = self.ParentSession.pixUnit

        self.SeshT = SeshT
        self.SeshF = SeshF
        self.SeshM = SeshM
        self.SeshZ = SeshZ
        self.SeshC = SeshC        
        
        C = self.ParentSession.Chan
        self.Chan = [c for i,c in enumerate(C) if i in self.SeshC]
        self.Chan = [genF.chanDic(c) for c in self.Chan]
        self.startChan = tuple(self.Chan)
         
        self.FieldIDs = [self.ParentSession.FieldIDMap[f] for f in self.SeshF]
        
        # if you alignExtract() you use a template for each field and
        # pad all fields to the biggest template so that they can still be
        # put in one np array. This records if you did that for future methods
        self.TemplatePadDic = {}
    
    
    def updateDimensions(self):
        """This updates the record of the dimensions of the TData according
        to the shape that numpy finds. This shape is already the one we want
        because makeTData() does it for us.
        """
        dims = self.data.shape
        self.NT = dims[0]
        self.NF = dims[1]
        self.NM = dims[2]
        self.NZ = dims[3]
        self.NC = dims[4]
        self.NY = dims[5]
        self.NX = dims[6]
        self.Shape = dims
    

    def TakeSubStack(self,T='all',F='all',M='all',Z='all',C='all'):
        """ 
        This method takes subsections of dimensions of the TData.
        The selection is wrt the TData, i.e. nothing to do with the session.
        
        Parameters
        ----------
        Q : 'all' or list or int
            Q represents any dimension. Either you take all, provide 
            list of indices to take or an int for the one index to take.
            C can be a channel name.
            
        Notes
        -------
        The way we do the actual selection from self.data is stupid! There's 
        definitely much better ways to do it using np.ravel, product etc 
        (see makeTData) but don't care for now.
           
        """
                  
        # interpret the user input of index selections
        if isinstance(C,str) and C != 'all':
            C = genF.chanDic(C)
            assert C in self.Chan,EM.mt1b
            C = self.Chan.index(C)
        userSel = [T,F,M,Z,C]
        userSel = [[x] if isinstance(x,int) else x for x in userSel]
        all2Range = lambda p: list(range(p[1])) if p[0]=='all' else p[0]        
        userSel = list(map(all2Range, zip(userSel,self.Shape[0:5])))
        
        # make date selection
        self.data = self.data[userSel[0]].copy()
        self.data = self.data[:,userSel[1]].copy()
        self.data = self.data[:,:,userSel[2]].copy()
        self.data = self.data[:,:,:,userSel[3]].copy()
        self.data = self.data[:,:,:,:,userSel[4]].copy()
        
        # update everything
        self.updateDimensions()
        self.SeshT = [self.SeshT[q] for q in userSel[0]]
        self.SeshF = [self.SeshF[q] for q in userSel[1]]
        self.SeshM = [self.SeshM[q] for q in userSel[2]]
        self.SeshZ = [self.SeshZ[q] for q in userSel[3]]
        self.SeshC = [self.SeshC[q] for q in userSel[4]]
        self.FieldIDs = [self.FieldIDs[q] for q in userSel[1]]
        self.Chan = [self.Chan[c] for c in userSel[4]]
        

    def MatchChannels(self,endChans,verbose=False):
        """ 
        Matches tdata channels (as well as ordering) to the user provided 
        tuple of channels. Will add blanks images for channels that are in 
        endChans but not in the data.
        
        Parameter
        ---------
        endChans : tuple or None or 'Auto'
            Output data will have these channels. If None or 'Auto' then it 
            will get set of all channels that appear in all sessions and order 
            according to XFold.chanOrder.
        """
        if np.prod(np.array(self.Shape))==0:
            return
        
        if endChans == None or endChans == 'Auto':
            pxfold = self.ParentXFold
            allSesh = [c for s in pxfold.SessionsList for c in s.Chan]
            endChans = set(allSesh)
            endChans = [genF.chanDic(c) for c in endChans]
            # sort them according to class variable chanOrder
            endChans = sorted([[XFold.chanOrder[c],c] for c in endChans])
            endChans = tuple([j for i,j in endChans])
        
        if verbose:
            print(endChans)
        
        # first add a blank channel at the end of the channels
        padTuple = ((0,0),(0,0),(0,0),(0,0),(0,1),(0,0),(0,0))
        self.data = np.pad(self.data,padTuple)
        # make foundChan list: position of endChan in self.chan
        foundChan = []
        for endChan in endChans:
            if endChan in self.Chan:
                foundChan.append(self.Chan.index(endChan))
            else: 
                foundChan.append(-1)
                
        # reorder tifdata channels according to foundChannels
        self.data = self.data[:,:,:,:,foundChan,:,:].copy()
        
        self.Chan = list(endChans)
        self.updateDimensions()
        self.SeshC = [None if c==-1 else c for c in foundChan]
        
                
    def DownSize(self,downsize=None,verbose=False):
        """
        Reduces downsizes the image data in x and y.
        
        Parameters
        ----------
        downsize : int or list
            If int then downsize x and y by this factor.
            If list [y,x] then downsize by different factors y and x.
        """
        if downsize==1 or downsize==[1,1]:
            downsize = None
        if np.prod(np.array(self.Shape))==0 or not downsize:
            return
        
        if isinstance(downsize,int):
            downsize = [downsize,downsize]
        
        self.data = downscale_local_mean(self.data,(1,1,1,1,1,*downsize))
        self.data = self.data.astype('uint16')
        
        self.updateDimensions()
        self.pixSizeY = self.pixSizeY/downsize[0]
        self.pixSizeX = self.pixSizeX/downsize[1]
        
        if verbose:
            print('Downsized by: ',str(downsize))

            
    def EmptyQ(self):
        """Return True for all 0 value pixels or no pixels, False otherwise."""
        if np.prod(np.array(self.Shape))==0:
            return True
        else:
            return not self.data.any()
        
                
    def DeleteEmptyT(self,verbose=False):
        """Delete any time points that don't contain data
        """
        
        if np.prod(np.array(self.Shape))==0:
            return        
        
        # find which time points have anything other than all zeros:
        nonEmpT = [self.data[t].any() for t in range(self.NT)]
        self.data = self.data[nonEmpT].copy()
        
        # update Session records of blank time points
        empSeshT = [self.SeshT[t] for t in range(self.NT) if not nonEmpT[t]]
        self.ParentSession.BlankTimePoints += empSeshT
        
        self.updateDimensions()
        self.SeshT = [x for x,q in zip(self.SeshT,nonEmpT) if q]
        
        if verbose:
            print('deleted empty time points')
        
        
    def Homogenise(self,HFiles={},chan='All',verbose=False):
        """
        This corrects for inhomogenous field of view sensitivities by 
        subtracting a provided 'dark field' image and dividing by a provided 
        'flat field' image.
        
        Parameters
        -----------
        HFiles : str or dict
            The locations of the images used for homogenisation. See 
            XFold.buildHomogFilts() for format. If empty list then it will 
            look to XFold.HomogFiltDic.
        chan : 'All' or list of ints or str
            If 'All' then all channels will be homogenised. If list then the 
            ints or str provide which channels to homogenise.
            
        Notes
        -----
        It will fail if the filters are not the same size as the TData so you 
        have to downsize your filters if you have downsized your TData etc.
        """  
        
        if np.prod(np.array(self.Shape))==0:
            return        
        
        assert HFiles or self.ParentXFold.HomogFiltDic,EM.hf1
        
        if not HFiles:
            HFilts = self.ParentXFold.HomogFiltDic
        else:
            HFilts = {}
            if isinstance(HFiles,str):
                if not os.path.split(HFiles)[0]:
                    HFiles = os.path.join(self.ParentXFold.XPathP,HFiles)
                fps = os.listdir(HFiles)
                HF = ['_FF.tif','_DF.tif']
                hNames = [c+f for c in XFold.chanOrder.keys() for f in HF]
                for h in hNames:
                    if h in fps:
                        if h[:-7] not in HFilts.keys():
                            HFilts[h[:-7]] = {}
                        im = io.imread(os.path.join(HFiles,h)).astype('float32')
                        HFilts[h[:-7]][h[-6:-4]] = im
            elif isinstance(HFiles,dict):
                for k,v in HFiles.items():
                    if k not in HFilts.keys():
                        HFilts[k] = {}                    
                    for k2,v2 in HFiles[k].items():
                        if isinstance(v2,str):
                            im = io.imread(v2).astype('float32')
                            HFilts[k][k2] = im
                        elif isinstance(v2,np.ndarray):
                            HFilts[k][k2] = v2
                        else:
                            raise Exception('HFiles format not correct.')
            else:
                raise Exception('HFiles must be a str or dict')
        
        if isinstance(chan,str) and chan!='All':
            chan = [chan]
        if chan=='All':
            chan = [i for i in range(len(self.Chan))]
        elif isinstance(chan,list):
            if all([isinstance(c,str) for c in chan]):
                chan = [self.Chan.index(c) for c in chan]
            elif not all([isinstance(c,int) for c in chan]):
                raise Exception('chan not in recognisable format.')
        else:
            raise Exception('chan not in recognisable format.')
        
        
        for c in chan:
            C = self.Chan[c]
            if C not in HFilts.keys():
                raise Exception(f'No filter found for {C} channel.')
            elif 'FF' not in  HFilts[C].keys():
                raise Exception(f'No FF filter found for {C} channel.')
            elif HFilts[C]['FF'].shape!=(self.NY,self.NX):
                raise Exception('Filter doesn\'t match the data shape.')
            elif 'DF' in HFilts[C].keys():
                if HFilts[C]['DF'].shape!=(self.NY,self.NX):
                    raise Exception('Filter doesn\'t match the data shape.')

        # loop over image in self.data
        dims = [self.NT,self.NF,self.NM,self.NZ,self.NC]
        ranges = map(range,dims)
        for t,f,m,z,c in product(*ranges):
            if c not in chan: # skip if this isn't a chosen channel
                continue
            C = self.Chan[c]
            # create a float32 of just that one image for division:
            _data = self.data[t,f,m,z,c].astype('float32')
            if 'DF' in HFilts[C].keys():
                _data = _data - HFilts[C]['DF']
                _data[_data<0] = 0 # otherwise negative gives overflow problem!
                _data = _data/HFilts[C]['FF']
            else:
                _data = _data/HFilts[C]['FF']
            # add to count if >=1 pix has become bigger than UINT16MAX
            self.ParentXFold.HomogOverflow[0] += 1
            if _data.max() > self.ParentXFold.UINT16MAX:
                self.ParentXFold.HomogOverflow[1] += 1
            # convert back to uint16 to put in self.data
            self.data[t,f,m,z,c] = _data.astype('uint16')
            del _data
        
        if verbose:
            print('homogenised')
 

    def zProject(self,meth='maxProject',downscale=None,verbose=False,
                 slices=1,fur=False):
        """This does z-projection of the data.
        
        Parameters
        ----------
        meth : {'maxProject', 'avProject','minProject',
                'signalDetect'}
            basic ones: maxProject,avProject,minProject
            Or it can do a fancy one that finds the layer with most features.
        downscale : int
            Just used if meth=signalDetect - how much to downscale the images 
            by when calculating which slices have signal... svaes lots of time.
        slices : int
            How many slices to return in the signalDetect method.
        fur : bool
            Whether to return the slice furthest from the signal (e.g. for 
            pulling out a background measure).
        """
        if np.prod(np.array(self.Shape))==0 or self.NZ==1:
            return        
        dims = (self.NT,self.NF,self.NM,1,self.NC,self.NY,self.NX)
        _data = np.zeros(dims,dtype='uint16')
        
        ranges = map(range,[self.NT,self.NF,self.NM,self.NC])
        # method1: maximum projection
        if meth == 'maxProject':
            for t,f,m,c in product(*ranges):
                _data[t,f,m,0,c] = maxProj(self.data[t,f,m,:,c])
        # method2: the signal detection one I made:
        elif meth == 'signalDetect':
            assert isinstance(downscale,int),EM.zp1
            p = self.pixSizeX
            for t,f,m,c in product(*ranges):
                _data[t,f,m,0,c] = signalProj(self.data[t,f,m,:,c],
                                              p,
                                              downscale,
                                              slices,
                                              proj=True,
                                              furthest=fur)
        elif meth == 'avProject':
            for t,f,m,c in product(*ranges):
                _data[t,f,m,0,c] = avProj(self.data[t,f,m,:,c])            
        elif meth == 'minProject':
            for t,f,m,c in product(*ranges):
                _data[t,f,m,0,c] = minProj(self.data[t,f,m,:,c]) 
        else:
            raise Exception('z-project method not recognised')
            
        self.data = _data.copy()
        del _data
        self.updateDimensions()
        self.SeshZ = [None]
        
        if verbose:
            print('z-projected')

    
    def LocalIntensity(self,downscale=False,radius=40,mode='step'):
        """
        This replaces each pixel by the average value of the surrounding 
        region.
        
        Parameters
        ----------
        downscale : int
            Factor to downscale everything first to speed up. (It will be 
            resized to original size).
        radius : int
            The radius of the structure element in um.
        
        """
        if np.prod(np.array(self.Shape))==0:
            return
        
        if downscale:
            radius = np.ceil(radius/(self.pixSizeY*downscale))
        else:
            radius = np.ceil(radius/(self.pixSizeY))
        selem = disk(radius)
        
        for f in range(self.NF):
            _,(pt,b,l,r) = genF.removePads(self.data[0,f,0,0,0],retPad=True)
            
            dims = (self.NT,self.NM,self.NZ,self.NC)
            ranges = map(range,dims)
            for t,m,z,c in product(*ranges):
                data = self.data[t,f,m,z,c,pt:self.NY-b,l:self.NX-r]
                if downscale:
                    data = downscale_local_mean(data,(downscale,downscale))
                if mode=='step':
                    data = generic_filter(data,
                                          lambda x:np.mean(x),
                                          footprint=selem,
                                          mode='reflect')
                elif mode=='gaussian':
                    data = gaussian_filter(data,radius)
                else:
                    raise Exception('Unrecognised mode')
             
                if downscale:
                    resize(data,(self.NY-pt-b,self.NX-l-r))
                self.data[t,f,m,z,c] = np.pad(data,((pt,b),(l,r)))


    def Rotate(self,degree):
        """
        This rotates all the images in a TData. It doesn't change the size of 
        the image to account for the rotation. Uses fast open cv.
        
        Parameters
        -----------
        degree : float
            The degrees rotation clockwise that you want to apply.
        """
        sh = (self.NT,self.NF,self.NM,self.NZ,self.NC,self.NY,self.NX,)
        sh1 = (self.NX,self.NY)
        image_center = (self.NX/2,self.NY/2)
        M = cv.getRotationMatrix2D(image_center,degree,1)
        lenDat = self.NT*self.NF*self.NM*self.NZ*self.NC
        sh2 = (self.NX,self.NY,lenDat)
        self.data = np.moveaxis(np.moveaxis(self.data,5,0),6,0).reshape(sh2)
        
        _data = []
        for i in range(lenDat//512):
            _data.append(cv.warpAffine(self.data[:,:,i*512:(i+1)*512],M,sh1))
        _data.append(cv.warpAffine(self.data[:,:,(lenDat//512)*512:],M,sh1))
        self.data = np.concatenate(_data,axis=2)
        self.data = np.moveaxis(np.moveaxis(self.data,1,-1),0,-1).reshape(sh)
        
    
    def Reflect(self,reflectX=False,reflectY=False):
        if reflectX:
            self.data = np.flip(self.data,axis=6)
        if reflectY:
            self.data = np.flip(self.data,axis=5)
        
        
    def StitchIt(self,method='',returnCens=False,cens=None,verbose=False):
        """ 
        Stitches together grid-like montage tiles in axis 2 of the TData.
        
        Parameters
        ----------
        method : str
            Put 'noAlign' to use guess from metadata instead of 
            cross-correlation.
        returnCens : bool
            Whether to return the centres that you found so they can be used 
            on another equivalent TData.
        cens : list of numpy.ndarray
            centres found previously to use instead of doing the search.
        
        Notes
        -----
        The parameters you give find here are in the form: 
        [threshold,ampPower,maxShiftFraction,boxsize,sdt]
        
        threshold - it searches for signal and does 'auto' aligning if 
                    not enough. This threshold defines 'enough signal'
        ampPower - the image is raised to this power at somepoint to 
                    amplify signal could increase for increase sensitivity?
        maxShiftFraction - maximum detected that is applied, as a fraction of
                            image size b/c if a big shift is detected it is
                            probably wrong if detected shift is bigger it does 
                            'auto' aligning
        boxsize - size of the box (in pixels) used in measuring 
                    signal with sobel
        sdt - standard dev of gaussian blur applied during 
                signal measuring
        minSize - for images smaller than this it won't do cross-correlation
                    alignment because the small size risks stupid results.
                    
        Since we are finding the best alignments for each tile, we may end up 
        with different sized images, both in the TData and across the whole 
        XFold. To avoid this the stitch functions does padding and/or cropping 
        to the final image so that you can define beforehand what size output 
        you want. To give the same size across a whole XFold, this looks to 
        the parent XFold to define final size.
        """
        
        if self.NM==1 or np.prod(np.array(self.Shape))==0:
            return
        
        # find if TData has been downsized to help define final size
        NY = self.ParentSession.NY
        NX = self.ParentSession.NX
        downX = round(NX/self.NX)
        downY = round(NY/self.NY)
        
        # decide what the output size will be
        # get all the values we need from all sessions in the XFold
        sessionsList = self.ParentXFold.SessionsList
        allOverlaps = [s.MOlap for s in sessionsList]
        allNY = [s.NMY for s in sessionsList]
        allNX = [s.NMX for s in sessionsList]
        allSizeY = [s.NY/downY for s in sessionsList]
        allSizeX = [s.NX/downX for s in sessionsList]
        # zip all these together
        allZipY = zip(allOverlaps,allNY,allSizeY)
        allZipX = zip(allOverlaps,allNX,allSizeX)
        
        # the size in x or y, call it q, would be given by:
        # (no. of tiles in Q)*(no. of pixels in Q) - overlapping part
        # with overlapping part given by: (N tiles - 1)*(N pixels)*overlap
        # we divide the overlap by 2 to give a number that is an overestimate
        # i.e. we hope we will always have some black padding at the edges:
        ySizeOut = [NMY*NY-(NMY-1)*NY*OL/2 for OL,NMY,NY in allZipY]
        xSizeOut = [NMX*NX-(NMX-1)*NX*OL/2 for OL,NMX,NX in allZipX]
        
        # we expect these to all be the same
        if len(set(ySizeOut)) != 1 or len(set(xSizeOut)) != 1:
            self.ParentXFold.Warnings.append(EM.si1)
        ySizeOut = int(max(ySizeOut))
        xSizeOut = int(max(xSizeOut))
        shapeOut = (ySizeOut,xSizeOut)
        
        # parameters to send to findCentres() (see __doc__)
        threshold = 0.04
        ampPower = 3
        maxShiftFraction = 0.1
        boxsize = 70
        sdt = 4
        minSize = 150
        cnts = self.ParentXFold.StitchCounts
        pars = [threshold,ampPower,maxShiftFraction,boxsize,sdt,minSize,cnts]
        
        # print a warning if we are skipping alignment due to small tiles
        if self.NY<minSize or self.NX<minSize:
            self.ParentXFold.Warnings.append(EM.si2 % minSize)
        
        xMon = self.ParentSession.NMX
        yMon = self.ParentSession.NMY
        olap = self.ParentSession.MOlap

        # reorder M-axis if it's not the normal LRUP ordering
        if self.ParentSession.MontageOrder == 'UDRL':
            reshape = genF.UDRL2LRUD(list(range(self.NM)),yMon,xMon)
            self.data = self.data[:,:,reshape]
        
        # only want to align using these channels
        # i.e. no BF because cross-correlation doesn't work well
        fluoChans = ['YFP','CFP','RFP','GFP','FR','DAPI']
        # remove possible blank channels added by matchChannels
        fluoChans = [c for c in fluoChans if c in self.startChan]
        aCh = []
        for c in fluoChans:
            if c in self.Chan:
                aCh.append(self.Chan.index(c))
        if aCh==[]:
            self.ParentXFold.Warnings.append(EM.si3)
            method += 'noAlign'
            aCh.append(0)
        
        # initiate arrays to send to findCentres
        # sigIms is zproj of is 1 time, 1 field and only chans of aCh
        # also centreLists storage array: one list (len=NM) for each t,f-point
        sigDims = (self.NM,len(aCh),self.NY,self.NX)
        sigIms = np.zeros(sigDims,dtype='uint16')
        cenListsTF = np.zeros((self.NT,self.NF,self.NM,2),dtype='uint16')
        
        # build new sigIm for each t,f-point,
        if isinstance(cens,np.ndarray):
            cenListsTF = cens.copy()
        else:
            ranges = map(range,[self.NT,self.NF])
            for t,f in product(*ranges):
                for c in range(len(aCh)):
                    sigIms[:,c] = self.data[t,f,:,:,aCh[c]].copy().max(axis=1)
                cenListsTF[t,f] = findCentres(sigIms,xMon,olap,method,pars)
            del sigIms
            
        # initiate data for storage of final assemblies
        dims = (self.NT,self.NF,1,self.NZ,self.NC,ySizeOut,xSizeOut)
        _data = np.zeros(dims,dtype='uint16')
        
        # now assemble montages
        ranges = map(range,[self.NT,self.NF,self.NZ,self.NC])
        for t,f,z,c in product(*ranges):
            _data2 = self.data[t,f,:,z,c].copy()
            _data[t,f,0,z,c] = noMergeStitch2(_data2,cenListsTF[t,f],
                                              shapeOut,xMon)
            del _data2
        
        self.data = _data.copy()
        del _data
        self.updateDimensions()
        self.SeshM = [None]
        if verbose:
            print('stitched')
        if returnCens:
            return cenListsTF
        
        
    def LabelVideo(self,roundM=30,verbose=False):
        """This function adds time labels to the data.
            
        roundM is the minute interval that it will round to.
        """
        
        # if 1 of dim sizes is zero then there's no data, so return
        if np.prod(np.array(self.Shape))==0:
            return        
        
        pSesh = self.ParentSession
        pXFold = self.ParentXFold
        
        assert pXFold.StartTimes,EM.la1
        
        # you need a new blank channel for the label to go in:
        padDims = ((0,0),(0,0),(0,0),(0,0),(0,1),(0,0),(0,0))
        self.data = np.pad(self.data,padDims)
        # update attributes
        self.Chan.append('Label')
        self.NC += 1
        self.SeshC.append(None)
                    
        # find time since field's experiment started for all t and f of 
        # data. f nested within t to make a list of lists of timedeltas
        tStrings = []
        for i,t in enumerate(self.SeshT):
            tStrings.append([])
            for iF in range(self.NF):
                
                # find the moment when frame was taken:
                frameTakenMom = pSesh.StartMom + pSesh.TStep*t
                # get the start time from StartTimes
                fieldStartMom = pXFold.StartTimes[self.FieldIDs[iF]]
                
                # this is the time we want to print on the image:
                tSinceFdStart = frameTakenMom - fieldStartMom
                tSinceFdStart = moment2Str(tSinceFdStart,roundM)
                tStrings[i].append(tSinceFdStart)
         
        # add the time string to the label channel:
        dims = [self.NT,self.NF,self.NM,self.NZ]
        ranges = map(range,dims)
        for t,f,m,z in product(*ranges):
            addTimeLabel(self.data[t,f,m,z,-1],tStrings[t][f])
        
        if verbose:
            print('labeled')
    
    
    def AlignExtract(self,templateDic,deltaAng=0.25,clip=False,maxAng=15,
                     manualScale=False,storedAlignments=False,verbose=False):
        """
        This does cross-correlation template matching to extract the regions 
        of your data corresponding to templates that you give it. The 
        templates should be rectanglular maximum projected BF images of the 
        original data, i.e. it will pull the max-projected BF image from the 
        TData to match against. The template may be rotated with respect to 
        the original data.
        
        Parameters
        ----------
        templateDic : str or dict
            If string then it must be a path to a folder containing the 
            template images saved as tifs. String with only one level of path 
            is interpreted as a directory within the parent of XPath. The 
            images must be in subdirectories for each field with name 
            'Exp'+fieldID. If dict then it must be a dictionary with 
            {fieldID : path to tif}.
        deltaAng : float
            The size of the steps in angle that it tests, in degrees.
        clip : bool or int
            Whather to clip the template intensity values to avoid problems 
            with bright spots. E.g. clip=90 will clip values above 90% of the 
            max.
        maxAng : float
            The maximum rotation that it will apply in the search, in degrees. 
            It will apply this angle in +ve and -ve directions.
        manualScale : int or list of ints
            If TData has been downscaled you must provide this to downscale 
            the template before cross-correlation. If int the it will 
            downscale by (int,int).
        storedAlignments : bool or str
            Whether to use use alignments stored in filepath storedAlignments 
            instead of doing the whole calculation. If not False then it will 
            also save alignments it does calculate to this file.
        
        Notes
        -----
        For best results you must of course have processed the templates 
        exactly as you have processed the TData.
        
        If the template size varies between fields then a global (i.e. the 
        same for entire XFold) output size will be determined and all 
        extract will be padded to this size. This avoids problems of jagged 
        arrays for TDatas containing multiple fields.
        """
        assert isinstance(clip,bool) or isinstance(clip,int),EM.ae0
        
        pXFold = self.ParentXFold

        if manualScale:
            if isinstance(manualScale,int):
                manualScale = tuple([manualScale,manualScale])
            if isinstance(manualScale,list):
                manualScale = tuple(manualScale)
        
        if np.prod(np.array(self.Shape))==0:
            return        
        assert self.NM==1,EM.ae6
        
        # package these to not bloat code
        ps = (deltaAng,maxAng)
        
        # load storedAlignments and build alignDic
        if storedAlignments:
            self.ParentXFold.buildStoredAlignments(storedAlignments)
            alignDic = self.ParentXFold.AlignDic[storedAlignments]
            
        # make templateDic
        if isinstance(templateDic,str):
            self.ParentXFold.buildTemplates(templateDic)
            templateDic = self.ParentXFold.TemplateDic[templateDic].copy()
        
        for FID in self.FieldIDs:
            assert FID in templateDic.keys(),EM.ae3
        
        # first find the max y and max x size of all templates
        maxYSize = []
        maxXSize = []
        for k,tem in templateDic.items():
            # downscale template if needed
            if manualScale:
                templateDic[k] = downscale_local_mean(tem,manualScale)
            ysizeT,xsizeT = templateDic[k].shape
            maxYSize.append(ysizeT)
            maxXSize.append(xsizeT)
        maxYSize = max(maxYSize)
        maxXSize = max(maxXSize)
        
        shapeMx = (maxYSize,maxXSize)
        
        dims = (self.NT,self.NF,1,self.NZ,self.NC,maxYSize,maxXSize)
        _data = np.zeros(dims,dtype='uint16')
        
        # cycle over field and then times because each field has a 
        # different template to be loaded and each time needs aligning 
        for i,f in enumerate(self.SeshF):
            template = templateDic[self.FieldIDs[i]]
            shape = template.shape
            assert shape[0]<self.data.shape[5],EM.ae8
            assert shape[1]<self.data.shape[6],EM.ae8
            
            if 'BF' in self.Chan:
                BFIndex = self.Chan.index('BF')
            else:
                BFIndex = None
            
            for t in range(self.NT):
                code = 'S'+str(self.ParentSession.SessionN)
                code += 'T'+str(self.SeshT[t])+'F'+str(f)
                if storedAlignments and code in alignDic.keys():
                    qs = alignDic[code]
                    if verbose:
                        print('found stored alignment: ',code)
                else:
                    # make max projection of chan BF to do the search in
                    assert BFIndex, EM.ae4
                    BFZProj = self.data[t,i,0,:,BFIndex].copy().max(axis=0)
                    BFZProj = BFZProj.astype('float32')
                    if clip:
                        if isinstance(clip,int):
                            maxP = clip
                        else:
                            maxP = 90
                        maxV = np.percentile(np.ravel(BFZProj),maxP)
                        BFZProj[BFZProj>maxV] = maxV
                        template[template>maxV] = maxV
                    ang,shift = findRegion(BFZProj,template,*ps)
                    qs = (ang,shift)
                    if storedAlignments:
                        line = '\n'+code+' : '+str(ang)+' '+str(shift[0])
                        line += ' '+str(shift[1])
                        with open(storedAlignments,'a') as file:
                            file.write(line)    
                _data[t,i] = extractRegion(self.data[t,i],*qs,*shape,*shapeMx)
                        
            # record in the TData that extraction from this template was padded
            pad = [a-b for a,b in zip(shapeMx,shape)]
            self.TemplatePadDic[self.FieldIDs[i]] = pad
        
        self.data = _data.copy()
        del _data
        self.updateDimensions()
    
    
    def ManualAlignExtract(self,al,dep,endLen=None,dil=[0,0],
                           storedAlignments=False):
        """
        This extracts a rectangular region from the TData according to two 
        points (which mark the top edge) and a provided region depth. The 
        rectangle does not have to be aligned with the image axes.
        
        Parameters
        ----------
        
        al : [[int_y0,int_x0],[int_yf,int_xf]]
            The points must mark the top two corners of the rectangle that 
            you want to extract.
        dep : int
            You are only marking the top line of the rectangle that you want 
            to extract so this gives the length of the region perpendicular 
            to the line.
        endLen : int (optional)
            The line can be shortened to this many pixels in length. This is 
            used to ensure all images are the same size when extracting from 
            many related images. 
        dil : [y_int,x_int]
            The number of pixels you want to dilate the extraction by. I.e. to 
            extract more that the rectangle you have marked. Gives number in 
            y-direction and x, respectively. This is additional to endLen.
            
        Notes
        ------
        Remember you must have marked the points on a tif which has been 
        processed exactly as you are processing during the extraction.
        
        Also, unlike most methods in this package, this method only works on 
        TDatas with one field, so processing must be done in the script 
        outside our package.
        """  
        y0,x0,yf,xf = [x for p in al for x in p]
        if not endLen:
            endLen = math.sqrt((xf-x0)**2 + (yf-f0)**2)
        ang = math.atan((yf-y0)/(xf-x0))
        ang = (ang/math.pi)*180
        
        TL = rotCoord_NoCrop(al[0],self.NY,self.NX,ang)
        NIms = self.NT*self.NF*self.NM*self.NZ*self.NC
        newD = (NIms,self.NY,self.NX)
        self.data = rotate_image(np.moveaxis(self.data.reshape(newD),0,-1),ang)
        h,w = self.data.shape[0:2]
        self.data = np.moveaxis(self.data,-1,0).reshape(self.Shape[0:5]+(h,w))
        xslice = slice(TL[1]-dil[1],TL[1]+endLen+dil[1],1)
        yslice = slice(TL[0]-dil[0],TL[0]+dep+dil[0],1)
        self.data = self.data[:,:,:,:,:,yslice,xslice]
        
        self.updateDimensions()
        
    
    def SaveData(self,outDir,overwrite=False,verbose=False):
        """
        This takes the image data from your TData and saves it such that 
        image j will be able to open it and have all the channel and 
        hyperstack info it needs.
        
        It ALWAYS separates fields into different files and folders, with the 
        folders named ExpFID where FID is the field ID.
        
        Parameters
        ----------
        outDir : str
            Where to put the data you save. XFold.OutDirSig is prefixed to new 
            directory. A path with just one level is interpreted as the folder 
            name within the XPath parent directory.
            You can give it a dictionary of outDirectories which gives 
            the path for each field. 
            
        Notes
        -----
        It strips old tags from the file name and adds new tags to
        all names. We have our own tag system, _s000N_t000M for the session 
        the data comes from and the time point relative to that session.
        """

        if np.prod(np.array(self.Shape))==0:
            return        
        
        xSig = XFold.OutDirSig 
        
        if isinstance(outDir,str):
            if os.path.split(outDir)[0]:
                parnt = os.path.split(outDir)[0]
                analPath = os.path.join(parnt,xSig+os.path.split(outDir)[1])
            else:
                analPath = os.path.join(self.ParentXFold.XPathP,xSig+outDir)
        else:
            raise Exception('You must provied an outDir.')
        
        if not os.path.exists(analPath):
            os.makedirs(analPath)        
        
        for i,f in enumerate(self.SeshF):
            
            fieldDir = XFold.FieldDir+self.FieldIDs[i]
            outDirPath = os.path.join(analPath,fieldDir)
                      
            if not os.path.exists(outDirPath):
                os.mkdir(outDirPath)
            
            # make the filename you will use to save, adding the required tags
            tpath = self.ParentTFiles[0].TPath
            mb = self.ParentSession.MadeBy
            strippedName = genF.stripTags(os.path.split(tpath)[1],mb)
            sessionN = self.ParentSession.SessionN
            sessionTag = '_s' + str(sessionN).zfill(4)
            timeTag = '_t' + str(self.SeshT[0]).zfill(4)
            tags = sessionTag + timeTag
            outName = strippedName + tags + '.tif'
            outPath = os.path.join(outDirPath,outName)   
            
            seshQ = [self.SeshT,[f],self.SeshM,self.SeshZ,self.SeshC]
            genF.saveTiffForIJ(outPath,self.data[:,[i]],self.Chan,seshQ)
            
            self.ParentXFold.SavedFilePaths.append(outPath)
            
        return
    
    
    def SwapXYZ(self,axisA,axisB):
        """ This can be used for swapping the XYZ axes around
        """
        # don't allow swapping of anything except XYZ for now:
        permittedAxes = [3,5,6]
        if axisA not in permittedAxes or axisB not in permittedAxes:
            errMess = 'You can only use SwapXYZ() to swap axes'\
                        '{permittedAxes}.'
            raise Exception(errMess.format(permittedAxes=permittedAxes))
        
        # do the swap
        self.data = np.swapaxes(self.data,axisA,axisB)
        
        self.updateDimensions()
        if axisA == 3 or axisB ==3:
            self.SeshZ = [None for z in range(self.NZ)]
        
    
    def TakeXYSection(self,Xi,Xf,Yi,Yf):
        """ This takes a basic rectangular section in XY of your data. 
        Give the values you would use for a numpy array.
        """
        a = abs(Xi)>self.NX
        b = abs(Xf)>self.NX
        c = abs(Yi)>self.NY
        d = abs(Yf)>self.NY
        if any([a,b,c,d]):
            raise Exception(EM.xy1)
        self.data = self.data[:,:,:,:,:,Yi:Yf,Xi:Xf].copy()
        self.updateDimensions()
    
    
    def Clip(self,maxV):
        """
        very simple method to just clip pixel intensities according to max.
        Needed because ExtractProfileRectangle needs the mask outline you draw 
        to be the maximum pixel value in the image and that can be annoying 
        for images with overexposed regions or random high pixels.
        """
        self.data[self.data>maxV] = maxV
            
            
    def ExtractProfileRectangle(self,outDir,windows=None,masks=None,
                                NXSegs=10,downsizeY=2):
        """
        This saves csvs containing averaged pixel values taken from the 
        gradient windows. I.e. if you want pixel intensites but saving a csv 
        of all pixels is be too large then do averaging with this.
        
        Parameters
        ----------
        outDir : str
            Name of directory to save csvs too. It is in the parent directory 
            of XPath. This directory will be created if needed.
        windows : str or None
            This defines the rectangular region from which measurements are 
            taken. Draw the rectangle with rectangle tool in image j and save 
            coordinates as .txt file. Remember to draw it on an image which 
            has been treated exactly the same as the TData that you use this 
            method on. It should be a string to the folder containing all such 
            .txt files. They should be separated into directories named 
            'Exp'+FieldID. If str is a level 0 path then it assumes the 
            directory with this name is in the parent directory of the XFold. 
            If None then it takes everything A trapezium shaped window will be 
            converted to the bounding rectangle.
        masks : str or None
            This is an image which defines a region of arbitrary shape to 
            decide which pixels to include (used in combination with windows). 
            This image should have the usable region outlined with the highest 
            pixel intensity of the image. Input as windows.
        NXSegs : int
            The number of segments to return along the x-axis. All pixel 
            values are averaged within each segment. The X position in pixels 
            of the middle of each segment will be given in the CSV row heading 
            (measured relative to the window).
        downsizeY : int
            Factor to downsize y-axis length by. Pixels are averaged. Position 
            put in CSV headings too.
        
        Returns
        -------
        Nothing returned but csvs are saved. The csvs have NSegs+1 columns and 
        1+NY//downsizeY rows. One separate csv for each F,T,M,Z,C.
        """
        
        outDir = XFold.OutDirSig+outDir
        
        # don't want to include label channel in future loops
        CC = [i for i,c in enumerate(self.Chan) if c!='Label']
        
        for i,FID in enumerate(self.FieldIDs):
            if isinstance(NXSegs,dict):
                NXSegsF = NXSegs[FID]
            else:
                NXSegsF = NXSegs
            # will need to know padding applied to self.data wrt to templates
            if FID in self.TemplatePadDic.keys():
                pd = self.TemplatePadDic[FID]
            else:
                pd = [0,0]
            
            # import and process the window into form [[y0,x0]...[y3,x3]]
            if windows == None:
                win = [[pd[0]//2,pd[1]//2],
                       [pd[0]//2,self.NX-math.ceil(pd[1]/2)],
                       [self.NY-math.ceil(pd[1]/2),self.NX-math.ceil(pd[1]/2)],
                       [self.NY-math.ceil(pd[0]/2),pd[1]//2]]
            else:
                self.ParentXFold.buildWindows(windows)
                win = self.ParentXFold.WindowDic[windows][FID]
                # apply pad to window if TData was extracted from same template
                win = [[a+b//2 for a,b in zip(v,pd)] for v in win]
            yi,yf,xi,xf = [win[0][0],win[2][0],win[0][1],win[2][1]]
            
            # similarly import the mask
            if masks==None:
                mask = np.ones((self.NY,self.NX)).astype('int')
            else:
                self.ParentXFold.buildMasks(masks)
                mask = self.ParentXFold.MaskDic[masks][FID]                
                pad1 = [[p//2,math.ceil(p/2)] for p in pd]
                mask = np.pad(mask,pad1).astype('int')
            # extract window from mask
            mask = mask[yi:yf,xi:xf].copy()
            
            # process separately for T,M,Z,chan
            ranges = [range(self.NT),range(self.NM),range(self.NZ),CC]
            for t,m,z,c in product(*ranges):
                # extract window of data from self:
                data = self.data[t,i,m,z,c,yi:yf,xi:xf].copy()
                # initiate np array and steps for collecting data
                dy = downsizeY
                NY = int((yf-yi)/dy)
                dx = int((xf-xi)/NXSegsF)
                _csv = np.zeros((NY,NXSegsF))
                for y in range(NY):
                    for x in range(NXSegsF):
                        # input the data
                        blockD = data[y*dy:(y+1)*dy,x*dx:(x+1)*dx].copy()
                        blockM = mask[y*dy:(y+1)*dy,x*dx:(x+1)*dx].copy()
                        result = blockD[blockM==1]
                        if result.size==0:
                            _csv[y,x] = 'NaN'
                        else:
                            _csv[y,x] = np.mean(result)
                        del blockD
                        del blockM
                del data

                # add x-slice and y-distance headings
                xlab = [str(dx*x+dx//2) for x in range(NXSegsF)]
                xlab = np.array(['x='+x+' pixels' for x in xlab])
                ylab = ['y='+str(dy*y+dy//2)+'pixels' for y in range(NY)]
                ylab = np.array(['Y distance']+ylab)
                _csv = np.vstack((xlab,_csv))
                _csv = np.hstack((ylab.reshape((NY+1,1)),_csv))
                
                # get exp time in mins of this time-point
                expStart = self.ParentXFold.StartTimes[FID]
                timeInSesh = self.ParentSession.TStep*self.SeshT[t]
                imageMom = self.ParentSession.StartMom + timeInSesh
                imXTime = int((imageMom - expStart).total_seconds()/60)
                
                outName = 'T'+str(imXTime)+'min_M'+str(m)+'_Z'+str(z)
                outName += '_C'+self.Chan[c]+'.csv'
                outF = XFold.FieldDir + FID
                outPath1 = os.path.join(self.ParentXFold.XPathP,outDir,outF)
                if not os.path.exists(outPath1):
                    os.makedirs(outPath1)
                outPath = os.path.join(outPath1,outName)
                assert not os.path.exists(outPath),EM.ae5
                
                with open(outPath,'w',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(_csv)
                
                    
def AutoLevel(data,minP=2,maxP=98,overWrite=False,returnTDatas=True):
    """For each field, this looks at all timepoints and applies autolevelling.
    That is, all pixels below/above the minP/maxP percentile pixel value are 
    set to 0/max value (where max is the max value for the data type) and all 
    pixel values in between scale linearly.
    
    You give it a TFile or a TData or a list of either.
    
    With lists of TFiles or TDatas, it of course autolevels globally across 
    the list. 
    
    It can overwrite the input files or just output TDatas (which will match 
    the structure of the input).
    """
    # first regularise input into a list of TDatas
    if not isinstance(data,list):
        data = [data]
    if all([isinstance(d,TFile) for d in data]):
        data = [tf.makeTData() for tf in data]
    elif all([isinstance(d,TData) for d in data]):
        pass # because this is wat we want
    else:
        # anything else is an error
        raise Exception(EM.al1)
    
    # now do the levelling
    for td in data:
        for f in range(td.NF):
            for c in range(td.NC):
                minV = np.percentile(np.ravel(td.data[:,f,:,:,c]),minP)
                maxV = np.percentile(np.ravel(td.data[:,f,:,:,c]),maxP)
                td.data[:,f,:,:,c][td.data[:,f,:,:,c]<minV] = minV
                td.data[:,f,:,:,c][td.data[:,f,:,:,c]>maxV] = maxV
                td.data[:,f,:,:,c] = td.data[:,f,:,:,c] - minV
                td.data[:,f,:,:,c] = td.data[:,f,:,:,c]*XFold.UINT16MAX/maxV
                td.data = td.data.astype('uint16')
    
    if overWrite:
        pass
    
    if returnTDatas:
        return outTDatas