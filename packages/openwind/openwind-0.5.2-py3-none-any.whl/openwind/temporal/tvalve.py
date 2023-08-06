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

"""Numerical theta-scheme for a 1-DOF valve model."""

from math import sqrt
import numpy as np

from openwind.temporal import TemporalComponentExit

def _positive_part(y):
    return y * (y > 0)

def _negative_part(y):
    return y * (y < 0)

def _abs_negative_part(y):
    return -y * (y < 0)

#NUMERICAL THETA SCHEME
class TemporalValve(TemporalComponentExit):
    """Simulate the interaction with lips or a reed at the end of the pipe.

    We use the one-degree-of-freedom model from [Bil09]_.
    The scheme used is a theta-scheme.
    TODO Add documentation for the scheme.

    References
    ----------
    .. [Bil09] Bilbao, S. (2009). Direct simulation of reed wind instruments.
       Computer Music Journal, 33(4), 43-55.

    Parameters
    ----------
    valve : openwind.continuous.Valve
        Continuous model with parameters
    pipe_ends : (openwind.temporal.TemporalPipe.End, )
        The tuple of the single pipe end this valve is connected to
    t_solver : openwind.temporal.TemporalSolver
        The TemporalSolver this object is a part of
    theta : float
        Parameter of the theta-scheme
    """

    def __init__(self, valve, pipe_ends, t_solver, theta):
        super().__init__(valve, t_solver)
        self.pipe_end, = pipe_ends
        self.valve = valve
        mouth_pressure = valve.mouth_pressure
        if callable(mouth_pressure):
            self.mouth_pressure = mouth_pressure
        elif isinstance(mouth_pressure, (int, float)):
            self.mouth_pressure = lambda t: mouth_pressure

        self.theta = theta
        print('Using Theta scheme, theta = ' + str(self.theta))

    def set_dt(self, dt):
        self.dt = dt
        self.reset_variables()
        self._precompute_constants()

    def _precompute_constants(self):
          # rien pour l'instant
        pass

        # %% j'ai besoin de :
        # valve.sr
        # valve.mr
        # valve.g
        # valve.omega02
        # valve.w
        # valve.y0

        # self.dt
        # self.theta
        # -1/self.pipe_end.get_alpha() : 2 m_end / Delta t
        # self.pipe_end.get_p_no_flow()
        # self.mouth_pressure(self._t)


    def one_step(self):
        """Advance one time step.

        Computes the evolution of internal variables `y`,
        and updates the flux on the connected
        ``PipeEnd``.
        """

        (_, rho, _) = self.pipe_end.get_physical_params()

        valve = self.valve

        p_no_flow = self.pipe_end.get_p_no_flow()
        #p_m = valve.mouth_pressure.get_value(self.t)

        # "opening", "mass","section","pulsation","dissip","width",
        # "mouth_pressure","model"
        # TODO : faire les 6 lignes et la precedente en un seul appel fonction

        # Sr = valve.section.get_value(self.t)
        # Mr = valve.mass.get_value(self.t)
        # g = valve.dissip.get_value(self.t)
        # omega02 = valve.pulsation.get_value(self.t)**2
        # w = valve.width.get_value(self.t)
        # y0 = valve.opening.get_value(self.t)
        # epsilon = valve.model.get_value(self.t)

        (Sr, Mr, g, omega02, w, y0, epsilon, p_m) = valve.get_all_values(self.t)


        dt = self.dt
        theta = self.theta
        m_end_tilde = -1/self.pipe_end.get_alpha()  # 2/ delta t * m_end

        last_y = self._last_y  # y^{n-1}
        this_y = self._this_y  # y^{n}
        prev_z = self._prev_z  # z^{n-\half}
       # print(last_y, this_y)

        #  values from Bilbao 2008
        omega_nl = valve.contact_pulsation.get_value(self.t)  #316
        alpha = valve.contact_exponent.get_value(self.t) #4

        # Calcul constantes :
        # =============== NEW LINEARLY IMPLICIT PRESERVING SCHEME =============
        # 1/ (4*Mr) (G^'(y^n))^2  = alpha omega1^alpha /(8 y0^(alpha-1)) |y^-|^(alpha-2)
        ynminus = _abs_negative_part(this_y)
        Gprime = alpha*0.5*np.sqrt(2*omega_nl**alpha*Mr/(alpha*y0**(alpha-1)))*ynminus**(alpha/2-1)
        NL_fact = Gprime**2/(4*Mr) # alpha*omega_nl**alpha / (8*y0**(alpha-2)) * ynminus**(alpha-2)
        AB_fact = 1/(1/dt**2  + g/(2*dt) + omega02*theta + NL_fact)
        B1 = (2/dt**2 - omega02*(1-2*theta))
        B2 = (-2/dt**2 - 2*omega02*theta)
        B3 = omega02*y0 - prev_z*Gprime/Mr
        # ======================================================================

        A = AB_fact * (epsilon*Sr/Mr)

        B = AB_fact * (B1*this_y + B2*last_y + B3)
        C = -m_end_tilde
        D = m_end_tilde * (p_m - p_no_flow)

        # print('D = {}, B = {}'.format(D, B))


        alpha = C + epsilon * (Sr/(2*dt) * A)
        beta = D + epsilon * (Sr/(2*dt) * B)
        gamma = w * _positive_part(this_y) * np.sqrt(2/rho)

        # # CALCUL DELTA P


        # if gamma == 0.0:
        #     # First order equation
        #     Delta_P = -beta/alpha
        #     # print('alpha = {}, beta = {}, gamma = {}'.format(alpha, beta, gamma))
        # else:
            # Second order equation
            # print('alpha = {}, beta = {}, gamma = {}'.format(alpha, beta, gamma))
        discr = gamma**2 + 4 * alpha * abs(beta)
        root = (-gamma + sqrt(discr)) / (2*alpha)
        Delta_P = -np.sign(beta) * root**2

        # CALCUL LAMBDA
        flow_lambda = C * Delta_P + D

        # CALCUL de y^(n+1)
        temp = A * Delta_P + B
        next_y = temp + last_y
        # print('Delta_P = {}, flow = {}, next_y = {}'.format(Delta_P, flow_lambda, next_y))
        # =============== NEW LINEARLY IMPLICIT PRESERVING SCHEME =============
        next_z = prev_z + Gprime*(next_y-last_y)*0.5
        # ======================================================================


        # mise à jour des valeurs
        self.pipe_end.update_flow(flow_lambda)
        self._this_y = next_y
        self._last_y = this_y
        self._last_last_y = last_y
        self._prev_z = next_z
        self._last_Delta_P = Delta_P
        self._last_lambda = flow_lambda
        self._last_pm = p_m
        self.t += self.dt

        super().remember_flow_and_pressure(self.pipe_end)  # For recording

    def get_maximal_dt(self):
        """This numerical scheme has a CFL condition."""
        theta = self.theta
        if theta >= 0.25:
            dt_max = np.inf
        else:
            # CFL is calculated from the value at t=0
            # TODO Which parameters are allowed to vary?
            omega02 = self.valve.pulsation.get_value(0)**2
            dt_max = np.sqrt(np.abs(1 / ((0.25 - theta) * omega02)))
        return dt_max

    def reset_variables(self):
        # _y is y^{n+1/2}
        self.y = self.valve.opening.get_value(0)

        self._last_last_y = self.y  # needed for energy dissipation
        self._last_y = self.y
        self._this_y = self.y

        # linearly imlpicit scheme for NL term
        # (it is assumed that y is far from contact at initial time)
        self._prev_z = 0.0 # z^{n+1}
        self._next_z = 0.0 # z^n

        self.t = self.dt/2

    def __str__(self):
        return "TValve({})".format(self.pipe_end)
    def __repr__(self):
        return self.__str__()

    def energy(self):
        """Compute the amount of energy stored in the valve."""
        z_n = (self._this_y - self._last_y)/self.dt
        y_bar = (self._this_y + self._last_y)/2
        y0 = self.valve.opening.get_value(self.t)
        mr = self.valve.mass.get_value(self.t)
        omega02 = self.valve.pulsation.get_value(self.t)**2

        spring_energy = mr/2 * omega02 * (y_bar - y0)**2 + 0.5*self._prev_z**2

        kinetic_energy = mr/2 * (1 +
                                 self.dt**2 *
                                 (self.theta - 1/4) *
                                 omega02) * z_n**2
        # %%
        return spring_energy + kinetic_energy


    def dissipated_last_step(self):
        (_, rho, _) = self.pipe_end.get_physical_params()

        z_bar = (self._this_y - self._last_last_y)/(2 * self.dt)

        spring_damping = self.valve.mass.get_value(self.t) \
            * self.valve.dissip.get_value(self.t) * z_bar**2
        bernoulli_dissip = self.valve.width.get_value(self.t) * sqrt(2/rho) * _positive_part(self._last_y) * abs(self._last_Delta_P)**(3/2)
        NL_dissip = 0
        # we add the term coming from the mouth pressure
        forcing_term = self._last_pm * self._last_lambda
        #print([spring_damping , bernoulli_dissip , NL_dissip , forcing_term])
        return (spring_damping + bernoulli_dissip + NL_dissip + forcing_term) * self.dt
