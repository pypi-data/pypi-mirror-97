class HyperImageSky:
    def __init__(self, sky_scale=0.0):
        """Class for scaling the background sky map and background noise_map of an grid.

        Parameters
        -----------
        sky_scale : float
            The value by which the background scale is increased or decreased (electrons per second).
        noise_scale : float
            The factor by which the background noise_maps is increased.
        """
        self.sky_scale = sky_scale

    def hyper_image_from_image(self, image):
        """
        Returns a new with the background sky level hyper. This can simply multiple by a instance factor \
        (assuming a uniform background sky) because the is in units electrons per second.

        Parameters
        -----------
        image : np.ndarray
            The before scaling (electrons per second).
        """
        return image + self.sky_scale


class HyperBackgroundNoise:
    def __init__(self, noise_scale=0.0):
        """Class for scaling the background sky map and background noise_map of an grid.

        Parameters
        -----------
        sky_scale : float
            The value by which the background scale is increased or decreased (electrons per second).
        noise_scale : float
            The factor by which the background noise_maps is increased.
        """
        self.noise_scale = noise_scale

    def hyper_noise_map_from_noise_map(self, noise_map):
        """
        Returns a hyper noise_maps from the background noise_maps grid.

            Parameters
            -----------
            noise_map : np.ndarray
                The noise_maps before scaling (electrons per second).
            background_noise : np.ndarray
                The background noise_maps values (electrons per second).
        """
        return noise_map + self.noise_scale

    def hyper_noise_map_from_complex_noise_map(self, noise_map):
        """
        Returns a hyper noise_maps from the background noise_maps grid.

            Parameters
            -----------
            noise_map : np.ndarray
                The noise_maps before scaling (electrons per second).
            background_noise : np.ndarray
                The background noise_maps values (electrons per second).
        """
        return noise_map + (1.0 + 1.0j) * self.noise_scale
