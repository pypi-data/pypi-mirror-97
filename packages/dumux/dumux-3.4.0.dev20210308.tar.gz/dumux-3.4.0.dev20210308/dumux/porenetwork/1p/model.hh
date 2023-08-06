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
 * \ingroup PNMOnePModel
 * \brief A one-phase-flow, isothermal pore-network model using the fully implicit scheme.
 *
 * A mass balance equation is formulated for each pore body \f$i\f$:
 *
 * \f[
 *	V_i \frac{\partial (\varrho_{i})}{\partial t} + \sum_j (\varrho Q)_{ij} = (V q)_i ~.
 * \f]
 *
 * \f$V_i\f$ is the pore body volume, and the advective mass flow \f$(\varrho Q)_{ij}\f$ through throat \f$ij\f$ can be based on the fluid phase density
 * \f$\varrho\f$ either of the upstream pore body \f$i\f$ or \f$j\f$ (upwinding) or on the respective averaged value. \f$q_i\f$ is a mass sink or source
 * term defined on pore body \f$i\f$.
 *
 * Per default, the volume flow rate \f$Q_{ij}\f$ follows a linear Hagen-Poiseuille-type law (Dumux::PoreNetworkModel::CreepingFlow) which is only valid for \f$Re < 1\f$:
 *
 * \f[
 *	Q_{ij} = g_{ij} (p_{i} - p_{j} + \Psi)  ~.
 * \f]
 *
 * \f$g_{ij}\f$ is a suitable throat conductance value (see e.g. Dumux::PoreNetwork::TransmissibilityPatzekSilin) while \f$p_i\f$ and \f$p_j\f$ are averaged pore body pressures.
 *
 * The (optional) influence of gravity is given by
 *
 * \f[
 *	\Psi = \varrho \mathbf{g} (\mathbf{x_i} - \mathbf{x_j}) ~,
 * \f]
 *
 * where \f$\mathbf{x_i} - \mathbf{x_j}\f$  is the distance vector between the centers of pore bodies \f$i\f$ and \f$j\f$ and \f$\mathbf{g}\f$ is the gravitational acceleration.
 */

#ifndef DUMUX_PNM1P_MODEL_HH
#define DUMUX_PNM1P_MODEL_HH

#include <dumux/common/properties.hh>
#include <dumux/flux/porenetwork/advection.hh>
#include <dumux/porenetwork/properties.hh>

#include <dumux/porousmediumflow/immiscible/localresidual.hh>
#include <dumux/porousmediumflow/nonisothermal/model.hh>
#include <dumux/porousmediumflow/nonisothermal/iofields.hh>

#include <dumux/porousmediumflow/1p/model.hh>

#include <dumux/material/spatialparams/porenetwork/porenetwork1p.hh>
#include <dumux/material/fluidmatrixinteractions/porenetwork/throat/transmissibility1p.hh>

#include "iofields.hh"
#include "volumevariables.hh"
#include "fluxvariablescache.hh"

namespace Dumux::Properties {

 //////////////////////////////////////////////////////////////////
 // Type tags
 //////////////////////////////////////////////////////////////////

//! The type tags for the implicit single-phase problems
namespace TTag {
struct PNMOneP { using InheritsFrom = std::tuple<PoreNetworkModel, OneP>; };

//! The type tags for the corresponding non-isothermal problems
struct PNMOnePNI { using InheritsFrom = std::tuple<PNMOneP>; };
} // end namespace TTag

///////////////////////////////////////////////////////////////////////////
// properties for the isothermal single phase model
///////////////////////////////////////////////////////////////////////////

//! Set the volume variables property
template<class TypeTag>
struct VolumeVariables<TypeTag, TTag::PNMOneP>
{
private:
    using PV = GetPropType<TypeTag, Properties::PrimaryVariables>;
    using FSY = GetPropType<TypeTag, Properties::FluidSystem>;
    using FST = GetPropType<TypeTag, Properties::FluidState>;
    using SSY = GetPropType<TypeTag, Properties::SolidSystem>;
    using SST = GetPropType<TypeTag, Properties::SolidState>;
    using MT = GetPropType<TypeTag, Properties::ModelTraits>;
    using PT = typename GetPropType<TypeTag, Properties::SpatialParams>::PermeabilityType;

