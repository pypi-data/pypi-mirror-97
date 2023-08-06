# -*- coding: utf-8 -*-
r"""
This module contains utilities for the visualization of spin configurations:
- calculation of the color code
- theta, phi, length representation
"""
import numpy as np
from typing import Tuple, List


def identifylayers(position: np.ndarray) -> Tuple[int, np.ndarray]:
    r"""
    Calculates the number of layers and the z-coordinates of these layers.

    Args:
        position: position of the spins or eigenvectors (or any other given quantity written in STM-format).
        Format [[x1,y1,z1], ..., [xn,yn,zn]]

    Returns:
        the number of layers (int) and the z-coordinates of these layers (np.ndarray). The z-coordinates are ordered in
        an increasing order, due to the use of numpys unique function
    """
    l_z = np.unique(position[:, 2])
    l_n = len(l_z)
    return l_n, l_z


def determine_layer_centers(position: np.ndarray) -> List[np.ndarray]:
    r"""
    Takes the positions of the 3d lattice and first split up the layers. Then determine the center of each layer as
    the centroid.

    Args:
        position(np.ndarray): positions of the objects. Format [[x1,y1,z1],...,[xn,yn,zn]]

    Returns:
        center for each layer [[cx1,cy1,cz1],...,[cxL,cyL,czL]], where L is the number of layers.
    """
    l_z = np.unique(position[:, 2])
    centers = []
    for zz in l_z:
        centers.append(np.mean(position[position[:, 2] - zz <= 1e-3], axis=0))
    return centers


def tabledist(position: np.ndarray, referencepoint: np.ndarray = np.array([0.0, 0.0])) -> np.ndarray:
    r"""
    Calculates the distances to the neighbor shells of a set of 2D positions with reference point at (0, 0).

    Args:
        position(np.ndarray): Positions of spins or vectors( or any other given quantity written in the STM-format)
        within the xy-plane

        referencepoint(np.ndarray): Reference point in the plane for the distance calculations

    Returns:
        distances to neighbor shells from reference point within 2d plane
    """
    if np.shape(position)[1] != 2 or np.shape(referencepoint)[0] != 2:
        raise ValueError('This tabledist-function only accepts positions within a plane with two coordinates.')
    return np.unique(np.round_(np.linalg.norm(position - referencepoint, axis=1), decimals=5))


def calculate_phi_theta(spin: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Calculates the spherical coordinates of an array of spins or vectors:

    Args:
        spin(np.ndarray): spins of the spin configuration (could be used for eigenvectors as well).
        Format [[sx1,sy1,sz1],...,[sxn,syn.szn]]

    Returns:
        phi(np.ndarray): polar angle for each spin in degree
        theta(np.ndarray): azimutal angle for each spin in degree
        length(np.ndarray): length of spin. Should be 1 for spins but different from one in the case of eigenvectors.
    """
    l_length = np.linalg.norm(spin, axis=1)
    l_length_ip = np.linalg.norm(spin[:, :2], axis=1)
    l_phi = np.arctan2(spin[:, 1], spin[:, 0]) * 180 / np.pi
    l_theta = np.arctan2(l_length_ip, spin[:, 2]) * 180 / np.pi
    return l_phi, l_theta, l_length


def calculate_colorcode_azimut(theta: np.ndarray) -> List[List[float]]:
    r"""
    Calculates the color code (adapted from SpinD code) for the azimutal orientation of spins. Spins pointing into the
    +z-direction will be painted in red as spins pointing in the -z-direction will be painted in blue. In plane spins
    will be painted in green no matter the polar angle.

    Args:
        phi(np.ndarray): polar angle for each spin in degree
        theta(np.ndarray): azimutal angle for each spin in degree

    Returns:
        the colorcode for the azimutal angle for each spin [[R1,B1,G1],...,[Rn,Bn,Gn]]
    """
    colorcode = []
    for th in theta:
        C = 2 * np.pi / 3
        D = 5
        E = np.pi * 2 * th / 300
        R = D * np.cos(E)
        G = D * np.cos(E + C)
        B = D * np.cos(E + 2 * C)
        if R <= 1e-6:
            R = 0
        if G <= 1e-6:
            G = 0
        if B <= 1e-6:
            B = 0
        colorcode.append([R, B, G])
    return colorcode


def angle_between(v1, v2):
    """
    Returns:
         the angle in radians between vectors 'v1' and 'v2':
    """
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.math.atan2(np.linalg.det([v1,v2]),np.dot(v1,v2))


def pointinpolygon(point: np.ndarray, vertices: np.ndarray) -> bool:
    r"""
    If only a subset of the lattice shall be shown one has to calculate whether a given point lies within a polygon.
    This refers to the following problem and algorithms:
    https://en.wikipedia.org/wiki/Point_in_polygon
    This problem is normally adressed either through ray tracing or calculating the winding number. However both
    complexities are O(n), but the winding number calculation involves inverse trigonometric function that are comp.
    costly.

    Here a simple winding number approach is chosen.

    Args:
         point(np.ndarray): point which shall be tested to lie within a polygon

         vertices(np.ndarray): vertices of the polygon (they have to be in the order along the contour. (It doesn't
         matter if they're given cw or ccw). Format vertices = [[v1x,v1y,v1z],..., [vNx,vNy,vNz]], where N is the number
         of vertices.
    """
    l_anglesum = 0
    for (idx,vertex) in enumerate(vertices):
        if idx == len(vertices)-1:
            l_next_vertex = vertices[0]
        else:
            l_next_vertex = vertices[idx + 1]
        l_anglesum += angle_between(vertex - point, l_next_vertex - point)
    if abs(abs(l_anglesum) - 2 * np.pi) <= 1e-2:
        return True
    elif abs(l_anglesum) <= 1e-2:
        return False
    else:
        raise ValueError('Error during calculation of winding number')

