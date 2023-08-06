"""
These are functions that extract metadata from an image file. 
Function work for all supported softwares that may have made the image 
data. 
"""

import os
import re
import numpy as np
from datetime import timedelta,datetime
import tifffile

if __package__ == '':
    import generalFunctions as genF
    import errorMessages as EM
else:
    from . import generalFunctions as genF
    from . import errorMessages as EM
    
imTypeReg = re.compile(r'Type : (\d+) bit') # image data type
NTReg = re.compile(r'Time : (\d*)') # number of time points
NFReg = re.compile(r'XY : (\d*)') # number of fields
# number of montage tiles, can extract x (group(1)) and y (group(2))
NMReg = re.compile(r'Montage Positions - \(\d* \( (\d*) by (\d*) \)\)')
NMReg2 = re.compile(r'Montage : (\d*)')
NZReg = re.compile(r'Z : (\d*)') # number of z-slices
NCReg = re.compile(r'Wavelength : (\d*)') # number of channels
NYReg = re.compile(r'y : (\d+) ') # y size
NXReg = re.compile(r'x : (\d+) ') # x size
pixSizeRegY = re.compile(r'y : \d+ \* (\d+.\d+)') # pixel size
pixSizeRegX = re.compile(r'x : \d+ \* (\d+.\d+)') # pixel size
pixUnitReg = re.compile(r'x : \d+ \* \d+.\d+ : (\w+)') # unit of pixel size
DTReg = re.compile(r'Repeat T - \d+ times? \((\d+) ([\s\w-]+)\)')
DZReg = re.compile(r'Repeat Z - (\d*) um in') # z-slice thickness
chanReg = re.compile(r'\t(?:Move )?Channel - (\w+)\n') # can get all names of chans
OlapReg = re.compile(r'Montage=(Region|Edge)\tOverlap (\d*)') 
startTimeReg = re.compile(r'Time=(\d\d:\d\d:\d\d)\n\[Created End\]')
startDateReg = re.compile(r'\[Created\]\nDate=(\d\d/\d\d/\d\d\d\d)')
startMomRegMM = re.compile(r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)')
# delay regex... i.e. time b/w start of protocol and start of imaging
delayReg = re.compile(r'Delay - (\d+) (\w+)')


