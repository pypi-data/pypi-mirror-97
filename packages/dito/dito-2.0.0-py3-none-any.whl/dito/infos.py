import collections

import cv2
import numpy as np

import dito.core
import dito.utils


def info(image):
    """
    Returns an ordered dictionary containing info about the given image.
    """

    result = collections.OrderedDict()
    result["size"] = "{:.1f} KiB".format(image.size * image.itemsize / 1024.0)
    result["shape"] = image.shape
    result["dtype"] = image.dtype
    result["mean"] = np.mean(image)
    result["std"] = np.std(image)
    result["min"] = np.min(image)
    result["1st quartile"] = np.percentile(image, 25.0)
    result["median"] = np.median(image)
    result["3rd quartile"] = np.percentile(image, 75.0)
    result["max"] = np.max(image)
    return result


def pinfo(image):
    """
    Prints info about the given image.
    """
    
    result = info(image=image)
    dito.utils.ptable(rows=result.items())


def hist(image, bin_count=256):
    """
    Return the histogram of the specified image.
    """
    
    # determine which channels to use
    if dito.core.is_gray(image):
        channels = [0]
    elif dito.core.is_color(image):
        channels = [0, 1, 2]
    else:
        raise ValueError("The given image must be a valid gray scale or color image")
    
    # accumulate histogram over all channels
    hist = sum(cv2.calcHist([image], [channel], mask=None, histSize=[bin_count], ranges=(0, 256)) for channel in channels)
    hist = np.squeeze(hist)
    
    return hist
    

def phist(image, bin_count=25, height=8, bar_symbol="#", background_symbol=" ", col_sep="."):
    """
    Print the histogram of the given image.
    """
    
    h = hist(image=image, bin_count=bin_count)
    h = h / np.max(h)
    
    print("^")
    for n_row in range(height):
        col_strs = []
        for n_bin in range(bin_count):
            if h[n_bin] > (1.0 - (n_row + 1) / height):
                col_str = bar_symbol
            else:
                col_str = background_symbol
            col_strs.append(col_str)
        print("|" + col_sep.join(col_strs))
    print("+" + "-" * ((bin_count - 1) * (1 + len(col_sep)) + 1) + ">")
