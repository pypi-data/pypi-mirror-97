import autogalaxy as ag


def test__tag__mixture_of_values():

    settings = ag.SettingsPhaseImaging(
        settings_masked_imaging=ag.SettingsMaskedImaging(
            grid_class=ag.Grid2D,
            grid_inversion_class=ag.Grid2D,
            sub_size=2,
            signal_to_noise_limit=2,
            psf_shape_2d=None,
        )
    )

    assert settings.phase_tag_no_inversion == "settings__imaging[grid_sub_2__snr_2]"
    assert (
        settings.phase_tag_with_inversion
        == "settings__imaging[grid_sub_2_inv_sub_2__snr_2]__pix[use_border]__inv[mat]"
    )

    settings = ag.SettingsPhaseImaging(
        settings_masked_imaging=ag.SettingsMaskedImaging(
            grid_class=ag.Grid2D,
            grid_inversion_class=ag.Grid2DIterate,
            sub_size=1,
            fractional_accuracy=0.1,
            signal_to_noise_limit=None,
            psf_shape_2d=(2, 2),
        )
    )

    assert settings.phase_tag_no_inversion == "settings__imaging[grid_sub_1__psf_2x2]"
    assert (
        settings.phase_tag_with_inversion
        == "settings__imaging[grid_sub_1_inv_facc_0.1__psf_2x2]__pix[use_border]__inv[mat]"
    )

    settings = ag.SettingsPhaseInterferometer(
        settings_masked_interferometer=ag.SettingsMaskedInterferometer(
            grid_class=ag.Grid2DIterate,
            grid_inversion_class=ag.Grid2D,
            fractional_accuracy=0.1,
            sub_size=3,
            sub_size_inversion=3,
            transformer_class=ag.TransformerDFT,
        ),
        settings_inversion=ag.SettingsInversion(use_linear_operators=False),
        log_likelihood_cap=200.001,
    )

    assert (
        settings.phase_tag_no_inversion
        == "settings__interferometer[grid_facc_0.1__dft]__lh_cap_200.0"
    )
    assert (
        settings.phase_tag_with_inversion
        == "settings__interferometer[grid_facc_0.1_inv_sub_3__dft]__pix[use_border]__inv[mat]__lh_cap_200.0"
    )

    settings = ag.SettingsPhaseInterferometer(
        settings_masked_interferometer=ag.SettingsMaskedInterferometer(
            grid_class=ag.Grid2DIterate,
            grid_inversion_class=ag.Grid2D,
            fractional_accuracy=0.1,
            sub_size=3,
            sub_size_inversion=3,
            transformer_class=ag.TransformerNUFFT,
        ),
        settings_inversion=ag.SettingsInversion(use_linear_operators=True),
    )

    assert (
        settings.phase_tag_no_inversion
        == "settings__interferometer[grid_facc_0.1__nufft]"
    )
    assert (
        settings.phase_tag_with_inversion
        == "settings__interferometer[grid_facc_0.1_inv_sub_3__nufft]__pix[use_border]__inv[lop]"
    )
