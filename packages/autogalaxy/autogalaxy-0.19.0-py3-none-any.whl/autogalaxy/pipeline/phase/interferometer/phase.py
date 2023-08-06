from os import path
import autofit as af
from astropy import cosmology as cosmo
from autogalaxy.dataset import interferometer
from autogalaxy.pipeline.phase.settings import SettingsPhaseInterferometer
from autogalaxy.pipeline.phase import dataset
from autogalaxy.pipeline.phase.interferometer.analysis import Analysis
from autogalaxy.pipeline.phase.interferometer.result import Result


class PhaseInterferometer(dataset.PhaseDataset):
    galaxies = af.PhaseProperty("galaxies")
    hyper_background_noise = af.PhaseProperty("hyper_background_noise")

    Analysis = Analysis
    Result = Result

    def __init__(
        self,
        *,
        search,
        real_space_mask,
        galaxies=None,
        hyper_background_noise=None,
        settings=SettingsPhaseInterferometer(),
        cosmology=cosmo.Planck15,
        use_as_hyper_dataset=False
    ):

        """

        A phase in an lens pipeline. Uses the set non_linear search to try to fit models and hyper_galaxies
        passed to it.

        Parameters
        ----------
        search: class
            The class of a non_linear search
        sub_size: int
            The side length of the subgrid
        """

        search.paths.tag = settings.phase_tag_with_inversion

        super().__init__(
            galaxies=galaxies,
            settings=settings,
            search=search,
            cosmology=cosmology,
            use_as_hyper_dataset=use_as_hyper_dataset,
        )

        self.hyper_background_noise = hyper_background_noise
        self.is_hyper_phase = False
        self.real_space_mask = real_space_mask

    def make_analysis(self, dataset, mask, results=None, preloads=None):
        """
        Returns an lens object. Also calls the prior passing and masked_interferometer modifying functions to allow child
        classes to change the behaviour of the phase.

        Parameters
        ----------
        mask: Mask2D
            The default masks passed in by the pipeline
        dataset: im.Interferometer
            An masked_interferometer that has been masked
        results: autofit.tools.pipeline.ResultsCollection
            The result from the previous phase

        Returns
        -------
        lens : Analysis
            An lens object that the `NonLinearSearch` calls to determine the fit of a set of values
        """

        masked_interferometer = interferometer.MaskedInterferometer(
            interferometer=dataset,
            visibilities_mask=mask,
            real_space_mask=self.real_space_mask,
            settings=self.settings.settings_masked_interferometer,
        )

        self.output_phase_info()

        analysis = self.Analysis(
            masked_interferometer=masked_interferometer,
            settings=self.settings,
            cosmology=self.cosmology,
            results=results,
            preloads=preloads,
        )

        return analysis

    def output_phase_info(self):

        file_phase_info = path.join(self.search.paths.output_path, "phase.info")

        with open(file_phase_info, "w") as phase_info:
            phase_info.write("Optimizer = {} \n".format(type(self.search).__name__))
            phase_info.write(
                "Sub-grid size = {} \n".format(
                    self.settings.settings_masked_interferometer.sub_size
                )
            )
            phase_info.write("Cosmology = {} \n".format(self.cosmology))

            phase_info.close()
