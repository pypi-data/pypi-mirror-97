#ifndef GENERATE_SURFACE_MESH_HPP
#define GENERATE_SURFACE_MESH_HPP

#include "domain.hpp"

#include <memory>
#include <string>

namespace pygalmesh {

void generate_surface_mesh(
    const std::shared_ptr<pygalmesh::DomainBase> & domain,
    const std::string & outfile,
    const double bounding_sphere_radius = 0.0,
    const double min_facet_angle = 0.0,
    const double max_radius_surface_delaunay_ball = 0.0,
    const double max_facet_distance = 0.0,
    const bool verbose = true,
    const int seed = 0
    );

} // namespace pygalmesh

#endif // GENERATE_SURFACE_MESH_HPP
