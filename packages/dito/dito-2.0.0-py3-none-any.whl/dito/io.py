import os.path

import cv2
import numpy as np

import dito.utils


def load(filename, color=None):
    """
    Load image from file given by `filename` and return NumPy array.

    If `color` is `None`, the image is loaded as-is. If `color` is `False`, a
    grayscale image is returned. If `color` is `True`, then a color image is
    returned, even if the original image is grayscale.

    The bit-depth (8 or 16 bit) of the image file will be preserved.
    """

    # check if file exists
    if not os.path.exists(filename):
        raise FileNotFoundError("Image file '{}' does not exist".format(filename))

    # flags - select grayscale or color mode
    if color is None:
        flags = cv2.IMREAD_UNCHANGED
    else:
        flags = cv2.IMREAD_ANYDEPTH | (cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE)

    # read image
    image = cv2.imread(filename=filename, flags=flags)
    
    # check if loading was successful
    if image is None:
        raise RuntimeError("Could not load image from file '{}'".format(filename))

    return image


def decode(b, color=None):
    """
    Load image from the byte array `b` containing the *encoded* image and
    return NumPy array.

    If `color` is `None`, the image is loaded as-is. If `color` is `False`, a
    grayscale image is returned. If `color` is `True`, then a color image is
    returned, even if the original image is grayscale.

    The bit-depth (8 or 16 bit) of the image file will be preserved.
    """

    # byte array -> NumPy array
    buf = np.frombuffer(b, dtype=np.uint8)

    # flags - select grayscale or color mode
    if color is None:
        flags = cv2.IMREAD_UNCHANGED
    else:
        flags = cv2.IMREAD_ANYDEPTH | (cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE)

    # read image
    image = cv2.imdecode(buf=buf, flags=flags)

    return image


def save(filename, image, mkdir=True):
    """
    Save image `image` to file `filename`.

    If `mkdir` is `True`, the parent dir of the given filename is created
    before saving the image.
    """

    if not isinstance(image, np.ndarray):
        raise RuntimeError("Invalid image (type '{}')".format(type(image).__name__))

    # create parent dir
    if mkdir:
        dito.utils.mkdir(dirname=os.path.dirname(filename))

    # write
    return cv2.imwrite(filename=filename, img=image)
