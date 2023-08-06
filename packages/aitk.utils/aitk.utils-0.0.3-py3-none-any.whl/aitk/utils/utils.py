# -*- coding: utf-8 -*-
# ***********************************************************
# aitk.utils: Python utils for AI
#
# Copyright (c) 2021 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.utils
#
# ***********************************************************

import math

try:
    from IPython.display import clear_output, display
except ImportError:
    clear_ouput = None

def gallery(images, border_width=1, background_color=(255, 255, 255),
            format=None, clear=True):
    """
    Construct a gallery of images
    """
    try:
        from PIL import Image
    except ImportError:
        print("gallery() requires Pillow, Python Image Library (PIL)")
        return

    gallery_cols = math.ceil(math.sqrt(len(images)))
    gallery_rows = math.ceil(len(images) / gallery_cols)

    size = images[0].size
    size = size[0] + (border_width * 2), size[1] + (border_width * 2)

    gallery_image = Image.new(
        mode="RGBA",
        size=(int(gallery_cols * size[0]), int(gallery_rows * size[1])),
        color=background_color,
    )

    for i, image in enumerate(images):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        location = (
            int((i % gallery_cols) * size[0]) + border_width,
            int((i // gallery_cols) * size[1]) + border_width,
        )
        gallery_image.paste(image, location)

    if format is None:
        if clear:
            if clear_output is not None:
                clear_output(wait=True)
        if clear_output is not None:
            display(gallery_image)
        else:
            return gallery_image
    elif format == "image":
        return gallery_image
    else:
        raise ValueError("unable to convert to format %r" % format)
