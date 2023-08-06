import os.path

import numpy as np

import dito.io


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datafiles")
DATA_FILENAMES = {
    "image:PM5544": os.path.join(DATA_DIR, "images", "PM5544.png"),
    "colormap:plot": os.path.join(DATA_DIR, "colormaps", "plot.png"),
}


####
#%%% real images
####


def pm5544():
    return dito.io.load(filename=DATA_FILENAMES["image:PM5544"])


####
#%%% synthetic images
####


def xslope(height=32, width=256):
    """
    Return image containing values increasing from 0 to 255 along the x axis.
    """
    
    slope = np.linspace(start=0, stop=255, num=width, endpoint=True, dtype=np.uint8)
    slope.shape = (1,) + slope.shape
    slope = np.repeat(a=slope, repeats=height, axis=0)
    return slope


def yslope(width=32, height=256):
    """
    Return image containing values increasing from 0 to 255 along the y axis.
    """
    
    return xslope(height=width, width=height).T
