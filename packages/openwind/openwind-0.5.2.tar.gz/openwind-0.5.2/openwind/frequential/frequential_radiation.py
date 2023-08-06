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
from openwind.frequential import FrequentialComponent
from openwind.continuous import RadiationModel


class FrequentialRadiation(FrequentialComponent):
    """Compute for every frequency the radiation data for the linear system to
    solve (Ah.Uh=Lh)

    Parameters
    ----------
    (freq_end,) : frequential pipe end associated to this radiation condition
    rad : PhysicalRadiation
    """

    def __init__(self, rad, freq_ends, opening_factor=1.0):
        self.freq_end, = freq_ends  # Unpack one
        self.rad = rad
        self._opening_factor = opening_factor

    def set_opening_factor(self, opening_factor):
        self._opening_factor = opening_factor

    def __get_physical_params(self):
        return self.freq_end.get_physical_params()

    def get_number_dof(self):
        return 0

    def get_contrib_freq(self, omegas_scaled):
        self.__compute_diags(omegas_scaled)
        Ah_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                            dtype='complex128')
        Ah_diags[self.freq_end.get_index(), :] = self.Ah_diags
        return Ah_diags

    def __compute_diags(self, omegas_scaled):
        radius, rho, c = self.__get_physical_params()
        coef_rad = self.rad.get_radiation_at(omegas_scaled,
                                             radius, rho, c,
                                             self._opening_factor)
        self.Ah_diags = coef_rad

# ----- differential -----
    def _compute_diags_dAh(self, omegas_scaled, diff_index):
        radius, rho, c = self.__get_physical_params()
        dr = self.freq_end.get_diff_radius(diff_index)
        local_dAh_diags = self.rad.get_diff_radiation_at(dr, omegas_scaled,
                                                         radius, rho, c,
                                                         self._opening_factor)
        return local_dAh_diags

    def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
        local_dAh_diags = self._compute_diags_dAh(omegas_scaled, diff_index)
        dAh_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                             dtype='complex128')
        dAh_diags[self.freq_end.get_index(), :] = local_dAh_diags
        return dAh_diags
