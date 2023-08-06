# -*- coding: utf-8 -*-
r"""
This module contains utilities for dealing with colors.
"""
import numpy as np


def RGB_255to1(colorcode: np.ndarray) -> np.ndarray:
    r"""
    converts RGB colorcodes from the 255 range within the range of povray which is 0 to 1.

    Args:
        colorcode(np.ndarray): [R, G, B] from 0 to 255

    Returns:
        colorcode [R, G, B] from 0 to 1
    """
    return colorcode / 255


def lightgray() -> np.ndarray:
    r"""
    Returns:
        lightgray colorcode
    """
    return RGB_255to1(np.array([207, 207, 207]))
