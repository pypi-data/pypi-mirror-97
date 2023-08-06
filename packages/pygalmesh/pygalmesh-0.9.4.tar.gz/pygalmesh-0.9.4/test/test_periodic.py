import numpy

import pygalmesh


def test_schwarz():
    class Schwarz(pygalmesh.DomainBase):
        def __init__(self):
            super().__init__()

        def eval(self, x):
            x2 = numpy.cos(x[0] * 2 * numpy.pi)
            y2 = numpy.cos(x[1] * 2 * numpy.pi)
            z2 = numpy.cos(x[2] * 2 * numpy.pi)
            return x2 + y2 + z2

    mesh = pygalmesh.generate_periodic_mesh(
        Schwarz(),
        [0, 0, 0, 1, 1, 1],
        max_cell_circumradius=0.05,
        min_facet_angle=30,
        max_radius_surface_delaunay_ball=0.05,
        max_facet_distance=0.025,
        max_circumradius_edge_ratio=2.0,
        number_of_copies_in_output=4,
        # odt=True,
        # lloyd=True,
        verbose=False,
    )

    # The RNG in CGAL makes the following assertions fail sometimes.
    # assert len(mesh.cells["triangle"]) == 12784
    # assert len(mesh.cells["tetra"]) == 67120

    return mesh


if __name__ == "__main__":
    import meshio

    mesh = test_schwarz()
    meshio.write("out.vtk", mesh)
