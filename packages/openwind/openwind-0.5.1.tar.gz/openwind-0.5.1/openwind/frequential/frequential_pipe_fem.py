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
from scipy.sparse import csr_matrix, bmat, hstack

from openwind.continuous import EndPos
from openwind.frequential import FrequentialComponent
from openwind.discretization import DiscretizedPipe
import pdb


class FrequentialPipeFEM(FrequentialComponent, DiscretizedPipe):
    """Compute for every frequency every data for the linear system to solve
    (Ah.Uh=Lh)

    Parameters
    ----------
    fs : numpy.array
        array of frequency
    d_pipe : DiscretizedPipe


    Attributes
    ----------
    Ah : (WARNING) contains only the non-diagonal elements of Ah
    Ah_diags : contains every element of Ah diagonal for every frequency
    Lh : contains the right-hand side of the linear system
    """

    class End:
        """Access to one end of a FrequentialPipeFEM.

        Parameters
        ----------
        f_pipe : the FrequentialPipeFEM to which this End corresponds
        pos : {EndPos.MINUS, EndPos.PLUS}
            Position in the pipe's indices.
            MINUS if start of the pipe, PLUS if end.

        """

        def __init__(self, f_pipe, pos):
            self.f_pipe = f_pipe
            assert isinstance(pos, EndPos)
            self.pos = pos
            self.convention = f_pipe.convention

        def get_index(self):
            """Index of the H1 variable at this pipe-end, in the assembled vector
            of all unknowns Uh."""
            indices = self.f_pipe.get_H1_indices()
            return indices[self.pos.array_pos]

        def get_index_L2(self):
            """Index of the L2 variable at this pipe-end, in the assembled vector
            of all unknowns Uh."""
            indices = self.f_pipe.get_L2_indices()
            return indices[self.pos.array_pos]

        def get_physical_params(self):
            """Get radius, rho, c at this pipe-end."""
            radius = self.f_pipe.pipe.get_radius_at(self.pos.x)
            rho = self.f_pipe.pipe.get_physics().rho(self.pos.x)
            c = self.f_pipe.pipe.get_physics().c(self.pos.x)
            return radius, rho, c

        def get_diff_radius(self, diff_index):
            return self.f_pipe.pipe.get_diff_radius_at(self.pos.x, diff_index)


    def __init__(self, pipe, **kwargs):
        DiscretizedPipe.__init__(self, pipe, **kwargs)
        self.label = pipe.label
        self.end_minus = self.End(self, EndPos.MINUS)
        self.end_plus = self.End(self, EndPos.PLUS)

    def _compute_indep_freq(self):
        Bh = self.get_Bh()
        # everything outside the diagonal
        local_Ah = bmat([[None, -Bh], [Bh.T, None]], dtype='complex128')
        return local_Ah

    def _compute_diags(self, omegas_scaled):
        """ Compute all the diagonals of the matrix Ah.
        All the diagonals are keep in a dense matrix used to actualize
        the diagonal of the sparse matrix at each iteration of the
        frequency loop (best methodology).

        .. warning ::
            Different for frequential_pipe_diffusive_representation
        """
        local_Ah_diags = self.get_mass_matrices_with_losses(omegas_scaled)
        return local_Ah_diags

    def get_ends(self):
        return self.end_minus, self.end_plus

    def get_number_dof(self):
        return self.nL2 + self.nH1

    def get_first_L2_index(self):
        return self.get_first_index()

    def get_first_H1_index(self):
        return self.get_first_index() + self.nL2

    def get_L2_indices(self):
        """
        Return the indices of the L2 variable.

        * Usage *

        ``V = Uh[f_pipe.get_L2_indices()]         # if convention is 'PH1'``
        """
        i0 = self.get_first_L2_index()
        return range(i0, i0 + self.nL2)

    def get_H1_indices(self):
        """
        Return the indices of the H1 variable.

        * Usage *

        ``P = Uh[f_pipe.get_H1_indices()]         # if convention is 'PH1'``
        """
        i0 = self.get_first_H1_index()
        return range(i0, i0 + self.nH1)

    def get_contrib_indep_freq(self):
        local_Ah = self._compute_indep_freq()
        return self.place_in_big_matrix(local_Ah)

    def get_contrib_freq(self, omegas_scaled):
        """ Compute all the diagonals of the matrix Ah.
        All the diagonals are keep in a dense matrix used to actualize
        the diagonal of the sparse matrix at each iteration of the
        frequency loop (best methodology). """
        local_Ah_diags = self._compute_diags(omegas_scaled)
        Ah_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                            dtype='complex128')
        Ah_diags[self.get_indices(), :] = local_Ah_diags

        return Ah_diags

    def place_interp_matrix(self, x_interp_local, variable='L2'):
        n_interp = len(x_interp_local)
        n_left = self.get_first_index()
        mat_left = csr_matrix((n_interp, n_left))
        n_right = self.ntot_dof - self.get_indices().stop
        mat_right = csr_matrix((n_interp, n_right))
        mat_H1 = csr_matrix((n_interp, self.nH1))
        mat_L2 = csr_matrix((n_interp, self.nL2))
        if variable=='L2':
            local_mat = self.get_interp_mat_L2(x_interp_local)
            interp_mat = hstack([mat_left, local_mat, mat_H1, mat_right])
        else:
            local_mat = self.get_interp_mat_H1(x_interp_local)
            interp_mat = hstack([mat_left, mat_L2, local_mat, mat_right])
        return  interp_mat

    def place_interp_matrix_grad(self, x_interp_local, variable='L2'):
        n_interp = len(x_interp_local)
        n_left = self.get_first_index()
        mat_left = csr_matrix((n_interp, n_left))
        n_right = self.ntot_dof - self.get_indices().stop
        mat_right = csr_matrix((n_interp, n_right))
        mat_H1 = csr_matrix((n_interp, self.nH1))
        mat_L2 = csr_matrix((n_interp, self.nL2))
        if variable=='L2':
            local_mat = self.get_interp_mat_L2_grad(x_interp_local)
            interp_mat = hstack([mat_left, local_mat, mat_H1, mat_right])
        else:
            local_mat = self.get_interp_mat_H1_grad(x_interp_local)
            interp_mat = hstack([mat_left, mat_L2, local_mat, mat_right])
        return  interp_mat
# %% differential
    def _compute_diags_dAh(self, omegas_scaled, diff_index):
        """ Compute all the diagonals of the matrix Ah.
        All the diagonals are keep in a dense matrix used to actualize
        the diagonal of the sparse matrix at each iteration of the
        frequency loop (best methodology). """
        local_dAh_diags = self.get_mass_matrices_with_losses_dAh(omegas_scaled,
                                                                 diff_index)
        return local_dAh_diags

    def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
        """ Compute all the diagonals of the matrix Ah.
        All the diagonals are keep in a dense matrix used to actualize
        the diagonal of the sparse matrix at each iteration of the
        frequency loop (best methodology). """
        local_dAh_diags = self._compute_diags_dAh(omegas_scaled, diff_index)
        dAh_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                            dtype='complex128')
        dAh_diags[self.get_indices(), :] = local_dAh_diags
        return dAh_diags
