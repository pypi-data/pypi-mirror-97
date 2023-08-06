import os

from autoconf import conf
import autogalaxy as ag
import numpy as np
import pytest
from autogalaxy import exc
from autogalaxy.mock import mock


class TestPointSources:
    def test__point_source_dict(self, ps_0, ps_1):

        galaxy = ag.Galaxy(redshift=0.5)

        assert galaxy.point_source_dict == {}

        galaxy = ag.Galaxy(redshift=0.5, point_0=ps_0)

        assert galaxy.point_source_dict == {"point_0": ps_0}

        galaxy = ag.Galaxy(redshift=0.5, point_0=ps_0, point_1=ps_1)

        assert galaxy.point_source_dict == {"point_0": ps_0, "point_1": ps_1}

        galaxy = ag.Galaxy(
            redshift=0.5,
            point_0=ps_0,
            point_1=ps_1,
            mass=ag.mp.SphericalIsothermal(),
            light=ag.lp.EllipticalSersic(),
        )

        assert galaxy.point_source_dict == {"point_0": ps_0, "point_1": ps_1}


class TestLightProfiles:
    class TestProfileImage:
        def test__no_light_profiles__image_returned_as_0s_of_shape_grid(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            image = galaxy.image_from_grid(grid=sub_grid_7x7)

            assert (image == np.zeros(shape=sub_grid_7x7.sub_shape_slim)).all()

        def test__using_no_light_profiles__check_reshaping_decorator_of_returned_image(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            image = galaxy.image_from_grid(grid=sub_grid_7x7)

            assert (image.native_binned == np.zeros(shape=(7, 7))).all()

            image = galaxy.image_from_grid(grid=sub_grid_7x7)

            assert (image == np.zeros(shape=sub_grid_7x7.sub_shape_slim)).all()

            image = galaxy.image_from_grid(grid=sub_grid_7x7)

            assert (
                image.slim_binned == np.zeros(shape=sub_grid_7x7.sub_shape_slim // 4)
            ).all()

        def test__galaxies_with_x1_and_x2_light_profiles__image_is_same_individual_profiles(
            self, lp_0, gal_x1_lp, lp_1, gal_x2_lp
        ):
            lp_image = lp_0.image_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_lp_image = gal_x1_lp.image_from_grid(grid=np.array([[1.05, -0.55]]))

            assert lp_image == gal_lp_image

            lp_image = lp_0.image_from_grid(grid=np.array([[1.05, -0.55]]))
            lp_image += lp_1.image_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_image = gal_x2_lp.image_from_grid(grid=np.array([[1.05, -0.55]]))

            assert lp_image == gal_image

        def test__coordinates_in__coordinates_out(
            self, lp_0, gal_x1_lp, lp_1, gal_x2_lp
        ):

            lp_image = lp_0.image_from_grid(grid=ag.Grid2DIrregular([(1.05, -0.55)]))

            gal_lp_image = gal_x1_lp.image_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            assert lp_image.in_list[0] == gal_lp_image.in_list[0]

        def test__sub_grid_in__grid_is_mapped_to_image_grid_by_wrapper_by_binning_sum_of_light_profile_values(
            self, sub_grid_7x7, gal_x2_lp
        ):

            lp_0_image = gal_x2_lp.light_profile_0.image_from_grid(grid=sub_grid_7x7)

            lp_1_image = gal_x2_lp.light_profile_1.image_from_grid(grid=sub_grid_7x7)

            lp_image = lp_0_image + lp_1_image

            lp_image_0 = (lp_image[0] + lp_image[1] + lp_image[2] + lp_image[3]) / 4.0

            lp_image_1 = (lp_image[4] + lp_image[5] + lp_image[6] + lp_image[7]) / 4.0

            gal_image = gal_x2_lp.image_from_grid(grid=sub_grid_7x7)

            assert gal_image.slim_binned[0] == lp_image_0
            assert gal_image.slim_binned[1] == lp_image_1

    class TestLuminosityWithin:
        def test__two_profile_galaxy__is_sum_of_individual_profiles(
            self, lp_0, lp_1, gal_x2_lp
        ):

            lp_0_luminosity = lp_0.luminosity_within_circle(radius=0.5)

            lp_1_luminosity = lp_1.luminosity_within_circle(radius=0.5)
            gal_luminosity = gal_x2_lp.luminosity_within_circle(radius=0.5)

            assert lp_0_luminosity + lp_1_luminosity == gal_luminosity

        def test__no_light_profile__returns_none(self):
            gal_no_lp = ag.Galaxy(redshift=0.5, mass=ag.mp.SphericalIsothermal())

            assert gal_no_lp.luminosity_within_circle(radius=1.0) == None

    class TestSymmetricProfiles:
        def test_1d_symmetry(self):
            lp_0 = ag.lp.EllipticalSersic(centre=(0.0, 0.0), intensity=1.0)

            lp_1 = ag.lp.EllipticalSersic(centre=(100.0, 0.0), intensity=1.0)

            gal_x2_lp = ag.Galaxy(
                redshift=0.5, light_profile_0=lp_0, light_profile_1=lp_1
            )

            assert gal_x2_lp.image_from_grid(
                grid=np.array([[0.0, 0.0]])
            ) == pytest.approx(
                gal_x2_lp.image_from_grid(grid=np.array([[100.0, 0.0]])), 1.0e-4
            )

            assert gal_x2_lp.image_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x2_lp.image_from_grid(grid=np.array([[51.0, 0.0]])), 1.0e-4
            )

        def test_2d_symmetry(self):
            lp_0 = ag.lp.EllipticalSersic(
                elliptical_comps=(0.0, 0.0),
                intensity=1.0,
                effective_radius=0.6,
                sersic_index=4.0,
            )

            lp_1 = ag.lp.EllipticalSersic(
                elliptical_comps=(0.0, 0.0),
                intensity=1.0,
                effective_radius=0.6,
                sersic_index=4.0,
                centre=(100, 0),
            )

            lp_2 = ag.lp.EllipticalSersic(
                elliptical_comps=(0.0, 0.0),
                intensity=1.0,
                effective_radius=0.6,
                sersic_index=4.0,
                centre=(0, 100),
            )

            lp_3 = ag.lp.EllipticalSersic(
                elliptical_comps=(0.0, 0.0),
                intensity=1.0,
                effective_radius=0.6,
                sersic_index=4.0,
                centre=(100, 100),
            )

            gal_x4_lp = ag.Galaxy(
                redshift=0.5,
                light_profile_0=lp_0,
                light_profile_1=lp_1,
                light_profile_3=lp_2,
                light_profile_4=lp_3,
            )

            assert gal_x4_lp.image_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x4_lp.image_from_grid(grid=np.array([[51.0, 0.0]])), 1e-5
            )

            assert gal_x4_lp.image_from_grid(
                grid=np.array([[0.0, 49.0]])
            ) == pytest.approx(
                gal_x4_lp.image_from_grid(grid=np.array([[0.0, 51.0]])), 1e-5
            )

            assert gal_x4_lp.image_from_grid(
                grid=np.array([[100.0, 49.0]])
            ) == pytest.approx(
                gal_x4_lp.image_from_grid(grid=np.array([[100.0, 51.0]])), 1e-5
            )

            assert gal_x4_lp.image_from_grid(
                grid=np.array([[49.0, 49.0]])
            ) == pytest.approx(
                gal_x4_lp.image_from_grid(grid=np.array([[51.0, 51.0]])), 1e-5
            )

    class TestBlurredProfileImages:
        def test__blurred_image_from_grid_and_psf(
            self, sub_grid_7x7, blurring_grid_7x7, psf_3x3, convolver_7x7
        ):

            light_profile_0 = ag.lp.EllipticalSersic(intensity=2.0)
            light_profile_1 = ag.lp.EllipticalSersic(intensity=3.0)

            galaxy = ag.Galaxy(
                light_profile_0=light_profile_0,
                light_profile_1=light_profile_1,
                redshift=0.5,
            )

            image = galaxy.image_from_grid(grid=sub_grid_7x7)

            blurring_image = galaxy.image_from_grid(grid=blurring_grid_7x7)

            blurred_image = convolver_7x7.convolved_image_from_image_and_blurring_image(
                image=image.slim_binned, blurring_image=blurring_image.slim_binned
            )

            light_profile_blurred_image = galaxy.blurred_image_from_grid_and_psf(
                grid=sub_grid_7x7, blurring_grid=blurring_grid_7x7, psf=psf_3x3
            )

            assert blurred_image.slim == pytest.approx(
                light_profile_blurred_image.slim, 1.0e-4
            )

            assert blurred_image.native == pytest.approx(
                light_profile_blurred_image.native, 1.0e-4
            )

        def test__blurred_image_from_grid_and_convolver(
            self, sub_grid_7x7, blurring_grid_7x7, convolver_7x7
        ):
            light_profile_0 = ag.lp.EllipticalSersic(intensity=2.0)
            light_profile_1 = ag.lp.EllipticalSersic(intensity=3.0)

            galaxy = ag.Galaxy(
                light_profile_0=light_profile_0,
                light_profile_1=light_profile_1,
                redshift=0.5,
            )

            image = galaxy.image_from_grid(grid=sub_grid_7x7)

            blurring_image = galaxy.image_from_grid(grid=blurring_grid_7x7)

            blurred_image = convolver_7x7.convolved_image_from_image_and_blurring_image(
                image=image.slim_binned, blurring_image=blurring_image.slim_binned
            )

            light_profile_blurred_image = galaxy.blurred_image_from_grid_and_convolver(
                grid=sub_grid_7x7,
                convolver=convolver_7x7,
                blurring_grid=blurring_grid_7x7,
            )

            assert blurred_image.slim == pytest.approx(
                light_profile_blurred_image.slim, 1.0e-4
            )

            assert blurred_image.native == pytest.approx(
                light_profile_blurred_image.native, 1.0e-4
            )

    class TestVisibilities:
        def test__visibilities_from_grid_and_transformer(
            self, sub_grid_7x7, transformer_7x7_7
        ):

            light_profile_0 = ag.lp.EllipticalSersic(intensity=2.0)
            light_profile_1 = ag.lp.EllipticalSersic(intensity=3.0)

            image = (
                light_profile_0.image_from_grid(grid=sub_grid_7x7).slim_binned
                + light_profile_1.image_from_grid(grid=sub_grid_7x7).slim_binned
            )

            visibilities = transformer_7x7_7.visibilities_from_image(image=image)

            galaxy = ag.Galaxy(
                light_profile_0=light_profile_0,
                light_profile_1=light_profile_1,
                redshift=0.5,
            )

            galaxy_visibilities = galaxy.profile_visibilities_from_grid_and_transformer(
                grid=sub_grid_7x7, transformer=transformer_7x7_7
            )

            assert visibilities == pytest.approx(galaxy_visibilities, 1.0e-4)


class TestMassProfiles:
    class TestConvergence:
        def test__no_mass_profiles__convergence_returned_as_0s_of_shape_grid(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            convergence = galaxy.convergence_from_grid(grid=sub_grid_7x7)

            assert (
                convergence.slim == np.zeros(shape=sub_grid_7x7.sub_shape_slim)
            ).all()

        def test__using_no_mass_profiles__check_reshaping_decorator_of_returned_convergence(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            convergence = galaxy.convergence_from_grid(grid=sub_grid_7x7)

            assert (convergence.native_binned == np.zeros(shape=(7, 7))).all()

            convergence = galaxy.convergence_from_grid(grid=sub_grid_7x7)

            assert (
                convergence.slim == np.zeros(shape=sub_grid_7x7.sub_shape_slim)
            ).all()

            convergence = galaxy.convergence_from_grid(grid=sub_grid_7x7)

            assert (
                convergence.slim_binned
                == np.zeros(shape=sub_grid_7x7.sub_shape_slim // 4)
            ).all()

        def test__galaxies_with_x1_and_x2_mass_profiles__convergence_is_same_individual_profiles(
            self, mp_0, gal_x1_mp, mp_1, gal_x2_mp
        ):
            mp_convergence = mp_0.convergence_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_mp_convergence = gal_x1_mp.convergence_from_grid(
                grid=np.array([[1.05, -0.55]])
            )

            assert mp_convergence == gal_mp_convergence

            mp_convergence = mp_0.convergence_from_grid(grid=np.array([[1.05, -0.55]]))
            mp_convergence += mp_1.convergence_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_convergence = gal_x2_mp.convergence_from_grid(
                grid=np.array([[1.05, -0.55]])
            )

            assert mp_convergence == gal_convergence

        def test__coordinates_in__coordinates_out(
            self, mp_0, gal_x1_mp, mp_1, gal_x2_mp
        ):

            mp_convergence = mp_0.convergence_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            gal_mp_convergence = gal_x1_mp.convergence_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            assert mp_convergence == gal_mp_convergence

            assert mp_convergence.in_list[0] == gal_mp_convergence.in_list[0]

        def test__sub_grid_in__grid_is_mapped_to_image_grid_by_wrapper_by_binning_sum_of_mass_profile_values(
            self, sub_grid_7x7, gal_x2_mp
        ):
            mp_0_convergence = gal_x2_mp.mass_profile_0.convergence_from_grid(
                grid=sub_grid_7x7
            )

            mp_1_convergence = gal_x2_mp.mass_profile_1.convergence_from_grid(
                grid=sub_grid_7x7
            )

            mp_convergence = mp_0_convergence + mp_1_convergence

            mp_convergence_0 = (
                mp_convergence[0]
                + mp_convergence[1]
                + mp_convergence[2]
                + mp_convergence[3]
            ) / 4.0

            mp_convergence_1 = (
                mp_convergence[4]
                + mp_convergence[5]
                + mp_convergence[6]
                + mp_convergence[7]
            ) / 4.0

            gal_convergence = gal_x2_mp.convergence_from_grid(grid=sub_grid_7x7)

            assert gal_convergence.slim_binned[0] == mp_convergence_0
            assert gal_convergence.slim_binned[1] == mp_convergence_1

    class TestPotential:
        def test__no_mass_profiles__potential_returned_as_0s_of_shape_grid(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            potential = galaxy.potential_from_grid(grid=sub_grid_7x7)

            assert (potential.slim == np.zeros(shape=sub_grid_7x7.sub_shape_slim)).all()

        def test__using_no_mass_profiles__check_reshaping_decorator_of_returned_potential(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            potential = galaxy.potential_from_grid(grid=sub_grid_7x7)

            assert (potential.native_binned == np.zeros(shape=(7, 7))).all()

            potential = galaxy.potential_from_grid(grid=sub_grid_7x7)

            assert (potential.slim == np.zeros(shape=sub_grid_7x7.sub_shape_slim)).all()

            potential = galaxy.potential_from_grid(grid=sub_grid_7x7)

            assert (
                potential.slim_binned
                == np.zeros(shape=sub_grid_7x7.sub_shape_slim // 4)
            ).all()

        def test__galaxies_with_x1_and_x2_mass_profiles__potential_is_same_individual_profiles(
            self, mp_0, gal_x1_mp, mp_1, gal_x2_mp
        ):
            mp_potential = mp_0.potential_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_mp_potential = gal_x1_mp.potential_from_grid(
                grid=np.array([[1.05, -0.55]])
            )

            assert mp_potential == gal_mp_potential

            mp_potential = mp_0.potential_from_grid(grid=np.array([[1.05, -0.55]]))
            mp_potential += mp_1.potential_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_potential = gal_x2_mp.potential_from_grid(
                grid=np.array([[1.05, -0.55]])
            )

            assert mp_potential == gal_potential

        def test__coordinates_in__coordinates_out(
            self, mp_0, gal_x1_mp, mp_1, gal_x2_mp
        ):

            mp_potential = mp_0.potential_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            gal_mp_potential = gal_x1_mp.potential_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            assert mp_potential == gal_mp_potential

            assert mp_potential.in_list[0] == gal_mp_potential.in_list[0]

        def test__sub_grid_in__grid_is_mapped_to_image_grid_by_wrapper_by_binning_sum_of_mass_profile_values(
            self, sub_grid_7x7, gal_x2_mp
        ):
            mp_0_potential = gal_x2_mp.mass_profile_0.potential_from_grid(
                grid=sub_grid_7x7
            )

            mp_1_potential = gal_x2_mp.mass_profile_1.potential_from_grid(
                grid=sub_grid_7x7
            )

            mp_potential = mp_0_potential + mp_1_potential

            mp_potential_0 = (
                mp_potential[0] + mp_potential[1] + mp_potential[2] + mp_potential[3]
            ) / 4.0

            mp_potential_1 = (
                mp_potential[4] + mp_potential[5] + mp_potential[6] + mp_potential[7]
            ) / 4.0

            gal_potential = gal_x2_mp.potential_from_grid(grid=sub_grid_7x7)

            assert gal_potential.slim_binned[0] == mp_potential_0
            assert gal_potential.slim_binned[1] == mp_potential_1

    class TestDeflectionAngles:
        def test__no_mass_profiles__deflections_returned_as_0s_of_shape_grid(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            deflections = galaxy.deflections_from_grid(grid=sub_grid_7x7)

            assert (
                deflections.slim == np.zeros(shape=(sub_grid_7x7.sub_shape_slim, 2))
            ).all()

        def test__using_no_mass_profiles__check_reshaping_decorator_of_returned_deflections(
            self, sub_grid_7x7
        ):
            galaxy = ag.Galaxy(redshift=0.5)

            deflections = galaxy.deflections_from_grid(grid=sub_grid_7x7)

            assert (deflections.native_binned == np.zeros(shape=(7, 7, 2))).all()

            deflections = galaxy.deflections_from_grid(grid=sub_grid_7x7)

            assert (
                deflections.slim == np.zeros(shape=(sub_grid_7x7.sub_shape_slim, 2))
            ).all()

            deflections = galaxy.deflections_from_grid(grid=sub_grid_7x7)

            assert (
                deflections.slim_binned
                == np.zeros(shape=(sub_grid_7x7.sub_shape_slim // 4, 2))
            ).all()

        def test__galaxies_with_x1_and_x2_mass_profiles__deflections_is_same_individual_profiles(
            self, mp_0, gal_x1_mp, mp_1, gal_x2_mp
        ):
            mp_deflections = mp_0.deflections_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_mp_deflections = gal_x1_mp.deflections_from_grid(
                grid=np.array([[1.05, -0.55]])
            )

            assert (mp_deflections == gal_mp_deflections).all()

            mp_deflections = mp_0.deflections_from_grid(grid=np.array([[1.05, -0.55]]))
            mp_deflections += mp_1.deflections_from_grid(grid=np.array([[1.05, -0.55]]))

            gal_deflections = gal_x2_mp.deflections_from_grid(
                grid=np.array([[1.05, -0.55]])
            )

            assert (mp_deflections == gal_deflections).all()

        def test__coordinates_in__coordinates_out(
            self, mp_0, gal_x1_mp, mp_1, gal_x2_mp
        ):

            mp_deflections = mp_0.deflections_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            gal_mp_deflections = gal_x1_mp.deflections_from_grid(
                grid=ag.Grid2DIrregular([(1.05, -0.55)])
            )

            assert type(gal_mp_deflections) == ag.Grid2DIrregular
            assert mp_deflections.in_list[0][0] == gal_mp_deflections.in_list[0][0]
            assert mp_deflections.in_list[0][1] == gal_mp_deflections.in_list[0][1]

        def test__sub_grid_in__grid_is_mapped_to_image_grid_by_wrapper_by_binning_sum_of_mass_profile_values(
            self, sub_grid_7x7, gal_x2_mp
        ):
            mp_0_deflections = gal_x2_mp.mass_profile_0.deflections_from_grid(
                grid=sub_grid_7x7
            )

            mp_1_deflections = gal_x2_mp.mass_profile_1.deflections_from_grid(
                grid=sub_grid_7x7
            )

            mp_deflections = mp_0_deflections + mp_1_deflections

            mp_deflections_y_0 = (
                mp_deflections[0, 0]
                + mp_deflections[1, 0]
                + mp_deflections[2, 0]
                + mp_deflections[3, 0]
            ) / 4.0

            mp_deflections_y_1 = (
                mp_deflections[4, 0]
                + mp_deflections[5, 0]
                + mp_deflections[6, 0]
                + mp_deflections[7, 0]
            ) / 4.0

            gal_deflections = gal_x2_mp.deflections_from_grid(grid=sub_grid_7x7)

            assert gal_deflections.slim_binned[0, 0] == mp_deflections_y_0
            assert gal_deflections.slim_binned[1, 0] == mp_deflections_y_1

            mp_deflections_x_0 = (
                mp_deflections[0, 1]
                + mp_deflections[1, 1]
                + mp_deflections[2, 1]
                + mp_deflections[3, 1]
            ) / 4.0

            mp_deflections_x_1 = (
                mp_deflections[4, 1]
                + mp_deflections[5, 1]
                + mp_deflections[6, 1]
                + mp_deflections[7, 1]
            ) / 4.0

            gal_deflections = gal_x2_mp.deflections_from_grid(grid=sub_grid_7x7)

            assert gal_deflections.slim_binned[0, 1] == mp_deflections_x_0
            assert gal_deflections.slim_binned[1, 1] == mp_deflections_x_1

    class TestMassWithin:
        def test__two_profile_galaxy__is_sum_of_individual_profiles(
            self, mp_0, mp_1, gal_x2_mp
        ):

            mp_0_mass = mp_0.mass_angular_within_circle(radius=0.5)

            mp_1_mass = mp_1.mass_angular_within_circle(radius=0.5)
            gal_mass = gal_x2_mp.mass_angular_within_circle(radius=0.5)

            assert mp_0_mass + mp_1_mass == gal_mass

        def test__no_mass_profile__returns_none(self):
            gal_no_mp = ag.Galaxy(redshift=0.5, light=ag.lp.SphericalSersic())

            with pytest.raises(exc.GalaxyException):
                gal_no_mp.mass_angular_within_circle(radius=1.0)

    class TestStellar:
        def test__stellar_profiles__is_list_of_stellar_profiles(self):
            galaxy = ag.Galaxy(redshift=0.5)

            assert galaxy.stellar_profiles == []

            galaxy = ag.Galaxy(
                redshift=0.5,
                light=ag.lp.EllipticalGaussian(),
                mass=ag.mp.EllipticalIsothermal(),
            )

            assert galaxy.stellar_profiles == []

            stellar_0 = ag.lmp.EllipticalSersic()
            galaxy = ag.Galaxy(redshift=0.5, stellar_0=stellar_0)

            assert galaxy.stellar_profiles == [stellar_0]

            stellar_0 = ag.lmp.SphericalDevVaucouleurs()
            stellar_1 = ag.lmp.EllipticalDevVaucouleurs()
            stellar_2 = ag.lmp.EllipticalGaussian()
            galaxy = ag.Galaxy(
                redshift=0.5,
                stellar_0=stellar_0,
                stellar_1=stellar_1,
                stellar_2=stellar_2,
            )

            assert galaxy.stellar_profiles == [stellar_0, stellar_1, stellar_2]

        def test__stellar_mass_angular_within_galaxy__is_sum_of_individual_profiles(
            self, smp_0, smp_1
        ):

            galaxy = ag.Galaxy(
                redshift=0.5,
                stellar_0=smp_0,
                non_stellar_profile=ag.mp.EllipticalIsothermal(einstein_radius=1.0),
            )

            stellar_mass_0 = smp_0.mass_angular_within_circle(radius=0.5)

            gal_mass = galaxy.stellar_mass_angular_within_circle(radius=0.5)

            assert stellar_mass_0 == gal_mass

            galaxy = ag.Galaxy(
                redshift=0.5,
                stellar_0=smp_0,
                stellar_1=smp_1,
                non_stellar_profile=ag.mp.EllipticalIsothermal(einstein_radius=1.0),
            )

            stellar_mass_1 = smp_1.mass_angular_within_circle(radius=0.5)

            gal_mass = galaxy.stellar_mass_angular_within_circle(radius=0.5)

            assert stellar_mass_0 + stellar_mass_1 == gal_mass

            galaxy = ag.Galaxy(redshift=0.5)

            with pytest.raises(exc.GalaxyException):
                galaxy.stellar_mass_angular_within_circle(radius=1.0)

        def test__stellar_fraction_at_radius(self, dmp_0, dmp_1, smp_0, smp_1):

            galaxy = ag.Galaxy(redshift=0.5, stellar_0=smp_0, dark_0=dmp_0)

            stellar_mass_0 = smp_0.mass_angular_within_circle(radius=1.0)
            dark_mass_0 = dmp_0.mass_angular_within_circle(radius=1.0)

            stellar_fraction = galaxy.stellar_fraction_at_radius(radius=1.0)

            assert stellar_fraction == pytest.approx(
                stellar_mass_0 / (dark_mass_0 + stellar_mass_0), 1.0e-4
            )

            galaxy = ag.Galaxy(
                redshift=0.5, stellar_0=smp_0, stellar_1=smp_1, dark_0=dmp_0
            )

            stellar_fraction = galaxy.stellar_fraction_at_radius(radius=1.0)
            stellar_mass_1 = smp_1.mass_angular_within_circle(radius=1.0)

            assert stellar_fraction == pytest.approx(
                (stellar_mass_0 + stellar_mass_1)
                / (dark_mass_0 + stellar_mass_0 + stellar_mass_1),
                1.0e-4,
            )

            galaxy = ag.Galaxy(
                redshift=0.5,
                stellar_0=smp_0,
                stellar_1=smp_1,
                dark_0=dmp_0,
                dark_mass_1=dmp_1,
            )

            stellar_fraction = galaxy.stellar_fraction_at_radius(radius=1.0)
            dark_mass_1 = dmp_1.mass_angular_within_circle(radius=1.0)

            assert stellar_fraction == pytest.approx(
                (stellar_mass_0 + stellar_mass_1)
                / (dark_mass_0 + dark_mass_1 + stellar_mass_0 + stellar_mass_1),
                1.0e-4,
            )

    class TestDark:
        def test__dark_profiles__is_list_of_dark_profiles(self):
            galaxy = ag.Galaxy(redshift=0.5)

            assert galaxy.dark_profiles == []

            galaxy = ag.Galaxy(
                redshift=0.5,
                light=ag.lp.EllipticalGaussian(),
                mass=ag.mp.EllipticalIsothermal(),
            )

            assert galaxy.dark_profiles == []

            dark_0 = ag.mp.SphericalNFW()
            galaxy = ag.Galaxy(redshift=0.5, dark_0=dark_0)

            assert galaxy.dark_profiles == [dark_0]

            dark_0 = ag.mp.SphericalNFW()
            dark_1 = ag.mp.EllipticalNFW()
            dark_2 = ag.mp.EllipticalGeneralizedNFW()
            galaxy = ag.Galaxy(
                redshift=0.5, dark_0=dark_0, dark_1=dark_1, dark_2=dark_2
            )

            assert galaxy.dark_profiles == [dark_0, dark_1, dark_2]

        def test__dark_mass_within_galaxy__is_sum_of_individual_profiles(
            self, dmp_0, dmp_1
        ):

            galaxy = ag.Galaxy(
                redshift=0.5,
                dark_0=dmp_0,
                non_dark_profile=ag.mp.EllipticalIsothermal(einstein_radius=1.0),
            )

            dark_mass_0 = dmp_0.mass_angular_within_circle(radius=0.5)

            gal_mass = galaxy.dark_mass_angular_within_circle(radius=0.5)

            assert dark_mass_0 == gal_mass

            galaxy = ag.Galaxy(
                redshift=0.5,
                dark_0=dmp_0,
                dark_1=dmp_1,
                non_dark_profile=ag.mp.EllipticalIsothermal(einstein_radius=1.0),
            )

            dark_mass_1 = dmp_1.mass_angular_within_circle(radius=0.5)

            gal_mass = galaxy.dark_mass_angular_within_circle(radius=0.5)

            assert dark_mass_0 + dark_mass_1 == gal_mass

            galaxy = ag.Galaxy(redshift=0.5)

            with pytest.raises(exc.GalaxyException):
                galaxy.dark_mass_angular_within_circle(radius=1.0)

        def test__dark_fraction_at_radius(self, dmp_0, dmp_1, smp_0, smp_1):

            galaxy = ag.Galaxy(redshift=0.5, dark_0=dmp_0, stellar_0=smp_0)

            stellar_mass_0 = smp_0.mass_angular_within_circle(radius=1.0)
            dark_mass_0 = dmp_0.mass_angular_within_circle(radius=1.0)

            dark_fraction = galaxy.dark_fraction_at_radius(radius=1.0)

            assert dark_fraction == dark_mass_0 / (stellar_mass_0 + dark_mass_0)

            galaxy = ag.Galaxy(
                redshift=0.5, dark_0=dmp_0, dark_1=dmp_1, stellar_0=smp_0
            )

            dark_fraction = galaxy.dark_fraction_at_radius(radius=1.0)
            dark_mass_1 = dmp_1.mass_angular_within_circle(radius=1.0)

            assert dark_fraction == pytest.approx(
                (dark_mass_0 + dark_mass_1)
                / (stellar_mass_0 + dark_mass_0 + dark_mass_1),
                1.0e-4,
            )

            galaxy = ag.Galaxy(
                redshift=0.5,
                dark_0=dmp_0,
                dark_1=dmp_1,
                stellar_0=smp_0,
                stellar_mass_1=smp_1,
            )

            dark_fraction = galaxy.dark_fraction_at_radius(radius=1.0)
            stellar_mass_1 = smp_1.mass_angular_within_circle(radius=1.0)

            assert dark_fraction == pytest.approx(
                (dark_mass_0 + dark_mass_1)
                / (stellar_mass_0 + stellar_mass_1 + dark_mass_0 + dark_mass_1),
                1.0e-4,
            )

    class TestSymmetricProfiles:
        def test_1d_symmetry(self):
            mp_0 = ag.mp.EllipticalIsothermal(
                elliptical_comps=(0.333333, 0.0), einstein_radius=1.0
            )

            mp_1 = ag.mp.EllipticalIsothermal(
                centre=(100, 0), elliptical_comps=(0.333333, 0.0), einstein_radius=1.0
            )

            gal_x4_mp = ag.Galaxy(
                redshift=0.5, mass_profile_0=mp_0, mass_profile_1=mp_1
            )

            assert gal_x4_mp.convergence_from_grid(
                grid=np.array([[1.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.convergence_from_grid(grid=np.array([[99.0, 0.0]])), 1.0e-4
            )

            assert gal_x4_mp.convergence_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.convergence_from_grid(grid=np.array([[51.0, 0.0]])), 1.0e-4
            )

            assert gal_x4_mp.potential_from_grid(
                grid=np.array([[1.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.potential_from_grid(grid=np.array([[99.0, 0.0]])), 1e-6
            )

            assert gal_x4_mp.potential_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.potential_from_grid(grid=np.array([[51.0, 0.0]])), 1e-6
            )

            assert gal_x4_mp.deflections_from_grid(
                grid=np.array([[1.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[99.0, 0.0]])), 1e-6
            )

            assert gal_x4_mp.deflections_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[51.0, 0.0]])), 1e-6
            )

        def test_2d_symmetry(self):
            mp_0 = ag.mp.SphericalIsothermal(einstein_radius=1.0)

            mp_1 = ag.mp.SphericalIsothermal(centre=(100, 0), einstein_radius=1.0)

            mp_2 = ag.mp.SphericalIsothermal(centre=(0, 100), einstein_radius=1.0)

            mp_3 = ag.mp.SphericalIsothermal(centre=(100, 100), einstein_radius=1.0)

            gal_x4_mp = ag.Galaxy(
                redshift=0.5,
                mass_profile_0=mp_0,
                mass_profile_1=mp_1,
                mass_profile_2=mp_2,
                mass_profile_3=mp_3,
            )

            assert gal_x4_mp.convergence_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.convergence_from_grid(grid=np.array([[51.0, 0.0]])), 1e-5
            )

            assert gal_x4_mp.convergence_from_grid(
                grid=np.array([[0.0, 49.0]])
            ) == pytest.approx(
                gal_x4_mp.convergence_from_grid(grid=np.array([[0.0, 51.0]])), 1e-5
            )

            assert gal_x4_mp.convergence_from_grid(
                grid=np.array([[100.0, 49.0]])
            ) == pytest.approx(
                gal_x4_mp.convergence_from_grid(grid=np.array([[100.0, 51.0]])), 1e-5
            )

            assert gal_x4_mp.convergence_from_grid(
                grid=np.array([[49.0, 49.0]])
            ) == pytest.approx(
                gal_x4_mp.convergence_from_grid(grid=np.array([[51.0, 51.0]])), 1e-5
            )

            assert gal_x4_mp.potential_from_grid(
                grid=np.array([[49.0, 0.0]])
            ) == pytest.approx(
                gal_x4_mp.potential_from_grid(grid=np.array([[51.0, 0.0]])), 1e-5
            )

            assert gal_x4_mp.potential_from_grid(
                grid=np.array([[0.0, 49.0]])
            ) == pytest.approx(
                gal_x4_mp.potential_from_grid(grid=np.array([[0.0, 51.0]])), 1e-5
            )

            assert gal_x4_mp.potential_from_grid(
                grid=np.array([[100.0, 49.0]])
            ) == pytest.approx(
                gal_x4_mp.potential_from_grid(grid=np.array([[100.0, 51.0]])), 1e-5
            )

            assert gal_x4_mp.potential_from_grid(
                grid=np.array([[49.0, 49.0]])
            ) == pytest.approx(
                gal_x4_mp.potential_from_grid(grid=np.array([[51.0, 51.0]])), 1e-5
            )

            assert -1.0 * gal_x4_mp.deflections_from_grid(grid=np.array([[49.0, 0.0]]))[
                0, 0
            ] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[51.0, 0.0]]))[0, 0],
                1e-5,
            )

            assert 1.0 * gal_x4_mp.deflections_from_grid(grid=np.array([[0.0, 49.0]]))[
                0, 0
            ] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[0.0, 51.0]]))[0, 0],
                1e-5,
            )

            assert 1.0 * gal_x4_mp.deflections_from_grid(
                grid=np.array([[100.0, 49.0]])
            )[0, 0] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[100.0, 51.0]]))[0, 0],
                1e-5,
            )

            assert -1.0 * gal_x4_mp.deflections_from_grid(
                grid=np.array([[49.0, 49.0]])
            )[0, 0] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[51.0, 51.0]]))[0, 0],
                1e-5,
            )

            assert 1.0 * gal_x4_mp.deflections_from_grid(grid=np.array([[49.0, 0.0]]))[
                0, 1
            ] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[51.0, 0.0]]))[0, 1],
                1e-5,
            )

            assert -1.0 * gal_x4_mp.deflections_from_grid(grid=np.array([[0.0, 49.0]]))[
                0, 1
            ] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[0.0, 51.0]]))[0, 1],
                1e-5,
            )

            assert -1.0 * gal_x4_mp.deflections_from_grid(
                grid=np.array([[100.0, 49.0]])
            )[0, 1] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[100.0, 51.0]]))[0, 1],
                1e-5,
            )

            assert -1.0 * gal_x4_mp.deflections_from_grid(
                grid=np.array([[49.0, 49.0]])
            )[0, 1] == pytest.approx(
                gal_x4_mp.deflections_from_grid(grid=np.array([[51.0, 51.0]]))[0, 1],
                1e-5,
            )

    class TestLensingObject:
        def test__correct_einstein_mass_caclulated_for_multiple_mass_profiles__means_all_innherited_methods_work(
            self,
        ):

            grid = ag.Grid2D.uniform(shape_native=(50, 50), pixel_scales=0.15)

            sis_0 = ag.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=2.0)

            sis_1 = ag.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=1.0)

            galaxy = ag.Galaxy(mass_profile_0=sis_0, mass_profile_1=sis_1, redshift=0.5)

            einstein_mass = galaxy.einstein_mass_angular_from_grid(grid=grid)

            assert einstein_mass == pytest.approx(np.pi * 3.0 ** 2.0, 1.0e-1)


