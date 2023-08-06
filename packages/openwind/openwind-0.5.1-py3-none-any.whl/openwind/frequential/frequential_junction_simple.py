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


class FrequentialJunctionSimple(FrequentialComponent):
    """Frequential representation of a junction between two pipes.

    Assumes convention PH1.

    Parameters
    ----------
    ends : list(FrequentialPipe.End)
        the pipe ends this junction connects
    junc : JunctionModel
    """

    def __init__(self, junc, ends):
        self.junc = junc
        assert len(ends) == 2
        self.ends = ends
        self.__set_physical_params()
        if any(end.convention != 'PH1' for end in ends):
            msg = ("FrequentialJunction does not yet support VH1 convention")
            raise ValueError(msg)

    def __set_physical_params(self):
        radii = []
        rhos = []
        for end in self.ends:
            radius, rho, _ = end.get_physical_params()
            radii.append(radius)
            rhos.append(rho)
        assert all(np.isclose(rhos, rho))
        self.rho = sum(rhos)/2.0
        self.r_minus, self.r_plus = radii

    def get_number_dof(self):
        return 1

    def get_contrib_freq(self, omegas_scaled):
        """ Contribution of this component to the frequency-dependent diagonal
        of Ah.

        Return a sparse matrix with a shape ((number of dof) x (size of freq.))
        """
        return 0

    def get_contrib_indep_freq(self):
        assembled_interaction_matrix = ssp.lil_matrix((self.ntot_dof,
                                                       self.ntot_dof))
        interaction = [-1, 1]
        for i in range(len(self.ends)):
            f_pipe_end = self.ends[i]
            assembled_interaction_matrix[self.get_indices(),
                                         f_pipe_end.get_index()] = interaction[i]
        return assembled_interaction_matrix - assembled_interaction_matrix.T
