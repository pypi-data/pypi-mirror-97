# -*- coding: utf-8 -*-
r"""
Module containing different camera classes
"""
from vapory import Camera
from typing import Union, List, Tuple
from povray.predefined_povrayobjects.icamera import ICamera
import numpy as np


def rotationmatrix(angle: float) -> np.ndarray:
    r"""
    Calculates the rotationmatrix as need for the definition of the camera in povray (left handed system)

    Args:
        angle(float): angle of rotation around x axis

    Returns:
        rotation matrix as np ndarray
    """
    return np.array([[1, 0, 0],
                     [0, np.cos(np.radians(90 - angle)), -1 * np.sin(np.radians(90 - angle))],
                     [0, np.sin(np.radians(90 - angle)), np.cos(np.radians(90 - angle))]])


class CCameraForSpinLattice(ICamera):
    r"""
    Camera class for spin lattices. Might be used for spin configuration as well as for eigenvectors.
    """

    def __init__(self, position: np.ndarray, location: Union[None, List[float]] = None,
                 lookat: Union[None, List[float]] = None, viewangle: float = 90,
                 viewdistance: Union[float, None] = None, translatelookatz: float = 0.0) -> None:
        r"""
        initializes the camera which is accesible through the property cam.

        Args:
            position(np.ndarray): Numpy arrays of the positions within the spin lattice. Format [[x1,y1,z1],....]

            location(List[float]): location of the observer. Default value is None. In that case the location will be
            automatically set with the use of the positions of the spins in the source file.

            lookat(List[float]): location of the observed point. Default value is None. In that case the location will
            be automatically set with the use of the positions of the spins in the source file.

            viewangle(float): Angle for vector from location to lookat. Default angle is 90 degree, which corresponds
            to a view from the top of the spin configuration. Will be used only if location and lookat are None

            viewdistance(float): Distance from the camera to the observed point. Default distance is None. Will be used
            only if location and lookat are None and if it is different from None. In case that location and lookat are
            not defined, a viewangle is selected and this parameter is None the distance will be calculated automatic
            from the spin configuration itself.

            translatelookatz(float): shift observed point in z direction (used in multilayer systems)
        """
        self._camera = self._load_camera(position, location, lookat, viewangle, viewdistance, translatelookatz)

    @classmethod
    def _load_camera(cls, position: np.ndarray, location: Union[None, List[float]], lookat: Union[None, List[float]],
                     viewangle: float, viewdistance: Union[float, None], translatelookatz: float) -> Camera:
        r"""
        Loads the camera based either on user input or, per default, from spin configuration itself.

        Args:
            location(List[float]): location of observer
            lookat(List[float]): location of observed point
            viewangle(float): incident camera angle (90 means perpendicular to plane)
            viewdistance(float): distance of camera to observer
            translatelookatz(float): shift observed point in z direction (used in multilayer systems)

        Returns:
            An instance of vaporys (povrays) Camera
        """
        l_angle = 40
        if location is None and lookat is None:
            # determine center of spin configuration (in cartesians this the centroid of a point cloud is just the mean)
            # if any coordinate of the centroid is less than 1e-8 it is set to zero.
            l_lookat = np.array([0 if abs(coord) <= 1e-8 else coord for coord in (np.mean(position, axis=0))]) + np.array(
                [0.0, 0.0, translatelookatz])
            # rotate orthogonal vec
            l_lookdir = rotationmatrix(viewangle).dot(np.array([0, 0, 1]))
            # norm view direction and remove small entries
            l_lookdir_vec = [0 if abs(ld) <= 1e-8 else ld for ld in l_lookdir / np.linalg.norm(l_lookdir)]
            if viewdistance is None:
                # if viewdistance is not given calculate from extent of spin configuration in x direction
                extent_x = 0.5 * (np.max(position[:, 0]) - np.min(position[:, 0]))
                viewdistance = extent_x / np.tan(np.radians(l_angle / 2))
            l_location = l_lookat + viewdistance * np.array(l_lookdir_vec)
        elif location is None:
            l_lookat = lookat
            # rotate orthogonal vec
            l_lookdir = rotationmatrix(viewangle).dot(np.array([0, 0, 1]))
            # norm view direction and remove small entries
            l_lookdir_vec = [0 if abs(ld) <= 1e-8 else ld for ld in l_lookdir / np.linalg.norm(l_lookdir)]
            if viewdistance is None:
                # if viewdistance is not given calculate from extent of spin configuratin in x direction
                extent_x = 0.5 * (np.max(position[:, 0]) - np.min(position[:, 0]))
                viewdistance = extent_x / np.tan(np.radians(l_angle / 2))
            l_location = np.array(l_lookat) + viewdistance * np.array(l_lookdir_vec)
        elif lookat is None:
            l_location = location
            l_lookat = np.array([0 if abs(coord) <= 1e-8 else coord for coord in (np.mean(position, axis=0))]) + np.array(
                [0.0, 0.0, translatelookatz])
        else:
            l_location = location
            l_lookat = lookat

        return Camera('location', list(l_location), 'sky', [0, 0, 1], 'look_at', list(l_lookat), 'right', [1, 0, 0],
                      'angle', l_angle)

    @property
    def cam(self) -> Camera:
        r"""
        Returns:
            the camera
        """
        return self._camera
