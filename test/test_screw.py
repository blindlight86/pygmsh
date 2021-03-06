#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygmsh

from helpers import compute_volume


def test(lcar=0.05):
    geom = pygmsh.built_in.Geometry()

    # Draw a cross with a circular hole
    circ = geom.add_circle([0.0, 0.0, 0.0], 0.1, lcar=lcar)
    poly = geom.add_polygon(
        [
            [+0.0, +0.5, 0.0],
            [-0.1, +0.1, 0.0],
            [-0.5, +0.0, 0.0],
            [-0.1, -0.1, 0.0],
            [+0.0, -0.5, 0.0],
            [+0.1, -0.1, 0.0],
            [+0.5, +0.0, 0.0],
            [+0.1, +0.1, 0.0],
        ],
        lcar=lcar,
        holes=[circ],
    )

    axis = [0, 0, 1.0]

    geom.extrude(
        poly,
        translation_axis=axis,
        rotation_axis=axis,
        point_on_axis=[0, 0, 0],
        angle=2.0 / 6.0 * np.pi,
    )

    ref = 0.16951514066385628
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == "__main__":
    import meshio

    meshio.write("screw.vtu", *test())
