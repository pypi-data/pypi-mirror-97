#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2019-2021, INRIA
#
# This file is part of Openwind.
#
# Openwind is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Openwind is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openwind.  If not, see <https://www.gnu.org/licenses/>.
#
# For more informations about authors, see the CONTRIBUTORS file

"""
Pipe defined as a portion of another pipe.
"""

from openwind.design import DesignShape, eval_, diff_

class ShapeSlice(DesignShape):
    """
    Pipe defined as a portion of another pipe.

    Parameters
    ----------
    mother_shape : openwind.design.design_shape.DesignShape
        The shape from which is defined this slice.
    X_range : list of two openwind.design.design_parameter.DesignParameter
        The two endpoints of the slice. They must be within the two
        endpoints of the mother shape.
    """

    def __init__(self, mother_shape, X_range):
        self.X_range = X_range
        self.mother_shape = mother_shape
        self._check_slice()

    def _check_slice(self):
        bounds_mother = eval_(list(self.mother_shape.get_endpoints_position()))
        bounds_slice = eval_(self.X_range)
        if bounds_slice[0]<bounds_mother[0] or bounds_slice[1]>bounds_mother[1]:
            raise ValueError("The slice bounds {} are outside the mother"
                             "bounds {}".format(bounds_slice,
                                                list(bounds_mother)))

    def is_TMM_compatible(self):
        return self.mother_shape.is_TMM_compatible()

    def get_position_from_xnorm(self, x_norm):
        Xmin, Xmax = eval_(self.X_range)
        return x_norm*(Xmax - Xmin) + Xmin

    def get_diff_position_from_xnorm(self, x_norm, diff_index):
        dXmin, dXmax = diff_(self.X_range, diff_index)
        return dXmin*(1-x_norm) + dXmax*x_norm

    def __xnorm_mother_from_xnorm(self, x_norm):
        x = self.get_position_from_xnorm(x_norm)
        X_mother = self.mother_shape.get_endpoints_position()
        Xmin_mother, Xmax_mother = eval_(list(X_mother))
        return (x - Xmin_mother) / (Xmax_mother - Xmin_mother)

    def __diff_xmother(self, x_norm, diff_index):
        x = self.get_position_from_xnorm(x_norm)

        X_mother = self.mother_shape.get_endpoints_position()
        Xmin_mother, Xmax_mother = eval_(list(X_mother))
        dXmin_mother, dXmax_mother = diff_(list(X_mother), diff_index)
        diff_xmother = ((dXmin_mother*(x - Xmax_mother)
                         - dXmax_mother*(x - Xmin_mother))
                        / (Xmax_mother - Xmin_mother)**2)

        diff_x = self.get_diff_position_from_xnorm(x_norm, diff_index)
        dx_norm_mother = diff_x / (Xmax_mother - Xmin_mother)
        return diff_xmother + dx_norm_mother

    def get_radius_at(self, x_norm):
        x_norm_mother = self.__xnorm_mother_from_xnorm(x_norm)
        return self.mother_shape.get_radius_at(x_norm_mother)

    def get_diff_radius_at(self, x_norm, diff_index):
        x_mother = self.__xnorm_mother_from_xnorm(x_norm)
        diff_xmother = self.__diff_xmother(x_norm, diff_index)
        diff = (self.mother_shape.get_diff_radius_at(x_mother, diff_index)
                + self.mother_shape.get_diff_shape_wr_x_norm(x_mother)
                * diff_xmother)
        return diff

    def get_diff_shape_wr_x_norm(self, x_norm):
        Xmin, Xmax = eval_(self.X_range)
        dx_dxnorm = (Xmax - Xmin)

        X_mother = self.mother_shape.get_endpoints_position()
        Xmin_mother, Xmax_mother = eval_(list(X_mother))
        dx_norm_mother_dx = 1 / (Xmax_mother - Xmin_mother)

        x_mother = self.__xnorm_mother_from_xnorm(x_norm)
        dshape_dx_norm_mother = self.mother_shape.get_diff_shape_wr_x_norm(x_mother)
        return dshape_dx_norm_mother * dx_norm_mother_dx * dx_dxnorm


    def get_endpoints_position(self):
        return self.X_range[0], self.X_range[1]

    def get_endpoints_radius(self):
        return 'The endpoints radii of a shape slice are not DesignParameters'
