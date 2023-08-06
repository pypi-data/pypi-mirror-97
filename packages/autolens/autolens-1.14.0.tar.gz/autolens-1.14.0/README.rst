PyAutoLens: Open-Source Strong Lensing
======================================

.. |nbsp| unicode:: 0xA0
    :trim:

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Jammy2211/autofit_workspace/HEAD

.. |code-style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |JOSS| image:: https://joss.theoj.org/papers/10.21105/joss.02825/status.svg
   :target: https://doi.org/10.21105/joss.02825

.. |arXiv| image:: https://img.shields.io/badge/arXiv-1708.07377-blue
    :target: https://arxiv.org/abs/1708.07377

|binder| |code-style| |JOSS| |arXiv|

`Installation Guide <https://pyautolens.readthedocs.io/en/latest/installation/overview.html>`_ |
`readthedocs <https://pyautolens.readthedocs.io/en/latest/index.html>`_ |
`Introduction on Binder <https://mybinder.org/v2/gh/Jammy2211/autolens_workspace/3b48dbc1b0ee85e68a24394895702df78e465323?filepath=introduction.ipynb>`_ |
`HowToLens <https://pyautolens.readthedocs.io/en/latest/howtolens/howtolens.html>`_

When two or more galaxies are aligned perfectly down our line-of-sight, the background galaxy appears multiple times.
This is called strong gravitational lensing and **PyAutoLens** makes it simple to model strong gravitational lenses,
like this one:

.. image:: https://github.com/Jammy2211/PyAutoLens/blob/master/files/imageaxis.png

Getting Started
---------------

The following links are useful for new starters:

- `The introduction Jupyter Notebook on Binder <https://mybinder.org/v2/gh/Jammy2211/autolens_workspace/3b48dbc1b0ee85e68a24394895702df78e465323?filepath=introduction.ipynb>`_, where you can try **PyAutoLens** in a web browser (without installation).

- `The PyAutoLens readthedocs <https://pyautolens.readthedocs.io/en/latest>`_, which includes `an installation guide <https://pyautolens.readthedocs.io/en/latest/installation/overview.html>`_ and an overview of **PyAutoLens**'s core features.

- `The autolens_workspace GitHub repository <https://github.com/Jammy2211/autolens_workspace>`_, which includes example scripts and the `HowToLens Jupyter notebook tutorials <https://github.com/Jammy2211/autolens_workspace/tree/master/notebooks/howtolens>`_ which give new users a step-by-step introduction to **PyAutoLens**.

API Overview
------------

Lensing calculations are performed in **PyAutoLens** by building a ``Tracer`` object from ``LightProfile``,
``MassProfile`` and ``Galaxy`` objects. Below, we create a simple strong lens system where a redshift 0.5
lens ``Galaxy`` with an ``EllipticalIsothermal`` ``MassProfile`` lenses a background source at redshift 1.0 with an
``EllipticalExponential`` ``LightProfile`` representing a disk.

.. code-block:: python

    import autolens as al
    import autolens.plot as aplt
    from astropy import cosmology as cosmo

    """
    To describe the deflection of light by mass, two-dimensional grids of (y,x) Cartesian
    coordinates are used.
    """
    grid = al.Grid2D.uniform(
        shape_native=(50, 50),
        pixel_scales=0.05,  # <- Conversion from pixel units to arc-seconds.
    )

    """
    The lens galaxy has an EllipticalIsothermal MassProfile and is at redshift 0.5.
    """
    mass = al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0), elliptical_comps=(0.1, 0.05), einstein_radius=1.6
    )

    lens_galaxy = al.Galaxy(redshift=0.5, mass=mass)

    """
    The source galaxy has an EllipticalExponential LightProfile and is at redshift 1.0.
    """
    disk = al.lp.EllipticalExponential(
        centre=(0.3, 0.2),
        elliptical_comps=(0.05, 0.25),
        intensity=0.05,
        effective_radius=0.5,
    )

    source_galaxy = al.Galaxy(redshift=1.0, disk=disk)

    """
    We create the strong lens using a Tracer, which uses the galaxies, their redshifts
    and an input cosmology to determine how light is deflected on its path to Earth.
    """
    tracer = al.Tracer.from_galaxies(
        galaxies=[lens_galaxy, source_galaxy], cosmology=cosmo.Planck15
    )

    """
    We can use the Grid2D and Tracer to perform many lensing calculations, for example
    plotting the image of the lensed source.
    """
    tracer_plotter = aplt.TracerPlotter(tracer=tracer, grid=grid)
    tracer_plotter.figures(image=True)

With **PyAutoLens**, you can begin modeling a lens in just a couple of minutes. The example below demonstrates
a simple analysis which fits the lens galaxy's mass with an ``EllipticalIsothermal`` and the source galaxy's light
with an ``EllipticalSersic``.

.. code-block:: python

    import autofit as af
    import autolens as al
    import autolens.plot as aplt

    """
    Load Imaging data of the strong lens from the dataset folder of the workspace.
    """
    imaging = al.Imaging.from_fits(
        image_path="/path/to/dataset/image.fits",
        noise_map_path="/path/to/dataset/noise_map.fits",
        psf_path="/path/to/dataset/psf.fits",
        pixel_scales=0.1,
    )

    """
    Create a mask for the data, which we setup as a 3.0" circle.
    """
    mask = al.Mask2D.circular(
        shape_native=imaging.shape_native, pixel_scales=imaging.pixel_scales, radius=3.0
    )

    """
    We model the lens galaxy using an EllipticalIsothermal MassProfile and
    the source galaxy using an EllipticalSersic LightProfile.
    """
    lens_mass_profile = al.mp.EllipticalIsothermal
    source_light_profile = al.lp.EllipticalSersic

    """
    To setup these profiles as model components whose parameters are free & fitted for
    we use the GalaxyModel class.
    """
    lens_galaxy_model = al.GalaxyModel(redshift=0.5, mass=lens_mass_profile)
    source_galaxy_model = al.GalaxyModel(redshift=1.0, disk=source_light_profile)

    """
    To perform the analysis we set up a phase, which takes our galaxy models & fits
    their parameters using a NonLinearSearch (in this case, Dynesty).
    """
    phase = al.PhaseImaging(
        search=af.DynestyStatic(name="phase[example]",n_live_points=50),
        galaxies=dict(lens=lens_galaxy_model, source=source_galaxy_model),
    )

    """
    We pass the imaging dataset and mask to the phase's run function, fitting it
    with the lens model & outputting the results (dynesty samples, visualization,
    etc.) to hard-disk.
    """
    result = phase.run(dataset=imaging, mask=mask)

    """
    The results contain information on the fit, for example the maximum likelihood
    model from the Dynesty parameter space search.
    """
    print(result.samples.max_log_likelihood_instance)

Support
-------

Support for installation issues, help with lens modeling and using **PyAutoLens** is available by
`raising an issue on the GitHub issues page <https://github.com/Jammy2211/PyAutoLens/issues>`_.

We also offer support on the **PyAutoLens** `Slack channel <https://pyautolens.slack.com/>`_, where we also provide the
latest updates on **PyAutoLens**. Slack is invitation-only, so if you'd like to join send
an `email <https://github.com/Jammy2211>`_ requesting an invite.
