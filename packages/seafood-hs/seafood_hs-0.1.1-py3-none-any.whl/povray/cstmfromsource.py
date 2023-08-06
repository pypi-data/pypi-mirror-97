# -*- coding: utf-8 -*-
r"""
Classes for visualization of spin configurations from STM files.

-CPovSTMSimpleMono: class for simple visualizations of monolayer systems

-CPovSTMSimpleBilayer: class for simple visualizations of bilayer systems
"""
from povray.ipovfromsource import IPovFromSource
from povray.predefined_povrayobjects.ccamera import CCameraForSpinLattice
from povray.utilities.spinconfiguration_utilities import calculate_phi_theta, calculate_colorcode_azimut
from povray.utilities.cfilterlattice import CFilterHexAroundCenter
from pathlib import Path
from typing import TypeVar, Tuple, List, Union
import vapory as vap
import numpy as np
import pandas as pd

PathLike = TypeVar("PathLike", str, Path)


class CPovSTMSimpleMono(IPovFromSource):
    r"""
    Class for simple visualization of STM source file.
    """

    def __call__(self, outputpath: PathLike = 'stmpov.png', width: float = 2000, height: float = 2000,
                 antialiasing: bool = False, antialiasingvalue: float = 0.001) -> None:
        r"""
        calls the rendering

        Args:
            outputpath(PathLike): name and path of created output. Default is stmpov in current directory
            width(float): width of the rendered image
            height(float): height of the rendered image
        """
        scene = vap.Scene(self._camera,
                          objects=self._objects,
                          included=['colors.inc', 'shapes.inc'])
        if antialiasing:
            scene.render(outfile=PathLike, width=width, height=height, antialiasing=antialiasingvalue)
        else:
            scene.render(outfile=PathLike, width=width, height=height)

    def __init__(self, sourcefile: PathLike, location: Union[None, List[float]] = None,
                 lookat: Union[None, List[float]] = None, viewangle: float = 90,
                 viewdistance: Union[float, None] = None, stretch: float = 1.5) -> None:
        r"""
        Initializes the visualization

        Args:
            sourcefile(PathLike): Path to source file of spin configuration

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

            stretch(float): Stretches the whole configuration by a factor for better visibility of cones

        """
        self._sourcefile = sourcefile
        self._position, self._spin = self._load_configuration(sourcefile=sourcefile)
        self._phi, self._theta, *_ = calculate_phi_theta(spin=self._spin)
        self._colorcode = calculate_colorcode_azimut(theta=self._theta)
        # stretching of lattice should be done before determining camera position. Otherwise camera could be wrong.
        self._position = self._position * stretch
        self._camera = CCameraForSpinLattice(self._position, location, lookat, viewangle, viewdistance).cam
        self._objects = []
        self._objects.append(self._load_background())
        self._objects.extend(self._load_lightsources())
        self._objects.extend(self._load_cones())

    @classmethod
    def _load_background(cls) -> vap.Background:
        r"""
        Returns:
            the background
        """
        return vap.Background('color Black')

    @classmethod
    def _load_lightsources(cls) -> List[vap.LightSource]:
        r"""
        Returns:
            the lightsources
        """
        return [vap.LightSource([12, -12, -12], 'color White', 'shadowless'),
                vap.LightSource([12, 0, -12], 'color White', 'area_light', [5, 0, 0], [0, 5, 0], 5, 5, 'adaptive', 1,
                                'jitter')]

    def _load_cones(self, length: float = 1.2, baseradius: float = 0.4) \
            -> List[vap.Cone]:
        r"""
        Create povray cones and returns them as a list

        Returns:
            A list of vapory cones which will be translated in povray cones when rendering
        """
        l_cones = []
        for (idx, pos) in enumerate(self._position):
            l_cones.append(vap.Cone([0.0, 0.0, length / 2], 0.0, [0.0, 0.0, -1 * length / 2], baseradius,
                                    'rotate', [0.0, self._theta[idx], 0.0],
                                    'rotate', [0.0, 0.0, self._phi[idx]],
                                    'translate', list(pos),
                                    vap.Texture(vap.Pigment('color', self._colorcode[idx]))))
        return l_cones

    @classmethod
    def _load_configuration(cls, sourcefile: PathLike) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Loads spin configuration from sourcefile. The source file is expected to have white spaces as separators and
        has to have the following structure in each line: x y z sx sy sz m (Usual structure of STM output from SpinD
        code)

        Args:
            sourcefile(PathLike): path to source file

        Returns:
            the positions, the spins
        """
        l_df = pd.read_csv(sourcefile, sep=r'\s+', header=None)
        l_position = l_df.iloc[:, :3].to_numpy()
        l_spin = l_df.iloc[:, 3:6].to_numpy()
        return l_position, l_spin

    def __repr__(self) -> str:
        r"""
        Returns:
            Representation of visualization class
        """
        return f"Representation of monolayer spin configuration with {len(self._position)} spins."

    @property
    def sourcefile(self) -> PathLike:
        r"""
        Returns:
             the source file
        """
        return self._sourcefile


class CPovSTMSimpleBilayer(IPovFromSource):
    r"""
    Class for simple visualization of STM source file.
    """

    def __call__(self, outputpath: PathLike = 'stmpov.png', width: float = 2000, height: float = 2000,
                 antialiasing: bool = False, antialiasingvalue: float = 0.001) -> None:
        r"""
        calls the rendering

        Args:
            outputpath(PathLike): name and path of created output. Default is stmpov in current directory
            width(float): width of the rendered image
            height(float): height of the rendered image
        """
        scene = vap.Scene(self._camera,
                          objects=self._objects,
                          included=['colors.inc', 'shapes.inc'])
        if antialiasing:
            scene.render(outfile=PathLike, width=width, height=height, antialiasing=antialiasingvalue)
        else:
            scene.render(outfile=PathLike, width=width, height=height)

    def __init__(self, sourcefile: PathLike, location: Union[None, List[float]] = None,
                 lookat: Union[None, List[float]] = None, viewangle: float = 0,
                 viewdistance: Union[float, None] = None, stretch: float = 1.51, filterlatt: bool = False,
                 filterkeyword: str = 'hexaroundcenter', percentage: float = 0.5) -> None:
        r"""
        Initializes the visualization

        Args:
            sourcefile(PathLike): Path to source file of spin configuration

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

            stretch(float): Stretches the whole configuration by a factor for better visibility of cones

            filterlatt(bool): boolean whether to filter the lattice to a specific region

            filterkeyword(str): decider string for factory patter, which filter algorithm shall be performed

            percentage(float): factor for some filtering algorithm. See the belonging implementation for details.
        """
        self._sourcefile = sourcefile
        self._position, self._spin = self._load_configuration(sourcefile=sourcefile)
        if filterlatt:
            self._filter_configuration(filterkeyword, percentage)
        self._phi, self._theta, *_ = calculate_phi_theta(spin=self._spin)
        self._colorcode = calculate_colorcode_azimut(theta=self._theta)
        self._position = self._position * stretch
        self._camera = CCameraForSpinLattice(self._position, location, lookat, viewangle, viewdistance,
                                             translatelookatz=5 * stretch).cam
        self._objects = []
        self._objects.append(self._load_background())
        self._objects.extend(self._load_lightsources())
        self._objects.extend(self._load_cones())

    def _filter_configuration(self, filterkeyword: str, percentage: float) -> None:
        r"""
        Sometimes one does not want to display the whole system. In most cases one only wants to look at an area around
        the center. This filtering operation takes the information for position and applies some filtering condition
        within the plane perpendicular to the z-direction. This is applied to all layers. The spin array is filtered the
        same way.

        Args:
            filterkeyword(str): Decider string for factory pattern of filter class.

            percentage(float): Some filters may need a percentage value to say how much of the lattice shall be filtered
            based on the original size.
        """
        if filterkeyword == 'hexaroundcenter':
            l_filter = CFilterHexAroundCenter(performfilteron=self._position, percentage=percentage)
        else:
            raise NotImplementedError('Filter not implemented yet.')
        self._position = l_filter.applyfilter(tofilter=self._position)
        self._spin = l_filter.applyfilter(tofilter=self._spin)

    @classmethod
    def _load_background(cls) -> vap.Background:
        r"""
        Returns:
            the background
        """
        return vap.Background('color Black')

    @classmethod
    def _load_lightsources(cls) -> List[vap.LightSource]:
        r"""
        Returns:
            the lightsources
        """
        return [vap.LightSource([12, -12, -12], 'color White', 'shadowless'),
                vap.LightSource([12, 0, -12], 'color White', 'area_light', [5, 0, 0], [0, 5, 0], 5, 5, 'adaptive', 1,
                                'jitter')]

    def _load_cones(self, length: float = 1.2, baseradius: float = 0.4) -> List[vap.Cone]:
        r"""
        Create povray cones and returns them as a list

        Returns:
            A list of vapory cones which will be translated in povray cones when rendering
        """
        l_cones = []
        for (idx, pos) in enumerate(self._position):
            l_cones.append(vap.Cone([0.0, 0.0, length / 2], 0.0, [0.0, 0.0, -1 * length / 2], baseradius,
                                    'rotate', [0.0, self._theta[idx], 0.0],
                                    'rotate', [0.0, 0.0, self._phi[idx]],
                                    'translate', [pos[0], pos[1], 10 * pos[2]],
                                    vap.Texture(vap.Pigment('color', self._colorcode[idx]))))
        return l_cones

    @classmethod
    def _load_configuration(cls, sourcefile: PathLike) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Loads spin configuration from sourcefile. The source file is expected to have white spaces as separators and
        has to have the following structure in each line: x y z sx sy sz m (Usual structure of STM output from SpinD
        code)

        Args:
            sourcefile(PathLike): path to source file

        Returns:
            the positions, the spins
        """
        l_df = pd.read_csv(sourcefile, sep=r'\s+', header=None)
        l_position = l_df.iloc[:, :3].to_numpy()
        l_spin = l_df.iloc[:, 3:6].to_numpy()
        return l_position, l_spin

    def __repr__(self) -> str:
        r"""
        Returns:
            Representation of visualization class
        """
        return f"Representation of bilayer spin configuration with {len(self._position)} spins."

    @property
    def sourcefile(self) -> PathLike:
        r"""
        Returns:
             the source file
        """
        return self._sourcefile
