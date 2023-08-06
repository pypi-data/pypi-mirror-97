# -*- coding: utf-8 -*-
r"""
abstract class for all cameras
"""
from vapory import Camera
from abc import ABC, abstractmethod


class ICamera(ABC):
    r"""
    abstract class for cameras
    """

    @property
    @abstractmethod
    def cam(self) -> Camera:
        r"""
        Returns:
             the camera
        """