class TestMassAndLightProfiles:
    def test_single_profile(self, lmp_0):
        gal_x1_lmp = ag.Galaxy(redshift=0.5, profile=lmp_0)

        assert 1 == len(gal_x1_lmp.light_profiles)
        assert 1 == len(gal_x1_lmp.mass_profiles)

        assert gal_x1_lmp.mass_profiles[0] == lmp_0
        assert gal_x1_lmp.light_profiles[0] == lmp_0

    def test_multiple_profile(self, lmp_0, lp_0, mp_0):
        gal_multi_profiles = ag.Galaxy(
            redshift=0.5, profile=lmp_0, light=lp_0, sie=mp_0
        )

        assert 2 == len(gal_multi_profiles.light_profiles)
        assert 2 == len(gal_multi_profiles.mass_profiles)


class TestHyperGalaxy:
    class TestContributionMaps:
        def test__model_image_all_1s__factor_is_0__contributions_all_1s(self):
            hyper_image = np.ones((3,))

            hyp = ag.HyperGalaxy(contribution_factor=0.0)
            contribution_map = hyp.contribution_map_from_hyper_images(
                hyper_model_image=hyper_image, hyper_galaxy_image=hyper_image
            )

            assert (contribution_map == np.ones((3,))).all()

        def test__different_values__factor_is_1__contributions_are_value_divided_by_factor_and_max(
            self,
        ):
            hyper_image = np.array([0.5, 1.0, 1.5])

            hyp = ag.HyperGalaxy(contribution_factor=1.0)
            contribution_map = hyp.contribution_map_from_hyper_images(
                hyper_model_image=hyper_image, hyper_galaxy_image=hyper_image
            )

            assert (
                contribution_map
                == np.array([(0.5 / 1.5) / (1.5 / 2.5), (1.0 / 2.0) / (1.5 / 2.5), 1.0])
            ).all()

        def test__galaxy_contribution_map_property(self):

            hyper_image = np.ones((3,))

            hyp = ag.HyperGalaxy(contribution_factor=0.0)

            galaxy = ag.Galaxy(
                redshift=0.5,
                hyper_galaxy=hyp,
                hyper_galaxy_image=hyper_image,
                hyper_model_image=hyper_image,
            )

            contribution_map = hyp.contribution_map_from_hyper_images(
                hyper_model_image=hyper_image, hyper_galaxy_image=hyper_image
            )

            assert (contribution_map == galaxy.contribution_map).all()

    class TestHyperNoiseMap:
        def test__contribution_all_1s__noise_factor_2__noise_adds_double(self):
            noise_map = np.array([1.0, 2.0, 3.0])
            contribution_map = np.ones((3, 1))

            hyper_galaxy = ag.HyperGalaxy(
                contribution_factor=0.0, noise_factor=2.0, noise_power=1.0
            )

            hyper_noise_map = hyper_galaxy.hyper_noise_map_from_contribution_map(
                noise_map=noise_map, contribution_map=contribution_map
            )

            assert (hyper_noise_map == np.array([2.0, 4.0, 6.0])).all()

        def test__same_as_above_but_contributions_vary(self):
            noise_map = np.array([1.0, 2.0, 3.0])
            contribution_map = np.array([[0.0, 0.5, 1.0]])

            hyper_galaxy = ag.HyperGalaxy(
                contribution_factor=0.0, noise_factor=2.0, noise_power=1.0
            )

            hyper_noise_map = hyper_galaxy.hyper_noise_map_from_contribution_map(
                noise_map=noise_map, contribution_map=contribution_map
            )

            assert (hyper_noise_map == np.array([0.0, 2.0, 6.0])).all()

        def test__same_as_above_but_change_noise_scale_terms(self):
            noise_map = np.array([1.0, 2.0, 3.0])
            contribution_map = np.array([[0.0, 0.5, 1.0]])

            hyper_galaxy = ag.HyperGalaxy(
                contribution_factor=0.0, noise_factor=2.0, noise_power=2.0
            )

            hyper_noise_map = hyper_galaxy.hyper_noise_map_from_contribution_map(
                noise_map=noise_map, contribution_map=contribution_map
            )

            assert (hyper_noise_map == np.array([0.0, 2.0, 18.0])).all()


