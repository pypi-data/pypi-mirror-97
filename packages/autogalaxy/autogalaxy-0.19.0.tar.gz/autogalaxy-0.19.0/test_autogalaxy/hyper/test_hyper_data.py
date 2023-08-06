from autoconf import conf
import autogalaxy as ag
import numpy as np

import pytest


class TestHyperImageSky:
    def test__scale_sky_in_image__increases_all_image_values(self):

        image = np.array([1.0, 2.0, 3.0])

        hyper_sky = ag.hyper_data.HyperImageSky(sky_scale=10.0)

        scaled_image = hyper_sky.hyper_image_from_image(image=image)

        assert (scaled_image == np.array([11.0, 12.0, 13.0])).all()


class TestHyperNoiseMapBackground:
    def test__scaled_background_noise__adds_to_input_noise(self):

        noise_map = np.array([1.0, 2.0, 3.0])

        hyper_background_noise_map = ag.hyper_data.HyperBackgroundNoise(noise_scale=2.0)

        hyper_noise_map = hyper_background_noise_map.hyper_noise_map_from_noise_map(
            noise_map=noise_map
        )

        assert (hyper_noise_map == np.array([3.0, 4.0, 5.0])).all()

        hyper_noise_map_background = ag.hyper_data.HyperBackgroundNoise(noise_scale=3.0)

        scaled_noise = hyper_noise_map_background.hyper_noise_map_from_noise_map(
            noise_map=noise_map
        )

        assert (scaled_noise == np.array([4.0, 5.0, 6.0])).all()

    def test__scaled_background_noise__adds_to_input_noise__uses_complex_if_input_is_complex(
        self,
    ):

        noise_map = np.array([1.0 + 1.0j, 2.0 + 2.0j, 3.0 + 3.0j])

        hyper_background_noise_map = ag.hyper_data.HyperBackgroundNoise(noise_scale=2.0)

        hyper_noise_map = hyper_background_noise_map.hyper_noise_map_from_complex_noise_map(
            noise_map=noise_map
        )

        assert (hyper_noise_map == np.array([3.0 + 3.0j, 4.0 + 4.0j, 5.0 + 5.0j])).all()

        hyper_noise_map_background = ag.hyper_data.HyperBackgroundNoise(noise_scale=3.0)

        scaled_noise = hyper_noise_map_background.hyper_noise_map_from_complex_noise_map(
            noise_map=noise_map
        )

        assert (scaled_noise == np.array([4.0 + 4.0j, 5.0 + 5.0j, 6.0 + 6.0j])).all()
