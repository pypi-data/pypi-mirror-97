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

from openwind.continuous import (ThermoviscousBessel,
                                 ThermoviscousLossless,
                                 Keefe,
                                 MiniKeefe,
                                 EndPos)
from openwind.frequential import (FrequentialComponent,
                                  FrequentialPipeFEM)
from .tmm_tools import cone_lossy, cone_lossless
import openwind.design

class FrequentialPipeTMM(FrequentialComponent):
    """Frequential pipe whose transfer matrix is given.

    A dirty trick is used to place the frequency-dependent
    coefficients A, B, C, D on the diagonal: \
        we add four additional variables, such that the Schur \
        complement of the new matrix restores the correct system \
        of equations.\
    """

    class End(FrequentialPipeFEM.End):
        """Access to one end of a FrequentialPipeTMM.

        Parameters
        ----------
        f_pipe : the FrequentialPipe to which this End corresponds
        pos : {EndPos.MINUS, EndPos.PLUS}
            Position in the pipe's indices.
            MINUS if start of the pipe, PLUS if end.
        """
        def __init__(self, f_pipe, pos):
            self.f_pipe = f_pipe
            assert isinstance(pos, EndPos)
            self.pos = pos
            self.convention = 'PH1'

        def get_index(self):
            if self.pos == EndPos.MINUS:
                return self.f_pipe.get_first_index() + 4
            elif self.pos == EndPos.PLUS:
                return self.f_pipe.get_first_index() + 6
            assert False

    def __init__(self, pipe, nb_sub=1, **kwargs):
        self.pipe = pipe

        # Supports only conical shapes with constant temperature
        # if not isinstance(pipe.get_shape(), openwind.design.Cone):
        if not pipe.get_shape().is_TMM_compatible():
            raise ValueError('TMM can only be used with Cones and not'
                             ' {}'.format(pipe.get_shape()))
        if not self.pipe.get_physics().uniform:
            raise ValueError('TMM can only be used with uniform temperature.')

        self.end_minus = FrequentialPipeTMM.End(self, EndPos.MINUS)
        self.end_plus = FrequentialPipeTMM.End(self, EndPos.PLUS)
        self._nb_sub = nb_sub

    def get_number_dof(self):
        return 8

    def get_ends(self):
        return self.end_minus, self.end_plus

    def _compute_tmm_coefs(self, omegas_scaled):
        physics = self.pipe.get_physics()
        omegas = omegas_scaled / self.pipe.get_scaling().get_time()
        lpart = self.pipe.get_length()
        R0 = self.pipe.get_radius_at(0)
        R1 = self.pipe.get_radius_at(1)
        nb_sub = self._nb_sub
        sph = self.pipe.is_spherical_waves()
        losses = self.pipe.get_losses()
        if isinstance(losses, ThermoviscousBessel):  # with bessel losses
            A, B, C, D = cone_lossy(physics, lpart, R0, R1,
                                        omegas, nb_sub, sph)
        elif isinstance(losses, Keefe): # Keefe losses
            A, B, C, D = cone_lossy(physics, lpart, R0, R1,
                                          omegas, nb_sub, sph, 'keefe')
        elif isinstance(losses, MiniKeefe): # Keefe losses
            A, B, C, D = cone_lossy(physics, lpart, R0, R1,
                                          omegas, nb_sub, sph, 'minikeefe')
        elif isinstance(losses, ThermoviscousLossless):  # lossless
            A, B, C, D = cone_lossless(physics, lpart, R0, R1,
                                           omegas, sph)
        else:
            raise ValueError("FPipeTMM only supports losses"
                             " {False, 'bessel, 'keefe', 'minikeefe'}, not " + str(type(losses)))

        # Nondimensionalization of the TMM matrix
        B /= self.pipe.get_scaling().get_impedance()
        C *= self.pipe.get_scaling().get_impedance()
        assert np.allclose(A*D - B*C, 1.0)  # determinant should be 1
        return A, B, C, D

    def _compute_diags(self, omegas_scaled):
        A, B, C, D = self._compute_tmm_coefs(omegas_scaled)

        assert all(coef.shape == (len(omegas_scaled),) for coef in [A, B, C, D])
        local_Ah_diags = np.zeros((8, len(omegas_scaled)), dtype='complex128')
        for i, coef in enumerate([A, B, C, D]):
            local_Ah_diags[i, :] = 1/coef
        return local_Ah_diags

    def get_contrib_freq(self, omegas_scaled):
        local_Ah_diags = self._compute_diags(omegas_scaled)
        Ah_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
                            dtype='complex128')
        Ah_diags[self.get_indices(), :] = local_Ah_diags
        return Ah_diags

    def get_contrib_indep_freq(self):
        """Contribution of this component to the frequency-independent
        terms of Ah."""
        local_Ah = csr_matrix([[0, 0, 0, 0,   0, 0, 1, 0],
                               [0, 0, 0, 0,   0, 0, 0, 1],
                               [0, 0, 0, 0,   0, 0, 1, 0],
                               [0, 0, 0, 0,   0, 0, 0, 1],

                               [0, 0, 0, 0,   0, 1, 0, 0],
                               [1, 1, 0, 0,   1, 0, 0, 0],
                               [0, 0, 0, 0,   0, 0, 0, -1],
                               [0, 0, 1, 1,   0, 1, 0, 0]])
        return self.place_in_big_matrix(local_Ah)

    def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
        # TODO if we want to do optimization with TMM
        raise NotImplementedError

    def get_contrib_dAh_indep_freq(self, diff_index):
        # TODO if we want to do optimization with TMM
        raise NotImplementedError