class TestBooleanProperties:
    def test_has_profile(self):
        assert ag.Galaxy(redshift=0.5).has_profile is False
        assert (
            ag.Galaxy(redshift=0.5, light_profile=ag.lp.LightProfile()).has_profile
            is True
        )
        assert (
            ag.Galaxy(redshift=0.5, mass_profile=ag.mp.MassProfile()).has_profile
            is True
        )

    def test_has_light_profile(self):
        assert ag.Galaxy(redshift=0.5).has_light_profile is False
        assert (
            ag.Galaxy(
                redshift=0.5, light_profile=ag.lp.LightProfile()
            ).has_light_profile
            is True
        )
        assert (
            ag.Galaxy(redshift=0.5, mass_profile=ag.mp.MassProfile()).has_light_profile
            is False
        )

    def test_has_mass_profile(self):
        assert ag.Galaxy(redshift=0.5).has_mass_profile is False
        assert (
            ag.Galaxy(redshift=0.5, light_profile=ag.lp.LightProfile()).has_mass_profile
            is False
        )
        assert (
            ag.Galaxy(redshift=0.5, mass_profile=ag.mp.MassProfile()).has_mass_profile
            is True
        )

    def test_has_redshift(self):
        assert ag.Galaxy(redshift=0.1).has_redshift is True

    def test_has_pixelization(self):
        assert ag.Galaxy(redshift=0.5).has_pixelization is False
        assert (
            ag.Galaxy(
                redshift=0.5, pixelization=object(), regularization=object()
            ).has_pixelization
            is True
        )

    def test_has_regularization(self):
        assert ag.Galaxy(redshift=0.5).has_regularization is False
        assert (
            ag.Galaxy(
                redshift=0.5, pixelization=object(), regularization=object()
            ).has_regularization
            is True
        )

    def test_has_hyper_galaxy(self):
        assert ag.Galaxy(redshift=0.5, hyper_galaxy=object()).has_hyper_galaxy is True

    def test__only_pixelization_raises_error(self):
        with pytest.raises(exc.GalaxyException):
            ag.Galaxy(redshift=0.5, pixelization=object())

    def test__only_regularization_raises_error(self):
        with pytest.raises(exc.GalaxyException):
            ag.Galaxy(redshift=0.5, regularization=object())


