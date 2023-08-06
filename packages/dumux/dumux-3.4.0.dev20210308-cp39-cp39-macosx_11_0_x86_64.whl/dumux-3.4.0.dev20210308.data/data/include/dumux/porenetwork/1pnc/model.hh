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
 * \ingroup PNMOnePNCModel
 * \brief Adaption of the fully implicit scheme to the one-phase n-component pore network model.
 *
 * A mass balance equation is formulated for each pore body \f$i\f$ and each component \f$\kappa\f$:
 *
 * \f[
 *	V_i \frac{\partial (\varrho_{i} X^\kappa)}{\partial t} + \sum_j (\varrho X^\kappa Q)_{ij} = (V q^\kappa)_i ~.
 * \f]
 *
 * \f$V_i\f$ is the pore body volume, and the advective mass flow \f$(\varrho Q X^\kappa)_{ij}\f$ through throat \f$ij\f$ can be based on the fluid phase density
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
 *
 * The model is able to use either mole or mass fractions. The property useMoles can be set to either true or false in the
 * problem file. Make sure that the according units are used in the problem setup. useMoles is set to true by default.
 *
 * The primary variables are the pressure \f$p\f$ and the mass or mole fraction of dissolved components \f$X^\kappa\f$ or \f$x^\kappa\f$.
 */

#ifndef DUMUX_PNM1PNC_MODEL_HH
#define DUMUX_PNM1PNC_MODEL_HH

#include <dumux/common/properties.hh>

#include <dumux/flux/porenetwork/fickslaw.hh>

#include <dumux/material/fluidmatrixinteractions/diffusivitymillingtonquirk.hh>
#include <dumux/material/fluidmatrixinteractions/porenetwork/throat/transmissibility1p.hh>
#include <dumux/material/fluidstates/immiscible.hh>
#include <dumux/material/spatialparams/porenetwork/porenetwork1p.hh>

#include <dumux/porenetwork/properties.hh>
#include <dumux/porenetwork/1p/model.hh>

#include <dumux/porousmediumflow/compositional/localresidual.hh>
#include <dumux/porousmediumflow/nonisothermal/model.hh>
#include <dumux/porousmediumflow/nonisothermal/indices.hh>
#include <dumux/porousmediumflow/nonisothermal/iofields.hh>
#include <dumux/porousmediumflow/1pnc/model.hh>
#include <dumux/porousmediumflow/1pnc/iofields.hh>

#include "iofields.hh"
#include "volumevariables.hh"

namespace Dumux::Properties {
//////////////////////////////////////////////////////////////////
// Type tags
//////////////////////////////////////////////////////////////////

//! The type tags for the implicit single-phase mulit-component problems
// Create new type tags
namespace TTag {
struct PNMOnePNC { using InheritsFrom = std::tuple<PoreNetworkModel, OnePNC>; };

//! The type tags for the corresponding non-isothermal problems
struct PNMOnePNCNI { using InheritsFrom = std::tuple<PNMOnePNC>; };
} // end namespace TTag

///////////////////////////////////////////////////////////////////////////
// properties for the isothermal single phase model
///////////////////////////////////////////////////////////////////////////

//! The spatial parameters to be employed.
//! Use PNMOnePSpatialParams by default.
template<class TypeTag>
struct SpatialParams<TypeTag, TTag::PNMOnePNC>
{
private:
    using GridGeometry = GetPropType<TypeTag, Properties::GridGeometry>;
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
public:
    using type = Dumux::PoreNetwork::OnePDefaultSpatialParams<GridGeometry, Scalar>;
};

//! The advection type
template<class TypeTag>
struct AdvectionType<TypeTag, TTag::PNMOnePNC>
{
private:
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using TransmissibilityLaw = Dumux::PoreNetwork::TransmissibilityPatzekSilin<Scalar, false/*considerPoreBodyResistance*/>;
public:
    using type = Dumux::PoreNetwork::CreepingFlow<Scalar, TransmissibilityLaw>;
};

//! Set as default that no component mass balance is replaced by the total mass balance
template<class TypeTag>
struct ReplaceCompEqIdx<TypeTag, TTag::PNMOnePNC>
{
private:
    using FluidSystem = GetPropType<TypeTag, Properties::FluidSystem>;
public:
    static constexpr auto value = FluidSystem::numComponents;
};

//! We use fick's law as the default for the diffusive fluxes
template<class TypeTag>
struct MolecularDiffusionType<TypeTag, TTag::PNMOnePNC>
{
private:
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using ModelTraits = GetPropType<TypeTag, Properties::ModelTraits>;
public:
    using type = Dumux::PoreNetwork::PNMFicksLaw<Scalar, ModelTraits::numFluidPhases(), ModelTraits::numFluidComponents()>;
};

//! Set the volume variables property
template<class TypeTag>
struct VolumeVariables<TypeTag, TTag::PNMOnePNC>
{
private:
    using PV = GetPropType<TypeTag, Properties::PrimaryVariables>;
    using FSY = GetPropType<TypeTag, Properties::FluidSystem>;
    using FST = GetPropType<TypeTag, Properties::FluidState>;
    using SSY = GetPropType<TypeTag, Properties::SolidSystem>;
    using SST = GetPropType<TypeTag, Properties::SolidState>;
    using MT = GetPropType<TypeTag, Properties::ModelTraits>;
    using PT = typename GetPropType<TypeTag, Properties::SpatialParams>::PermeabilityType;
    static_assert(FSY::numComponents == MT::numFluidComponents(), "Number of components mismatch between model and fluid system");
    static_assert(FST::numComponents == MT::numFluidComponents(), "Number of components mismatch between model and fluid state");
    static_assert(FSY::numPhases == MT::numFluidPhases(), "Number of phases mismatch between model and fluid system");
    static_assert(FST::numPhases == MT::numFluidPhases(), "Number of phases mismatch between model and fluid state");
    using BaseTraits = Dumux::OnePVolumeVariablesTraits<PV, FSY, FST, SSY, SST, PT, MT>;