def allSeshMeta(tp):
    """
    gets all the main meta that we use and returns in a dictionary
    
    Parameters
    -----------
    tp : str
        file path to the mage filel in question.
    """
    
    allMeta = {}
    try:
        # set madeBy and extract everything we'll need from the file
        with tifffile.TiffFile(tp) as tif:
            m = tif.fluoview_metadata
            I = tif.imagej_metadata
            if I:
                I = 'tw_nt' in I.keys()
            if m or I:
                allMeta['madeBy'] = 'Andor'
            else:
                m = tif.micromanager_metadata
                if m:
                    allMeta['madeBy'] = 'MicroManager'
                    t = tif.pages[0].tags['MicroManagerMetadata'].value
                else:
                    raise Exception(EM.md1.format(tp))
    except tifffile.TiffFileError as TFE:
        print('Critical problem with tiff file: ',tp)
        raise TFE
    
    if allMeta['madeBy']=='Andor':
        
        # get a metadata txt file
        mp = genF.stripTags(tp,'Andor')+'.txt'
        assert os.path.exists(tp),EM.md2
        with open(mp,'rt') as file:
            allMeta['metadata'] = file.read()
        meta = allMeta['metadata']
            
        # take start moment from the txt metadata
        startT = re.search(startTimeReg,meta).group(1)
        startDate = re.search(startDateReg,meta).group(1)
        startMom = startDate + ' ' + startT
        TX = '%d/%m/%Y %H:%M:%S'
        startMom = datetime.strptime(startMom,TX)  
        
        # add the delay time if necessary
        if re.search(delayReg,meta):
            delayT = int(re.search(delayReg,meta).group(1))
            if re.search(delayReg,meta).group(2)=='min':
                delayT = timedelta(minutes=delayT)
                startMom += delayT
            elif re.search(delayReg,meta).group(2)=='hr':
                delayT = timedelta(hours=delayT)
                startMom += delayT
            elif re.search(delayReg,meta).group(2)=='ms':
                delayT = timedelta(milliseconds=delayT)
                startMom += delayT                
            else:
                raise Exception('Unknown format for start delay in session.')
        allMeta['startMom'] = startMom         
        
        # take interval between time points from txt meta
        seshTStep = re.search(DTReg,meta)
        if seshTStep:
            seshTStep = int(seshTStep.group(1))
            if re.search(DTReg,meta).group(2) == 'hr':
                allMeta['TStep'] = timedelta(hours=seshTStep)
            elif re.search(DTReg,meta).group(2) == 'min':
                allMeta['TStep'] = timedelta(minutes=seshTStep)
            elif re.search(DTReg,meta).group(2) == 'sec':
                allMeta['TStep'] = timedelta(seconds=seshTStep)
            elif 'fastest' in re.search(DTReg,meta).group(2):
                allMeta['TStep'] = timedelta(seconds=0)
            else:
                raise Exception(EM.md3)
        else:
            allMeta['TStep'] = timedelta(seconds=0)
        
        allMeta['Chan'] = re.findall(chanReg,meta)
        
        # set the session imaging parameters and dimensions etc
        if re.search(NTReg,meta):
            allMeta['NT'] = int(re.search(NTReg,meta).group(1))
        else:
            allMeta['NT'] = 1
        if re.search(NFReg,meta):
            allMeta['NF'] = int(re.search(NFReg,meta).group(1))
        else:
            allMeta['NF'] = 1
        if re.search(NMReg2,meta):
            allMeta['NM'] = int(re.search(NMReg2,meta).group(1))
        else:
            allMeta['NM'] = 1
        if re.search(NZReg,meta):
            allMeta['NZ'] = int(re.search(NZReg,meta).group(1))
        else:
            allMeta['NZ'] = 1
        if re.search(NCReg,meta):
            allMeta['NC'] = int(re.search(NCReg,meta).group(1))
        else:
            allMeta['NC'] = 1
        if re.search(NYReg,meta):
            allMeta['NY'] = int(re.search(NYReg,meta).group(1))
        else:
            allMeta['NY'] = 1
        if re.search(NXReg,meta):
            allMeta['NX'] = int(re.search(NXReg,meta).group(1))
        else:
            allMeta['NX'] = 1 
            
        if re.search(imTypeReg,meta):
            allMeta['imType'] = int(re.search(imTypeReg,meta).group(1))
        else: 
            raise Exception(EM.it1)
        assert allMeta['imType'] <= 16,EM.it2
        
        allAxes = ['NT','NF','NM','NZ','NC','NY','NX']
        allMeta['Shape'] = tuple([allMeta[k] for k in allAxes])
        
        # montage overlap, NMY and NMX (= numbers of tiles) and pixel stuff 
        molap = re.search(OlapReg,meta)
        if molap:
            allMeta['MOlap'] = int(molap.group(2))/100
        else:
            allMeta['MOlap'] = 0.01
        nm1 = re.search(NMReg,meta)
        if nm1:
            allMeta['NMY'] = int(nm1.group(2))
            allMeta['NMX'] = int(nm1.group(1))
        else:
            allMeta['NMY'] = 1
            allMeta['NMX'] = 1
        allMeta['FieldNMYs'] = [allMeta['NMY'] for f in range(allMeta['NF'])]
        allMeta['FieldNMXs'] = [allMeta['NMX'] for f in range(allMeta['NF'])]
        
        allMeta['MontageOrder'] = 'LRUD'
        allMeta['pixSizeY'] = float(re.search(pixSizeRegY,meta).group(1))
        allMeta['pixSizeX'] = float(re.search(pixSizeRegX,meta).group(1))
        allMeta['pixUnit'] = re.search(pixUnitReg,meta).group(1)

        
    elif allMeta['madeBy']=='MicroManager':
        
        # no .txt metadata file in micromanager
        allMeta['metadata'] = ''
        
        # start moment from image file metadata
        startMom = t['Time']
        startMom = re.search(startMomRegMM,startMom).group(1)
        TX = '%Y-%m-%d %H:%M:%S'
        allMeta['startMom'] = datetime.strptime(startMom,TX)  
        
        # take start moment from image file metadata
        allMeta['TStep'] = timedelta(seconds=m['Summary']['Interval_ms']/1000)
        
        # currently don't know how to get this
        allMeta['Chan'] = ['BF']
        
        # these things will be useful: (details for every position)
        summary =  m['Summary']['InitialPositionList']
        #labels = [im['Label'].split('Pos_')[0] for im in summary] # old way!!
        labels = [im['Label'] for im in summary]
        labels = [re.sub(r'_\d\d\d_\d\d\d','',l) for l in labels]
        labelsSet = sorted(set(labels))
        cols = [s['GridColumnIndex'] for s in summary]
        rows = [s['GridRowIndex'] for s in summary]


        allMeta['imType'] = int(t['BitDepth'])
        assert allMeta['imType'] <= 16,EM.it2
        
        allMeta['NT'] = max(m['IndexMap']['Frame'])+1
        allMeta['NF'] = len(labelsSet)
        # allMeta['NM'] is done below where it is easier
        allMeta['NZ'] = max(m['IndexMap']['Slice'])+1
        allMeta['NC'] = max(m['IndexMap']['Channel'])+1
        allMeta['NY'] = t['Height']
        allMeta['NX'] = t['Width']

        
        # montage overlap, NMY and NMX (= numbers of tiles) and pixel stuff 
        # currently don't know how to get most of them
        allMeta['MOlap'] = 0.05 # doesn't seem to be in metadata
        allMeta['pixSizeY'] = 1 # doesn't seem to be in metadata
        allMeta['pixSizeX'] = 1 # doesn't seem to be in metadata
        allMeta['pixUnit'] = None
        cols2 = [[c for c,L in zip(cols,labels) if l in L] for l in labelsSet]
        rows2 = [[r for r,L in zip(rows,labels) if l in L] for l in labelsSet]
        allMeta['NMY'] = max([max(c)+1 for c in cols2])
        allMeta['NMX'] = max([max(r)+1 for r in rows2])
        allMeta['NM'] = allMeta['NMY']*allMeta['NMX']
        allMeta['MontageOrder'] = 'UDRL'

        allMeta['FieldNMYs'] = [max(c)+1 for c in cols2]
        allMeta['FieldNMXs'] = [max(r)+1 for r in rows2]
        
        allAxes = ['NT','NF','NM','NZ','NC','NY','NX']
        allMeta['Shape'] = tuple([allMeta[k] for k in allAxes])

    else:
        raise Exception(EM.md1)
    
    allMeta['Name'] = genF.stripTags(os.path.split(tp)[1],allMeta['madeBy'])
    
    return allMeta



