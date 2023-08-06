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

import numpy as np
from scipy.sparse import csr_matrix
from openwind.frequential import FrequentialComponent


class FrequentialSource(FrequentialComponent):
    """Compute the source terme Lh for the linear system to solve (Ah.Uh=Lh)

    Parameters
    ----------
    source : Excitator. Must be Flow.
    (end,) : frequential pipe end associated to this source condition
    """

    def __init__(self, source, ends):
        self.end, = ends  # Unpack one
        self.source = source

    def get_scaling(self):
        return self.source.scaling

    def get_convention(self):
        return self.end.convention

    def get_number_dof(self):
        return 0

    def get_contrib_source(self):
        index_source = self.get_source_index()
        return csr_matrix(([1], ([index_source], [0])),
                          shape=(self.ntot_dof, 1))

    def get_source_index(self):
        """Get index where this source brings a nonzero term.
        """
        return self.end.get_index()

    def get_Zc0(self):
        radius, rho, c = self.end.get_physical_params()
        return rho*c/(np.pi*radius**2)
