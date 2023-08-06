import numpy as np
import pytest

import autogalaxy as ag
from autogalaxy import exc
from autogalaxy.mock import mock


class TestGalaxyFitData:
    def test__image_noise_map_and_mask(self, gal_data_7x7, sub_mask_7x7):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7, mask=sub_mask_7x7, use_image=True
        )

        assert galaxy_fit_data.pixel_scales == (1.0, 1.0)
        assert (galaxy_fit_data.galaxy_data.image.native == np.ones((7, 7))).all()
        assert (
            galaxy_fit_data.galaxy_data.noise_map.native == 2.0 * np.ones((7, 7))
        ).all()

        assert (galaxy_fit_data.image.slim == np.ones(9)).all()
        assert (galaxy_fit_data.noise_map.slim == 2.0 * np.ones(9)).all()

        assert (
            galaxy_fit_data.mask
            == np.array(
                [
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.image.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.noise_map.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

    def test__grid(
        self,
        gal_data_7x7,
        sub_mask_7x7,
        grid_7x7,
        sub_grid_7x7,
        blurring_grid_7x7,
        grid_iterate_7x7,
    ):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7,
            mask=sub_mask_7x7,
            use_image=True,
            grid_class=ag.Grid2D,
        )

        assert isinstance(galaxy_fit_data.grid, ag.Grid2D)
        assert (galaxy_fit_data.grid == sub_grid_7x7).all()

        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7,
            mask=sub_mask_7x7,
            use_image=True,
            grid_class=ag.Grid2DIterate,
        )

        assert isinstance(galaxy_fit_data.grid, ag.Grid2DIterate)
        assert (galaxy_fit_data.grid.slim_binned == grid_iterate_7x7).all()

        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7,
            mask=sub_mask_7x7,
            use_image=True,
            grid_class=ag.Grid2DInterpolate,
            pixel_scales_interp=1.0,
        )

        grid = ag.Grid2DInterpolate.from_mask(
            mask=sub_mask_7x7, pixel_scales_interp=1.0
        )

        assert isinstance(galaxy_fit_data.grid, ag.Grid2DInterpolate)
        assert (galaxy_fit_data.grid == grid).all()
        assert (galaxy_fit_data.grid.grid_interp == grid.grid_interp).all()
        assert (galaxy_fit_data.grid.vtx == grid.vtx).all()
        assert (galaxy_fit_data.grid.wts == grid.wts).all()

    def test__gal_data_7x7_image(self, gal_data_7x7, sub_mask_7x7):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7, mask=sub_mask_7x7, use_image=True
        )

        assert galaxy_fit_data.pixel_scales == (1.0, 1.0)
        assert (galaxy_fit_data.galaxy_data.image.native == np.ones((7, 7))).all()
        assert (
            galaxy_fit_data.galaxy_data.noise_map.native == 2.0 * np.ones((7, 7))
        ).all()

        assert (galaxy_fit_data.image.slim == np.ones(9)).all()
        assert (galaxy_fit_data.noise_map.slim == 2.0 * np.ones(9)).all()

        assert (
            galaxy_fit_data.mask
            == np.array(
                [
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.image.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.noise_map.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        galaxy = mock.MockGalaxy(value=1, shape=36)

        image = galaxy_fit_data.profile_quantity_from_galaxies(galaxies=[galaxy])

        assert (image.slim_binned == np.ones(9)).all()

        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.SphericalSersic(intensity=1.0))

        image_gal = galaxy.image_from_grid(grid=galaxy_fit_data.grid)

        image_gd = galaxy_fit_data.profile_quantity_from_galaxies(galaxies=[galaxy])

        assert (image_gal == image_gd).all()

    def test__gal_data_7x7_convergence(self, gal_data_7x7, sub_mask_7x7):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7, mask=sub_mask_7x7, use_convergence=True
        )

        assert galaxy_fit_data.pixel_scales == (1.0, 1.0)
        assert (galaxy_fit_data.galaxy_data.image.native == np.ones((7, 7))).all()
        assert (
            galaxy_fit_data.galaxy_data.noise_map.native == 2.0 * np.ones((7, 7))
        ).all()

        assert (galaxy_fit_data.image.slim == np.ones(9)).all()
        assert (galaxy_fit_data.noise_map.slim == 2.0 * np.ones(9)).all()

        assert (
            galaxy_fit_data.mask
            == np.array(
                [
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.image.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.noise_map.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        galaxy = mock.MockGalaxy(value=1, shape=36)

        convergence = galaxy_fit_data.profile_quantity_from_galaxies(galaxies=[galaxy])

        assert (convergence.slim_binned == np.ones(9)).all()

        galaxy = ag.Galaxy(
            redshift=0.5, mass=ag.mp.SphericalIsothermal(einstein_radius=1.0)
        )

        convergence_gal = galaxy.convergence_from_grid(grid=galaxy_fit_data.grid)

        convergence_gd = galaxy_fit_data.profile_quantity_from_galaxies(
            galaxies=[galaxy]
        )

        assert (convergence_gal == convergence_gd).all()

    def test__gal_data_7x7_potential(self, gal_data_7x7, sub_mask_7x7):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7, mask=sub_mask_7x7, use_potential=True
        )

        assert galaxy_fit_data.pixel_scales == (1.0, 1.0)
        assert (galaxy_fit_data.galaxy_data.image.native == np.ones((7, 7))).all()
        assert (
            galaxy_fit_data.galaxy_data.noise_map.native == 2.0 * np.ones((7, 7))
        ).all()

        assert (galaxy_fit_data.image.slim == np.ones(9)).all()
        assert (galaxy_fit_data.noise_map.slim == 2.0 * np.ones(9)).all()

        assert (
            galaxy_fit_data.mask
            == np.array(
                [
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.image.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.noise_map.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        galaxy = mock.MockGalaxy(value=1, shape=36)

        potential = galaxy_fit_data.profile_quantity_from_galaxies(galaxies=[galaxy])

        assert (potential.slim_binned == np.ones(9)).all()

        galaxy = ag.Galaxy(
            redshift=0.5, mass=ag.mp.SphericalIsothermal(einstein_radius=1.0)
        )

        potential_gal = galaxy.potential_from_grid(grid=galaxy_fit_data.grid)

        potential_gd = galaxy_fit_data.profile_quantity_from_galaxies(galaxies=[galaxy])

        assert (potential_gal == potential_gd).all()

    def test__gal_data_7x7_deflections_y(self, gal_data_7x7, sub_mask_7x7):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7, mask=sub_mask_7x7, use_deflections_y=True
        )
        assert galaxy_fit_data.pixel_scales == (1.0, 1.0)
        assert (galaxy_fit_data.galaxy_data.image.native == np.ones((7, 7))).all()
        assert (
            galaxy_fit_data.galaxy_data.noise_map.native == 2.0 * np.ones((7, 7))
        ).all()

        assert (galaxy_fit_data.image.slim == np.ones(9)).all()
        assert (galaxy_fit_data.noise_map.slim == 2.0 * np.ones(9)).all()

        assert (
            galaxy_fit_data.mask
            == np.array(
                [
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.image.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.noise_map.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        galaxy = mock.MockGalaxy(value=1, shape=36)

        deflections_y = galaxy_fit_data.profile_quantity_from_galaxies(
            galaxies=[galaxy]
        )

        assert (deflections_y.slim_binned == np.ones(9)).all()

        galaxy = ag.Galaxy(
            redshift=0.5, mass=ag.mp.SphericalIsothermal(einstein_radius=1.0)
        )

        deflections_gal = galaxy.deflections_from_grid(grid=galaxy_fit_data.grid)
        deflections_gal = np.asarray(
            [
                np.multiply(
                    deflections_gal.mask.sub_fraction,
                    deflections_gal[:, 0]
                    .reshape(-1, deflections_gal.mask.sub_length)
                    .sum(axis=1),
                ),
                np.multiply(
                    deflections_gal.mask.sub_fraction,
                    deflections_gal[:, 1]
                    .reshape(-1, deflections_gal.mask.sub_length)
                    .sum(axis=1),
                ),
            ]
        ).T

        deflections_gd = galaxy_fit_data.profile_quantity_from_galaxies(
            galaxies=[galaxy]
        )

        assert (deflections_gal[:, 0] == deflections_gd.slim_binned).all()

    def test__gal_data_7x7_deflections_x(self, gal_data_7x7, sub_mask_7x7):
        galaxy_fit_data = ag.MaskedGalaxyDataset(
            galaxy_data=gal_data_7x7, mask=sub_mask_7x7, use_deflections_x=True
        )

        assert galaxy_fit_data.pixel_scales == (1.0, 1.0)
        assert (galaxy_fit_data.galaxy_data.image.native == np.ones((7, 7))).all()
        assert (
            galaxy_fit_data.galaxy_data.noise_map.native == 2.0 * np.ones((7, 7))
        ).all()

        assert (galaxy_fit_data.image.slim == np.ones(9)).all()
        assert (galaxy_fit_data.noise_map.slim == 2.0 * np.ones(9)).all()

        assert (
            galaxy_fit_data.mask
            == np.array(
                [
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, False, False, False, True, True],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, True, True, True],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.image.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        assert (
            galaxy_fit_data.noise_map.native
            == np.array(
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            )
        ).all()

        galaxy = mock.MockGalaxy(value=1, shape=36)

        deflections_x = galaxy_fit_data.profile_quantity_from_galaxies(
            galaxies=[galaxy]
        )

        assert (deflections_x.slim_binned == np.ones(9)).all()

        galaxy = ag.Galaxy(
            redshift=0.5, mass=ag.mp.SphericalIsothermal(einstein_radius=1.0)
        )

        deflections_gal = galaxy.deflections_from_grid(grid=galaxy_fit_data.grid)
        deflections_gal = np.asarray(
            [
                np.multiply(
                    deflections_gal.mask.sub_fraction,
                    deflections_gal[:, 0]
                    .reshape(-1, deflections_gal.mask.sub_length)
                    .sum(axis=1),
                ),
                np.multiply(
                    deflections_gal.mask.sub_fraction,
                    deflections_gal[:, 1]
                    .reshape(-1, deflections_gal.mask.sub_length)
                    .sum(axis=1),
                ),
            ]
        ).T

        deflections_gd = galaxy_fit_data.profile_quantity_from_galaxies(
            galaxies=[galaxy]
        )

        assert (deflections_gal[:, 1] == deflections_gd.slim_binned).all()

    def test__no_use_method__raises_exception(
        self, image_7x7, noise_map_7x7, sub_mask_7x7
    ):
        gal_data_7x7 = ag.GalaxyData(
            image=image_7x7, noise_map=noise_map_7x7, pixel_scales=3.0
        )

        with pytest.raises(exc.GalaxyException):
            ag.MaskedGalaxyDataset(galaxy_data=gal_data_7x7, mask=sub_mask_7x7)

    def test__multiple_use_methods__raises_exception(
        self, image_7x7, noise_map_7x7, sub_mask_7x7
    ):
        gal_data_7x7 = ag.GalaxyData(
            image=image_7x7, noise_map=noise_map_7x7, pixel_scales=3.0
        )

        with pytest.raises(exc.GalaxyException):
            ag.MaskedGalaxyDataset(
                galaxy_data=gal_data_7x7,
                mask=sub_mask_7x7,
                use_image=True,
                use_convergence=True,
            )

        with pytest.raises(exc.GalaxyException):
            ag.MaskedGalaxyDataset(
                galaxy_data=gal_data_7x7,
                mask=sub_mask_7x7,
                use_image=True,
                use_potential=True,
            )

        with pytest.raises(exc.GalaxyException):
            ag.MaskedGalaxyDataset(
                galaxy_data=gal_data_7x7,
                mask=sub_mask_7x7,
                use_image=True,
                use_deflections_y=True,
            )

        with pytest.raises(exc.GalaxyException):
            ag.MaskedGalaxyDataset(
                galaxy_data=gal_data_7x7,
                mask=sub_mask_7x7,
                use_image=True,
                use_convergence=True,
                use_potential=True,
            )

        with pytest.raises(exc.GalaxyException):
            ag.MaskedGalaxyDataset(
                galaxy_data=gal_data_7x7,
                mask=sub_mask_7x7,
                use_image=True,
                use_convergence=True,
                use_potential=True,
                use_deflections_x=True,
            )
