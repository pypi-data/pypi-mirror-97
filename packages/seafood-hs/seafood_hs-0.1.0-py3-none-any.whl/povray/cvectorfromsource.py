# -*- coding: utf-8 -*-
r"""
Classes for visualization of eigenvector configurations from STM files.

-CPovVectorSimpleMono: @todo

-CPovVectorSimpleBilayer: class for simple visualizations of bilayer systems
"""
from povray.ipovfromsource import IPovFromSource, PathLike
from povray.utilities.spinconfiguration_utilities import calculate_phi_theta, calculate_colorcode_azimut, \
    identifylayers, tabledist, determine_layer_centers
from povray.predefined_povrayobjects.ccamera import CCameraForSpinLattice
import povray.utilities.colors as col
import vapory as vap
from typing import Union, List, Tuple
import pandas as pd
import numpy as np


class CPovVectorSimpleMono(IPovFromSource):
    r"""
    simple visualization class for eigenvectors for monolayer spin configurations.
    """

    def __init__(self) -> None:
        r"""
        initializes visualization of eigenvector for monolayer configuration
        """
        raise NotImplementedError('Visualizations of monolayer eigenvectors are not yet coded.')

    def __repr__(self) -> str:
        r"""
        Returns:
            representation of class
        """
        pass

    def __call__(self, outputpath: PathLike, width: float = 2000, height: float = 2000, antialiasing: bool = False,
                 antialiasingvalue: float = 0.001) -> None:
        r"""
        calls the rendering

        Args:
            outputpath(PathLike): name and path of created output. Default is stmpov in current directory
            width(float): width of the rendered image
            height(float): height of the rendered image
        """
        pass


