import autogalaxy as ag
import numpy as np
import pytest
from autogalaxy import exc
from autogalaxy.util.plane_util import (
    plane_image_of_galaxies_from,
    ordered_plane_redshifts_from,
    ordered_plane_redshifts_with_slicing_from,
    galaxies_in_redshift_ordered_planes_from,
)


class TestPlaneImageFromGrid:
    def test__3x3_grid__extracts_max_min_coordinates__creates_grid_including_half_pixel_offset_from_edge(
        self,
    ):
        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        grid = np.array([[-1.5, -1.5], [1.5, 1.5]])

        plane_image = plane_image_of_galaxies_from(
            shape=(3, 3), grid=grid, galaxies=[galaxy], buffer=0.0
        )

        mask = ag.Mask2D.manual(
            mask=np.full(shape=(3, 3), fill_value=False), pixel_scales=1.0, sub_size=1
        )

        grid = ag.Grid2D.manual_mask(
            grid=np.array(
                [
                    [-1.0, -1.0],
                    [-1.0, 0.0],
                    [-1.0, 1.0],
                    [0.0, -1.0],
                    [0.0, 0.0],
                    [0.0, 1.0],
                    [1.0, -1.0],
                    [1.0, 0.0],
                    [1.0, 1.0],
                ]
            ),
            mask=mask,
        )

        plane_image_galaxy = galaxy.image_from_grid(grid)

        assert (plane_image.array == plane_image_galaxy).all()

    def test__3x3_grid__extracts_max_min_coordinates__ignores_other_coordinates_more_central(
        self,
    ):
        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        grid = np.array(
            [
                [-1.5, -1.5],
                [1.5, 1.5],
                [0.1, -0.1],
                [-1.0, 0.6],
                [1.4, -1.3],
                [1.5, 1.5],
            ]
        )

        plane_image = plane_image_of_galaxies_from(
            shape=(3, 3), grid=grid, galaxies=[galaxy], buffer=0.0
        )

        mask = ag.Mask2D.manual(
            mask=np.full(shape=(3, 3), fill_value=False), pixel_scales=1.0, sub_size=1
        )

        grid = ag.Grid2D.manual_mask(
            grid=np.array(
                [
                    [-1.0, -1.0],
                    [-1.0, 0.0],
                    [-1.0, 1.0],
                    [0.0, -1.0],
                    [0.0, 0.0],
                    [0.0, 1.0],
                    [1.0, -1.0],
                    [1.0, 0.0],
                    [1.0, 1.0],
                ]
            ),
            mask=mask,
        )

        plane_image_galaxy = galaxy.image_from_grid(grid=grid)

        assert (plane_image.array == plane_image_galaxy).all()

    def test__2x3_grid__shape_change_correct_and_coordinates_shift(self):
        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        grid = np.array([[-1.5, -1.5], [1.5, 1.5]])

        plane_image = plane_image_of_galaxies_from(
            shape=(2, 3), grid=grid, galaxies=[galaxy], buffer=0.0
        )

        mask = ag.Mask2D.manual(
            mask=np.full(shape=(2, 3), fill_value=False), pixel_scales=1.0, sub_size=1
        )

        grid = ag.Grid2D.manual_mask(
            grid=np.array(
                [
                    [-0.75, -1.0],
                    [-0.75, 0.0],
                    [-0.75, 1.0],
                    [0.75, -1.0],
                    [0.75, 0.0],
                    [0.75, 1.0],
                ]
            ),
            mask=mask,
        )

        plane_image_galaxy = galaxy.image_from_grid(grid=grid)

        assert (plane_image.array == plane_image_galaxy).all()

    def test__3x2_grid__shape_change_correct_and_coordinates_shift(self):
        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        grid = np.array([[-1.5, -1.5], [1.5, 1.5]])

        plane_image = plane_image_of_galaxies_from(
            shape=(3, 2), grid=grid, galaxies=[galaxy], buffer=0.0
        )

        mask = ag.Mask2D.manual(
            mask=np.full(shape=(3, 2), fill_value=False), pixel_scales=1.0, sub_size=1
        )

        grid = ag.Grid2D.manual_mask(
            grid=np.array(
                [
                    [-1.0, -0.75],
                    [-1.0, 0.75],
                    [0.0, -0.75],
                    [0.0, 0.75],
                    [1.0, -0.75],
                    [1.0, 0.75],
                ]
            ),
            mask=mask,
        )

        plane_image_galaxy = galaxy.image_from_grid(grid=grid)

        assert (plane_image.array == plane_image_galaxy).all()

    def test__3x3_grid__buffer_aligns_two_grids(self):
        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        grid_without_buffer = np.array([[-1.48, -1.48], [1.48, 1.48]])

        plane_image = plane_image_of_galaxies_from(
            shape=(3, 3), grid=grid_without_buffer, galaxies=[galaxy], buffer=0.02
        )

        mask = ag.Mask2D.manual(
            mask=np.full(shape=(3, 3), fill_value=False), pixel_scales=1.0, sub_size=1
        )

        grid = ag.Grid2D.manual_mask(
            grid=np.array(
                [
                    [-1.0, -1.0],
                    [-1.0, 0.0],
                    [-1.0, 1.0],
                    [0.0, -1.0],
                    [0.0, 0.0],
                    [0.0, 1.0],
                    [1.0, -1.0],
                    [1.0, 0.0],
                    [1.0, 1.0],
                ]
            ),
            mask=mask,
        )

        plane_image_galaxy = galaxy.image_from_grid(grid=grid)

        assert (plane_image.array == plane_image_galaxy).all()


