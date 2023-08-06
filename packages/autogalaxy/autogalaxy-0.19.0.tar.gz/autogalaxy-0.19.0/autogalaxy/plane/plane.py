import numpy as np

from autoarray.inversion import inversions as inv
from autoarray.inversion import pixelizations as pix
from autoarray.structures.arrays import values
from autoarray.structures.arrays.two_d import array_2d
from autoarray.structures.grids.two_d import grid_2d_irregular
from autoarray.structures.grids import grid_decorators
from autoarray.structures import visibilities as vis
from autogalaxy import exc
from autogalaxy import lensing
from autogalaxy.galaxy import galaxy as g
from autogalaxy.util import plane_util


class AbstractPlane(lensing.LensingObject):
    def __init__(self, redshift, galaxies):
        """A plane of galaxies where all galaxies are at the same redshift.

        Parameters
        -----------
        redshift : float or None
            The redshift of the plane.
        galaxies : [Galaxy]
            The list of galaxies in this plane.
        """

        if redshift is None:

            if not galaxies:
                raise exc.PlaneException(
                    "No redshift and no galaxies were input to a Plane. A redshift for the Plane therefore cannot be"
                    "determined"
                )
            elif not all(
                [galaxies[0].redshift == galaxy.redshift for galaxy in galaxies]
            ):
                redshift = np.mean([galaxy.redshift for galaxy in galaxies])
            else:
                redshift = galaxies[0].redshift

        self.redshift = redshift
        self.galaxies = galaxies

    @property
    def galaxy_redshifts(self):
        return [galaxy.redshift for galaxy in self.galaxies]

    @property
    def has_light_profile(self):
        if self.galaxies is not None:
            return any(
                list(map(lambda galaxy: galaxy.has_light_profile, self.galaxies))
            )

    @property
    def has_mass_profile(self):
        if self.galaxies is not None:
            return any(list(map(lambda galaxy: galaxy.has_mass_profile, self.galaxies)))

    @property
    def has_pixelization(self):
        return any([galaxy.pixelization for galaxy in self.galaxies])

    @property
    def has_regularization(self):
        return any([galaxy.regularization for galaxy in self.galaxies])

    @property
    def galaxies_with_light_profile(self):
        return list(filter(lambda galaxy: galaxy.has_light_profile, self.galaxies))

    @property
    def galaxies_with_mass_profile(self):
        return list(filter(lambda galaxy: galaxy.has_mass_profile, self.galaxies))

    @property
    def galaxies_with_pixelization(self):
        return list(filter(lambda galaxy: galaxy.has_pixelization, self.galaxies))

    @property
    def galaxies_with_regularization(self):
        return list(filter(lambda galaxy: galaxy.has_regularization, self.galaxies))

    @property
    def pixelization(self):

        if len(self.galaxies_with_pixelization) == 0:
            return None
        if len(self.galaxies_with_pixelization) == 1:
            return self.galaxies_with_pixelization[0].pixelization
        elif len(self.galaxies_with_pixelization) > 1:
            raise exc.PixelizationException(
                "The number of galaxies with pixelizations in one plane is above 1"
            )

    @property
    def regularization(self):

        if len(self.galaxies_with_regularization) == 0:
            return None
        if len(self.galaxies_with_regularization) == 1:
            return self.galaxies_with_regularization[0].regularization
        elif len(self.galaxies_with_regularization) > 1:
            raise exc.PixelizationException(
                "The number of galaxies with regularizations in one plane is above 1"
            )

    @property
    def hyper_galaxy_image_of_galaxy_with_pixelization(self):
        galaxies_with_pixelization = self.galaxies_with_pixelization
        if galaxies_with_pixelization:
            return galaxies_with_pixelization[0].hyper_galaxy_image

    @property
    def has_hyper_galaxy(self):
        return any(list(map(lambda galaxy: galaxy.has_hyper_galaxy, self.galaxies)))

    @property
    def point_source_dict(self):

        point_source_dict = {}

        for galaxy in self.galaxies:
            for key, value in galaxy.point_source_dict.items():
                point_source_dict[key] = value

        return point_source_dict

    @property
    def mass_profiles(self):
        return [
            item
            for mass_profile in self.mass_profiles_of_galaxies
            for item in mass_profile
        ]

    @property
    def mass_profiles_of_galaxies(self):
        return [
            galaxy.mass_profiles for galaxy in self.galaxies if galaxy.has_mass_profile
        ]

    def extract_attribute(self, cls, name):
        """
        Returns an attribute of a class in `Plane` as a `ValueIrregular` or `Grid2DIrregular` object.

        For example, if a plane has a galaxy which two light profiles and we want its axis-ratios, the following:

        `plane.extract_attribute(cls=LightProfile, name="axis_ratio")`

        would return:

        ValuesIrregular(values=[axis_ratio_0, axis_ratio_1])

        If a galaxy has three mass profiles and we want their centres, the following:

        `plane.extract_attribute(cls=MassProfile, name="centres")`

        would return:

        GridIrregular2D(grid=[(centre_y_0, centre_x_0), (centre_y_1, centre_x_1), (centre_y_2, centre_x_2)])

        This is used for visualization, for example plotting the centres of all mass profiles colored by their profile.
        """

        def extract(value, name):

            try:
                return getattr(value, name)
            except (AttributeError, IndexError):
                return None

        attributes = [
            extract(value, name)
            for galaxy in self.galaxies
            for value in galaxy.__dict__.values()
            if isinstance(value, cls)
        ]

        if attributes == []:
            return None
        elif isinstance(attributes[0], float):
            return values.ValuesIrregular(values=attributes)
        elif isinstance(attributes[0], tuple):
            return grid_2d_irregular.Grid2DIrregular(grid=attributes)

    def extract_attributes_of_galaxies(self, cls, name, filter_nones=False):
        """
        Returns an attribute of a class in the plane as a list of `ValueIrregular` or `Grid2DIrregular` objects,
        where the list indexes correspond to each galaxy in the plane..

        For example, if a plane has two galaxies which each have a light profile the following:

        `plane.extract_attributes_of_galaxies(cls=LightProfile, name="axis_ratio")`

        would return:

        [ValuesIrregular(values=[axis_ratio_0]), ValuesIrregular(values=[axis_ratio_1])]

        If a plane has two galaxies, the first with a mass profile and the second with two mass profiles ,the following:

        `plane.extract_attributes_of_galaxies(cls=MassProfile, name="centres")`

        would return:
        [
            Grid2DIrregular(grid=[(centre_y_0, centre_x_0)]),
            Grid2DIrregular(grid=[(centre_y_0, centre_x_0), (centre_y_1, centre_x_1)])
        ]

        If a Profile does not have a certain entry, it is replaced with a None. Nones can be removed by
        setting `filter_nones=True`.

        This is used for visualization, for example plotting the centres of all mass profiles colored by their profile.
        """
        if filter_nones:

            return [
                galaxy.extract_attribute(cls=cls, name=name)
                for galaxy in self.galaxies
                if galaxy.extract_attribute(cls=cls, name=name) is not None
            ]

        else:

            return [
                galaxy.extract_attribute(cls=cls, name=name) for galaxy in self.galaxies
            ]