def file2Dims(filePath,checkCorrupt=True):
    """
    This find the dimensions of the file in 7D format.
    
    Parameters
    -----------
    filePath : str
        The path to the image file
    checkCorrupt : bool
        Whether to raise an assertion if the number of images in the file 
        doesn't correspond to the dimensions it thinks it has. I.e. if the 
        file is corrupt.
        
    Returns
    ---------
    dims : tuple
        (NT,NF,NM,NZ,NC,NY,NX)
    """
    try:
        with tifffile.TiffFile(filePath) as tif:
            m = tif.fluoview_metadata
            I = tif.imagej_metadata
            mm = tif.micromanager_metadata
            if m and 'Dimensions' in m.keys():
                dimDic = {l[0]:l[1] for l in m['Dimensions']}
                shapeKeys = ['Time','XY','Montage','Z','Wavelength','y','x']
                dims = []
                for k in shapeKeys:
                    if k in dimDic.keys():
                        dims.append(dimDic[k])
                    else:
                        dims.append(1)
                if 'Time1' in dimDic.keys():
                    dims[0] = dims[0]*dimDic['Time1']
            elif I and 'tw_nt' in I.keys():
                baseString = 'tw_n'
                dimStrings = ['t','f','m','z','c','y','x']
                dims = [I[baseString+LL] for LL in dimStrings]
            elif mm:
                p = tif.pages[0].tags['MicroManagerMetadata'].value
                summ = mm['Summary']['InitialPositionList']
                nt = len(set(mm['IndexMap']['Frame']))
                nf = 1
                nm = 1
                nz = len(set(mm['IndexMap']['Slice']))
                nc = len(set(mm['IndexMap']['Channel']))
                ny = p['Height']
                nx = p['Width']
                dims = [nt,nf,nm,nz,nc,ny,nx]
            else:
                raise Exception(EM.md1)
            if checkCorrupt:
                L = len(tif.pages)
                assert np.prod(dims[:5])==L,EM.cf1.format(filePath)
    except tifffile.TiffFileError as TFE:
        print('Critical problem with tiff file: ',filePath)
        raise TFE
        
    return tuple(dims)
        