class TestPlaneRedshifts:
    def test__from_galaxies__3_galaxies_reordered_in_ascending_redshift(self):
        galaxies = [
            ag.Galaxy(redshift=2.0),
            ag.Galaxy(redshift=1.0),
            ag.Galaxy(redshift=0.1),
        ]

        ordered_plane_redshifts = ordered_plane_redshifts_from(galaxies=galaxies)

        assert ordered_plane_redshifts == [0.1, 1.0, 2.0]

    def test_from_galaxies__3_galaxies_two_same_redshift_planes_redshift_order_is_size_2_with_redshifts(
        self,
    ):
        galaxies = [
            ag.Galaxy(redshift=1.0),
            ag.Galaxy(redshift=1.0),
            ag.Galaxy(redshift=0.1),
        ]

        ordered_plane_redshifts = ordered_plane_redshifts_from(galaxies=galaxies)

        assert ordered_plane_redshifts == [0.1, 1.0]

    def test__from_galaxies__6_galaxies_producing_4_planes(self):
        g0 = ag.Galaxy(redshift=1.0)
        g1 = ag.Galaxy(redshift=1.0)
        g2 = ag.Galaxy(redshift=0.1)
        g3 = ag.Galaxy(redshift=1.05)
        g4 = ag.Galaxy(redshift=0.95)
        g5 = ag.Galaxy(redshift=1.05)

        galaxies = [g0, g1, g2, g3, g4, g5]

        ordered_plane_redshifts = ordered_plane_redshifts_from(galaxies=galaxies)

        assert ordered_plane_redshifts == [0.1, 0.95, 1.0, 1.05]

    def test__from_main_plane_redshifts_and_slices(self):
        ordered_plane_redshifts = ordered_plane_redshifts_with_slicing_from(
            lens_redshifts=[1.0],
            source_plane_redshift=3.0,
            planes_between_lenses=[1, 1],
        )

        assert ordered_plane_redshifts == [0.5, 1.0, 2.0]

    def test__different_number_of_slices_between_planes(self):
        ordered_plane_redshifts = ordered_plane_redshifts_with_slicing_from(
            lens_redshifts=[1.0],
            source_plane_redshift=2.0,
            planes_between_lenses=[2, 3],
        )

        assert ordered_plane_redshifts == [
            (1.0 / 3.0),
            (2.0 / 3.0),
            1.0,
            1.25,
            1.5,
            1.75,
        ]

    def test__if_number_of_input_slices_is_not_equal_to_number_of_plane_intervals__raises_errror(
        self,
    ):
        with pytest.raises(exc.PlaneException):
            ordered_plane_redshifts_with_slicing_from(
                lens_redshifts=[1.0],
                source_plane_redshift=2.0,
                planes_between_lenses=[2, 3, 1],
            )

        with pytest.raises(exc.PlaneException):
            ordered_plane_redshifts_with_slicing_from(
                lens_redshifts=[1.0],
                source_plane_redshift=2.0,
                planes_between_lenses=[2],
            )

        with pytest.raises(exc.PlaneException):
            ordered_plane_redshifts_with_slicing_from(
                lens_redshifts=[1.0, 3.0],
                source_plane_redshift=2.0,
                planes_between_lenses=[2],
            )