class AbstractPlaneLensing(AbstractPlane):
    def __init__(self, redshift, galaxies):
        super().__init__(redshift=redshift, galaxies=galaxies)

    @grid_decorators.grid_like_to_structure
    def image_from_grid(self, grid):
        """
        Returns the profile-image plane image of the list of galaxies of the plane's sub-grid, by summing the
        individual images of each galaxy's light profile.

        The image is calculated on the sub-grid and binned-up to the original grid by taking the mean
        value of every set of sub-pixels, provided the *returned_binned_sub_grid* bool is `True`.

        If the plane has no galaxies (or no galaxies have mass profiles) an arrays of all zeros the shape of the plane's
        sub-grid is returned.

        Parameters
        -----------

        """
        if self.galaxies:
            return sum(
                map(lambda galaxy: galaxy.image_from_grid(grid=grid), self.galaxies)
            )
        return np.zeros((grid.shape[0],))

    def images_of_galaxies_from_grid(self, grid):
        return list(
            map(lambda galaxy: galaxy.image_from_grid(grid=grid), self.galaxies)
        )

    def padded_image_from_grid_and_psf_shape(self, grid, psf_shape_2d):

        padded_grid = grid.padded_grid_from_kernel_shape(
            kernel_shape_native=psf_shape_2d
        )

        return self.image_from_grid(grid=padded_grid)

    @grid_decorators.grid_like_to_structure
    def convergence_from_grid(self, grid):
        """
        Returns the convergence of the list of galaxies of the plane's sub-grid, by summing the individual convergences \
        of each galaxy's mass profile.

        The convergence is calculated on the sub-grid and binned-up to the original grid by taking the mean
        value of every set of sub-pixels, provided the *returned_binned_sub_grid* bool is `True`.

        If the plane has no galaxies (or no galaxies have mass profiles) an arrays of all zeros the shape of the plane's
        sub-grid is returned.

        Parameters
        -----------
        grid : Grid2D
            The grid (or sub) of (y,x) arc-second coordinates at the centre of every unmasked pixel which the \
            potential is calculated on.
        galaxies : [g.Galaxy]
            The galaxies whose mass profiles are used to compute the surface densities.
        """
        if self.galaxies:
            return sum(map(lambda g: g.convergence_from_grid(grid=grid), self.galaxies))
        return np.zeros(shape=(grid.shape[0],))

    @grid_decorators.grid_like_to_structure
    def potential_from_grid(self, grid):
        """
        Returns the potential of the list of galaxies of the plane's sub-grid, by summing the individual potentials \
        of each galaxy's mass profile.

        The potential is calculated on the sub-grid and binned-up to the original grid by taking the mean
        value of every set of sub-pixels, provided the *returned_binned_sub_grid* bool is `True`.

        If the plane has no galaxies (or no galaxies have mass profiles) an arrays of all zeros the shape of the plane's
        sub-grid is returned.

        Parameters
        -----------
        grid : Grid2D
            The grid (or sub) of (y,x) arc-second coordinates at the centre of every unmasked pixel which the \
            potential is calculated on.
        galaxies : [g.Galaxy]
            The galaxies whose mass profiles are used to compute the surface densities.
        """
        if self.galaxies:
            return sum(map(lambda g: g.potential_from_grid(grid=grid), self.galaxies))
        return np.zeros((grid.shape[0]))

    @grid_decorators.grid_like_to_structure
    def deflections_from_grid(self, grid):
        if self.galaxies:
            return sum(map(lambda g: g.deflections_from_grid(grid=grid), self.galaxies))
        return np.zeros(shape=(grid.shape[0], 2))

    @grid_decorators.grid_like_to_structure
    def traced_grid_from_grid(self, grid):
        """Trace this plane's grid_stacks to the next plane, using its deflection angles."""
        return grid - self.deflections_from_grid(grid=grid)