    using Traits = Dumux::OnePVolumeVariablesTraits<PV, FSY, FST, SSY, SST, PT, MT>;
public:
    using type = Dumux::PoreNetwork::OnePVolumeVariables<Traits>;
};

//! The spatial parameters to be employed.
//! Use OnePDefaultSpatialParams by default.
template<class TypeTag>
struct SpatialParams<TypeTag, TTag::PNMOneP>
{
private:
    using GridGeometry = GetPropType<TypeTag, Properties::GridGeometry>;
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
public:
    using type = Dumux::PoreNetwork::OnePDefaultSpatialParams<GridGeometry, Scalar>;
};

//! The flux variables cache
template<class TypeTag>
struct FluxVariablesCache<TypeTag, TTag::PoreNetworkModel>
{ using type = Dumux::PoreNetwork::OnePFluxVariablesCache<GetPropType<TypeTag, Properties::AdvectionType>>; };

//! Default I/O fields specific to this model
template<class TypeTag>
struct IOFields<TypeTag, TTag::PNMOneP> { using type = Dumux::PoreNetwork::OnePIOFields; };

//! The advection type
template<class TypeTag>
struct AdvectionType<TypeTag, TTag::PNMOneP>
{
private:
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using TransmissibilityLaw = Dumux::PoreNetwork::TransmissibilityPatzekSilin<Scalar, false/*considerPoreBodyResistance*/>;
public:
    using type = Dumux::PoreNetwork::CreepingFlow<Scalar, TransmissibilityLaw>;
};

//////////////////////////////////////////////////////////////////
// Property values for isothermal model required for the general non-isothermal model
//////////////////////////////////////////////////////////////////

//! Set the volume variables property
template<class TypeTag>
struct VolumeVariables<TypeTag, TTag::PNMOnePNI>
{
private:
    using PV = GetPropType<TypeTag, Properties::PrimaryVariables>;
    using FSY = GetPropType<TypeTag, Properties::FluidSystem>;
    using FST = GetPropType<TypeTag, Properties::FluidState>;
    using SSY = GetPropType<TypeTag, Properties::SolidSystem>;
    using SST = GetPropType<TypeTag, Properties::SolidState>;
    using PT = typename GetPropType<TypeTag, Properties::SpatialParams>::PermeabilityType;
    using MT = GetPropType<TypeTag, Properties::ModelTraits>;
    using BaseTraits = OnePVolumeVariablesTraits<PV, FSY, FST, SSY, SST, PT, MT>;

    using ETCM = GetPropType<TypeTag, Properties::ThermalConductivityModel>;
    template<class BaseTraits, class ETCM>
    struct NITraits : public BaseTraits { using EffectiveThermalConductivityModel = ETCM; };

public:
    using type = Dumux::PoreNetwork::OnePVolumeVariables<NITraits<BaseTraits, ETCM>>;
};

//! Add temperature to the output
template<class TypeTag>
struct IOFields<TypeTag, TTag::PNMOnePNI> { using type = EnergyIOFields<Dumux::PoreNetwork::OnePIOFields>; };

//! The model traits of the non-isothermal model
template<class TypeTag>
struct ModelTraits<TypeTag, TTag::PNMOnePNI> { using type = PorousMediumFlowNIModelTraits<OnePModelTraits>; };

//! Use the average for effective conductivities
template<class TypeTag>
struct ThermalConductivityModel<TypeTag, TTag::PNMOnePNI> { using type = ThermalConductivityAverage<GetPropType<TypeTag, Properties::Scalar>>; };

} // end namespace Dumux::Properies

#endif
