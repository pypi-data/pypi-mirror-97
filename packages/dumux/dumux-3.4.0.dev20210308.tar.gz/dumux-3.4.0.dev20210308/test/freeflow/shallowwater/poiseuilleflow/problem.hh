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

#ifndef DUMUX_POISEUILLE_FLOW_TEST_PROBLEM_HH
#define DUMUX_POISEUILLE_FLOW_TEST_PROBLEM_HH

#include <dumux/common/properties.hh>
#include <dumux/common/parameters.hh>
#include <dumux/freeflow/shallowwater/problem.hh>
#include <dumux/freeflow/shallowwater/boundaryfluxes.hh>

#include <algorithm>
#include <cctype>

namespace Dumux {

/*!
 * \ingroup ShallowWaterTests
 * \brief A simple test for the 2D flow in a channel with rough side walls (Poiseuille flow).
 *
 * The domain has a length L =  400 meters long and a width W = 100 meters.
 * The domain extent is from (x,y) = (0.0, -50.0) to (400.0, 50.0), i.e. the channel centreline is at y = 0.
 * The bed level is sloped from z = -9.98 (x = 0) to z = -10.0 meters (x = L).
 * The initital water depth corresponds to the analytical solution:
 * having a slope equal to \f$ ib = d \Theta / L \f$ , where \f$ d \Theta \f$ is the water level difference between upstream and downstream: \f$ d \Theta \f$ = 0.02 m (positive downwards).
 * With L = 400 m, the slope is ib = 0.00005 m/m, resulting in a constant water depth along the channel of H = 10.0 m.

 * At the west/left  (inflow)  boundary a discharge is prescribed of \f$ Q_{in} = -408.75 m^3/s \f$ or \f$ q_{in} = 4.0875 m^2/s \f$ per meter.
 * At the east/right (outflow) boundary a fixed water level is prescribed of \f$ \Theta \f$ = 0.0 m.
 * The south and north boundaries are set to roughwall type boundaries,
 * with a coefficient alphaWall = 1.0, where:
 *      alphaWall = 0.0: full    slip (smooth wall)
 * 0.0 <alphaWall < 1.0: partial slip (partially-rough wall)
 *      alphaWall = 1.0: no      slip (fully-rough wall)
 * Additionally these (south and north) boundaries are (automatically) set to no-flow boundaries.

 * The flow in the channel experiences two forces:
 * 1) the pressure gradient, driving the flow downstream
 * 2) the wall roughness,

 * It can be verified that this force balance reduces the momentum equation in X-direction to:
 *
  \f[
  \frac{\partial p}{\partial x} = \nu_T \frac{\partial^2 u}{\partial y^2}
  \f]
 * where \f$ \nu_T \f$ is the turbulent viscosity.
 *
 * This ordinary differential equation can be solved (applying the boundary conditions to obtain the integration constants),
 * resulting in a parabolic velocity profile in lateral direction (over the width of the channel):
 *
  \f[
  u(y) = \frac{g d \Theta}{8 \nu_T L} \left(4y^2 - W^2\right)
  \f]
 *
 * where y the coordinate in lateral direction.
 * The velocity has a maximum value at y = 0:
  \f[
  u_{max} = \frac{g d \Theta W^2}{8 \nu_T L}
  \f]
 *
 * Therefore \f$ u_{max} \f$ can be calculated to be:
 *
  \f[
  u_{max} = \frac{9.81*0.02*100^2}{8*0.1*400} = 6.13125 m/s
  \f]
 *
  The formula for \f$ u(y) \f$ is also used to calculate the analytic solution.
 * It should be noted that u = f(x) and that v = 0 in the whole domain (in the final steady state).
 * Therefore the momentum advection/convection terms should be zero for this test, as:
 * \f$ u \partial u / \partial x = v \partial u / \partial y = u \partial v / \partial x = v \partial v / \partial y = 0 \f$
 *
 * This problem uses the \ref ShallowWaterModel
 */
template<class TypeTag>
class PoiseuilleFlowProblem
: public ShallowWaterProblem<TypeTag>
{
    using ParentType = ShallowWaterProblem<TypeTag>;
    using PrimaryVariables = GetPropType<TypeTag, Properties::PrimaryVariables>;
    using BoundaryTypes = Dumux::BoundaryTypes<GetPropType<TypeTag, Properties::ModelTraits>::numEq()>;
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using Indices = typename GetPropType<TypeTag, Properties::ModelTraits>::Indices;
    using GridGeometry = GetPropType<TypeTag, Properties::GridGeometry>;
    using NeumannFluxes = GetPropType<TypeTag, Properties::NumEqVector>;
    using ElementVolumeVariables = typename GetPropType<TypeTag, Properties::GridVolumeVariables>::LocalView;
    using GridVariables = GetPropType<TypeTag, Properties::GridVariables>;
    using ElementFluxVariablesCache = typename GridVariables::GridFluxVariablesCache::LocalView;
    using VolumeVariables = typename ElementVolumeVariables::VolumeVariables;
    using FVElementGeometry = typename GetPropType<TypeTag, Properties::GridGeometry>::LocalView;
    using SubControlVolumeFace = typename FVElementGeometry::SubControlVolumeFace;
    using GridView = typename GetPropType<TypeTag, Properties::GridGeometry>::GridView;
    using Element = typename GridView::template Codim<0>::Entity;
    using GlobalPosition = typename Element::Geometry::GlobalCoordinate;
    using NumEqVector = GetPropType<TypeTag, Properties::NumEqVector>;
    using SubControlVolume = typename FVElementGeometry::SubControlVolume;

public:
    PoiseuilleFlowProblem(std::shared_ptr<const GridGeometry> gridGeometry)
    : ParentType(gridGeometry)
    {
        name_ = getParam<std::string>("Problem.Name");
        exactWaterDepth_.resize(gridGeometry->numDofs(), 0.0);
        exactVelocityX_.resize(gridGeometry->numDofs(), 0.0);
        exactVelocityY_.resize(gridGeometry->numDofs(), 0.0);
        bedSlope_ = getParam<Scalar>("Problem.BedSlope");
        discharge_ = getParam<Scalar>("Problem.Discharge");
        hBoundary_ = getParam<Scalar>("Problem.HBoundary");
        alphaWall_ = getParam<Scalar>("Problem.AlphaWall");
        turbViscosity_ = getParam<Scalar>("ShallowWater.TurbulentViscosity");
        ksWall_ = getParam<Scalar>("Problem.KsWall");
        wallFrictionLawType_ = getParam<std::string>("Problem.WallFrictionLaw");
        // Make the wallFrictionLawType_ lower case
        std::transform(wallFrictionLawType_.begin(), wallFrictionLawType_.end(), wallFrictionLawType_.begin(), [](unsigned char c){ return std::tolower(c); });
    }

    //! Get the analytical water depth
    const std::vector<Scalar>& getExactWaterDepth() const
    { return exactWaterDepth_; }

    //! Get the analytical U-velocity
    const std::vector<Scalar>& getExactVelocityX() const
    { return exactVelocityX_; }

    //! Get the analytical V-velocity
    const std::vector<Scalar>& getExactVelocityY() const
    { return exactVelocityY_; }

    //! Update the analytical solution
    void updateAnalyticalSolution()
    {
        for (const auto& element : elements(this->gridGeometry().gridView()))
        {
            const auto eIdx = this->gridGeometry().elementMapper().index(element);
            const auto& globalPos = element.geometry().center();
            const auto gravity = this->spatialParams().gravity(globalPos);
            const Scalar y = globalPos[1];
            const Scalar width = this->gridGeometry().bBoxMax()[1] - this->gridGeometry().bBoxMin()[1];
            const Scalar h = hBoundary_;
            const Scalar u = -(gravity*bedSlope_/(8.0*turbViscosity_)) * (4.0*y*y - width*width);
            exactWaterDepth_[eIdx] = h;
            exactVelocityX_[eIdx]  = u;
            exactVelocityY_[eIdx]  = 0.0;
        }
    }

    const std::string& name() const
    { return name_; }

    /*!
     * \name Boundary conditions
     */
    // \{

    /*!
     * \brief Specifies which kind of boundary condition should be
     *        used for which equation on a given boundary segment.
     *
     * \param globalPos The position for which the boundary type is set
     */
    BoundaryTypes boundaryTypesAtPos(const GlobalPosition &globalPos) const
    {
        BoundaryTypes bcTypes;
        bcTypes.setAllNeumann();
        return bcTypes;
    }

    /*!
     * \brief Specifies the neumann boundary
     *
     *  We need the Riemann invariants to compute the values depending of the boundary type.
     *  Since we use a weak imposition we do not have a dirichlet value. We impose fluxes
     *  based on q, h, etc. computed with the Riemann invariants
     */
    NeumannFluxes neumann(const Element& element,
                          const FVElementGeometry& fvGeometry,
                          const ElementVolumeVariables& elemVolVars,
                          const ElementFluxVariablesCache& elemFluxVarsCache,
                          const SubControlVolumeFace& scvf) const
    {
        NeumannFluxes values(0.0);

        const auto& insideScv = fvGeometry.scv(scvf.insideScvIdx());
        const auto& insideVolVars = elemVolVars[insideScv];
        const auto& unitNormal = scvf.unitOuterNormal();
        const auto gravity = this->spatialParams().gravity(scvf.center());
        std::array<Scalar, 3> boundaryStateVariables;

        // impose discharge at the left side
        if (scvf.center()[0] < this->gridGeometry().bBoxMin()[0] + eps_)
        {
            // Prescribe the exact q-distribution long the inflow boundaryStateVariables
            // based on the parabolic u-profile:
            // q(y) = (g*H*ib/(8*nu_T)) * (4*y^2^-W^2)
            // Note the opposite sign to the velocity u, due to the fact that it is an inflow discharge
            const auto y     = scvf.center()[1];
            const auto width = this->gridGeometry().bBoxMax()[1] - this->gridGeometry().bBoxMin()[1];
            const auto h     = hBoundary_;
            // Now compute a weighted average between the constant q (from input) and the parabolic q from the analytical solution
            // based on the prescribed alphaWall
            const auto q_in0 = (gravity*h*bedSlope_/(8.0*turbViscosity_)) * (4.0*y*y - width*width);
            const auto q_in1 = discharge_;
            const auto q_in  = (1.0-alphaWall_)*q_in1 + alphaWall_*q_in0;
            boundaryStateVariables = ShallowWater::fixedDischargeBoundary(q_in,
                                                                          insideVolVars.waterDepth(),
                                                                          insideVolVars.velocity(0),
                                                                          insideVolVars.velocity(1),
                                                                          gravity,
                                                                          unitNormal);
        }
        // impose water depth at the right side
        else if (scvf.center()[0] > this->gridGeometry().bBoxMax()[0] - eps_)
        {
            boundaryStateVariables =  ShallowWater::fixedWaterDepthBoundary(hBoundary_,
                                                                            insideVolVars.waterDepth(),
                                                                            insideVolVars.velocity(0),
                                                                            insideVolVars.velocity(1),
                                                                            gravity,
                                                                            unitNormal);
        }
        // no flow boundary
        else
        {
            // For the rough side walls of type no-slip we prescribe a slip condition based on alphaWall
            // for smooth closed walls we prescribed a full-slip condition (zero-roughness)

            // Get inside velocity components in cell face coordinates (t,n) using normal vector unitNormal
            // Note that the first component is the normal component
            // since we are rotating to the normal vector coordinate system
            const Scalar insideVelocityNWall =  insideVolVars.velocity(0)*unitNormal[0] + insideVolVars.velocity(1)*unitNormal[1];
            const Scalar insideVelocityTWall = -insideVolVars.velocity(0)*unitNormal[1] + insideVolVars.velocity(1)*unitNormal[0];

            // Initialisation of outside velocities
            auto outsideVelocityNWall = insideVelocityNWall;
            auto outsideVelocityTWall = insideVelocityTWall;

            // Now set the outside (ghost cell) velocities based on the chosen slip condition
            if ((scvf.center()[1] < this->gridGeometry().bBoxMin()[1] + eps_ || scvf.center()[1] > this->gridGeometry().bBoxMax()[1] - eps_) && (wallFrictionLawType_ == "noslip" || wallFrictionLawType_ == "nikuradse"))
            {
                // Set the outside state using the no-slip wall roughness conditions based on alphaWall
                // alphaWall = 0.0: full slip (wall tangential velocity equals inside tangential velocity)
                // alphaWall = 1.0: no slip (wall tangential velocity=0.0: point mirroring of the velocity)
                // 0.0 < alphaWall < 1.0: 'partial' slip.
                // e.g. for alphaWall = 0.5 the wall tangential velocity is half the inside tangential velocity.
                outsideVelocityNWall = -insideVelocityNWall;
                outsideVelocityTWall =  (1.0 - 2.0*alphaWall_)*insideVelocityTWall;
            }
            else
            {
                // Set the outside state using the full-slip wall roughness conditions (line mirroring in the boundary face)
                // Only mirror the normal component
                outsideVelocityNWall = -insideVelocityNWall;
                outsideVelocityTWall =  insideVelocityTWall;
            }
            // Rotate back to cartesian coordinate system
            const Scalar outsideVelocityXWall = outsideVelocityNWall*unitNormal[0] - outsideVelocityTWall*unitNormal[1];
            const Scalar outsideVelocityYWall = outsideVelocityNWall*unitNormal[1] + outsideVelocityTWall*unitNormal[0];

            boundaryStateVariables[0] = insideVolVars.waterDepth();
            boundaryStateVariables[1] = outsideVelocityXWall;
            boundaryStateVariables[2] = outsideVelocityYWall;

        }

        auto riemannFlux = ShallowWater::riemannProblem(insideVolVars.waterDepth(),
                                                        boundaryStateVariables[0],
                                                        insideVolVars.velocity(0),
                                                        boundaryStateVariables[1],
                                                        insideVolVars.velocity(1),
                                                        boundaryStateVariables[2],
                                                        insideVolVars.bedSurface(),
                                                        insideVolVars.bedSurface(),
                                                        gravity,
                                                        unitNormal);

        values[Indices::massBalanceIdx] = riemannFlux[0];
        values[Indices::velocityXIdx] = riemannFlux[1];
        values[Indices::velocityYIdx] = riemannFlux[2];

        // Addition of viscosity/diffusive flux rough wall boundaries
        // No-slip wall (with coefficient alphaWall):
        // Compute wall shear stress using turbulent viscosity and local velocity gradient
        // Assume velocity gradient (in cell adjacent to wall) equal to alphaWall*(0 - u_c)
        std::array<Scalar, 3> roughWallFlux{};
        if (scvf.center()[1] < this->gridGeometry().bBoxMin()[1] + eps_ || scvf.center()[1] > this->gridGeometry().bBoxMax()[1] - eps_)
        {
            // Distance vector between the inside cell center and the boundary face center
            const auto& cellCenterToBoundaryFaceCenter = scvf.center() - insideScv.center();

            // The left (inside) state vector
            const auto& leftState  = insideVolVars.priVars();

            if (wallFrictionLawType_ == "noslip")
            {
                roughWallFlux = ShallowWater::noslipWallBoundary(alphaWall_,
                                                                 turbViscosity_,
                                                                 leftState,
                                                                 cellCenterToBoundaryFaceCenter,
                                                                 unitNormal);
            }
            else if (wallFrictionLawType_ == "nikuradse")
            {
                roughWallFlux = ShallowWater::nikuradseWallBoundary(ksWall_,
                                                                    leftState,
                                                                    cellCenterToBoundaryFaceCenter,
                                                                    unitNormal);
            }
        }

        values[Indices::massBalanceIdx] += roughWallFlux[0];
        values[Indices::velocityXIdx] += roughWallFlux[1];
        values[Indices::velocityYIdx] += roughWallFlux[2];

        return values;
    }

    // \}

    /*!
     * \brief Evaluate the initial values for a control volume.
     * \param globalPos The position for which the boundary type is set
     */
    PrimaryVariables initialAtPos(const GlobalPosition &globalPos) const
    {
        PrimaryVariables values(0.0);

        // Set the initial values to the analytical solution
        const auto gravity = this->spatialParams().gravity(globalPos);
        const auto width = this->gridGeometry().bBoxMax()[1] - this->gridGeometry().bBoxMin()[1];

        values[0] = hBoundary_;
        values[1] = -(gravity*bedSlope_/(8.0*turbViscosity_)) * (4.0*globalPos[1]*globalPos[1] - width*width);
        values[2] = 0.0;

        return values;
    };

private:

    std::vector<Scalar> exactWaterDepth_;
    std::vector<Scalar> exactVelocityX_;
    std::vector<Scalar> exactVelocityY_;

    Scalar hBoundary_; // water level at the outflow boundary
    Scalar bedSlope_; // bed slope (positive downwards)
    Scalar discharge_; // discharge at the inflow boundary
    Scalar alphaWall_; // wall roughness coefficient for no-slip type wall roughness
    Scalar ksWall_; // Nikuradse wall roughness height for Nikuradse type wall roughness
    Scalar turbViscosity_; // turbulent viscosity
    std::string wallFrictionLawType_; // wall friction law type

    static constexpr Scalar eps_ = 1.0e-6;
    std::string name_;
};

} //end namespace Dumux

#endif
