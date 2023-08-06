import pytest
from matplotlib import pyplot
from os import path

from autoconf import conf
from autogalaxy.mock import fixtures


class PlotPatch:
    def __init__(self):
        self.paths = []

    def __call__(self, path, *args, **kwargs):
        self.paths.append(path)


@pytest.fixture(name="plot_patch")
def make_plot_patch(monkeypatch):
    plot_patch = PlotPatch()
    monkeypatch.setattr(pyplot, "savefig", plot_patch)
    return plot_patch


directory = path.dirname(path.realpath(__file__))


@pytest.fixture(autouse=True)
def set_config_path(request):

    conf.instance.push(
        new_path=path.join(directory, "config"),
        output_path=path.join(directory, "output"),
    )


### Datasets ###


@pytest.fixture(name="psf_3x3")
def make_psf_3x3():
    return fixtures.make_psf_3x3()


@pytest.fixture(name="rectangular_inversion_7x7_3x3")
def make_rectangular_inversion_7x7_3x3():
    return fixtures.make_rectangular_inversion_7x7_3x3()


@pytest.fixture(name="voronoi_inversion_9_3x3")
def make_voronoi_inversion_9_3x3():
    return fixtures.make_voronoi_inversion_9_3x3()


@pytest.fixture(name="rectangular_mapper_7x7_3x3")
def make_rectangular_mapper_7x7_3x3():
    return fixtures.make_rectangular_mapper_7x7_3x3()


@pytest.fixture(name="fit_interferometer_7")
def make_masked_interferometer_fit_x1_plane_7(masked_interferometer_7):
    return fixtures.make_masked_interferometer_fit_x1_plane_7()


@pytest.fixture(name="noise_map_7x7")
def make_noise_map_7x7():
    return fixtures.make_noise_map_7x7()


@pytest.fixture(name="sub_mask_7x7")
def make_sub_mask_7x7():
    return fixtures.make_sub_mask_7x7()


@pytest.fixture(name="imaging_7x7")
def make_imaging_7x7():
    return fixtures.make_imaging_7x7()


@pytest.fixture(name="image_7x7")
def make_image_7x7():
    return fixtures.make_image_7x7()


@pytest.fixture(name="masked_imaging_7x7")
def make_masked_imaging_7x7():
    return fixtures.make_masked_imaging_7x7()


@pytest.fixture(name="masked_imaging_no_blur_7x7")
def make_masked_imaging_no_blur_7x7():
    return fixtures.make_masked_imaging_no_blur_7x7()


@pytest.fixture(name="interferometer_7")
def make_interferometer_7():
    return fixtures.make_interferometer_7()


@pytest.fixture(name="mask_7x7")
def make_mask_7x7():
    return fixtures.make_mask_7x7()


@pytest.fixture(name="convolver_7x7")
def make_convolver_7x7():
    return fixtures.make_convolver_7x7()


@pytest.fixture(name="mask_7x7_1_pix")
def make_mask_7x7_1_pix():
    return fixtures.make_mask_7x7_1_pix()


@pytest.fixture(name="grid_iterate_7x7")
def make_grid_iterate_7x7():
    return fixtures.make_grid_iterate_7x7()


@pytest.fixture(name="grid_irregular_7x7")
def make_grid_irregular_7x7():
    return fixtures.make_grid_irregular_7x7()


@pytest.fixture(name="grid_irregular_7x7_list")
def make_grid_irregular_7x7_list():
    return fixtures.make_grid_irregular_7x7_list()


@pytest.fixture(name="transformer_7x7_7")
def make_transformer_7x7_7():
    return fixtures.make_transformer_7x7_7()


@pytest.fixture(name="visibilities_mask_7")
def make_visibilities_mask_7():
    return fixtures.make_visibilities_mask_7()


@pytest.fixture(name="blurring_grid_7x7")
def make_blurring_grid_7x7():
    return fixtures.make_blurring_grid_7x7()


@pytest.fixture(name="noise_map_7")
def make_noise_map_7():
    return fixtures.make_visibilities_noise_map_7()


@pytest.fixture(name="visibilities_7")
def make_visibilities_7():
    return fixtures.make_visibilities_7()


@pytest.fixture(name="grid_7x7")
def make_grid_7x7():
    return fixtures.make_grid_7x7()


@pytest.fixture(name="sub_grid_7x7")
def make_sub_grid_7x7():
    return fixtures.make_sub_grid_7x7()


@pytest.fixture(name="sub_grid_7x7_simple")
def make_sub_grid_7x7_simple():
    return fixtures.make_sub_grid_7x7_simple()


@pytest.fixture(name="masked_interferometer_7")
def make_masked_interferometer_7():
    return fixtures.make_masked_interferometer_7()


@pytest.fixture(name="masked_interferometer_7_lop")
def make_masked_interferometer_7_lop():
    return fixtures.make_masked_interferometer_7_lop()


@pytest.fixture(name="ps_0")
def make_ps_0():
    return fixtures.make_ps_0()


@pytest.fixture(name="ps_1")
def make_ps_1():
    return fixtures.make_ps_1()


@pytest.fixture(name="lp_0")
def make_lp_0():
    return fixtures.make_lp_0()


@pytest.fixture(name="lp_1")
def make_lp_1():
    return fixtures.make_lp_1()


@pytest.fixture(name="mp_0")
def make_mp_0():
    return fixtures.make_mp_0()


