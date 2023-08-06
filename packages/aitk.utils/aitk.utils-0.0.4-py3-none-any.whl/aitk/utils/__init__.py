# -*- coding: utf-8 -*-
# ***********************************************************
# aitk.utils: Python utils for AI
#
# Copyright (c) 2021 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.utils
#
# ***********************************************************

from .utils import gallery
from .joystick import Joystick, NoJoystick, has_ipywidgets, has_ipycanvas

try:
    _in_colab = 'google.colab' in str(get_ipython())
except Exception:
    _in_colab = False


def in_colab():
    return _in_colab

def make_joystick(*args, **kwargs):
    if in_colab():
        return NoJoystick(*args, **kwargs)
    elif has_ipycanvas():
        return Joystick(*args, **kwargs)
    elif has_ipywidgets():
        return NoJoystick(*args, **kwargs)
    else:
        raise Exception("please install ipycanvas, or ipywidgets to use make_joystick")
