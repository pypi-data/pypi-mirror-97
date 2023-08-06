# -*- coding: utf-8 -*-
r"""
procedural rendering of spin configurations. An object oriented version is planned. There are methods for rendering
the povray source files generated from the SpinD-Kiel-code.
"""

from pathlib import Path
from typing import TypeVar

PathLike = TypeVar("PathLike", str, Path)
from vapory import *
import numpy as np


def calculate_phi_theta(sx, sy, sz):
    length = np.sqrt(sx * sx + sy * sy + sz * sz)
    length_ip = np.sqrt(sy * sy + sx * sx)
    phi = np.arctan2(sy, sx) * 180 / np.pi
    theta = np.arctan2(length_ip, sz) * 180 / np.pi
    return phi, theta, length


def calculate_colorcode(phi, theta):
    C = 2 * np.pi / 3
    D = 5
    E = np.pi * 2 * theta / 300
    R = D * np.cos(E)
    G = D * np.cos(E + C)
    B = D * np.cos(E + 2 * C)
    if R <= 1e-6:
        R = 0
    if G <= 1e-6:
        G = 0
    if B <= 1e-6:
        B = 0
    return R, G, B


def renderSpinSTM(sourcefile: PathLike) -> None:
    r"""
    Render spin configuration from source file. Implies the makro Spin(...) to be defined.

    Args:
        sourcefile(PathLike): file of the SpinSTM
    """
    l_objects = [Background('color Black'),
                 LightSource([12, -12, -12],
                             'color White',
                             'shadowless'),
                 LightSource([12, 0, -12],
                             'color White',
                             'area_light', [5, 0, 0], [0, 5, 0], 5, 5,
                             'adaptive', 1,
                             'jitter')]

    with open(sourcefile) as f:
        for line in f:
            L = line.split()
            x = float(L[0])
            y = float(L[1])
            z = float(L[2])
            theta, phi, length = calculate_phi_theta(sx=float(L[3]), sy=float(L[4]), sz=float(L[5]))
            R, G, B = calculate_colorcode(phi=theta, theta=phi)
            l_objects.append(Cone([0.0, 0.0, 0.6], 0.0, [0.0, 0.0, -0.6], 0.4,
                                  'rotate', [0.0, phi, 0.0],
                                  'rotate', [0.0, 0.0, theta],
                                  'translate', [1.5 * x, 1.5 * y, 10 * z],
                                  Texture(Pigment('color', [R, B, G]))))

    scene = Scene(Camera('location', [25 * 1.5, -45, 5],
                         'sky', [0, 0, 1],
                         'look_at', [25 * 1.5, 0, 0],
                         'right', [1, 0, 0],
                         'angle', 40),
                  objects=l_objects,
                  included=['colors.inc', 'shapes.inc']
                  )
    # We use antialiasing. Remove this option for faster rendering.
    scene.render("stmtest.png", width=2000, height=2000)  # , antialiasing=0.001)


def renderEigenvector(sourcefile: PathLike) -> None:
    r"""
    """
    l_objects = [Background('color Black'),
                 LightSource([12, -12, -12],
                             'color White',
                             'shadowless'),
                 LightSource([12, 0, -12],
                             'color White',
                             'area_light', [5, 0, 0], [0, 5, 0], 5, 5,
                             'adaptive', 1,
                             'jitter')]
    with open(sourcefile) as f:
        for line in f:
            L = line.split()
            x = float(L[0])
            y = float(L[1])
            z = float(L[2])
            vecx = float(L[3])
            vecy = float(L[4])
            vecz = float(L[5])
            thick = 0.07
            theta, phi, length = calculate_phi_theta(sx=vecx, sy=vecy, sz=vecz)
            long = length*7
            theta, phi, length = calculate_phi_theta(sx=vecx, sy=vecy, sz=vecz)
            R, G, B = calculate_colorcode(phi=theta, theta=phi)
            if long <= 1e-6:
                l_objects.append(Sphere([x,y,11*z],thick,
                                        Texture(Pigment('color', [R,B,G]))))
            else:
                l_objects.append(Union(Cylinder([0.0, 0.0, -long / 2], [0.0, 0.0, long / 2], thick,
                                                Texture(Pigment('color', [R, B, G]))),
                                       Cone([0.0, 0.0, long / 2 + long * 0.7], 0.0, [0.0, 0.0, long / 2],
                                            thick + thick * 1.1,
                                            Texture(Pigment('color', [R, B, G]))),
                                       'rotate', [0.0, phi, 0.0],
                                       'rotate', [0.0, 0.0, theta],
                                       'translate', [x, y, 10 * z]))
    scene = Scene(Camera('location', [25, -45, 5],
                         'sky', [0, 0, 1],
                         'look_at', [25, 0, 0],
                         'right', [1, 0, 0],
                         'angle', 40),
                  objects=l_objects,
                  included=['colors.inc', 'shapes.inc']
                  )
    # We use antialiasing. Remove this option for faster rendering.
    scene.render("vectest.png", width=2000, height=2000)  # , antialiasing=0.001)


# renderSpinSTM(sourcefile='spin_0001.dat')
#renderEigenvector(sourcefile='vector_sp.dat_0004.dat')