class TestGalaxyOrdering:
    def test__3_galaxies_reordered_in_ascending_redshift__planes_match_galaxy_redshifts(
        self,
    ):
        galaxies = [
            ag.Galaxy(redshift=2.0),
            ag.Galaxy(redshift=1.0),
            ag.Galaxy(redshift=0.1),
        ]

        ordered_plane_redshifts = [0.1, 1.0, 2.0]

        galaxies_in_redshift_ordered_planes = galaxies_in_redshift_ordered_planes_from(
            galaxies=galaxies, plane_redshifts=ordered_plane_redshifts
        )

        assert galaxies_in_redshift_ordered_planes[0][0].redshift == 0.1
        assert galaxies_in_redshift_ordered_planes[1][0].redshift == 1.0
        assert galaxies_in_redshift_ordered_planes[2][0].redshift == 2.0

    def test_3_galaxies_x2_same_redshift__order_is_size_2_with_redshifts__plane_match_galaxy_redshifts(
        self,
    ):
        galaxies = [
            ag.Galaxy(redshift=1.0),
            ag.Galaxy(redshift=1.0),
            ag.Galaxy(redshift=0.1),
        ]

        ordered_plane_redshifts = [0.1, 1.0]

        galaxies_in_redshift_ordered_planes = galaxies_in_redshift_ordered_planes_from(
            galaxies=galaxies, plane_redshifts=ordered_plane_redshifts
        )

        assert galaxies_in_redshift_ordered_planes[0][0].redshift == 0.1
        assert galaxies_in_redshift_ordered_planes[1][0].redshift == 1.0
        assert galaxies_in_redshift_ordered_planes[1][1].redshift == 1.0

    def test__6_galaxies_producing_4_planes__galaxy_redshift_match_planes(self):
        g0 = ag.Galaxy(redshift=1.0)
        g1 = ag.Galaxy(redshift=1.0)
        g2 = ag.Galaxy(redshift=0.1)
        g3 = ag.Galaxy(redshift=1.05)
        g4 = ag.Galaxy(redshift=0.95)
        g5 = ag.Galaxy(redshift=1.05)

        galaxies = [g0, g1, g2, g3, g4, g5]

        ordered_plane_redshifts = [0.1, 0.95, 1.0, 1.05]

        galaxies_in_redshift_ordered_planes = galaxies_in_redshift_ordered_planes_from(
            galaxies=galaxies, plane_redshifts=ordered_plane_redshifts
        )

        assert galaxies_in_redshift_ordered_planes[0][0].redshift == 0.1
        assert galaxies_in_redshift_ordered_planes[1][0].redshift == 0.95
        assert galaxies_in_redshift_ordered_planes[2][0].redshift == 1.0
        assert galaxies_in_redshift_ordered_planes[2][1].redshift == 1.0
        assert galaxies_in_redshift_ordered_planes[3][0].redshift == 1.05
        assert galaxies_in_redshift_ordered_planes[3][1].redshift == 1.05

        assert galaxies_in_redshift_ordered_planes[0] == [g2]
        assert galaxies_in_redshift_ordered_planes[1] == [g4]
        assert galaxies_in_redshift_ordered_planes[2] == [g0, g1]
        assert galaxies_in_redshift_ordered_planes[3] == [g3, g5]

    def test__galaxy_redshifts_dont_match_plane_redshifts__tied_to_nearest_plane(self):
        ordered_plane_redshifts = [0.5, 1.0, 2.0, 3.0]

        galaxies = [
            ag.Galaxy(redshift=0.2),
            ag.Galaxy(redshift=0.4),
            ag.Galaxy(redshift=0.8),
            ag.Galaxy(redshift=1.2),
            ag.Galaxy(redshift=2.9),
        ]

        galaxies_in_redshift_ordered_planes = galaxies_in_redshift_ordered_planes_from(
            galaxies=galaxies, plane_redshifts=ordered_plane_redshifts
        )

        assert galaxies_in_redshift_ordered_planes[0][0].redshift == 0.2
        assert galaxies_in_redshift_ordered_planes[0][1].redshift == 0.4
        assert galaxies_in_redshift_ordered_planes[1][0].redshift == 0.8
        assert galaxies_in_redshift_ordered_planes[1][1].redshift == 1.2
        assert galaxies_in_redshift_ordered_planes[2] == []
        assert galaxies_in_redshift_ordered_planes[3][0].redshift == 2.9

    def test__different_number_of_slices_between_planes(self):
        ordered_plane_redshifts = [(1.0 / 3.0), (2.0 / 3.0), 1.0, 1.25, 1.5, 1.75, 2.0]

        galaxies = [
            ag.Galaxy(redshift=0.1),
            ag.Galaxy(redshift=0.2),
            ag.Galaxy(redshift=1.25),
            ag.Galaxy(redshift=1.35),
            ag.Galaxy(redshift=1.45),
            ag.Galaxy(redshift=1.55),
            ag.Galaxy(redshift=1.9),
        ]

        galaxies_in_redshift_ordered_planes = galaxies_in_redshift_ordered_planes_from(
            galaxies=galaxies, plane_redshifts=ordered_plane_redshifts
        )

        assert galaxies_in_redshift_ordered_planes[0][0].redshift == 0.1
        assert galaxies_in_redshift_ordered_planes[0][1].redshift == 0.2
        assert galaxies_in_redshift_ordered_planes[1] == []
        assert galaxies_in_redshift_ordered_planes[2] == []
        assert galaxies_in_redshift_ordered_planes[3][0].redshift == 1.25
        assert galaxies_in_redshift_ordered_planes[3][1].redshift == 1.35
        assert galaxies_in_redshift_ordered_planes[4][0].redshift == 1.45
        assert galaxies_in_redshift_ordered_planes[4][1].redshift == 1.55
        assert galaxies_in_redshift_ordered_planes[6][0].redshift == 1.9
