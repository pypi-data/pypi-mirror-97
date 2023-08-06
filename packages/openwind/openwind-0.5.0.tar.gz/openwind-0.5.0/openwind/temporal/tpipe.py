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
Numerical scheme for a Pipe without losses.
"""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigs
from scipy.linalg import eig

from openwind.continuous import EndPos
from openwind.discretization import DiscretizedPipe
from openwind.temporal import TemporalComponent


class TemporalPipe(DiscretizedPipe, TemporalComponent):
    """A TemporalPipe is a DiscretizedPipe with additionnal P, V data.

    It has two ends: end_minus and end_plus. Each end must be attached to
    some end-interaction.
    A time step is performed by first updating all the end-interactions, and
    then all the pipes.


    Only convention 'PH1' is supported yet, but the computations are
    almost the same for 'VH1'.
    """


    class End:
        def __init__(self, t_pipe, pos):
            """
            Used to reference either of the pipe's ends

            Parameters
            ----------
            t_pipe : TemporalPipe
            pos : 0 if end_minus, 1 if end_plus

            We always assume that the intermediate pressure is
            q^{n+1/2} = p_{no flow} - alpha * w^{n+1/2}
            """
            self.t_pipe = t_pipe
            assert isinstance(pos, EndPos)
            self.pos = pos
            self.reset_variables()

        def reset_variables(self):
            self._w_nph = 0.0
            # Used to check that we use the pipe properly:
            # we will raise an error during simulation if two different
            # junctions try to update this TPipeEnd before the TPipe fetches the
            # value.
            self._updated = False

        def set_alpha(self, alpha_update):
            """
            alpha_update : float
                Coefficient used in the scheme update.
            """
            assert isinstance(alpha_update, float)
            self._alpha = alpha_update

        def get_alpha(self):
            return self._alpha

#        def get_mass(self): # Deprecated
#            """Compute m_end such that
#            alpha = -dt/(2*m_end)
#            """
#            return self.pipe.get_dt() / (2 * self._alpha)


        def get_p_no_flow(self):
            """Compute the pressure at time n+1/2, if the flow was 0.

            This value is used by many of the interactions.

            The actual pressure at time n+1/2 will be
            P_corr - alpha * w^{n+1/2}.
            """
            return self.t_pipe.get_p_no_flow(self.pos.array_pos)

        def get_q_nph(self):
            """Compute the average pressure at this end
            between timesteps n and n+1.

            Must be called after calculating the flow, and before updating
            the t_pipe.
            """
            self._assert_updated(True)
            return self.get_p_no_flow() - self._alpha * self._w_nph

        def get_w_nph(self):
            return self._w_nph

        # def work(self):
        #     """Compute the amount of work performed through this end
        #     between timesteps n and n+1.

        #     Must be called after calculating the flow, and before updating
        #     the t_pipe.
        #     """
        #     return self.t_pipe.dt * self._w_nph * self.get_q_nph()


        def update_flow(self, flow):
            """
            Set the value of w^{n+1/2} the flow out of the pipe end at time n+1/2

            Raises
            ------
            AssertionError
                if the flux has already been updated since the last timestep
            """
            self._assert_updated(False)
            self._updated = True
            assert isinstance(flow, (float, int))
            self._w_nph = flow

        # def accept_w_nph(self):
        #     """
        #     Read the value of the exiting flow w^{n+1/2}.

        #     For use in ``TemporalPipe.one_step()``.

        #     Raises
        #     ------
        #     AssertionError
        #         if the flux has not been updated since the last timestep
        #     """
        #     self._assert_updated(True)
        #     self._updated = False
        #     return self._w_nph

        def accept_q_nph(self):
            """
            Read the value of the intermediate pressure q^{n+1/2}.
            """
            q_nph = self.get_q_nph()
            self._assert_updated(True)
            self._updated = False
            return q_nph

        def accept_contribution(self):
            self._assert_updated(True)
            self._updated = False
            return -2 * self._alpha * self._w_nph

        def __repr__(self):
            if self is self.t_pipe.end_minus:
                return str(self.t_pipe)+".E-"
            if self is self.t_pipe.end_plus:
                return str(self.t_pipe)+".E+"
            raise Exception("This pipe-end is not attached to its TPipe!")


        def _assert_updated(self, should_be_updated):
            if self._updated and not should_be_updated:
                msg = "{} was updated several times before a pipe update. "\
                    "Make sure it is connected to only one interaction, "\
                    "and that pipes are updated after all other TElements."
                raise Exception(msg.format(self))
            if not self._updated and should_be_updated:
                msg = "{} was not updated by an interaction. "\
                    "Make sure it is connected to one interaction,"\
                    "and that pipes are updated after all other TElements."
                raise Exception(msg.format(self))

        def get_physical_params(self):
            """Get radius, rho, c at this pipe-end."""
            radius = self.t_pipe.pipe.get_radius_at(self.pos.x)
            rho = self.t_pipe.pipe.get_physics().rho(self.pos.x)
            c = self.t_pipe.pipe.get_physics().c(self.pos.x)
            return radius, rho, c

    def __init__(self, pipe, t_solver,
                 **params):
        """Discretize the pipe and prepare it for temporal simulation.

        Parameters
        ----------
        pipe : openwind.continous.Pipe
            The pipe we are simulating.
        t_solver : TemporalSolver
            What instrument does this pipe belong to?
        **params :
            Discretization parameters.
            See openwind.discretization.DiscretizedPipe.

        Returns
        -------
        None.

        """
        # Problème dû au double héritage
        # On ne peut pas faire appel à super() sans être obligé de modifier
        # DPipe et TComponent
        DiscretizedPipe.__init__(self, pipe, **params)
        TemporalComponent.__init__(self, pipe, t_solver)

        self.mL2, self.mH1 = self.get_mass_matrices()
        assert self.mL2.shape == (self.nL2,)
        assert self.mH1.shape == (self.nH1,)
        self.Bh = self.get_Bh()

        # "mass" of end will be different when there are losses
        self.end_minus = TemporalPipe.End(self, EndPos.MINUS)
        self.end_plus = TemporalPipe.End(self, EndPos.PLUS)
        self.label = pipe.label

    def set_dt(self, dt):
        self._dt = dt

        self._precompute_matrices()
        self.reset_variables()
    def get_dt(self):
        return self._dt
    def get_ends(self):
        return self.end_minus, self.end_plus
    def __str__(self):
        return "TPipe{}".format(self.label)
    def __repr__(self):
        return self.__str__()
    def get_P(self):
        P, V = self.PV
        return P
    def get_V(self):
        P, V = self.PV
        return V


    def reset_variables(self):
        """
        Reinitialize all variables to start the simulation over.
        """
        # At each step, we suppose P corresponds to P^n
        # and V corresponds to V^{n+1/2}, and dtinvMBtV is dt * (M^H1)^-1 @ B.T @ V
        self.PV = np.zeros(self.nH1), np.zeros(self.nL2)
        self._V_prev = np.zeros(self.nL2)
        # Next increment of P : P^{n+1} - P^n
        # (except at the ends)
        self.dtinvMBtV = np.zeros(self.nH1)
        self.end_minus.reset_variables()
        self.end_plus.reset_variables()

    def _precompute_matrices(self):
        self.end_minus.set_alpha(self._dt / (2 * self.mH1[0]))
        self.end_plus.set_alpha(self._dt / (2 * self.mH1[-1]))
        self.MH1inv = diags(1/self.mH1)
        self.ML2inv = diags(1/self.mL2)
        self.dtinvMBt = self._dt * self.MH1inv @ self.Bh.T
        self.dtinvML2B = self._dt * self.ML2inv @ self.Bh

        self.energy_matrix = diags(self.mH1) - self._dt**2/4 * self.CFL_matrix
        # Check that energy_matrix is positive definite
        # Eigenvalue with smallest real part should be positive
        if self.energy_matrix.shape[0] <= 2:  # Avoid scipy error for low-order elements
            self.energy_matrix = self.energy_matrix.toarray()
            w, _ = eig(self.energy_matrix)#, k=1, which='SR')
            w = np.min(w)
        else:
            w, _ = eigs(self.energy_matrix, k=1, which='SR')
        assert np.real(w) > 0

    def get_p_no_flow(self, pos):
        P, V = self.PV
        return P[pos] - self.dtinvMBtV[pos]/2

    def one_step(self, check_scheme=False):
        """Advance one time step.

        Assumes the flux of both pipe ends have already been updated.

        Raises
        ------
        AssertionError
            if either of the fluxes of the pipe ends has not been updated since
            the last time step
        """

        P_old, V_old = self.PV

        # Pressure update : inexpensive, since dtinvMBtV is precomputed
        P = P_old - self.dtinvMBtV
        # Edge contributions