@pytest.fixture(name="mp_1")
def make_mp_1():
    return fixtures.make_mp_1()


@pytest.fixture(name="lmp_0")
def make_lmp_0():
    return fixtures.make_lmp_0()


@pytest.fixture(name="dmp_0")
def make_dmp_0():
    return fixtures.make_dmp_0()


@pytest.fixture(name="dmp_1")
def make_dmp_1():
    return fixtures.make_dmp_1()


@pytest.fixture(name="smp_0")
def make_smp_0():
    return fixtures.make_smp_0()


@pytest.fixture(name="smp_1")
def make_smp_1():
    return fixtures.make_smp_1()


@pytest.fixture(name="gal_x1_lp")
def make_gal_x1_lp():
    return fixtures.make_gal_x1_lp()


@pytest.fixture(name="gal_x2_lp")
def make_gal_x2_lp():
    return fixtures.make_gal_x2_lp()


@pytest.fixture(name="gal_x1_mp")
def make_gal_x1_mp():
    return fixtures.make_gal_x1_mp()


@pytest.fixture(name="gal_x2_mp")
def make_gal_x2_mp():
    return fixtures.make_gal_x2_mp()


@pytest.fixture(name="gal_x1_lp_x1_mp")
def make_gal_x1_lp_x1_mp():
    return fixtures.make_gal_x1_lp_x1_mp()


@pytest.fixture(name="hyper_galaxy")
def make_hyper_galaxy():
    return fixtures.make_hyper_galaxy()


@pytest.fixture(name="plane_7x7")
def make_plane_7x7():
    return fixtures.make_plane_7x7()


@pytest.fixture(name="gal_data_7x7")
def make_gal_data_7x7():
    return fixtures.make_gal_data_7x7()


@pytest.fixture(name="gal_fit_7x7_image")
def make_gal_fit_7x7_image():
    return fixtures.make_gal_fit_7x7_image()


@pytest.fixture(name="gal_fit_7x7_convergence")
def make_gal_fit_7x7_convergence():
    return fixtures.make_gal_fit_7x7_convergence()


@pytest.fixture(name="gal_fit_7x7_potential")
def make_gal_fit_7x7_potential():
    return fixtures.make_gal_fit_7x7_potential()


@pytest.fixture(name="gal_fit_7x7_deflections_y")
def make_gal_fit_7x7_deflections_y():
    return fixtures.make_gal_fit_7x7_deflections_y()


@pytest.fixture(name="gal_fit_7x7_deflections_x")
def make_gal_fit_7x7_deflections_x():
    return fixtures.make_gal_fit_7x7_deflections_x()


@pytest.fixture(name="hyper_model_image_7x7")
def make_hyper_model_image_7x7():
    return fixtures.make_hyper_model_image_7x7()


@pytest.fixture(name="hyper_galaxy_image_0_7x7")
def make_hyper_galaxy_image_0_7x7():
    return fixtures.make_hyper_galaxy_image_0_7x7()


@pytest.fixture(name="hyper_galaxy_image_path_dict_7x7")
def make_hyper_galaxy_image_path_dict_7x7():
    return fixtures.make_hyper_galaxy_image_path_dict_7x7()


@pytest.fixture(name="contribution_map_7x7")
def make_contribution_map_7x7(
    hyper_model_image_7x7, hyper_galaxy_image_0_7x7, hyper_galaxy
):
    return hyper_galaxy.contribution_map_from_hyper_images(
        hyper_model_image=hyper_model_image_7x7,
        hyper_galaxy_image=hyper_galaxy_image_0_7x7,
    )


### FITS ###


@pytest.fixture(name="masked_imaging_fit_7x7")
def make_masked_imaging_fit_7x7():
    return fixtures.make_masked_imaging_fit_7x7()


@pytest.fixture(name="masked_imaging_fit_x2_galaxy_7x7")
def make_masked_imaging_fit_x2_galaxy_7x7():
    return fixtures.make_masked_imaging_fit_x2_galaxy_7x7()


@pytest.fixture(name="masked_imaging_fit_x2_galaxy_inversion_7x7")
def make_masked_imaging_fit_x2_galaxy_inversion_7x7():
    return fixtures.make_masked_imaging_fit_x2_galaxy_inversion_7x7()


@pytest.fixture(name="masked_interferometer_fit_7x7")
def make_masked_interferometer_fit_7x7():
    return fixtures.make_masked_interferometer_fit_7x7()


@pytest.fixture(name="masked_interferometer_fit_x2_galaxy_inversion_7x7")
def make_masked_interferometer_fit_x2_galaxy_inversion_7x7():
    return fixtures.make_masked_interferometer_fit_x2_galaxy_inversion_7x7()


@pytest.fixture(name="samples_with_result")
def make_samples_with_result():
    return fixtures.make_samples_with_result()


@pytest.fixture(name="phase_dataset_7x7")
def make_phase_data():
    return fixtures.make_phase_data()


@pytest.fixture(name="phase_imaging_7x7")
def make_phase_imaging_7x7():
    return fixtures.make_phase_imaging_7x7()


@pytest.fixture(name="phase_interferometer_7")
def make_phase_interferometer_7():
    return fixtures.make_phase_interferometer_7()


@pytest.fixture(name="voronoi_mapper_9_3x3")
def make_voronoi_mapper_9_3x3():
    return fixtures.make_voronoi_mapper_9_3x3()


@pytest.fixture(name="include_2d_all")
def make_include_all():
    return fixtures.make_include_all()
