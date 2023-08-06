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
from openwind.continuous import (ThermoviscousBessel,
                                 ThermoviscousLossless,
                                 Keefe,
                                 MiniKeefe)
from openwind.frequential.tmm_tools import cone_lossy, cone_lossless


class FrequentialJunctionHoleTMM(FrequentialComponent):
    """



    Parameters
    ----------
    ends : list(FrequentialPipe.End)
        the pipe ends this junction connects
    junc : JunctionModel

    References
    ----------

    [1] V.Dubos, J. Kergomard, A. Khettabi, J.-P. Dalmont, D. H. Keefe, and\
        C. J. Nederveen, “Theory of sound propagation in a duct with a \
        branched tube using modal decomposition,” Acta Acustica united with\
        Acustica, vol. 85, no. 2, pp. 153–169, 1999.

    [2] A.Lefebvre and G. P. Scavone, “Characterization of woodwind\
        instrument toneholes with the finite element method,” The Journal of\
        the Acoustical Society of America, vol. 131, no.4, pp. 3153–3163, 2012.

    """

    def __init__(self, junc, ends, nb_sub=1, opening_factor=1.0):
        self.junc = junc
        assert len(ends) == 2
        self.ends = ends
        self._nb_sub = nb_sub
        self._opening_factor = opening_factor
        if any(end.convention != 'PH1' for end in ends):
            msg = ("FrequentialJunction needs PH1 convention")
            raise ValueError(msg)
        assert self.pipe.get_physics().uniform

    def set_opening_factor(self, opening_factor):
        self._opening_factor = opening_factor

    def __get_physical_params(self):
        radii = []
        rhos = []
        cs = []
        for end in self.ends:
            radius, rho_i, c_i = end.get_physical_params()
            radii.append(radius)
            rhos.append(rho_i)
            cs.append(c_i)
        assert all(np.isclose(rhos, rho_i))
        assert np.isclose(radii[0], radii[1])
        rho = sum(rhos)/2.0
        c = sum(cs)/2.0
        r_main = sum(radii[0:2])/2.0

        r_hole = self.junc.get_radius()
        length = self.junc.get_length()

        return r_main, r_hole, length, rho, c

    def _radiation_impedance(self, omegas_scaled, r_hole, rho, c):
        Zr = self.junc.radiation.get_impedance(omegas_scaled, r_hole,
                                               rho, c, self._opening_factor)
        return Zr

    def _chimney_impedance(self, omegas_scaled, r_hole, length, rho, c):
        physics = self.junc.get_physics()
        omegas = omegas_scaled / self.junc.get_scaling().get_time()
        nb_sub = self._nb_sub
        sph = self.junc.is_spherical_waves()
        losses = self.junc.get_losses()

        if isinstance(losses, ThermoviscousBessel):  # with bessel losses
            A, B, C, D = cone_lossy(physics, length, r_hole, r_hole,
                                    omegas, nb_sub, sph)
        elif isinstance(losses, Keefe):  # Keefe losses
            A, B, C, D = cone_lossy(physics, length, r_hole, r_hole,
                                    omegas, nb_sub, sph, 'keefe')
        elif isinstance(losses, MiniKeefe):  # Keefe losses
            A, B, C, D = cone_lossy(physics, length, r_hole, r_hole,
                                    omegas, nb_sub, sph, 'minikeefe')
        elif isinstance(losses, ThermoviscousLossless):  # lossless
            A, B, C, D = cone_lossless(physics, length, r_hole, r_hole,
                                       omegas, sph)
        else:
            raise ValueError("Tonehole TMM only supports losses"
                             " {False, 'bessel, 'keefe', 'minikeefe'}, not "
                             + str(type(losses)))

        # Nondimensionalization of the TMM matrix
        B /= self.scaling.get_impedance()
        C *= self.scaling.get_impedance()

        assert np.allclose(A*D - B*C, 1.0)  # determinant should be 1

        Zr = self._radiation_impedance(omegas_scaled, r_hole, rho, c)
        Zchimney = (A*Zr + B) / (C*Zr + D)
        return Zchimney

    def get_TMM_coef(self, omegas_scaled):
        """
        Compute the TMM coefficient from Lebfevre theory

        Parameters
        ----------
        omegas_scaled : TYPE
            DESCRIPTION.

        Returns
        -------
        A : TYPE
            DESCRIPTION.
        B : TYPE
            DESCRIPTION.
        C : TYPE
            DESCRIPTION.
        D : TYPE
            DESCRIPTION.

        """
        r_main, r_hole, length, rho, c = self.__get_physical_params()
        Zchimney = self._chimney_impedance(omegas_scaled, r_hole, length,
                                           rho, c)
        m_s, m_a = self.compute_masses(r_main, r_hole, rho)
        Zs = 1j*omegas_scaled*(m_s - m_a/4) + Zchimney
        Za = 1j*omegas_scaled*m_a
        A = 1 + Za/(2*Zs)
        B = Za*(1 + Za/(4*Zs))
        C = 1/Zs
        D = A

        assert np.allclose(A*D - B*C, 1.0)  # determinant should be 1

        return A, B, C, D


#     def get_number_dof(self):
#         return 2  # len(self.mass_junction)

#     def get_contrib_freq(self, omegas_scaled):
#         """ Contribution of this component to the frequency-dependent diagonal
#         of Ah.

#         Return a sparse matrix with a shape ((number of dof) x (size of freq.))
#         """
#         mass_junction, _ = self.__get_masses()
#         my_contrib = 1j * omegas_scaled * mass_junction[:, np.newaxis]
#         # Place on our indices
#         Ah_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
#                             dtype='complex128')
#         Ah_diags[self.get_indices(), :] = my_contrib
#         return Ah_diags

#     def get_contrib_indep_freq(self):
#         _, interaction_matrix = self.__get_masses()
#         assembled_interaction_matrix = ssp.lil_matrix((self.ntot_dof,
#                                                        self.ntot_dof))
#         for i in range(len(self.ends)):
#             f_pipe_end = self.ends[i]
#             interaction = interaction_matrix[:, i]
#             for k, val in zip(self.get_indices(), np.ravel(interaction)):
#                 assembled_interaction_matrix[k, f_pipe_end.get_index()] = val
#         return assembled_interaction_matrix - assembled_interaction_matrix.T

# # ----- differential -----
#     def get_diff_masses(self, diff_index):
#         r_main, r_side, rho, _ = self.__get_physical_params()

#         d_radii = []
#         for end in self.ends:
#             d_radius = end.get_diff_radius(diff_index)
#             d_radii.append(d_radius)
#         assert np.isclose(d_radii[0], d_radii[1])
#         d_r_main = sum(d_radii[0:2])/2.0
#         d_r_side = d_radii[2]
#         dM, dT = self.junc.diff_diagonal_masses(r_main, r_side, rho,
#                                                 d_r_main, d_r_side)
#         return dM, dT

#     def get_contrib_dAh_freq(self, omegas_scaled, diff_index):
#         dM, _ = self.get_diff_masses(diff_index)
#         local_dAh_diags = 1j * omegas_scaled * dM[:, np.newaxis]
#         # Place on our indices
#         dAh_diags = np.zeros((self.ntot_dof, len(omegas_scaled)),
#                              dtype='complex128')
#         dAh_diags[self.get_indices(), :] = local_dAh_diags
#         return dAh_diags