#        P[0] = 2 * self.end_minus.accept_q_nph() - P_old[0]
#        P[-1] = 2 * self.end_plus.accept_q_nph() - P_old[-1]
        P[0] += self.end_minus.accept_contribution()
        P[-1] += self.end_plus.accept_contribution()

        # *******************************
        # HEAVY COMPUTATIONS HAPPEN HERE:
        # *******************************
        # Flow update
        V = V_old + self.dtinvML2B * P
        # Prepare next pressure update
        self.dtinvMBtV = self.dtinvMBt * V

#        if check_scheme:
#            dt = self._dt
#            eq1 = self.mH1 * (P - P_old)/dt + self.Bh.T @ V_old
#            eq1[0] += flow_left
#            eq1[-1] += flow_right
#            eq2 = self.mL2 * (V - V_old)/dt - self.Bh @ P
#            print("Rel. error on dtP :",np.sum(np.abs(eq1)) / (np.sum(np.abs(self.mH1 * (P - P_old)/dt))))
#            print("Rel. error on dtV :",np.sum(np.abs(eq2)) / (np.sum(np.abs(self.mL2 * (V - V_old)/dt))))

            #raise NotImplementedError


        # Remember evolution of P and V
        self.PV = P, V
        self._V_prev = V_old

    def add_pressure(self, dP):
        """
        Modify the pressure in-place.

        Use only for testing purposes, this modifies the energy in an
        unpredictable way.
        As the scheme is not not verified between the current state and the
        last, calling energy() after add_pressure() will yield a meaningless
        result (until the next one_step()).
        """
        P, V = self.PV
        P += dP # In-place modification

    def energy(self):
        r"""Compute the amount of energy stored in the pipe.

        Internal variable P represents :math:`P^n`,
        and V represents :math:`V^{n+1/2}`.
        We compute

        .. math::
            E^n = 1/2( (P^n)^* \tilde{M}^{H^1} P^n +  (\bar{V})^* M^{L^2} \bar{V}),

        where :math:`\bar{V}` is the average of
        :math:`V^{n+1/2}` and :math:`V^{n-1/2}`.

        Parameters
        ----------
        step : int
            the step at which to compute the energy.
            (Default is -1, which implies the current step)
        """
        energy_P = self.energy_P()
        energy_V = self.energy_V()
        assert energy_P >= 0 and energy_V >= 0
        return energy_P + energy_V

    def energy_P(self):
        P, V_npd = self.PV
        return np.sum(P @ self.energy_matrix @ P) / 2

    def energy_V(self):
        P, V_npd = self.PV
        V_mid = (V_npd + self._V_prev)/2
        return np.sum(V_mid * self.mL2 * V_mid) / 2

    def dissipated_last_step(self):
        return 0

    def get_maximal_dt(self):
        """Calculate the largest time step allowed for temporal simulation."""
        ML2inv = diags(1/self.mL2)
        MH1inv = diags(1/self.mH1)
        self.CFL_matrix = self.Bh.T @ ML2inv @ self.Bh
        # Compute the spectral radius of this matrix
        A = MH1inv @ self.CFL_matrix

        if A.shape[0] <= 2:  # Avoid scipy error for low-order elements
            A = A.toarray()
            rho, _ = eig(A)#, k=1, which='LM')
        else:
            # Find largest-modulus eigenvalue rho and eigenvector x s.t.
            # A @ x == rho * M @ x
            rho, _ = eigs(A, k=1, which='LM')
#        rho, _ = eigs(self.CFL_matrix, M=diags(self.mH1), k=1, which='LM')
        # rho is already a positive real, but eigs returns complex numbers
        rho = abs(np.max(rho))
        # rho* dt**2/4 has to be less than 1
        cfl = 2/np.sqrt(rho)
        return cfl

    def get_values_to_record(self):
        # Recording of energy is automated in RecordingDevice
        return {}
