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
Pipe the radius of which follows an exponential equation.
"""

import numpy as np

from openwind.design import DesignShape, eval_, diff_

def exponential(x, x1, x2, r1, r2):
    """Calculate images with exponential function between 2 points.

    ..math::
        \\begin{eqnarray}
        r(x) & = & r_1 \\left( \\frac{r_2}{r_1}\\right)^{\\alpha}  \\\\
        \\alpha & = & \\frac{x - x_1}{x_2 - x_1}
        \\end{eqnarray}

    with

    - \(x_1, r_1\) the coordinate of the first endpoint
    - \(x_2, r_2\) the coordinate of the second endpoint

    Parameters
    ----------
    x : float
        the point at which the value of y is calculated
    x1, r1 : float
        the first point
    x2, r2 : float
        the second point
    """
    # return r1 * np.exp((1 / (x2 - x1)) * np.log(r2 / r1) * (x - x1))
    power = (x - x1) / (x2 - x1)
    return r1 * (r2/r1)**power

def exponential_diff_x(x, x1, x2, r1, r2):
    power = (x - x1) / (x2 - x1)
    dpower_dx = 1 / (x2 - x1)
    return r1 * np.log(r2/r1) * dpower_dx * (r2/r1)**power

def exponential_diff_r1(x, x1, x2, r1, r2):
    power = (x - x1) / (x2 - x1)
    return (1 - power) * (r2/r1)**power

def exponential_diff_r2(x, x1, x2, r1, r2):
    power = (x - x1) / (x2 - x1)
    return power * (r2/r1)**(power - 1)

def exponential_diff_x1(x, x1, x2, r1, r2):
    power = (x - x1) / (x2 - x1)
    dpower_dx1 = (x - x2) / (x2 - x1)**2
    return r1 * np.log(r2/r1) * dpower_dx1 * (r2/r1)**power

def exponential_diff_x2(x, x1, x2, r1, r2):
    power = (x - x1) / (x2 - x1)
    dpower_dx2 =  - (x - x1) / (x2 - x1)**2
    return r1 * np.log(r2/r1) * dpower_dx2 * (r2/r1)**power

class Exponential(DesignShape):
    """
    Pipe the radius of which follows an exponential equation.

    The shape is defined only from the coordinate of the two endpoints, by
    following this equation:

    ..math::
        \\begin{eqnarray}
        r(x) & = & r_1 \\left( \\frac{r_2}{r_1} \\right)^{\\alpha} \\\\
        \\alpha & = & \\frac{x - x_1}{x_2 - x_1}
        \\end{eqnarray}

    with

    - \(x_1, r_1\) the coordinate of the first endpoint
    - \(x_2, r_2\) the coordinate of the second endpoint

    Parameters
    ----------
    *params: 4 openwind.design.design_parameter.DesignParameter
        The five parameters in this order: \(x_1, x_2, r_1, r_2\)
    """


    def __init__(self, *params):
        if len(params) != 4:
            raise ValueError("A conical furstum need 4 parameters.")
        self.params = params

    def __repr__(self):
        return 'Exponential, length {0:.2f} cm'.format(100*self.get_length())

    def __str__(self):
        geom = ''
        for param in self.params:
            geom += '{} '.format(param)
        return '{geom}{class_}'.format(geom=geom, class_=type(self).__name__)

    def get_position_from_xnorm(self, x_norm):
        Xmin = self.params[0].get_value()
        Xmax = self.params[1].get_value()
        return x_norm*(Xmax - Xmin) + Xmin

    def get_radius_at(self, x_norm):
        x1, x2, r1, r2 = eval_(self.params)
        x = self.get_position_from_xnorm(x_norm)
        radius = exponential(x, x1, x2, r1, r2)
        self.check_bounds(x, [x1, x2])
        return radius

    def get_diff_radius_at(self, x_norm, diff_index):
        x1, x2, r1, r2 = eval_(self.params)
        dx1, dx2, dr1, dr2 = diff_(self.params, diff_index)
        dx_norm = self.get_diff_position_from_xnorm(x_norm, diff_index)
        x = self.get_position_from_xnorm(x_norm)
        diff_radius = exponential_diff_x(x, x1, x2, r1, r2)*dx_norm
        if dx1 != 0:
            diff_radius += dx1 * exponential_diff_x1(x, x1, x2, r1, r2)
        if dx2 != 0:
            diff_radius += dx2 * exponential_diff_x2(x, x1, x2, r1, r2)
        if dr1 != 0:
            diff_radius += dr1 * exponential_diff_r1(x, x1, x2, r1, r2)
        if dr2 != 0:
            diff_radius += dr2 * exponential_diff_r2(x, x1, x2, r1, r2)
        self.check_bounds(x, [x1, x2])
        return diff_radius

    def get_diff_shape_wr_x_norm(self, x_norm):
        x1, x2, r1, r2 = eval_(self.params)
        x = self.get_position_from_xnorm(x_norm)
        dx_dxnorm = (x2 - x1)
        return dx_dxnorm * exponential_diff_x(x, x1, x2, r1, r2)

    def get_endpoints_position(self):
        return self.params[0], self.params[1]

    def get_endpoints_radius(self):
        return self.params[2], self.params[3]
