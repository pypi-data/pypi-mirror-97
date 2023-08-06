import cv2
import numpy as np

import dito.core
import dito.data


def get_colormap(name):
    """
    Returns the colormap specified by `name` as `uint8` NumPy array of size
    `(256, 1, 3)`.
    """
    
    # source 1: non-OpenCV colormaps
    data_key = "colormap:{}".format(name.lower())
    if data_key in dito.data.DATA_FILENAMES.keys():
        return dito.io.load(filename=dito.data.DATA_FILENAMES[data_key])
    
    # source 2: OpenCV colormaps
    full_cv2_name = "COLORMAP_{}".format(name.upper())
    if hasattr(cv2, full_cv2_name):
        return cv2.applyColorMap(src=dito.data.yslope(width=1), colormap=getattr(cv2, full_cv2_name))
    
    # no match
    raise ValueError("Unknown colormap '{}'".format(name))


def is_colormap(colormap):
    """
    Returns `True` iff `colormap` is a OpenCV-compatible colormap.
    
    For this, `colormap` must be a `uint8` array of shape `(256, 1, 3)`, i.e.
    a color image of size `1x256`.
    """
    if not dito.core.is_image(image=colormap):
        return False
    if colormap.dtype != np.uint8:
        return False
    if colormap.shape != (256, 1, 3):
        return False
    return True


def colorize(image, colormap):
    """
    Colorize the `image` using the colormap identified by `colormap_name`.
    """
    if isinstance(colormap, str):
        return cv2.applyColorMap(src=image, userColor=get_colormap(name=colormap))
    elif is_colormap(colormap=colormap):
        return cv2.applyColorMap(src=image, userColor=colormap)
    else:
        raise TypeError("Argument `colormap` must either be a string (the colormap name) or a valid colormap.")


####
#%%% image stacking
####


def stack(images, padding=0, background_color=0, dtype=None, gray=None):
    """
    Stack given images into one image.

    `images` must be a vector of images (in which case the images are stacked
    horizontally) or a vector of vectors of images, defining rows and columns.
    """

    # check argument `images`
    if isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], np.ndarray):
        # `images` is a vector of images
        rows = [images]
    elif isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], (tuple, list)) and (len(images[0]) > 0) and isinstance(images[0][0], np.ndarray):
        # `images` is a vector of vectors of images
        rows = images
    else:
        raise ValueError("Invalid argument 'images' - must be vector of images or vector of vectors of images")

    # find common data type and color mode
    if dtype is None:
        dtype = dito.core.dtype_common((image.dtype for row in rows for image in row))
    if gray is None:
        gray = all(dito.core.is_gray(image=image) for row in rows for image in row)

    # step 1/2: construct stacked image for each row
    row_images = []
    width = 0
    for (n_row, row) in enumerate(rows):
        # determine row height
        row_height = 0
        for image in row:
            row_height = max(row_height, image.shape[0])
        if n_row == 0:
            row_height += 2 * padding
        else:
            row_height += padding

        # construct image
        row_image = None
        for (n_col, image) in enumerate(row):
            # convert individual image to target data type and color mode
            image = dito.core.convert(image=image, dtype=dtype)
            if gray:
                image = dito.core.as_gray(image=image)
            else:
                image = dito.core.as_color(image=image)

            # add padding
            pad_width = [[padding if n_row == 0 else 0, padding], [padding if n_col == 0 else 0, padding]]
            if not gray:
                pad_width.append([0, 0])
            image = np.pad(array=image, pad_width=pad_width, mode="constant", constant_values=background_color)

            # ensure that image has the height of the row
            gap = row_height - image.shape[0]
            if gap > 0:
                if gray:
                    image_fill = np.zeros(shape=(gap, image.shape[1]), dtype=dtype) + background_color
                else:
                    image_fill = np.zeros(shape=(gap, image.shape[1], 3), dtype=dtype) + background_color
                image = np.vstack(tup=(image, image_fill))

            # add to current row image
            if row_image is None:
                row_image = image
            else:
                row_image = np.hstack(tup=(row_image, image))

        # update max width
        width = max(width, row_image.shape[1])
        row_images.append(row_image)

    # step 2/2: construct stacked image from the row images
    stacked_image = None
    for row_image in row_images:
        # ensure that the row image has the width of the final image
        gap = width - row_image.shape[1]
        if gap > 0:
            if gray:
                image_fill = np.zeros(shape=(row_image.shape[0], gap), dtype=dtype) + background_color
            else:
                image_fill = np.zeros(shape=(row_image.shape[0], gap, 3), dtype=dtype) + background_color
            row_image = np.hstack(tup=(row_image, image_fill))

        # add to final image
        if stacked_image is None:
            stacked_image = row_image
        else:
            stacked_image = np.vstack(tup=(stacked_image, row_image))

    return stacked_image


####
#%%% text
####


