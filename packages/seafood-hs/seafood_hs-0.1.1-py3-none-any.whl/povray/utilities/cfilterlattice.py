# -*- coding: utf-8 -*-
r"""
Classes for filtering the spin or eigenvector lattices that are load from source. Contains a base abstract filter
class and inheriting ones.
"""
from abc import ABC, abstractmethod
from povray.utilities.spinconfiguration_utilities import pointinpolygon
import numpy as np


class CFilterLattice(ABC):
    r"""
    Abstract base class for filtering lattices
    """

    @abstractmethod
    def applyfilter(self, tofilter: np.ndarray) -> np.ndarray:
        r"""
        """

    @abstractmethod
    def _filter(self, performfilteron: np.ndarray) -> np.ndarray:
        r"""
        """

    @abstractmethod
    def __init__(self, performfilteron: np.ndarray) -> None:
        r"""
        Initializes the filtering.

        Args:
            performfilteron(np.ndarray): The quantity to which the filter condition applies. Every quantity with the
            same shape as this quantity can be filtered based on the filtering performed for this input array using the
            method applyfilter.
        """


class CFilterHexAroundCenter(CFilterLattice):
    r"""
    Filters a hexagonal lattice around the center of the lattice.
    """

    def applyfilter(self, tofilter: np.ndarray) -> np.ndarray:
        r"""
        Performs the filtering based on the boolean condition derived for the quantity which was initialized in constr.
        the filter.

        Args:
            tofilter(np.ndarray): quantity which shall be filtered based one this filter instance. Has to have the same
            shape as performfilteron

        Returns:
            the filtered quantity
        """
        ind = np.where(self._condition)
        return tofilter[ind]

    def _filter(self, performfilteron: np.ndarray) -> np.ndarray:
        r"""
        performs filtering. The filtering is performed in an hexagonal area around the center of the lattice.

        Args:
            performfilteron(np.ndarray): quantity on which the filter is derived.

        Returns:
            A boolean numpy array which can be used via np.extract(condition, otherarray)
        """
        l_centroid = np.mean(performfilteron, axis=0)
        l_edgelength = np.max(performfilteron[:, 0]) - np.min(performfilteron[:, 0])
        l_edge_reduced = l_edgelength * self._percentage
        l_polygon = np.array([[0.0, 0.0], [0.5 * l_edge_reduced, np.sqrt(3) / 2 * l_edge_reduced], [l_edge_reduced, 0],
                              [0.5 * l_edge_reduced, -1 * np.sqrt(3) / 2 * l_edge_reduced]]) + np.array(
            [l_edgelength / 2 * (1 - self._percentage), 0.0])
        l_cond = []
        for position in performfilteron:
            l_cond.append(pointinpolygon(point=position[:2], vertices=l_polygon))
        return np.array(l_cond)

    def __init__(self, performfilteron: np.ndarray, percentage: float = 0.5) -> None:
        r"""
        initializes the filter

        Args:
             performfilteron(np.ndarray): quantity on which the filter is derived.
             percentage(float): percentage for edgelength_filtered / edgelength_unfiltered.
        """
        super().__init__(performfilteron)
        self._percentage = percentage
        self._condition = self._filter(performfilteron=performfilteron)
