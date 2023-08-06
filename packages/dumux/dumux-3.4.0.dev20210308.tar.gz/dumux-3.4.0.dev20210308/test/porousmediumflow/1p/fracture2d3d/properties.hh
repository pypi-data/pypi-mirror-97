// -*- mode: C++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*-
// vi: set et ts=4 sw=4 sts=4:
/*****************************************************************************
 *   See the file COPYING for full copying permissions.                      *
 *                                                                           *
 *   This program is free software: you can redistribute it and/or modify    *
 *   it under the terms of the GNU General Public License as published by    *
 *   the Free Software Foundation, either version 3 of the License, or       *
 *   (at your option) any later version.                                     *
 *                                                                           *
 *   This program is distributed in the hope that it will be useful,         *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of          *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the            *
 *   GNU General Public License for more details.                            *
 *                                                                           *
 *   You should have received a copy of the GNU General Public License       *
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.   *
 *****************************************************************************/
/*!
 * \file
 * \ingroup OnePTests
 * \brief A discrete fracture network embedded in an impermeable matrix.
 *
 * The fracture is a 2D network embedded in 3D.
 */

#ifndef DUMUX_ONEP_FRACTURE_TEST_PROPERTIES_HH
#define DUMUX_ONEP_FRACTURE_TEST_PROPERTIES_HH

#if HAVE_DUNE_FOAMGRID
#include <dune/foamgrid/foamgrid.hh>
#endif

#include <dumux/material/components/simpleh2o.hh>
#include <dumux/material/fluidsystems/1pliquid.hh>

#include <dumux/porousmediumflow/1p/model.hh>

#include <dumux/discretization/box.hh>
#include <dumux/discretization/cctpfa.hh>
#include <dumux/discretization/ccmpfa.hh>

#include "problem.hh"
#include "spatialparams.hh"

namespace Dumux::Properties {
// Create new type tags
namespace TTag {
struct Fracture { using InheritsFrom = std::tuple<OneP>; };
struct FractureBox { using InheritsFrom = std::tuple<Fracture, BoxModel>; };
struct FractureCCTpfa { using InheritsFrom = std::tuple<Fracture, CCTpfaModel>; };
struct FractureCCMpfa { using InheritsFrom = std::tuple<Fracture, CCMpfaModel>; };
} // end namespace TTag

//! Enable caching (more memory, but faster runtime)
template<class TypeTag>
struct EnableGridGeometryCache<TypeTag, TTag::Fracture> { static constexpr bool value = true; };
template<class TypeTag>
struct EnableGridVolumeVariablesCache<TypeTag, TTag::Fracture> { static constexpr bool value = true; };
template<class TypeTag>
struct EnableGridFluxVariablesCache<TypeTag, TTag::Fracture> { static constexpr bool value = true; };

//! The grid type
#if HAVE_DUNE_FOAMGRID
template<class TypeTag>
struct Grid<TypeTag, TTag::Fracture> { using type = Dune::FoamGrid<2, 3>; };
#endif

// Set the problem property
template<class TypeTag>
struct Problem<TypeTag, TTag::Fracture> { using type = Dumux::FractureProblem<TypeTag>; };

// the fluid system
template<class TypeTag>
struct FluidSystem<TypeTag, TTag::Fracture>
{
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using type = FluidSystems::OnePLiquid<Scalar, Components::SimpleH2O<Scalar> >;
};
// Set the spatial parameters
template<class TypeTag>
struct SpatialParams<TypeTag, TTag::Fracture>
{
    using GridGeometry = GetPropType<TypeTag, Properties::GridGeometry>;
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using type = FractureSpatialParams<GridGeometry, Scalar>;
};

} // end namespace Dumux::Properties

#endif
