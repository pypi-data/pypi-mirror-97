# -*- coding: utf-8 -*-
r"""
Abstract base class for all povray visualization that are created from a source file. E.g. SpinSTM-files or
Eigenvectors.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

PathLike = TypeVar("PathLike", str, Path)


class IPovFromSource(ABC):
    r"""
    Abstract base class for visualization of source files
    """

    @abstractmethod
    def __repr__(self) -> str:
        r"""
        Returns:
            string representation of visualization class
        """

    @abstractmethod
    def __call__(self, outputpath: PathLike, width: float = 2000, height: float = 2000, antialiasing: bool = False,
                 antialiasingvalue: float = 0.001) -> None:
        r"""
        calls the rendering

        Args:
            outputpath(PathLike): name and path of created output
            width(float): width of the rendered image
            height(float): height of the rendered image
            antialiasing(bool): bool whether rendering is done with antialiasing
            antialiasingvalue(float): value for antialiasing
        """
