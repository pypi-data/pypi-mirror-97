# %%
"""
__Positions Tester__

This tool creates a set of positions using the _peaks criteria from a high resolution grid, without any buffering or
upscaling. This means:

    - It will not incorrectly remove any true multiple images due to grid buffering / refinement.
    - Extra multiple images will be includded corresponding to peaks in the mass profile that are local, not global.

These results are used to test whether more efficient position solvers implementations lose multiple images.
"""


# %%
import autofit as af
import autolens as al
import autolens.plot as aplt
from test_autolens.positions_solver import util
import os

# %%
"""The pickle path is where the `Tracer` and `Positions` are output, so they can be loaded by other scripts."""

# %%
path = "{}".format(os.path.dirname(os.path.realpath(__file__)))
pickle_path = f"{path}/pickles"

# %%
"""The initial grid for position solver which is upscaled iteratively by the solver."""

# %%
grid = al.Grid2D.uniform(
    shape_native=(200, 200),
    pixel_scales=0.05,  # <- The pixel-scale describes the conversion from pixel units to arc-seconds.
)

"""Use a `PositionsSolver` which uses grid upscaling."""

solver = al.PositionsSolver(grid=grid, pixel_scale_precision=0.01, upscale_factor=3)

iters = 50

for i in range(iters):

    tracer = al.Tracer.load(file_path=pickle_path, filename=f"tracer_{str(i)}")

    positions = solver.solve(
        lensing_obj=tracer,
        source_plane_coordinate=tracer.source_plane.galaxies[0].light.centre,
    )

    positions_true = al.Grid2DIrregular.load(
        file_path=pickle_path, filename=f"positions_{str(i)}"
    )

    minimum_separations = util.minimum_separations_from(
        positions_true=positions, positions=positions_true
    )
    in_positions_true = util.check_if_positions_in_positions_true(
        positions_true=positions_true, positions=positions, threshold=0.1
    )

    print()
    print(positions_true.in_grouped_list)
    print(positions.in_grouped_list)
    print(minimum_separations)
    print(in_positions_true)

    positions_plot = al.Grid2DIrregular(
        grid=[positions.in_grouped_list[0], positions_true.in_grouped_list[0]]
    )

    visuals_2d = aplt.Visuals2D(positions=positions_plot)

    tracer_plotter = aplt.TracerPlotter(tracer=tracer, grid=grid)
    tracer_plotter.figure_image(visuals_2d=visuals_2d)