def text(image, message, position=(0.0, 0.0), anchor="lt", font="sans", scale=1.0, thickness=1, padding_rel=1.0, inner_color=(255, 255, 255), outer_color=None, background_color=0, line_type=cv2.LINE_AA):
    """
    Draws the text `message` into the given `image`.

    The `position` is given as 2D point in relative coordinates (i.e., with
    coordinate ranges of [0.0, 1.0]). The `anchor` must be given as two letter
    string, following the pattern `[lcr][tcb]`. It specifies the horizontal
    and vertical alignment of the text with respect to the given position. The
    `padding_rel` is given in (possibly non-integer) multiples of the font's
    baseline height.
    """

    # keep input image unchanged
    image = image.copy()

    # font
    if font == "sans":
        font_face = cv2.FONT_HERSHEY_DUPLEX
    elif font == "serif":
        font_face = cv2.FONT_HERSHEY_TRIPLEX
    else:
        raise ValueError("Invalid font '{}'".format(font))
    font_scale = scale
    font_thickness = thickness

    # calculate width and height of the text
    ((text_width, text_height), baseline) = cv2.getTextSize(
        text=message,
        fontFace=font_face,
        fontScale=font_scale,
        thickness=font_thickness,
    )

    # base offset derived from the specified position
    offset = np.array([
        position[0] * image.shape[1],
        position[1] * (image.shape[0] - baseline),
    ])

    # adjust offset based on the specified anchor type
    if not (isinstance(anchor, str) and (len(anchor) == 2) and (anchor[0] in ("l", "c", "r")) and (anchor[1] in ("t", "c", "b"))):
        raise ValueError("Argument 'anchor' must be a string of length two (pattern: '[lcr][tcb]') , but is '{}'".format(anchor))
    (anchor_h, anchor_v) = anchor
    if anchor_h == "l":
        pass
    elif anchor_h == "c":
        offset[0] -= text_width * 0.5
    elif anchor_h == "r":
        offset[0] -= text_width
    if anchor_v == "t":
        offset[1] += text_height
    elif anchor_v == "c":
        offset[1] += text_height * 0.5
    elif anchor_v == "b":
        pass

    # finalize offset
    offset = dito.core.tir(*offset)

    # add padding to offset
    padding_abs = round(padding_rel * baseline)

    # draw background rectangle
    if background_color is not None:
        # TODO: allow actual BGR color, not just one intensity value (use cv2.rectangle for drawing)
        image[max(0, offset[1] - text_height - padding_abs):min(image.shape[0], offset[1] + max(baseline, padding_abs)), max(0, offset[0] - padding_abs):min(image.shape[1], offset[0] + text_width + padding_abs), ...] = background_color

    # draw text
    if outer_color is not None:
        cv2.putText(
            img=image,
            text=message,
            org=offset,
            fontFace=font_face,
            fontScale=font_scale,
            color=outer_color,
            thickness=font_thickness + 2,
            lineType=line_type,
            bottomLeftOrigin=False,
        )
    cv2.putText(
        img=image,
        text=message,
        org=offset,
        fontFace=font_face,
        fontScale=font_scale,
        color=inner_color,
        thickness=font_thickness,
        lineType=line_type,
        bottomLeftOrigin=False,
    )

    return image


####
#%%% image visualization
####


def get_screenres():
    """
    Return the resolution (width, height) of the screen in pixels.

    If it can not be determined, assume 1920x1080.
    See http://stackoverflow.com/a/3949983 for info.
    """

    try:
        import tkinter as tk
    except ImportError:
        return (1920, 1080)

    root = tk.Tk()
    (width, height) = (root.winfo_screenwidth(), root.winfo_screenheight())
    root.destroy()
    return (width, height)


def qkeys():
    """
    Returns a tuple of key codes ('unicode code points', as returned by
    `ord()` which correspond to key presses indicating the desire to
    quit (`<ESC>`, `q`).

    >>> qkeys()
    (27, 113)
    """

    return (27, ord("q"))


def show(image, wait=0, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None, window_name="dito.show", close_window=False, engine=None):
    """
    Show `image` on the screen.

    If `image` is a list of images or a list of lists of images, they are
    stacked into one image.
    """

    if isinstance(image, np.ndarray):
        # use image as is
        pass
    elif isinstance(image, (list, tuple)) and (len(image) > 0) and isinstance(image[0], np.ndarray):
        # list of images: stack them into one image
        image = stack(images=[image])
    elif isinstance(image, (list, tuple)) and (len(image) > 0) and isinstance(image[0], (list, tuple)) and (len(image[0]) > 0) and isinstance(image[0][0], np.ndarray):
        # list of lists of images: stack them into one image
        image = stack(images=image)
    else:
        raise ValueError("Invalid value for parameter `image` ({}) - it must either be (i) an image, (ii) a non-empty list of images or a non-empty list of non-empty lists of images".format(image))

    # normalize intensity values
    if normalize_mode is not None:
        image = dito.core.normalize(image=image, mode=normalize_mode, **normalize_kwargs)

    # resize image
    if scale is None:
        # try to find a good scale factor automatically
        (width, height) = get_screenres()
        scale = 0.85 * min(height / image.shape[0], width / image.shape[1])
    image = dito.core.resize(image=image, scale_or_size=scale)

    # apply colormap
    if colormap is not None:
        image = colorize(image=image, colormap=colormap)

    # determine how to display the image
    if engine is None:
        # TODO: auto-detect if in notebook
        engine = "cv2"

    # show
    if engine == "cv2":
        try:
            cv2.imshow(window_name, image)
            key = cv2.waitKey(wait)
        finally:
            if close_window:
                cv2.destroyWindow(window_name)

    elif engine == "ipython":
        # source: https://gist.github.com/uduse/e3122b708a8871dfe9643908e6ef5c54
        import io
        import IPython.display
        import PIL.Image
        f = io.BytesIO()
        # TODO: this just encodes the image array as PNG bytes - we don't need PIL for that -> remove PIL
        PIL.Image.fromarray(image).save(f, "png")
        IPython.display.display(IPython.display.Image(data=f.getvalue()))
        key = -1

    else:
        raise RuntimeError("Unsupported engine '{}'".format(engine))

    return key
