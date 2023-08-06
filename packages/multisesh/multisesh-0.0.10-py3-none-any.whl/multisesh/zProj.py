import numpy as np
import math
from skimage.morphology import disk
from scipy.ndimage.filters import generic_filter
from skimage.transform import downscale_local_mean
from skimage.transform import resize


def maxProj(stack):
    """Normal maximum projection."""
    return np.max(stack,axis=0)

def avProj(stack):
    """Normal average projection."""
    return np.mean(stack,axis=0)

def minProj(stack):
    """Normal minimum projection."""
    return np.min(stack,axis=0)

def signalF(vals):
    """A measure of signal."""
    return vals.mean()*vals.std()


def signalProj(stack,pixelSize,dscale,slices=1,proj=True,furthest=False):
    """
    A 2D projection which applies a filter to select the slice of most signal 
    for each pixel. The measure of signal is mean * std. 
    
    Parameters
    ----------
    stack : numpy array
        The image stack
    pixelSize : float
        The size in um of the pixel in the image. The structure element of the 
        filter is a circle of 20um because that is a bit bigger than a nucleus.
    dscale : int
        The factor by which to dscale the images during analysis to make 
        analysis faster.
    slices : int
        The number of slices to include in the output. These are taken 
        alternatingly from above-below the highest signal slice. NA is put 
        in if the number goes beyond the slices of the image stack.
    proj : bool
        Whether to do a mean projection of the final array.
    furthest : bool
        Whether to simply return the pixels (currently only does it with 1 
        slice) furthest from the signal. I.e. can be used to return a 
        background image.
    """
    assert isinstance(dscale,int),'dscale must be an int'
    assert isinstance(slices,int),'slices must be an int'
    NZ,YSIZE,XSIZE = np.shape(stack)
    # radius wants to be about 30um so it is definitely bigger than nuclei
    radius = np.ceil(20/(pixelSize*dscale))
    selem = disk(radius)
    
    #initiate mask:
    stack2 = np.zeros((NZ,math.ceil(YSIZE/dscale),math.ceil(XSIZE/dscale)))
    for i,im in enumerate(stack):
        stack2[i] = generic_filter(downscale_local_mean(im,(dscale,dscale)),
                                   signalF,
                                   footprint=selem,
                                   mode='reflect')
    stack2 = np.argmax(stack2,axis=0)
    stack2 = resize(stack2,(YSIZE,XSIZE),preserve_range=True)
    stack2 = np.rint(stack2).astype(int)
    I,J = np.ogrid[:YSIZE,:XSIZE]
    
    if furthest:
        stack2 = np.where(stack2>=NZ/2,0,NZ-1)
        assert slices==1,'slices must be 1 when using furthest'
    
    if slices==1:
        return stack[stack2,I,J]
    else:
        out = stack[stack2,I,J][np.newaxis]
        NAN = np.empty((YSIZE,XSIZE))
        NAN.fill(np.nan)
        stack = np.concatenate((stack,NAN[np.newaxis]))
        for s in range(slices):
            sel = stack2 + ((s+1)//2)*((-1)**s)
            sel[sel<0] = NZ
            sel[sel>=NZ] = NZ
            sel = sel.astype(int)
            out = np.concatenate((out,stack[sel,I,J][np.newaxis]))
        if proj:
            return np.nanmean(out,axis=0)
        else:
            return out

        
def selectSlices_byMeanSTD_takeN(stack,N):
    """
    This selects N adjacent slices to take out. 
    Selection is based on mean*STD signal measure. 
    It does a rolling average and selects N slices with min rolling average.
    """
    #this is the signal measure, smaller for more signal:
    measures = [MAXSIGNALMEASURE/(im.mean()*im.std()) for im in stack]
    measures = np.convolve(measures, np.ones((N,))/N, mode='valid')
    
    # find min position and return the appropriate slice of stack
    minIndex = np.argmin(measures)  
    return stack[minIndex:minIndex + N]


def selectSlices_byMeanSTD_thresh(stack,thresh):
    """Returns any slices where the measure is below a threshold."""
    # just do list comprehension filtering:    
    return [im for im in stack if MAXSIGNALMEASURE/(im.mean()*im.std()) < thresh]


def sectioniseStack(stack,N,NZ):
    """Divides a stack into N*N smaller stacks."""
    # first divide it up
    # look how np.array_split returns a list not a numpy array! (I guess because it can be jagged)
    sections = []
    for im in stack:
        sections.append(np.array_split(im,N))
        for n in range(N):
            sections[-1][n] = np.array_split(sections[-1][n],N,axis=1)
   
    # now need to reshape it so that each element of the list is a section 
    # with all z-slices
    # i.e. the thing returned is N*N long
    resections = [ [] for i in range(N*N) ]
    for n in range(N*N):
        for z in range(NZ):
            resections[n].append(sections[z][n%N][n//N])
    return resections



def reassembleSections(imageList):
    """
    Takes a list of images which is N*N long and together form a N*N square 
    image puts it back together watch out it doesn't work with a list of N*N 
    image stacks! They have to be single images.
    """
    N = int(math.sqrt(len(imageList)))
    columns = []
    for n in range(N):
        columns.append(np.concatenate(imageList[n*N:(n+1)*N]))
    image = np.concatenate(columns,axis=1)
    return image