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
 * \ingroup SpatialParameters
 * \brief The base class for spatial parameters of problems using the
 *        fv method.
 */
#ifndef DUMUX_SEQUENTIAL_FV_SPATIAL_PARAMS_ONE_P_HH
#define DUMUX_SEQUENTIAL_FV_SPATIAL_PARAMS_ONE_P_HH

#include <dumux/common/properties.hh>
#include <dumux/common/math.hh>

#include <dune/common/fmatrix.hh>

namespace Dumux {

/*!
 * \ingroup SpatialParameters
 * \brief The base class for spatial parameters of problems using the
 *        fv method.
 */
template<class TypeTag>
class SequentialFVSpatialParamsOneP
{
    using Problem = GetPropType<TypeTag, Properties::Problem>;
    using Scalar = GetPropType<TypeTag, Properties::Scalar>;
    using GridView = typename GetPropType<TypeTag, Properties::GridGeometry>::GridView;
    using Implementation = GetPropType<TypeTag, Properties::SpatialParams>;

    enum
    {
        dim = GridView::dimension,
        dimWorld = GridView::dimensionworld
    };

    using Element = typename GridView::template Codim<0>::Entity;
    using GlobalPosition = typename Element::Geometry::GlobalCoordinate;
    using DimWorldMatrix = Dune::FieldMatrix<Scalar, dimWorld, dimWorld>;

public:
    SequentialFVSpatialParamsOneP(const Problem& problem)
    {
    }
    /*!
     * \brief Averages the intrinsic permeability (Scalar).
     * \param K1 intrinsic permeability of the first element
     * \param K2 intrinsic permeability of the second element
     */
    Scalar meanK(Scalar K1, Scalar K2) const
    {
        const Scalar K = harmonicMean(K1, K2);
        return K;
    }

    /*!
     * \brief Averages the intrinsic permeability (Scalar).
     * \param result averaged intrinsic permeability
     * \param K1 intrinsic permeability of the first element
     * \param K2 intrinsic permeability of the second element
     */
    void meanK(DimWorldMatrix &result, Scalar K1, Scalar K2) const
    {
        const Scalar K = harmonicMean(K1, K2);
        for (int i = 0; i < dimWorld; ++i)
        {
            for (int j = 0; j < dimWorld; ++j)
                result[i][j] = 0;
            result[i][i] = K;
        }
    }

    /*!
     * \brief Averages the intrinsic permeability (Tensor).
     * \param result averaged intrinsic permeability
     * \param K1 intrinsic permeability of the first element
     * \param K2 intrinsic permeability of the second element
     */
    void meanK(DimWorldMatrix &result, const DimWorldMatrix &K1, const DimWorldMatrix &K2) const
    {
        // entry-wise harmonic mean at the main diagonal and arithmetic mean at the off-diagonal
        for (int i = 0; i < dimWorld; ++i)
        {
            result[i][i] = harmonicMean(K1[i][i], K2[i][i]);
            for (int j = 0; j < dimWorld; ++j)
            {
                if (i != j)
                {
                    result[i][j] = 0.5 * (K1[i][j] + K2[i][j]);
                }
            }
        }
    }

    /*!
     * \brief Dummy function that can be used if only one value exist (boundaries).
     * \param result intrinsic permeability
     * \param K intrinsic permeability of the element
     */
    void meanK(DimWorldMatrix &result, Scalar K) const
    {
        for (int i = 0; i < dimWorld; ++i)
        {
            for (int j = 0; j < dimWorld; ++j)
                result[i][j] = 0;
            result[i][i] = K;
        }
    }

    /*!
     * \brief Dummy function that can be used if only one value exist (boundaries).
     * \param result intrinsic permeability
     * \param K intrinsic permeability of the element
     */
    void meanK(DimWorldMatrix &result, const DimWorldMatrix &K) const
    {
        result = K;
    }

    /*!
     * \brief Function for defining the intrinsic (absolute) permeability.
     *
     * \return intrinsic (absolute) permeability
     * \param element The element
     */
    const DimWorldMatrix& intrinsicPermeability (const Element& element) const
    {
        return asImp_().intrinsicPermeabilityAtPos(element.geometry().center());
    }

    /*!
     * \brief Function for defining the intrinsic (absolute) permeability.
     *
     * \return intrinsic (absolute) permeability
     * \param globalPos The position of the center of the element
     */
    const DimWorldMatrix& intrinsicPermeabilityAtPos (const GlobalPosition& globalPos) const
    {
        DUNE_THROW(Dune::InvalidStateException,
                   "The spatial parameters do not provide "
                   "a intrinsicPermeabilityAtPos() method.");
    }

    /*!
     * \brief Function for defining the porosity.
     *
     * \return porosity
     * \param element The element
     */
    Scalar porosity(const Element& element) const
    {
        return asImp_().porosityAtPos(element.geometry().center());
    }

    /*!
     * \brief Function for defining the porosity.
     *
     * \return porosity
     * \param globalPos The position of the center of the element
     */
    Scalar porosityAtPos(const GlobalPosition& globalPos) const
    {
        DUNE_THROW(Dune::InvalidStateException,
                   "The spatial parameters do not provide "
                   "a porosityAtPos() method.");
    }

private:
    Implementation &asImp_()
    {
        return *static_cast<Implementation*> (this);
    }

    const Implementation &asImp_() const
    {
        return *static_cast<const Implementation*> (this);
    }
};

} // namespace Dumux

#endif
