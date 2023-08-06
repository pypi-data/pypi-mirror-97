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
 * \ingroup OnePNCMinTests
 * \brief Definition of the properties for thermochemical heat storage using \f$ \textnormal{CaO},
 * \textnormal{Ca} \left( \textnormal{OH} \right)_2\f$.
 */
#ifndef DUMUX_THERMOCHEM_PROBLEM_PROPERTIES_HH
#define DUMUX_THERMOCHEM_PROBLEM_PROPERTIES_HH

#include <dune/grid/yaspgrid.hh>

#include <dumux/discretization/box.hh>
#include <dumux/porousmediumflow/1pncmin/model.hh>

#include <dumux/material/fluidsystems/1padapter.hh>
#include <dumux/material/fluidsystems/h2on2.hh>
#include <dumux/material/components/cao2h2.hh>
#include <dumux/material/solidsystems/compositionalsolidphase.hh>

#include "problem.hh"
#include "spatialparams.hh"
#include "modifiedcao.hh"

namespace Dumux::Properties {

// Create new type tags
namespace TTag {
struct ThermoChem { using InheritsFrom = std::tuple<OnePNCMinNI>; };
struct ThermoChemBox { using InheritsFrom = std::tuple<ThermoChem, BoxModel>; };
} // end namespace TTag

// Set the grid type
template<class TypeTag>
struct Grid<TypeTag, TTag::ThermoChem> { using type = Dune::YaspGrid<2>; };

// Set the problem property
template<class TypeTag>
struct Problem<TypeTag, TTag::ThermoChem> { using type = ThermoChemProblem<TypeTag>; };

// The fluid system
template<class TypeTag>
struct FluidSystem<TypeTag, TTag::ThermoChem>
{
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using H2ON2 = FluidSystems::H2ON2<Scalar>;
    static constexpr auto phaseIdx = H2ON2::gasPhaseIdx; // simulate the air phase
    using type = FluidSystems::OnePAdapter<H2ON2, phaseIdx>;
};

// The solid system
template<class TypeTag>
struct SolidSystem<TypeTag, TTag::ThermoChem>
{
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using ComponentOne = Components::ModifiedCaO<Scalar>;
    using ComponentTwo = Components::CaO2H2<Scalar>;
    using type = SolidSystems::CompositionalSolidPhase<Scalar, ComponentOne, ComponentTwo>;
};

// Set the spatial parameters
template<class TypeTag>
struct SpatialParams<TypeTag, TTag::ThermoChem>
{
    using GridGeometry = GetPropType<TypeTag, Properties::GridGeometry>;
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using type = ThermoChemSpatialParams<GridGeometry, Scalar>;
};

// Define whether mole(true) or mass (false) fractions are used
template<class TypeTag>
struct UseMoles<TypeTag, TTag::ThermoChem> { static constexpr bool value = true; };

} // end namespace Properties

#endif
