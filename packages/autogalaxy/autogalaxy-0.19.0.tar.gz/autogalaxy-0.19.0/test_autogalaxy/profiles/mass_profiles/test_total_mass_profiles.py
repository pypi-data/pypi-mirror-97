import os

from autoconf import conf
import autogalaxy as ag
import numpy as np
import pytest


grid = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])


class TestPointMass:
    def test__deflections__correct_values(self):

        # The radial coordinate at (1.0, 1.0) is sqrt(2)
        # This is decomposed into (y,x) angles of sin(45) = cos(45) = sqrt(2) / 2.0
        # Thus, for an EinR of 1.0, the deflection angle is (1.0 / sqrt(2)) * (sqrt(2) / 2.0)

        point_mass = ag.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(grid=np.array([[1.0, 1.0]]))
        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)

        point_mass = ag.mp.PointMass(centre=(0.0, 0.0), einstein_radius=2.0)

        deflections = point_mass.deflections_from_grid(grid=np.array([[1.0, 1.0]]))
        assert deflections[0, 0] == pytest.approx(2.0, 1e-3)
        assert deflections[0, 1] == pytest.approx(2.0, 1e-3)

        point_mass = ag.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(grid=np.array([[2.0, 2.0]]))
        assert deflections[0, 0] == pytest.approx(0.25, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.25, 1e-3)

        point_mass = ag.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(grid=np.array([[2.0, 1.0]]))
        assert deflections[0, 0] == pytest.approx(0.4, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.2, 1e-3)

        point_mass = ag.mp.PointMass(centre=(0.0, 0.0), einstein_radius=2.0)

        deflections = point_mass.deflections_from_grid(grid=np.array([[4.0, 9.0]]))
        assert deflections[0, 0] == pytest.approx(16.0 / 97.0, 1e-3)
        assert deflections[0, 1] == pytest.approx(36.0 / 97.0, 1e-3)

        point_mass = ag.mp.PointMass(centre=(1.0, 2.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(grid=np.array([[2.0, 3.0]]))
        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)

    def test__deflections__change_geometry(self):

        point_mass_0 = ag.mp.PointMass(centre=(0.0, 0.0))
        point_mass_1 = ag.mp.PointMass(centre=(1.0, 1.0))
        deflections_0 = point_mass_0.deflections_from_grid(grid=np.array([[1.0, 1.0]]))
        deflections_1 = point_mass_1.deflections_from_grid(grid=np.array([[0.0, 0.0]]))
        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        point_mass_0 = ag.mp.PointMass(centre=(0.0, 0.0))
        point_mass_1 = ag.mp.PointMass(centre=(0.0, 0.0))
        deflections_0 = point_mass_0.deflections_from_grid(grid=np.array([[1.0, 0.0]]))
        deflections_1 = point_mass_1.deflections_from_grid(grid=np.array([[0.0, 1.0]]))
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

    def test__multiple_coordinates_in__multiple_coordinates_out(self):

        point_mass = ag.mp.PointMass(centre=(1.0, 2.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=np.array([[2.0, 3.0], [2.0, 3.0], [2.0, 3.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)
        assert deflections[1, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.5, 1e-3)
        assert deflections[2, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[2, 1] == pytest.approx(0.5, 1e-3)

        point_mass = ag.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=np.array([[1.0, 1.0], [2.0, 2.0], [1.0, 1.0], [2.0, 2.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)

        assert deflections[1, 0] == pytest.approx(0.25, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.25, 1e-3)

        assert deflections[2, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[2, 1] == pytest.approx(0.5, 1e-3)

        assert deflections[3, 0] == pytest.approx(0.25, 1e-3)
        assert deflections[3, 1] == pytest.approx(0.25, 1e-3)

    def test__output_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        point_mass = ag.mp.PointMass()

        deflections = point_mass.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestBrokenPowerLaw:
    def test__convergence_correct_values(self):

        broken_power_law = ag.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        convergence = broken_power_law.convergence_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert convergence == pytest.approx(0.0355237, 1e-4)

        convergence = broken_power_law.convergence_from_grid(
            grid=np.array([[0.5, 1.0], [0.5, 1.0]])
        )

        assert convergence == pytest.approx([0.0355237, 0.0355237], 1e-4)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.096225, 0.055555),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        convergence = broken_power_law.convergence_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert convergence == pytest.approx(0.05006035, 1e-4)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(-0.113433, 0.135184),
            einstein_radius=1.0,
            inner_slope=1.8,
            outer_slope=2.2,
            break_radius=0.1,
        )

        convergence = broken_power_law.convergence_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert convergence == pytest.approx(0.034768, 1e-4)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.113433, -0.135184),
            einstein_radius=1.0,
            inner_slope=1.8,
            outer_slope=2.2,
            break_radius=0.1,
        )

        convergence = broken_power_law.convergence_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert convergence == pytest.approx(0.03622852, 1e-4)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(-0.173789, -0.030643),
            einstein_radius=1.0,
            inner_slope=1.8,
            outer_slope=2.2,
            break_radius=0.1,
        )

        convergence = broken_power_law.convergence_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert convergence == pytest.approx(0.026469, 1e-4)

    def test__deflections__correct_values(self):

        broken_power_law = ag.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.404076, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.808152, 1e-3)

        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0], [0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.404076, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.808152, 1e-3)
        assert deflections[1, 0] == pytest.approx(0.404076, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.808152, 1e-3)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.096225, 0.055555),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.40392, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.811619, 1e-3)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(-0.07142, -0.085116),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.4005338, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.8067221, 1e-3)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.109423, 0.019294),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.399651, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.813372, 1e-3)

        broken_power_law = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            elliptical_comps=(-0.216506, -0.125),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.402629, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.798795, 1e-3)

    def test__convergence__change_geometry(self):

        broken_power_law_0 = ag.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = ag.mp.SphericalBrokenPowerLaw(centre=(1.0, 1.0))

        convergence_0 = broken_power_law_0.convergence_from_grid(
            grid=np.array([[1.0, 1.0]])
        )

        convergence_1 = broken_power_law_1.convergence_from_grid(
            grid=np.array([[0.0, 0.0]])
        )

        assert convergence_0 == convergence_1

        broken_power_law_0 = ag.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = ag.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))

        convergence_0 = broken_power_law_0.convergence_from_grid(
            grid=np.array([[1.0, 0.0]])
        )

        convergence_1 = broken_power_law_1.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence_0 == convergence_1

        broken_power_law_0 = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        broken_power_law_1 = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        convergence_0 = broken_power_law_0.convergence_from_grid(
            grid=np.array([[1.0, 0.0]])
        )

        convergence_1 = broken_power_law_1.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence_0 == convergence_1

    def test__deflections__change_geometry(self):

        broken_power_law_0 = ag.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = ag.mp.SphericalBrokenPowerLaw(centre=(1.0, 1.0))

        deflections_0 = broken_power_law_0.deflections_from_grid(
            grid=np.array([[1.0, 1.0]])
        )
        deflections_1 = broken_power_law_1.deflections_from_grid(
            grid=np.array([[0.0, 0.0]])
        )

        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        broken_power_law_0 = ag.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = ag.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))

        deflections_0 = broken_power_law_0.deflections_from_grid(
            grid=np.array([[1.0, 0.0]])
        )
        deflections_1 = broken_power_law_1.deflections_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

        broken_power_law_0 = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        broken_power_law_1 = ag.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        deflections_0 = broken_power_law_0.deflections_from_grid(
            grid=np.array([[1.0, 0.0]])
        )
        deflections_1 = broken_power_law_1.deflections_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

    def test__deflections__compare_to_power_law(self):

        broken_power_law = ag.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=2.0,
            inner_slope=1.999,
            outer_slope=2.0001,
            break_radius=0.0001,
        )
        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        # Use of ratio avoids normalization definition difference effects

        broken_yx_ratio = deflections[0, 0] / deflections[0, 1]

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0, 0), einstein_radius=2.0, slope=2.0
        )
        deflections = power_law.deflections_from_grid(grid=np.array([[0.5, 1.0]]))

        power_law_yx_ratio = deflections[0, 0] / deflections[0, 1]

        assert broken_yx_ratio == pytest.approx(power_law_yx_ratio, 1.0e-4)

        broken_power_law = ag.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=2.0,
            inner_slope=2.399,
            outer_slope=2.4001,
            break_radius=0.0001,
        )
        deflections = broken_power_law.deflections_from_grid(
            grid=np.array([[0.5, 1.0]])
        )

        # Use of ratio avoids normalization difference effects

        broken_yx_ratio = deflections[0, 0] / deflections[0, 1]

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0, 0), einstein_radius=2.0, slope=2.4
        )
        deflections = power_law.deflections_from_grid(grid=np.array([[0.5, 1.0]]))

        power_law_yx_ratio = deflections[0, 0] / deflections[0, 1]

        assert broken_yx_ratio == pytest.approx(power_law_yx_ratio, 1.0e-4)

    def test__output_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        cored_power_law = ag.mp.EllipticalBrokenPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)

        cored_power_law = ag.mp.SphericalBrokenPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestCoredPowerLaw:
    def test__convergence_correct_values(self):

        cored_power_law = ag.mp.SphericalCoredPowerLaw(
            centre=(1, 1), einstein_radius=1.0, slope=2.2, core_radius=0.1
        )

        convergence = cored_power_law.convergence_func(grid_radius=1.0)

        assert convergence == pytest.approx(0.39762, 1e-4)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            slope=2.3,
            core_radius=0.2,
        )

        convergence = cored_power_law.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.45492, 1e-3)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=2.0,
            slope=1.7,
            core_radius=0.2,
        )

        convergence = cored_power_law.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(1.3887, 1e-3)

    def test__potential_correct_values(self):
        power_law = ag.mp.SphericalCoredPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.0, slope=1.8, core_radius=0.2
        )

        potential = power_law.potential_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert potential == pytest.approx(0.54913, 1e-3)

        power_law = ag.mp.SphericalCoredPowerLaw(
            centre=(0.2, -0.2), einstein_radius=0.5, slope=2.4, core_radius=0.5
        )

        potential = power_law.potential_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert potential == pytest.approx(0.01820, 1e-3)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.2, -0.2),
            elliptical_comps=(-0.216506, -0.125),
            einstein_radius=0.5,
            slope=2.4,
            core_radius=0.5,
        )

        potential = cored_power_law.potential_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert potential == pytest.approx(0.02319, 1e-3)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            slope=1.8,
            core_radius=0.2,
        )

        potential = cored_power_law.potential_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert potential == pytest.approx(0.71185, 1e-3)

    def test__deflections__correct_values(self):

        power_law = ag.mp.SphericalCoredPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.0, slope=1.8, core_radius=0.2
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(0.80677, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.30680, 1e-3)

        power_law = ag.mp.SphericalCoredPowerLaw(
            centre=(0.2, -0.2), einstein_radius=0.5, slope=2.4, core_radius=0.5
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(-0.00321, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.09316, 1e-3)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            slope=1.8,
            core_radius=0.2,
        )

        deflections = cored_power_law.deflections_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.9869, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.54882, 1e-3)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.2, -0.2),
            elliptical_comps=(-0.216506, -0.125),
            einstein_radius=0.5,
            slope=2.4,
            core_radius=0.5,
        )

        deflections = cored_power_law.deflections_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.01111, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.11403, 1e-3)

    def test__convergence__change_geometry(self):
        cored_power_law_0 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = ag.mp.SphericalCoredPowerLaw(centre=(1.0, 1.0))

        convergence_0 = cored_power_law_0.convergence_from_grid(
            grid=np.array([[1.0, 1.0]])
        )

        convergence_1 = cored_power_law_1.convergence_from_grid(
            grid=np.array([[0.0, 0.0]])
        )

        assert convergence_0 == convergence_1

        cored_power_law_0 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))

        convergence_0 = cored_power_law_0.convergence_from_grid(
            grid=np.array([[1.0, 0.0]])
        )

        convergence_1 = cored_power_law_1.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence_0 == convergence_1

        cored_power_law_0 = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        cored_power_law_1 = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        convergence_0 = cored_power_law_0.convergence_from_grid(
            grid=np.array([[1.0, 0.0]])
        )

        convergence_1 = cored_power_law_1.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence_0 == convergence_1

    def test__potential__change_geometry(self):
        cored_power_law_0 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = ag.mp.SphericalCoredPowerLaw(centre=(1.0, 1.0))

        potential_0 = cored_power_law_0.potential_from_grid(grid=np.array([[1.0, 1.0]]))

        potential_1 = cored_power_law_1.potential_from_grid(grid=np.array([[0.0, 0.0]]))

        assert potential_0 == potential_1

        cored_power_law_0 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))

        potential_0 = cored_power_law_0.potential_from_grid(grid=np.array([[1.0, 0.0]]))

        potential_1 = cored_power_law_1.potential_from_grid(grid=np.array([[0.0, 1.0]]))

        assert potential_0 == potential_1

        cored_power_law_0 = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        cored_power_law_1 = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )
        potential_0 = cored_power_law_0.potential_from_grid(grid=np.array([[1.0, 0.0]]))

        potential_1 = cored_power_law_1.potential_from_grid(grid=np.array([[0.0, 1.0]]))

        assert potential_0 == potential_1

    def test__deflections__change_geometry(self):
        cored_power_law_0 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = ag.mp.SphericalCoredPowerLaw(centre=(1.0, 1.0))

        deflections_0 = cored_power_law_0.deflections_from_grid(
            grid=np.array([[1.0, 1.0]])
        )
        deflections_1 = cored_power_law_1.deflections_from_grid(
            grid=np.array([[0.0, 0.0]])
        )

        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        cored_power_law_0 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = ag.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))

        deflections_0 = cored_power_law_0.deflections_from_grid(
            grid=np.array([[1.0, 0.0]])
        )
        deflections_1 = cored_power_law_1.deflections_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

        cored_power_law_0 = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        cored_power_law_1 = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        deflections_0 = cored_power_law_0.deflections_from_grid(
            grid=np.array([[1.0, 0.0]])
        )
        deflections_1 = cored_power_law_1.deflections_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

    def test__spherical_and_elliptical_match(self):
        elliptical = ag.mp.EllipticalCoredPowerLaw(
            centre=(1.1, 1.1),
            elliptical_comps=(0.0, 0.0),
            einstein_radius=3.0,
            slope=2.2,
            core_radius=0.1,
        )
        spherical = ag.mp.SphericalCoredPowerLaw(
            centre=(1.1, 1.1), einstein_radius=3.0, slope=2.2, core_radius=0.1
        )

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__output_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        cored_power_law = ag.mp.EllipticalCoredPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = cored_power_law.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)

        cored_power_law = ag.mp.SphericalCoredPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = cored_power_law.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestPowerLaw:
    def test__convergence_correct_values(self):

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=1.0, slope=2.0
        )

        convergence = power_law.convergence_from_grid(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(0.5, 1e-3)

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=2.0, slope=2.2
        )

        convergence = power_law.convergence_from_grid(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.4, 1e-3)

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=2.0, slope=2.2
        )

        convergence = power_law.convergence_from_grid(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.4, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            slope=2.3,
        )

        convergence = power_law.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.466666, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=2.0,
            slope=1.7,
        )

        convergence = power_law.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(1.4079, 1e-3)

    def test__potential_correct_values(self):
        power_law = ag.mp.SphericalPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=2.3
        )

        potential = power_law.potential_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert potential == pytest.approx(1.90421, 1e-3)

        power_law = ag.mp.SphericalPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=1.8
        )

        potential = power_law.potential_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert potential == pytest.approx(0.93758, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            slope=2.2,
        )

        potential = power_law.potential_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert potential == pytest.approx(1.53341, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            slope=1.8,
        )

        potential = power_law.potential_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert potential == pytest.approx(0.96723, 1e-3)

    def test__deflections__correct_values(self):

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0.2, 0.2), einstein_radius=1.0, slope=2.0
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(-0.31622, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.94868, 1e-3)

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0.2, 0.2), einstein_radius=1.0, slope=2.5
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(-1.59054, 1e-3)
        assert deflections[0, 1] == pytest.approx(-4.77162, 1e-3)

        power_law = ag.mp.SphericalPowerLaw(
            centre=(0.2, 0.2), einstein_radius=1.0, slope=1.5
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(-0.06287, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.18861, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            slope=2.0,
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(0.79421, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.50734, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            slope=2.5,
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(1.29641, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.99629, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(0, 0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            slope=1.5,
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(0.48036, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.26729, 1e-3)

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            slope=1.9,
        )

        deflections = power_law.deflections_from_grid(grid=np.array([[0.1625, 0.1625]]))

        # assert deflections[0, 0] == pytest.approx(1.12841, 1e-3)
        # assert deflections[0, 1] == pytest.approx(-0.60205, 1e-3)

    def test__compare_to_cored_power_law(self):

        power_law = ag.mp.EllipticalPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.333333, 0.0),
            einstein_radius=1.0,
            slope=2.3,
        )

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.333333, 0.0),
            einstein_radius=1.0,
            slope=2.3,
            core_radius=0.0,
        )

        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):

        elliptical = ag.mp.EllipticalPowerLaw(
            centre=(1.1, 1.1),
            elliptical_comps=(0.0, 0.0),
            einstein_radius=3.0,
            slope=2.4,
        )

        spherical = ag.mp.SphericalPowerLaw(
            centre=(1.1, 1.1), einstein_radius=3.0, slope=2.4
        )

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__output_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        power_law = ag.mp.EllipticalPowerLaw()

        convergence = power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = power_law.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)

        power_law = ag.mp.SphericalPowerLaw()

        convergence = power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = power_law.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestCoredIsothermal:
    def test__convergence_correct_values(self):

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(1, 1), einstein_radius=1.0, core_radius=0.1
        )

        convergence = cored_isothermal.convergence_func(grid_radius=1.0)

        assert convergence == pytest.approx(0.49752, 1e-4)

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(1, 1), einstein_radius=1.0, core_radius=0.1
        )

        convergence = cored_isothermal.convergence_func(grid_radius=1.0)

        assert convergence == pytest.approx(0.49752, 1e-4)

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0, core_radius=0.2
        )

        convergence = cored_isothermal.convergence_from_grid(
            grid=np.array([[1.0, 0.0]])
        )

        assert convergence == pytest.approx(0.49029, 1e-3)

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0, core_radius=0.2
        )

        convergence = cored_isothermal.convergence_from_grid(
            grid=np.array([[1.0, 0.0]])
        )

        assert convergence == pytest.approx(2.0 * 0.49029, 1e-3)

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0, core_radius=0.2
        )

        convergence = cored_isothermal.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(0.49029, 1e-3)

        # axis ratio changes only einstein_rescaled, so wwe can use the above value and times by 1.0/1.5.
        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            core_radius=0.2,
        )

        convergence = cored_isothermal.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(0.49029 * 1.33333, 1e-3)

        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            einstein_radius=2.0,
            core_radius=0.2,
        )

        convergence = cored_isothermal.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(2.0 * 0.49029, 1e-3)

        # for axis_ratio = 1.0, the factor is 1/2
        # for axis_ratio = 0.5, the factor is 1/(1.5)
        # So the change in the value is 0.5 / (1/1.5) = 1.0 / 0.75
        # axis ratio changes only einstein_rescaled, so wwe can use the above value and times by 1.0/1.5.

        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            einstein_radius=1.0,
            core_radius=0.2,
        )

        convergence = cored_isothermal.convergence_from_grid(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx((1.0 / 0.75) * 0.49029, 1e-3)

    def test__potential__correct_values(self):

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3, core_radius=0.2
        )

        potential = cored_isothermal.potential_from_grid(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert potential == pytest.approx(0.72231, 1e-3)

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(0.2, -0.2), einstein_radius=0.5, core_radius=0.5
        )

        potential = cored_isothermal.potential_from_grid(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert potential == pytest.approx(0.03103, 1e-3)

        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            core_radius=0.2,
        )

        potential = cored_isothermal.potential_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert potential == pytest.approx(0.74354, 1e-3)

        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(0.2, -0.2),
            elliptical_comps=(-0.216506, -0.125),
            einstein_radius=0.5,
            core_radius=0.5,
        )

        potential = cored_isothermal.potential_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert potential == pytest.approx(0.04024, 1e-3)

    def test__deflections__correct_values(self):

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3, core_radius=0.2
        )

        deflections = cored_isothermal.deflections_from_grid(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.98582, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.37489, 1e-3)

        cored_isothermal = ag.mp.SphericalCoredIsothermal(
            centre=(0.2, -0.2), einstein_radius=0.5, core_radius=0.5
        )

        deflections = cored_isothermal.deflections_from_grid(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(-0.00559, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.16216, 1e-3)

        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
            core_radius=0.2,
        )

        deflections = cored_isothermal.deflections_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.95429, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.52047, 1e-3)

        cored_isothermal = ag.mp.EllipticalCoredIsothermal(
            centre=(0.2, -0.2),
            elliptical_comps=(-0.216506, -0.125),
            einstein_radius=0.5,
            core_radius=0.5,
        )

        deflections = cored_isothermal.deflections_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.02097, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.20500, 1e-3)

    def test__compare_to_cored_power_law(self):

        power_law = ag.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            elliptical_comps=(0.333333, 0.0),
            einstein_radius=1.0,
            core_radius=0.1,
        )

        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.333333, 0.0),
            einstein_radius=1.0,
            slope=2.0,
            core_radius=0.1,
        )

        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):
        elliptical = ag.mp.EllipticalCoredIsothermal(
            centre=(1.1, 1.1),
            elliptical_comps=(0.0, 0.0),
            einstein_radius=3.0,
            core_radius=1.0,
        )
        spherical = ag.mp.SphericalCoredIsothermal(
            centre=(1.1, 1.1), einstein_radius=3.0, core_radius=1.0
        )

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__output_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        cored_isothermal = ag.mp.EllipticalCoredIsothermal()

        convergence = cored_isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = cored_isothermal.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = cored_isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)

        cored_isothermal = ag.mp.SphericalCoredIsothermal()

        convergence = cored_isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = cored_isothermal.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = cored_isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestIsothermal:
    def test__convergence__correct_values(self):

        # eta = 1.0
        # kappa = 0.5 * 1.0 ** 1.0

        isothermal = ag.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=2.0)

        convergence = isothermal.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.5 * 2.0, 1e-3)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), einstein_radius=1.0
        )

        convergence = isothermal.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.5, 1e-3)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), einstein_radius=2.0
        )

        convergence = isothermal.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.5 * 2.0, 1e-3)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.333333), einstein_radius=1.0
        )

        convergence = isothermal.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.66666, 1e-3)

    def test__potential__correct_values(self):

        isothermal = ag.mp.SphericalIsothermal(centre=(-0.7, 0.5), einstein_radius=1.3)

        potential = isothermal.potential_from_grid(grid=np.array([[0.1875, 0.1625]]))

        assert potential == pytest.approx(1.23435, 1e-3)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(-0.7, 0.5),
            elliptical_comps=(0.152828, -0.088235),
            einstein_radius=1.3,
        )

        potential = isothermal.potential_from_grid(grid=np.array([[0.1625, 0.1625]]))

        assert potential == pytest.approx(1.19268, 1e-3)

    def test__deflections__correct_values(self):

        isothermal = ag.mp.SphericalIsothermal(centre=(-0.7, 0.5), einstein_radius=1.3)

        deflections = isothermal.deflections_from_grid(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(1.21510, 1e-4)
        assert deflections[0, 1] == pytest.approx(-0.46208, 1e-4)

        isothermal = ag.mp.SphericalIsothermal(centre=(-0.1, 0.1), einstein_radius=5.0)

        deflections = isothermal.deflections_from_grid(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(4.88588, 1e-4)
        assert deflections[0, 1] == pytest.approx(1.06214, 1e-4)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0, 0), elliptical_comps=(0.0, 0.333333), einstein_radius=1.0
        )

        deflections = isothermal.deflections_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.79421, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.50734, 1e-3)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0, 0), elliptical_comps=(0.0, 0.333333), einstein_radius=1.0
        )

        deflections = isothermal.deflections_from_grid(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.79421, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.50734, 1e-3)

    def test__shear__correct_values(self):

        isothermal = ag.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=2.0)

        convergence = isothermal.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        shear = isothermal.shear_from_grid(grid=np.array([[0.0, 1.0]]))

        assert shear[0, 0] == pytest.approx(0.0, 1e-4)
        assert shear[0, 1] == pytest.approx(-convergence, 1e-4)

        convergence = isothermal.convergence_from_grid(grid=np.array([[2.0, 1.0]]))
        shear = isothermal.shear_from_grid(grid=np.array([[2.0, 1.0]]))

        assert shear[0, 0] == pytest.approx(-(4.0 / 5.0) * convergence, 1e-4)
        assert shear[0, 1] == pytest.approx((3.0 / 5.0) * convergence, 1e-4)

        convergence = isothermal.convergence_from_grid(grid=np.array([[3.0, 5.0]]))
        shear = isothermal.shear_from_grid(grid=np.array([[3.0, 5.0]]))

        assert shear[0, 0] == pytest.approx(-(30.0 / 34.0) * convergence, 1e-4)
        assert shear[0, 1] == pytest.approx(-(16.0 / 34.0) * convergence, 1e-4)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), einstein_radius=2.0
        )

        convergence = isothermal.convergence_from_grid(grid=np.array([[0.0, 1.0]]))

        shear = isothermal.shear_from_grid(grid=np.array([[0.0, 1.0]]))

        assert shear[0, 0] == pytest.approx(0.0, 1e-4)
        assert shear[0, 1] == pytest.approx(-convergence, 1e-4)

        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.3, 0.4), einstein_radius=2.0
        )

        shear = isothermal.shear_from_grid(grid=np.array([[0.0, 1.0]]))

        assert shear[0, 0] == pytest.approx(0.35355, 1e-4)
        assert shear[0, 1] == pytest.approx(-1.06066, 1e-4)

    def test__compare_to_cored_power_law(self):
        isothermal = ag.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.333333, 0.0), einstein_radius=1.0
        )
        cored_power_law = ag.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            elliptical_comps=(0.333333, 0.0),
            einstein_radius=1.0,
            core_radius=0.0,
        )

        assert isothermal.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert isothermal.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert isothermal.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )
        assert isothermal.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):
        elliptical = ag.mp.EllipticalIsothermal(
            centre=(1.1, 1.1), elliptical_comps=(0.0, 0.0), einstein_radius=3.0
        )
        spherical = ag.mp.SphericalIsothermal(centre=(1.1, 1.1), einstein_radius=3.0)

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__output_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        isothermal = ag.mp.EllipticalIsothermal()

        convergence = isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = isothermal.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)

        isothermal = ag.mp.SphericalIsothermal()

        convergence = isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_native == (2, 2)

        potential = isothermal.potential_from_grid(grid=grid)

        assert potential.shape_native == (2, 2)

        deflections = isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_native == (2, 2)
