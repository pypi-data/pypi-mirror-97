import autofit as af
from autogalaxy.pipeline.phase.abstract import analysis as abstract_analysis
from autogalaxy.galaxy import galaxy as g
from autogalaxy.plane import plane as pl

import numpy as np
import pickle
import dill


def last_result_with_use_as_hyper_dataset(results):

    if results is not None:
        if results.last is not None:
            for index, result in enumerate(reversed(results)):
                if hasattr(result, "use_as_hyper_dataset"):
                    if result.use_as_hyper_dataset:
                        return result


class Analysis(abstract_analysis.Analysis):
    def __init__(self, masked_dataset, cosmology, settings, results, preloads=None):

        super().__init__(cosmology=cosmology, settings=settings)

        self.masked_dataset = masked_dataset

        result = last_result_with_use_as_hyper_dataset(results=results)

        if result is not None:

            self.hyper_galaxy_image_path_dict = result.hyper_galaxy_image_path_dict
            self.hyper_model_image = result.hyper_model_image

        else:

            self.hyper_galaxy_image_path_dict = None
            self.hyper_model_image = None

        self.preloads = preloads

    def hyper_image_sky_for_instance(self, instance):

        if hasattr(instance, "hyper_image_sky"):
            return instance.hyper_image_sky

    def hyper_background_noise_for_instance(self, instance):

        if hasattr(instance, "hyper_background_noise"):
            return instance.hyper_background_noise

    def plane_for_instance(self, instance):
        return pl.Plane(galaxies=instance.galaxies)

    def associate_hyper_images(self, instance: af.ModelInstance) -> af.ModelInstance:
        """
        Takes images from the last result, if there is one, and associates them with galaxies in this phase
        where full-path galaxy names match.

        If the galaxy collection has a different name then an association is not made.

        e.g.
        galaxies.lens will match with:
            galaxies.lens
        but not with:
            galaxies.lens
            galaxies.source

        Parameters
        ----------
        instance
            A model instance with 0 or more galaxies in its tree

        Returns
        -------
        instance
           The input instance with images associated with galaxies where possible.
        """

        if self.hyper_galaxy_image_path_dict is not None:

            for galaxy_path, galaxy in instance.path_instance_tuples_for_class(
                g.Galaxy
            ):
                if galaxy_path in self.hyper_galaxy_image_path_dict:
                    galaxy.hyper_model_image = self.hyper_model_image

                    galaxy.hyper_galaxy_image = self.hyper_galaxy_image_path_dict[
                        galaxy_path
                    ]

        return instance

    def save_attributes_for_aggregator(self, paths: af.Paths):

        self.save_dataset(paths=paths)
        self.save_mask(paths=paths)
        self.save_settings(paths=paths)
        self.save_attributes(paths=paths)

    def save_dataset(self, paths: af.Paths):
        """
        Save the dataset associated with the phase
        """
        with open(f"{paths.pickle_path}/dataset.pickle", "wb") as f:
            pickle.dump(self.masked_dataset.dataset, f)

    def save_mask(self, paths: af.Paths):
        """
        Save the mask associated with the phase
        """
        with open(f"{paths.pickle_path}/mask.pickle", "wb") as f:
            dill.dump(self.masked_dataset.mask, f)

    def make_attributes(self):
        raise NotImplementedError

    def save_attributes(self, paths: af.Paths):

        attributes = self.make_attributes()
        with open(f"{paths.pickle_path}/attributes.pickle", "wb+") as f:
            pickle.dump(attributes, f)