class TestExtract:
    def test__extract_attribute(self):

        galaxy = ag.Galaxy(redshift=0.5)

        values = galaxy.extract_attribute(cls=ag.lp.LightProfile, name="value")

        assert values == None

        galaxy = ag.Galaxy(
            redshift=0.5,
            lp_0=mock.MockLightProfile(value=0.9, value1=(0.0, 1.0)),
            lp_1=mock.MockLightProfile(value=0.8, value1=(2.0, 3.0)),
            lp_2=mock.MockLightProfile(value=0.7, value1=(4.0, 5.0)),
        )

        values = galaxy.extract_attribute(cls=ag.lp.LightProfile, name="value")

        assert values.in_list == [0.9, 0.8, 0.7]

        values = galaxy.extract_attribute(cls=ag.lp.LightProfile, name="value1")

        assert values.in_list == [(0.0, 1.0), (2.0, 3.0), (4.0, 5.0)]

        galaxy = ag.Galaxy(
            redshift=0.5,
            lp_3=ag.lp.LightProfile(),
            lp_0=mock.MockLightProfile(value=1.0),
            lp_1=mock.MockLightProfile(value=2.0),
            mp_0=mock.MockMassProfile(value=5.0),
            lp_2=mock.MockLightProfile(value=3.0),
        )

        values = galaxy.extract_attribute(cls=ag.lp.LightProfile, name="value")

        assert values.in_list == [1.0, 2.0, 3.0]