    using DT = GetPropType<TypeTag, Properties::MolecularDiffusionType>;
    using EDM = GetPropType<TypeTag, Properties::EffectiveDiffusivityModel>;
    template<class BaseTraits, class DT, class EDM>
    struct NCTraits : public BaseTraits
    {
        using DiffusionType = DT;
        using EffectiveDiffusivityModel = EDM;
    };

public:
    using type = Dumux::PoreNetwork::OnePNCVolumeVariables<NCTraits<BaseTraits, DT, EDM>>;
};

//!< Set the vtk output fields specific to this model
template<class TypeTag>
struct IOFields<TypeTag, TTag::PNMOnePNC>
{ using type = Dumux::PoreNetwork::OnePNCIOFields<GetPropType<TypeTag, Properties::FluidSystem>>; };

template<class TypeTag>
struct UseMoles<TypeTag, TTag::PNMOnePNC> { static constexpr bool value = true; };

//////////////////////////////////////////////////////////////////
// Property values for isothermal model required for the general non-isothermal model
//////////////////////////////////////////////////////////////////

//! model traits of the non-isothermal model.
template<class TypeTag>
struct ModelTraits<TypeTag, TTag::PNMOnePNCNI>
{
private:
    using FluidSystem = GetPropType<TypeTag, Properties::FluidSystem>;
    using IsothermalTraits = OnePNCModelTraits<FluidSystem::numComponents, getPropValue<TypeTag, Properties::UseMoles>(), getPropValue<TypeTag, Properties::ReplaceCompEqIdx>()>;
public:
    using type = PorousMediumFlowNIModelTraits<IsothermalTraits>;
};

template<class TypeTag>
struct VolumeVariables<TypeTag, TTag::PNMOnePNCNI>
{
private:
    using PV = GetPropType<TypeTag, Properties::PrimaryVariables>;
    using FSY = GetPropType<TypeTag, Properties::FluidSystem>;
    using FST = GetPropType<TypeTag, Properties::FluidState>;
    using SSY = GetPropType<TypeTag, Properties::SolidSystem>;
    using SST = GetPropType<TypeTag, Properties::SolidState>;
    using MT = GetPropType<TypeTag, Properties::ModelTraits>;
    using PT = typename GetPropType<TypeTag, Properties::SpatialParams>::PermeabilityType;
    static_assert(FSY::numComponents == MT::numFluidComponents(), "Number of components mismatch between model and fluid system");
    static_assert(FST::numComponents == MT::numFluidComponents(), "Number of components mismatch between model and fluid state");
    static_assert(FSY::numPhases == MT::numFluidPhases(), "Number of phases mismatch between model and fluid system");
    static_assert(FST::numPhases == MT::numFluidPhases(), "Number of phases mismatch between model and fluid state");
    using BaseTraits = Dumux::OnePVolumeVariablesTraits<PV, FSY, FST, SSY, SST, PT, MT>;

    using DT = GetPropType<TypeTag, Properties::MolecularDiffusionType>;
    using EDM = GetPropType<TypeTag, Properties::EffectiveDiffusivityModel>;
    using ETCM = GetPropType< TypeTag, Properties:: ThermalConductivityModel>;
    template<class BaseTraits, class DT, class EDM, class ETCM>
    struct NCNITraits : public BaseTraits
    {
        using DiffusionType = DT;
        using EffectiveDiffusivityModel = EDM;
        using EffectiveThermalConductivityModel = ETCM;
    };

public:
    using type = Dumux::PoreNetwork::OnePNCVolumeVariables<NCNITraits<BaseTraits, DT, EDM, ETCM>>;
};

template<class TypeTag>
struct IOFields<TypeTag, TTag::PNMOnePNCNI>
{
private:
    using FluidSystem = GetPropType<TypeTag, Properties::FluidSystem>;
    using IsothermalFields = Dumux::PoreNetwork::OnePNCIOFields<FluidSystem>;
public:
    using type = EnergyIOFields<IsothermalFields>;
};

template<class TypeTag>
struct ThermalConductivityModel<TypeTag, TTag::PNMOnePNCNI>
{
    using type = ThermalConductivityAverage<GetPropType<TypeTag, Properties::Scalar>>;
}; //!< Use the average for effective conductivities

} // end namespace Dumux::Properties
#endif
