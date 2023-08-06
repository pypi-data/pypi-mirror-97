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
import scipy.sparse as ssp

from openwind.frequential import FrequentialComponent


class FrequentialJunctionTjoint(FrequentialComponent):
    """Frequential representation of a T-junction of pipes.

    Assumes similar main tube radius at both side of the branched tube.
    Assumes convention PH1.

    Parameters
    ----------
    ends : list(FrequentialPipe.End)
        the pipe ends this junction connects
    junc : JunctionModel
    """

    def __init__(self, junc, ends):
        self.junc = junc
        assert len(ends) == 3
        self.ends = ends
        if any(end.convention != 'PH1' for end in ends):
            msg = ("FrequentialJunction does not support adimensioning,"
                   + "and needs PH1 convention")
            raise ValueError(msg)

    def __get_physical_params(self):
        radii = []
        rhos = []
        for end in self.ends:
            radius, rho_i, _ = end.get_physical_params()
            radii.append(radius)
            rhos.append(rho_i)
        assert all(np.isclose(rhos, rho_i))
        assert np.isclose(radii[0], radii[1])
        rho = sum(rhos)/3.0
        r_main = sum(radii[0:2])/2.0
        r_side = radii[2]
        return r_main, r_side, rho

    def __get_masses(self):
        r_main, r_side, rho = self.__get_physical_params()
        M, T = self.junc.compute_diagonal_masses(r_main, r_side, rho)
        return M, T

    def get_number_dof(self):
        return 2  # len(self.mass_junction)

    def get_contrib_freq(self, omegas_scaled):
        """ Contribution of this component to the frequency-dependent diagonal
        of Ah.

        Return a sparse matrix with a shape ((number of dof) x (size of freq.))
        """
        mass_junction, _ = self.__get_masses()
        my_contrib = 1j * omegas_scaled * mass_junction[:, np.newaxis]
        # Place on our indices
        Ah_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                            dtype='complex128')
        Ah_diags[self.get_indices(), :] = my_contrib
        return Ah_diags

    def get_contrib_indep_freq(self):
        _, interaction_matrix = self.__get_masses()
        assembled_interaction_matrix = ssp.lil_matrix((self.ntot_dof,
                                                       self.ntot_dof))
        for i in range(len(self.ends)):
            f_pipe_end = self.ends[i]
            interaction = interaction_matrix[:, i]
            for k, val in zip(self.get_indices(), np.ravel(interaction)):
                assembled_interaction_matrix[k, f_pipe_end.get_index()] = val
        return assembled_interaction_matrix - assembled_interaction_matrix.T

# ----- differential -----
    def get_diff_masses(self, diff_index):
        r_main, r_side, rho = self.__get_physical_params()

        d_radii = []
        for end in self.ends:
            d_radius = end.get_diff_radius(diff_index)
            d_radii.append(d_radius)
        assert np.isclose(d_radii[0], d_radii[1])
        d_r_main = sum(d_radii[0:2])/2.0
        d_r_side = d_radii[2]
        dM, dT = self.junc.diff_diagonal_masses(r_main, r_side, rho,
                                                d_r_main, d_r_side)
        return dM, dT

    def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
        dM, _ = self.get_diff_masses(diff_index)
        local_dAh_diags = 1j * omegas_scaled * dM[:, np.newaxis]
        # Place on our indices
        dAh_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                             dtype='complex128')
        dAh_diags[self.get_indices(), :] = local_dAh_diags
        return dAh_diags