class TestRegression:
    def test__centre_of_profile_in_right_place(self):

        grid = ag.Grid2D.uniform(shape_native=(7, 7), pixel_scales=1.0)

        galaxy = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.EllipticalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
            mass_0=ag.mp.EllipticalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
        )

        convergence = galaxy.convergence_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            convergence.native.argmax(), convergence.shape_native
        )
        assert max_indexes == (1, 4)

        potential = galaxy.potential_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            potential.native.argmin(), potential.shape_native
        )
        assert max_indexes == (1, 4)

        deflections = galaxy.deflections_from_grid(grid=grid)
        assert deflections.native[1, 4, 0] > 0
        assert deflections.native[2, 4, 0] < 0
        assert deflections.native[1, 4, 1] > 0
        assert deflections.native[1, 3, 1] < 0

        galaxy = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.SphericalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
            mass_0=ag.mp.SphericalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
        )
        convergence = galaxy.convergence_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            convergence.native.argmax(), convergence.shape_native
        )
        assert max_indexes == (1, 4)

        potential = galaxy.potential_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            potential.native.argmin(), potential.shape_native
        )
        assert max_indexes == (1, 4)

        deflections = galaxy.deflections_from_grid(grid=grid)
        assert deflections.native[1, 4, 0] > 0
        assert deflections.native[2, 4, 0] < 0
        assert deflections.native[1, 4, 1] > 0
        assert deflections.native[1, 3, 1] < 0

        grid = ag.Grid2DIterate.uniform(
            shape_native=(7, 7),
            pixel_scales=1.0,
            fractional_accuracy=0.99,
            sub_steps=[2, 4],
        )

        galaxy = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.EllipticalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
            mass_0=ag.mp.EllipticalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
        )
        convergence = galaxy.convergence_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            convergence.native.argmax(), convergence.shape_native
        )
        assert max_indexes == (1, 4)

        potential = galaxy.potential_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            potential.native.argmin(), potential.shape_native
        )
        assert max_indexes == (1, 4)

        deflections = galaxy.deflections_from_grid(grid=grid)
        assert deflections.native[1, 4, 0] >= 0
        assert deflections.native[2, 4, 0] <= 0
        assert deflections.native[1, 4, 1] >= 0
        assert deflections.native[1, 3, 1] <= 0

        galaxy = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.SphericalIsothermal(centre=(2.0, 1.0), einstein_radius=1.0),
        )
        convergence = galaxy.convergence_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            convergence.native.argmax(), convergence.shape_native
        )
        assert max_indexes == (1, 4)

        potential = galaxy.potential_from_grid(grid=grid)
        max_indexes = np.unravel_index(
            potential.native.argmin(), potential.shape_native
        )
        assert max_indexes == (1, 4)

        deflections = galaxy.deflections_from_grid(grid=grid)
        assert deflections.native[1, 4, 0] >= 0
        assert deflections.native[2, 4, 0] <= 0
        assert deflections.native[1, 4, 1] >= 0
        assert deflections.native[1, 3, 1] <= 0


