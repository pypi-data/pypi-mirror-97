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
One individual element of a finite elements Mesh.
"""

from openwind.discretization import GLQuad
import numpy as np


__quads = dict()
def _get_quad(order):
    """Memorized version of GLQuad, to not recompute each time.

    Maybe useless, or maybe move it to GLQuad itself ?
    """
    if order not in __quads:
        __quads[order] = GLQuad(order)
    return __quads[order]


class Element:

    def __init__(self, x0, x1, order):
        self._x_start = x0
        self._length = x1 - x0
        self.order = int(order)

    def get_length(self):
        return self._length

    def get_nodes(self):
        return self._x_start + _get_quad(self.order).pts*self._length

    def get_weights(self):
        return self._length * _get_quad(self.order).weight

    def get_Bh_coeff(self):
        return _get_quad(self.order).BK

    def get_lagrange(self, x):
        assert all(x >= 0) and all(x <= 1)
        if x.size > 0:
            lagrange = _get_quad(self.order).lagranPolys()
            return np.vstack([lag(x) for lag in lagrange]).T
        else:
            return np.zeros((0, self.order + 1))

    def get_diff_lagrange(self, x):
        assert all(x >= 0) and all(x <= 1)
        if x.size > 0:
            lagrange = _get_quad(self.order).lagran_polys_derivate()
            return np.vstack([lag(x)/self._length for lag in lagrange]).T
        else:
            return np.zeros((0, self.order + 1))