class AbstractPlaneData(AbstractPlaneLensing):
    def __init__(self, redshift, galaxies):

        super().__init__(redshift=redshift, galaxies=galaxies)

    def blurred_image_from_grid_and_psf(self, grid, psf, blurring_grid):

        image = self.image_from_grid(grid=grid)

        blurring_image = self.image_from_grid(grid=blurring_grid)

        return psf.convolved_array_from_array_and_mask(
            array=image.native_binned + blurring_image.native_binned, mask=grid.mask
        )

    def blurred_images_of_galaxies_from_grid_and_psf(self, grid, psf, blurring_grid):
        return [
            galaxy.blurred_image_from_grid_and_psf(
                grid=grid, psf=psf, blurring_grid=blurring_grid
            )
            for galaxy in self.galaxies
        ]

    def blurred_image_from_grid_and_convolver(self, grid, convolver, blurring_grid):

        image = self.image_from_grid(grid=grid)

        blurring_image = self.image_from_grid(grid=blurring_grid)

        return convolver.convolved_image_from_image_and_blurring_image(
            image=image, blurring_image=blurring_image
        )

    def blurred_images_of_galaxies_from_grid_and_convolver(
        self, grid, convolver, blurring_grid
    ):
        return [
            galaxy.blurred_image_from_grid_and_convolver(
                grid=grid, convolver=convolver, blurring_grid=blurring_grid
            )
            for galaxy in self.galaxies
        ]

    def unmasked_blurred_image_from_grid_and_psf(self, grid, psf):

        padded_grid = grid.padded_grid_from_kernel_shape(
            kernel_shape_native=psf.shape_native
        )

        padded_image = self.image_from_grid(grid=padded_grid)

        return padded_grid.mask.unmasked_blurred_array_from_padded_array_psf_and_image_shape(
            padded_array=padded_image, psf=psf, image_shape=grid.mask.shape
        )

    def unmasked_blurred_image_of_galaxies_from_grid_and_psf(self, grid, psf):

        padded_grid = grid.padded_grid_from_kernel_shape(
            kernel_shape_native=psf.shape_native
        )

        unmasked_blurred_images_of_galaxies = []

        for galaxy in self.galaxies:

            padded_image_1d = galaxy.image_from_grid(grid=padded_grid)

            unmasked_blurred_array_2d = padded_grid.mask.unmasked_blurred_array_from_padded_array_psf_and_image_shape(
                padded_array=padded_image_1d, psf=psf, image_shape=grid.mask.shape
            )

            unmasked_blurred_images_of_galaxies.append(unmasked_blurred_array_2d)

        return unmasked_blurred_images_of_galaxies

    def profile_visibilities_from_grid_and_transformer(self, grid, transformer):

        if self.galaxies:
            image = self.image_from_grid(grid=grid)
            return transformer.visibilities_from_image(image=image)
        else:
            return vis.Visibilities.zeros(
                shape_slim=(transformer.uv_wavelengths.shape[0],)
            )

    def profile_visibilities_of_galaxies_from_grid_and_transformer(
        self, grid, transformer
    ):
        return [
            galaxy.profile_visibilities_from_grid_and_transformer(
                grid=grid, transformer=transformer
            )
            for galaxy in self.galaxies
        ]

    def sparse_image_plane_grid_from_grid(
        self, grid, settings_pixelization=pix.SettingsPixelization()
    ):

        if not self.has_pixelization:
            return None

        hyper_galaxy_image = self.hyper_galaxy_image_of_galaxy_with_pixelization

        return self.pixelization.sparse_grid_from_grid(
            grid=grid, hyper_image=hyper_galaxy_image, settings=settings_pixelization
        )

    def mapper_from_grid_and_sparse_grid(
        self,
        grid,
        sparse_grid,
        sparse_image_plane_grid=None,
        settings_pixelization=pix.SettingsPixelization(),
    ):

        galaxies_with_pixelization = list(
            filter(lambda galaxy: galaxy.pixelization is not None, self.galaxies)
        )

        if len(galaxies_with_pixelization) == 0:
            return None
        if len(galaxies_with_pixelization) == 1:

            pixelization = galaxies_with_pixelization[0].pixelization

            return pixelization.mapper_from_grid_and_sparse_grid(
                grid=grid,
                sparse_grid=sparse_grid,
                sparse_image_plane_grid=sparse_image_plane_grid,
                hyper_image=galaxies_with_pixelization[0].hyper_galaxy_image,
                settings=settings_pixelization,
            )

        elif len(galaxies_with_pixelization) > 1:
            raise exc.PixelizationException(
                "The number of galaxies with pixelizations in one plane is above 1"
            )

    def inversion_imaging_from_grid_and_data(
        self,
        grid,
        image,
        noise_map,
        convolver,
        settings_pixelization=pix.SettingsPixelization(),
        settings_inversion=inv.SettingsInversion(),
    ):

        sparse_grid = self.sparse_image_plane_grid_from_grid(grid=grid)

        mapper = self.mapper_from_grid_and_sparse_grid(
            grid=grid,
            sparse_grid=sparse_grid,
            settings_pixelization=settings_pixelization,
        )

        return inv.InversionImagingMatrix.from_data_mapper_and_regularization(
            image=image,
            noise_map=noise_map,
            convolver=convolver,
            mapper=mapper,
            regularization=self.regularization,
            settings=settings_inversion,
        )

    def inversion_interferometer_from_grid_and_data(
        self,
        grid,
        visibilities,
        noise_map,
        transformer,
        settings_pixelization=pix.SettingsPixelization(),
        settings_inversion=inv.SettingsInversion(),
    ):

        sparse_grid = self.sparse_image_plane_grid_from_grid(grid=grid)

        mapper = self.mapper_from_grid_and_sparse_grid(
            grid=grid,
            sparse_grid=sparse_grid,
            settings_pixelization=settings_pixelization,
        )

        return inv.AbstractInversionInterferometer.from_data_mapper_and_regularization(
            visibilities=visibilities,
            noise_map=noise_map,
            transformer=transformer,
            mapper=mapper,
            regularization=self.regularization,
            settings=settings_inversion,
        )

    def plane_image_from_grid(self, grid):
        return plane_util.plane_image_of_galaxies_from(
            shape=grid.mask.shape,
            grid=grid.mask.unmasked_grid_sub_1,
            galaxies=self.galaxies,
        )

    def hyper_noise_map_from_noise_map(self, noise_map):
        hyper_noise_maps = self.hyper_noise_maps_of_galaxies_from_noise_map(
            noise_map=noise_map
        )
        return sum(hyper_noise_maps)

    def hyper_noise_maps_of_galaxies_from_noise_map(self, noise_map):
        """For a contribution map and noise-map, use the model hyper_galaxy galaxies to compute a hyper noise-map.

        Parameters
        -----------
        noise_map : imaging.NoiseMap or ndarray
            An arrays describing the RMS standard deviation error in each pixel, preferably in units of electrons per
            second.
        """
        hyper_noise_maps = []

        for galaxy in self.galaxies:

            if galaxy.has_hyper_galaxy:

                hyper_noise_map_1d = galaxy.hyper_galaxy.hyper_noise_map_from_hyper_images_and_noise_map(
                    noise_map=noise_map,
                    hyper_model_image=galaxy.hyper_model_image,
                    hyper_galaxy_image=galaxy.hyper_galaxy_image,
                )

                hyper_noise_maps.append(hyper_noise_map_1d)

            else:

                hyper_noise_map = array_2d.Array2D.manual_mask(
                    array=np.zeros(noise_map.mask.mask_sub_1.pixels_in_mask),
                    mask=noise_map.mask.mask_sub_1,
                )

                hyper_noise_maps.append(hyper_noise_map)

        return hyper_noise_maps

    @property
    def contribution_map(self):

        contribution_maps = self.contribution_maps_of_galaxies

        contribution_maps = [i for i in contribution_maps if i is not None]

        if contribution_maps:
            return sum(contribution_maps)
        else:
            return None

    @property
    def contribution_maps_of_galaxies(self):

        contribution_maps = []

        for galaxy in self.galaxies:

            if galaxy.hyper_galaxy is not None:

                contribution_maps.append(galaxy.contribution_map)

            else:

                contribution_maps.append(None)

        return contribution_maps

    def galaxy_image_dict_from_grid(self, grid) -> {g.Galaxy: np.ndarray}:
        """
        A dictionary associating galaxies with their corresponding model images
        """

        galaxy_image_dict = dict()

        images_of_galaxies = self.images_of_galaxies_from_grid(grid=grid)
        for (galaxy_index, galaxy) in enumerate(self.galaxies):
            galaxy_image_dict[galaxy] = images_of_galaxies[galaxy_index]

        return galaxy_image_dict

    def galaxy_blurred_image_dict_from_grid_and_convolver(
        self, grid, convolver, blurring_grid
    ) -> {g.Galaxy: np.ndarray}:
        """
        A dictionary associating galaxies with their corresponding model images
        """

        galaxy_blurred_image_dict = dict()

        blurred_images_of_galaxies = self.blurred_images_of_galaxies_from_grid_and_convolver(
            grid=grid, convolver=convolver, blurring_grid=blurring_grid
        )
        for (galaxy_index, galaxy) in enumerate(self.galaxies):
            galaxy_blurred_image_dict[galaxy] = blurred_images_of_galaxies[galaxy_index]

        return galaxy_blurred_image_dict

    def galaxy_profile_visibilities_dict_from_grid_and_transformer(
        self, grid, transformer
    ) -> {g.Galaxy: np.ndarray}:
        """
        A dictionary associating galaxies with their corresponding model images
        """

        galaxy_profile_visibilities_image_dict = dict()

        profile_visibilities_of_galaxies = self.profile_visibilities_of_galaxies_from_grid_and_transformer(
            grid=grid, transformer=transformer
        )
        for (galaxy_index, galaxy) in enumerate(self.galaxies):
            galaxy_profile_visibilities_image_dict[
                galaxy
            ] = profile_visibilities_of_galaxies[galaxy_index]

        return galaxy_profile_visibilities_image_dict


class Plane(AbstractPlaneData):
    def __init__(self, redshift=None, galaxies=None):

        super(Plane, self).__init__(redshift=redshift, galaxies=galaxies)


class PlaneImage:
    def __init__(self, array, grid):

        self.array = array
        self.grid = grid