class TestDecorators:
    def test__grid_iterate_in__iterates_array_result_correctly(self, gal_x1_lp):

        mask = ag.Mask2D.manual(
            mask=[
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, False, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ],
            pixel_scales=(1.0, 1.0),
        )

        grid = ag.Grid2DIterate.from_mask(
            mask=mask, fractional_accuracy=1.0, sub_steps=[2]
        )

        galaxy = ag.Galaxy(redshift=0.5, light=ag.lp.EllipticalSersic(intensity=1.0))

        image = galaxy.image_from_grid(grid=grid)

        mask_sub_2 = mask.mask_new_sub_size_from_mask(mask=mask, sub_size=2)
        grid_sub_2 = ag.Grid2D.from_mask(mask=mask_sub_2)
        image_sub_2 = galaxy.image_from_grid(grid=grid_sub_2).slim_binned

        assert (image == image_sub_2).all()

        grid = ag.Grid2DIterate.from_mask(
            mask=mask, fractional_accuracy=0.95, sub_steps=[2, 4, 8]
        )

        galaxy = ag.Galaxy(
            redshift=0.5,
            light=ag.lp.EllipticalSersic(centre=(0.08, 0.08), intensity=1.0),
        )

        image = galaxy.image_from_grid(grid=grid)

        mask_sub_4 = mask.mask_new_sub_size_from_mask(mask=mask, sub_size=4)
        grid_sub_4 = ag.Grid2D.from_mask(mask=mask_sub_4)
        image_sub_4 = galaxy.image_from_grid(grid=grid_sub_4).slim_binned

        assert image[0] == image_sub_4[0]

        mask_sub_8 = mask.mask_new_sub_size_from_mask(mask=mask, sub_size=8)
        grid_sub_8 = ag.Grid2D.from_mask(mask=mask_sub_8)
        image_sub_8 = galaxy.image_from_grid(grid=grid_sub_8).slim_binned

        assert image[4] == image_sub_8[4]

    def test__grid_iterate_in__iterates_grid_result_correctly(self, gal_x1_mp):

        mask = ag.Mask2D.manual(
            mask=[
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, False, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ],
            pixel_scales=(1.0, 1.0),
        )

        grid = ag.Grid2DIterate.from_mask(
            mask=mask, fractional_accuracy=1.0, sub_steps=[2]
        )

        galaxy = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.EllipticalIsothermal(centre=(0.08, 0.08), einstein_radius=1.0),
        )

        deflections = galaxy.deflections_from_grid(grid=grid)

        mask_sub_2 = mask.mask_new_sub_size_from_mask(mask=mask, sub_size=2)
        grid_sub_2 = ag.Grid2D.from_mask(mask=mask_sub_2)
        deflections_sub_2 = galaxy.deflections_from_grid(grid=grid_sub_2).slim_binned

        assert (deflections == deflections_sub_2).all()

        grid = ag.Grid2DIterate.from_mask(
            mask=mask, fractional_accuracy=0.99, sub_steps=[2, 4, 8]
        )

        galaxy = ag.Galaxy(
            redshift=0.5,
            mass=ag.mp.EllipticalIsothermal(centre=(0.08, 0.08), einstein_radius=1.0),
        )

        deflections = galaxy.deflections_from_grid(grid=grid)

        mask_sub_4 = mask.mask_new_sub_size_from_mask(mask=mask, sub_size=4)
        grid_sub_4 = ag.Grid2D.from_mask(mask=mask_sub_4)
        deflections_sub_4 = galaxy.deflections_from_grid(grid=grid_sub_4).slim_binned

        assert deflections[0, 0] == deflections_sub_4[0, 0]

        mask_sub_8 = mask.mask_new_sub_size_from_mask(mask=mask, sub_size=8)
        grid_sub_8 = ag.Grid2D.from_mask(mask=mask_sub_8)
        deflections_sub_8 = galaxy.deflections_from_grid(grid=grid_sub_8).slim_binned

        assert deflections[4, 0] == deflections_sub_8[4, 0]

    def test__grid_interp_in__interps_based_on_intepolate_config(self):

        # `False` in interpolate.ini

        mask = ag.Mask2D.manual(
            mask=[
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, False, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ],
            pixel_scales=(1.0, 1.0),
        )

        grid = ag.Grid2D.from_mask(mask=mask)

        grid_interp = ag.Grid2DInterpolate.from_mask(mask=mask, pixel_scales_interp=0.1)

        light_profile = ag.lp.EllipticalSersic(intensity=1.0)
        light_profile_interp = ag.lp.SphericalSersic(intensity=1.0)

        image_no_interp = light_profile.image_from_grid(grid=grid)

        array_interp = light_profile.image_from_grid(grid=grid_interp.grid_interp)
        image_interp = grid_interp.interpolated_array_from_array_interp(
            array_interp=array_interp
        )

        galaxy = ag.Galaxy(
            redshift=0.5, light=light_profile_interp, light_0=light_profile
        )

        image = galaxy.image_from_grid(grid=grid_interp)

        assert (image == image_no_interp + image_interp).all()

        mass_profile = ag.mp.EllipticalIsothermal(einstein_radius=1.0)
        mass_profile_interp = ag.mp.SphericalIsothermal(einstein_radius=1.0)

        convergence_no_interp = mass_profile.convergence_from_grid(grid=grid)

        array_interp = mass_profile_interp.convergence_from_grid(
            grid=grid_interp.grid_interp
        )
        convergence_interp = grid_interp.interpolated_array_from_array_interp(
            array_interp=array_interp
        )

        galaxy = ag.Galaxy(redshift=0.5, mass=mass_profile_interp, mass_0=mass_profile)

        convergence = galaxy.convergence_from_grid(grid=grid_interp)

        assert (convergence == convergence_no_interp + convergence_interp).all()

        potential_no_interp = mass_profile.potential_from_grid(grid=grid)

        array_interp = mass_profile_interp.potential_from_grid(
            grid=grid_interp.grid_interp
        )
        potential_interp = grid_interp.interpolated_array_from_array_interp(
            array_interp=array_interp
        )

        galaxy = ag.Galaxy(redshift=0.5, mass=mass_profile_interp, mass_0=mass_profile)

        potential = galaxy.potential_from_grid(grid=grid_interp)

        assert (potential == potential_no_interp + potential_interp).all()

        deflections_no_interp = mass_profile.deflections_from_grid(grid=grid)

        grid_interp_0 = mass_profile_interp.deflections_from_grid(
            grid=grid_interp.grid_interp
        )
        deflections_interp = grid_interp.interpolated_grid_from_grid_interp(
            grid_interp=grid_interp_0
        )

        galaxy = ag.Galaxy(redshift=0.5, mass=mass_profile_interp, mass_0=mass_profile)

        deflections = galaxy.deflections_from_grid(grid=grid_interp)

        assert (deflections == deflections_no_interp + deflections_interp).all()
