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
Numerical scheme for a junction of three pipes.
"""

import numpy as np
from numpy.linalg import inv
from scipy.sparse import diags

from openwind.continuous import JunctionTjoint
from openwind.temporal import TemporalComponent


class TemporalJunction(TemporalComponent):
    """Junction of three Pipes for time-domain simulation.

    /!\ WARNING: uses modified acoustic masses, that do not correspond exactly
    to the model from [Chaigne--Kergomard]. Instead of a negative
    acoustic mass, we use a small positive one, computed by
    `JunctionTjoint.compute_passive_masses()`. /!\

    """

    def __init__(self, junct, ends, **kwargs):
        """
        Parameters
        ----------
        end1, end2, end3
            The three ``TemporalPipe.PipeEnd`` objects the junction connects
        junct : openwind.Junction
            The acoustic masses of the junction
        """
        super().__init__(junct, **kwargs)
        self._end1, self._end2, self._end3 = ends

        r_main, rho, _ = self._end1.get_physical_params()
        r_side, _, _ = self._end3.get_physical_params()
        self.m11, self.m12, self.m22 = junct.compute_passive_masses(r_main, r_side, rho)

        self.reset_variables()
        self._should_recompute_constants = True

    def set_dt(self, dt):
        self.dt = dt
        self._should_recompute_constants = True

    def reset_variables(self):
        """
        Reinitialize all variables to start the simulation over.
        """
        self._gamma = np.zeros(2)
        self._P_corr = np.zeros(3)

    def _precompute_constants(self):
        """Compute constant matrices used in the update"""
        m_end1 = self.dt / (2 * self._end1.get_alpha())
        m_end2 = self.dt / (2 * self._end2.get_alpha())
        m_end3 = self.dt / (2 * self._end3.get_alpha())

        M_J = np.array([[self.m11, self.m12],
                        [self.m12, self.m22]])
        invM_end = diags([1/m_end1, 1/m_end2, 1/m_end3])
        T_J = np.array([[1, 0, -1],
                        [0, 1, -1]])

        # Matrix of self-contribution of gamma trough the evolution of pressure
        A_g = T_J @ invM_end @ T_J.T
        # Matrix M_{J,dt}, to invert for performing a half-timestep
        M_Jdt = M_J + self.dt**2/4 * A_g
        invM_Jdt = np.array(inv(M_Jdt))
        # Matrix used to update gamma by half a step
        self.Step = invM_Jdt @ M_J
        # Influence of each pipe's pressure and velocity on the update of gamma
        self.Infl = -self.dt/2 * invM_Jdt @ T_J
        #print(self.Step, type(self.Step), self.Infl, type(self.Infl))

        self._should_recompute_constants = False


    def _read_end_values(self):
        # Predicted value of P at time n+1/2
        self._P_corr[0] = self._end1.get_p_no_flow()
        self._P_corr[1] = self._end2.get_p_no_flow()
        self._P_corr[2] = self._end3.get_p_no_flow()

    def _update_flows(self, gamma_b):
        # Flow calculated with old convention : inverted sign
        self._end1.update_flow(-gamma_b[0])
        self._end2.update_flow(-gamma_b[1])
        self._end3.update_flow(gamma_b[0] + gamma_b[1])

    def one_step(self):
        """Advance one time step

        Computes the evolution of internal variables ``gamma``,
        and updates the flow on the three connected
        ``PipeEnd``.
        """
        if self._should_recompute_constants:
            self._precompute_constants()

        self._read_end_values()
        gamma = self._gamma
        gamma_b = self.Step @ gamma + self.Infl @ self._P_corr
        self._gamma = 2*gamma_b - gamma
        self._update_flows(gamma_b)

    def __str__(self):
        name = "TJunction({}, {}, {})"
        return name.format(self._end1, self._end2, self._end3)
    def __repr__(self):
        return self.__str__()

    def energy(self):
        """Compute the amount of energy stored
        in the junction at time step `step`.
        """
        gamma = self._gamma
        energy_1 = self.m11/2 * gamma[0]**2
        energy_2 = self.m22/2 * gamma[1]**2
        energy_cross = self.m12 * gamma[0] * gamma[1]
        return energy_1 + energy_2 + energy_cross

    def dissipated_last_step(self):
        return 0

    def get_maximal_dt(self):
        return np.infty