class CPovVectorSimpleBilayer(IPovFromSource):
    r"""
    simple visualization class for eigenvectors for bilayer spin configurations.
    """

    def __init__(self, sourcefile: PathLike, location: Union[None, List[float]] = None,
                 lookat: Union[None, List[float]] = None, viewangle: float = 0,
                 viewdistance: Union[float, None] = None, stretch: float = 1.5, drawcircles: bool = True,
                 circleshift: np.ndarray = np.array([0.0, 0.0, 0.0])) -> None:
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

            drawcircles(bool): For better three dimensional visibility the next neighbors can be elucidated via circles.
        """
        self._sourcefile = sourcefile
        self._position, self._eigenvector = self._load_configuration(sourcefile=sourcefile)
        # stretch configuration by factor
        self._position = self._position * stretch
        self._phi, self._theta, self._length = calculate_phi_theta(spin=self._eigenvector)
        self._colorcode = calculate_colorcode_azimut(theta=self._theta)
        self._stretch = stretch
        self._camera = CCameraForSpinLattice(self._position, location, lookat, viewangle, viewdistance,
                                             translatelookatz=5 * stretch).cam
        self._objects = []
        self._objects.append(self._load_background())
        self._objects.extend(self._load_lightsources())
        self._objects.extend(self._load_vectors())
        if drawcircles:
            self._objects.extend(self._load_circles(circleshift=circleshift))

    def _load_circles(self, circleshift: np.ndarray, numberofcircles: int = 4, circlewidth: float = 0.025) -> List[
        vap.Object]:
        r"""
        Supports the visibility of the eigenvector representation via next neighbor shells. Written for arbitrary
        lattice types and arbitray numbers of layers. The reference point is the centroid of the layer.

        Args:
            circleshift(np.ndarray): Shift vector for all circles. This is sometimes necessary as the center of the
            circle is determined by the center of the lattice but the skyrmion or saddlepoint isnt alway directly
            centered (3-spin center)

            numberofcircles(int): if the parameter "drawcircles" is enabled this parameter defines the number of next
            neighbor shells drawn.

            circlewidth(float): width of the circle border
        """
        circles = []
        l_n, l_zcoords = identifylayers(self._position)
        for n in range(l_n):
            l_pos_layer = self._position[self._position[:, 2] - l_zcoords[n] <= 1e-3]
            l_centroidoflayer = np.array([coord if coord >=1e-8 else 0 for coord in np.mean(l_pos_layer, axis=0)])
            l_shells = tabledist(l_pos_layer[:, :2], referencepoint=l_centroidoflayer[:2] + circleshift[:2])[:numberofcircles]
            l_circlecenter = l_centroidoflayer + np.array([0.0, 0.0, 10 * l_zcoords[n]]) + circleshift
            for shell in l_shells:
                circles.append(vap.Object(vap.Macro('Circle_Line', l_circlecenter, shell, circlewidth, [0.0, 0.0, 1.0]),
                                          vap.Texture(vap.Pigment('color', col.lightgray()))))
        return circles

    def _load_vectors(self, headlength: float = 0.35, headwidth: float = 0.15, tailwidth: float = 0.08,
                      scale: float = 10, lowerlengthlimit: float = 1e-5) -> List[vap.Union]:
        r"""
        Create unions of povray cones and cylinders which represent arrows and returns them as a list. The union of the
        cone and the cylinder corresponds to the length L of the certain vector. The position of each vector is meant to
        be L / 2.

        If the length of the whole arrow is smaller than the headlength only the cone is displayed. This means that
        really short vectors are not displayed with the correct length.

        Args:
            headlength(float): height of the cone representing the head of the arrow (in real length)

            headwidth(float): base radius of the cone representing the head of the arrow

            tailwidth(float): radius of the cylinder representing the tail of the arrow

            scale(float): generally eigenvectors are small. For a visibility the scale parameter multiplies the length
            of each vector by this fixed "scale" value.

            lowerlengthlimit(float): Vectors which are shorter than this parameter are displayed as spheres.

        Returns:
            A list of vapory objects which will be translated in povray objects when rendering
        """
        l_vectors = []
        for (idx, pos) in enumerate(self._position):
            if self._length[idx] >= lowerlengthlimit:
                ll = scale * self._length[idx]
                if ll < headlength:
                    l_vectors.append(vap.Cone([0.0, 0.0, -1 * headlength / 2], headwidth,
                                     [0.0, 0.0, headlength / 2], 0,
                              'rotate', [0.0, self._theta[idx], 0.0],
                              'rotate', [0.0, 0.0, self._phi[idx]],
                              'translate', [pos[0], pos[1], 10 * pos[2]],
                              vap.Texture(vap.Pigment('color', self._colorcode[idx]))))
                else:
                    l_cylbase = [0.0, 0.0, -1 * ll / 2]
                    l_cylcap = [0.0, 0.0, ll / 2 - headlength]
                    l_conecap = [0.0, 0.0, ll / 2]
                    l_vectors.append(
                        vap.Union(vap.Cylinder(l_cylbase, l_cylcap, tailwidth),
                                  vap.Cone(l_cylcap, headwidth, l_conecap, 0),
                                  'rotate', [0.0, self._theta[idx], 0.0],
                                  'rotate', [0.0, 0.0, self._phi[idx]],
                                  'translate', [pos[0], pos[1], 10 * pos[2]],
                                  vap.Texture(vap.Pigment('color', self._colorcode[idx]))))
            else:
                l_vectors.append(
                    vap.Sphere([pos[0], pos[1], 10 * pos[2]], tailwidth,
                               vap.Texture(vap.Pigment('color', self._colorcode[idx])))
                )
        return l_vectors

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

    @classmethod
    def _load_configuration(cls, sourcefile: PathLike) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Loads eigenvector of spin configuration from sourcefile. The source file is expected to have white spaces as
        separators and has to have the following structure in each line: x y z vx vy vz v (Usual structure of
        eigenvector output from SpinD code)

        Args:
            sourcefile(PathLike): path to source file

        Returns:
            the positions, the vectors
        """
        l_df = pd.read_csv(sourcefile, sep=r'\s+', header=None)
        l_position = l_df.iloc[:, :3].to_numpy()
        l_vector = l_df.iloc[:, 3:6].to_numpy()
        return l_position, l_vector

    def __repr__(self) -> str:
        pass

    def __call__(self, outputpath: PathLike = 'vecpov.png', width: float = 2000, height: float = 2000,
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
                          included=['colors.inc', 'shapes.inc', 'analytical_g.inc'])
        if antialiasing:
            scene.render(outfile=PathLike, width=width, height=height, antialiasing=antialiasingvalue)
        else:
            scene.render(outfile=PathLike, width=width, height=height)
