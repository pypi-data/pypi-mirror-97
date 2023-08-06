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
import scipy.special as sp
from abc import ABC, abstractmethod

def losses_model(losses=True):
    """Create the right thermoviscous model.

    Parameters
    ----------
    losses : {False, True, 'bessel', 'diffrepr', 'wl', 'keefe' ,'minikeefe'}
        Which model of losses to use.
        False means lossless, True is the same as 'bessel'.
        'diffrepr' stands for 'diffusive representation', which approximates
        the 'bessel' model but can be simulated in the time domain.
        'wl' stands for "Webster-Lokshin"

    Returns
    -------
    losses_model : ThermoviscousModel
    """

    if isinstance(losses, ThermoviscousModel):
        return losses

    if losses in [False]:
        return ThermoviscousLossless()
    if losses in [True, 'bessel']:
        return ThermoviscousBessel()
    if losses.startswith('diffrepr'):
        return ThermoviscousDiffusiveRepresentation(losses)
    if losses == 'wl':
        return WebsterLokshin()
    if losses == 'keefe':
        return Keefe()
    if losses == 'minikeefe':
        return MiniKeefe()

    raise ValueError("`losses` argument should be one of: "
                     "{False, True (default), 'bessel' (same as True),"
                     " 'diffrepr', 'wl', 'keefe', 'minikeefe'}")


class ThermoviscousModel(ABC): # Abstract Base Class
    """Which model to use for thermoviscous losses.

    Assume that the model can be put under the form:

     .. math::
        Y_t(\\omega, x)  p + d_x u = 0, \\\\
        Z_v(\\omega, x)  u + d_x p = 0.

    where:

    - \(u\) is the scaled flow
    - \(p\) is the scaled pressure
    - \(x\) is the scaled position ( \(0 \\leq x \\leq 1\) ),
    - \(\\omega\) is the scaled angular frequency,

    And the coefficients

    .. math::
        Y_t(\\omega, x) = j \\omega \\left( \\frac{1}{Y_t^{\\ast}} \
        \\frac{S}{\\rho c^2} \\ell + \\text{Losses}_p(\\omega, x)  \\right) \\\\
        Z_v(\\omega, x) = j \\omega\\left( \\frac{1}{Z_v^{\\ast}}  \
        \\frac{\\rho}{S} \\ell + \\text{Losses}_u(\\omega, x) \\right)

    where :

    - \(S(x)\) is the cross section area at the \(x\) position
    - \(\\rho\) is the air density at the \(x\) position
    - \(c\) is the sound celerity at the \(x\) position
    - \(\\ell\) is the length of the pipe
    - \(Y_t^{\\ast}, Z_v^{\\ast}\) are scaling coefficients

    The aim of this class is to compute the two termes
    \(\\text{Losses}(\\omega, x)\) at given positions and frequencies.


    .. warning::
        In the losses functions, the physical parameters are generally not
        scaled!! They must have their physical dimension!

    """

    # ------ Frequency-domain functions ------
    @staticmethod
    @abstractmethod
    def get_loss_flow_at(pipe, x, omegas_scaled):
        """
        Scaled loss coefficient associated to the flow.

        .. math::
            \\text{Losses}_u(\\omega, x)

        This coefficient is used in the telegraphist equations in frequential
        domain. It is scaled to be consistent with the rest of the
        equation.

        Parameters
        ----------
        pipe : openwind.continuous.pipe.pipe
            The pipe considered
        x : float or array of float, within 0 and 1
            The normalized position(s) at which the coefficient is evaluated.
        omegas_scaled : float or array of float
            Scaled angular frequency(ies) at which the coefficient is evaluated
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_loss_pressure_at(pipe, x, omegas_scaled):
        """
        Scaled loss coefficient associated to the pressure.

        .. math::
            \\text{Losses}_p(\\omega, x)

        This coefficient is used in the telegraphist equations in frequential
        domain. It is scaled to be consistent with the rest of the
        equation.

        Parameters
        ----------
        pipe : openwind.continuous.pipe.pipe
            The pipe considered
        x : float or array of float, within 0 and 1
            The normalized position(s) at which the coefficient is evaluated.
        omegas_scaled : float or array of float
            Scaled angular frequency(ies) at which the coefficient is evaluated
        """
        raise NotImplementedError()

    @staticmethod
    def get_diff_loss_flow(pipe, x, omegas_scaled, diff_index):
        """Differential of flow coefficient w.r.t. diff_index.

        .. math::
            \\frac{\\partial \\text{Losses}_u(\\omega, x)}{\\partial m_i}

        This coefficient is scaled to be consistent with the rest of the
        equation.

        Parameters
        ----------
        pipe : openwind.continuous.pipe.pipe
            The pipe considered
        x : float or array of float, within 0 and 1
            The normalized position(s) at which the coefficient is evaluated.
        omegas_scaled : float or array of float
            Scaled angular frequency(ies) at which the coefficient is evaluated
        diff_index : int
            The index at which is stored the design parameter \(m_i\) in the
            `openwind.design.design_parameter.OptimizationParameters`
        """
        raise NotImplementedError()

    @staticmethod
    def get_diff_loss_pressure(pipe, x, omegas_scaled, diff_index):
        """Differential of pressure coefficient w.r.t. diff_index.

        .. math::
            \\frac{\\partial \\text{Losses}_p(\\omega, x)}{\\partial m_i}

        This coefficient is scaled to be consistent with the rest of the
        equation.

        Parameters
        ----------
        pipe : openwind.continuous.pipe.pipe
            The pipe considered
        x : float or array of float, within 0 and 1
            The normalized position(s) at which the coefficient is evaluated.
        omegas_scaled : float or array of float
            Scaled angular frequency(ies) at which the coefficient is evaluated
        diff_index : int
            The index at which is stored the design parameter \(m_i\) in the
            `openwind.design.design_parameter.OptimizationParameters`
        """
        raise NotImplementedError()

    def __repr__(self):
        return "<openwind.continuous.{}>".format(self.__class__.__name__)


_ZERO = np.array([[0]])


class ThermoviscousLossless(ThermoviscousModel):
    """
    No thermoviscous losses.

    .. math::
        \\text{Losses}_p(\\omega, x) = \\text{Losses}_u(\\omega, x) = 0

    This particular case is managed by returning a 1x1 matrix containing a
    single zero, and let the magic of numpy's broadcasting do the rest.
    """

    @staticmethod
    def get_loss_flow_at(pipe, x, omegas_scaled):
        return _ZERO

    @staticmethod
    def get_loss_pressure_at(pipe, x, omegas_scaled):
        return _ZERO

    @staticmethod
    def get_diff_loss_flow(pipe, x, omegas_scaled, diff_index):
        return _ZERO

    @staticmethod
    def get_diff_loss_pressure(pipe, x, omegas_scaled, diff_index):
        return _ZERO

    def __str__(self):
        return "<openwind.continuous.{}>: no losses".format(self.__class__.__name__)


def _sqrt_omegas(pipe, omegas_scaled):
    """
    Redimensionalization and square root of the frequency.

    .. math::
        \\sqrt{\\tilde{\\omega} T^{\\ast}}

    with \(\\tilde{\\omega}\) the scaled angular frequencies and \(T^{\\ast}\)
    the reference time used to scaled the frequencies.

    Parameters
    ----------
    pipe: openwind.continuous.Pipe
    omegas_scaled: np.array (n,)
        Dimensionless frequencies (scaled by the global time scaling).

    Returns
    -------
    sqrt_omegas: np.array (n,1)
        Redimensionalized frequencies, put in a shape that is
        convenient for broadcasting operations to all frequencies.
    """
    omegas = omegas_scaled / pipe.get_scaling().get_time()
    return np.sqrt(omegas)[:, np.newaxis]



class ThermoviscousBessel(ThermoviscousModel):
    """Bessel model for thermoviscous losses.

    Model is given by the formulae (5.132 - 5.134) of [1].
    Note that the lossless part is included in the cited equations,
    but excluded from this computation.

    References
    ----------
    [1] Chaigne, A., & Kergomard, J. (2016). Acoustics of musical instruments.
        Springer New York.
    """

    def __str__(self):
        return "Zwikker and Kosten losses with Bessel function"

    @staticmethod
    def get_loss_flow_at(pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)

        rhos, mus = pipe.get_physics().get_coefs(x, 'rho', 'mu')
        radius = pipe.get_radius_at(x)

        kvr = (radius * np.sqrt(-1j*rhos/mus)) * sqrt_omegas
        coefZ = -2 * sp.jve(1, kvr) / (kvr * sp.jve(2, kvr))  # = Jv / (1 - Jv)

        coef_flow = pipe.get_coef_flow_at(x)
        coef_loss_flow = coef_flow * coefZ
        return coef_loss_flow

    @staticmethod
    def get_loss_pressure_at(pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, kappas, Cp, gamma = \
            pipe.get_physics().get_coefs(x, 'rho', 'kappa', 'Cp', 'gamma')
        radius = pipe.get_radius_at(x)

        ktr = (radius * np.sqrt(-1j*rhos*Cp/kappas)) * sqrt_omegas
        coefY = 2 * sp.jve(1, ktr) / (ktr * sp.jve(0, ktr))

        coef_pressure = pipe.get_coef_pressure_at(x)
        coef_loss_pressure = coef_pressure * (gamma - 1) * coefY
        return coef_loss_pressure

    @staticmethod
    def get_diff_loss_flow(pipe, x, omegas_scaled, diff_index):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, mus = pipe.get_physics().get_coefs(x, 'rho', 'mu')
        radius = pipe.get_radius_at(x)
        diff_radius = pipe.get_diff_radius_at(x, diff_index)

        coef_flow = pipe.get_coef_flow_at(x)
        kv = np.sqrt(-1j * rhos/mus) * sqrt_omegas
        kvr = radius * kv
        jv = -2 * sp.jve(1, kvr) / (kvr * sp.jve(2, kvr))
        jvprime = kvr/2 * jv**2 + 2/kvr * (1 + jv)

        diff_coef_flow = pipe.get_diff_coef_flow_at(x, diff_index)
        diff_loss_flow = (diff_coef_flow*jv + diff_radius*coef_flow*kv*jvprime)
        return diff_loss_flow

    @staticmethod
    def get_diff_loss_pressure(pipe, x, omegas_scaled, diff_index):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, kappas, Cp, gamma = \
            pipe.get_physics().get_coefs(x, 'rho', 'kappa', 'Cp', 'gamma')
        radius = pipe.get_radius_at(x)
        diff_radius = pipe.get_diff_radius_at(x, diff_index)

        coef_pressure = pipe.get_coef_pressure_at(x)
        kt = (np.sqrt(-1j * rhos * Cp / kappas)) * sqrt_omegas
        ktr = radius * kt
        jt = 2 * sp.jve(1, ktr) / (ktr * sp.jve(0, ktr))
        jtprime = ktr/2 * jt**2 + 2/ktr * (1 - jt)

        diff_coef_pressure = pipe.get_diff_coef_pressure_at(x, diff_index)
        diff_loss_pressure = (diff_coef_pressure * (gamma - 1) * jt +
                              (diff_radius * coef_pressure * (gamma - 1) *
                               kt * jtprime))
        return diff_loss_pressure


class Keefe(ThermoviscousModel):
    """Bessel model for Keefe losses.

    Model is given in [1] .
    Note that the lossless part is included in the cited equations,
    but excluded from this computation.

    References
    ----------
    [1] Chaigne, A., & Kergomard, J. (2016). Acoustics of musical instruments.
        Springer New York.
    """

    def __str__(self):
        return "2nd order approx. of ZK losses (from Keefe)"

    @staticmethod
    def get_loss_flow_at(pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)

        rhos, mus = pipe.get_physics().get_coefs(x, 'rho', 'mu')
        radius = pipe.get_radius_at(x)

        #kvr = (radius * np.sqrt(-1j*rhos/mus)) * sqrt_omegas
        ## coefZ = 2*np.sqrt(-1j)/kvr - 3*1j/(kvr**2)
        #coefZ = -2*1j/kvr - 3/(kvr**2)

        rv = (radius * np.sqrt(rhos/mus)) * sqrt_omegas
        coefZ = 2*np.sqrt(-1j)/rv - 3*1j/(rv**2)

        coef_flow = pipe.get_coef_flow_at(x)
        coef_loss_flow = coef_flow * coefZ
        return coef_loss_flow

    @staticmethod
    def get_loss_pressure_at(pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, kappas, Cp, gamma = \
            pipe.get_physics().get_coefs(x, 'rho', 'kappa', 'Cp', 'gamma')
        radius = pipe.get_radius_at(x)

        #ktr = (radius * np.sqrt(-1j*rhos*Cp/kappas)) * sqrt_omegas
        #coefY = 2*np.sqrt(-1j)/ktr + 1j/(ktr**2)
        rt = (radius * np.sqrt(rhos*Cp/kappas)) * sqrt_omegas
        coefY = 2*np.sqrt(-1j)/rt + 1j/(rt**2)

        coef_pressure = pipe.get_coef_pressure_at(x)
        coef_loss_pressure = coef_pressure * (gamma - 1) * coefY
        return coef_loss_pressure

    @staticmethod
    def get_diff_loss_flow(pipe, x, omegas_scaled, diff_index):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, mus = pipe.get_physics().get_coefs(x, 'rho', 'mu')
        radius = pipe.get_radius_at(x)
        diff_radius = pipe.get_diff_radius_at(x, diff_index)

        rv = (radius * np.sqrt(rhos/mus)) * sqrt_omegas
        d_rv = (diff_radius * np.sqrt(rhos/mus)) * sqrt_omegas
        coefZ = 2*np.sqrt(-1j)/rv - 3*1j/(rv**2)
        d_coefZ = -d_rv*2*np.sqrt(-1j)/rv**2 + 6*d_rv*1j/(rv**3)

        coef_flow = pipe.get_coef_flow_at(x)
        diff_coef_flow = pipe.get_diff_coef_flow_at(x, diff_index)

        diff_loss_flow = diff_coef_flow*coefZ + coef_flow*d_coefZ
        return diff_loss_flow

    @staticmethod
    def get_diff_loss_pressure(pipe, x, omegas_scaled, diff_index):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, kappas, Cp, gamma = \
            pipe.get_physics().get_coefs(x, 'rho', 'kappa', 'Cp', 'gamma')
        radius = pipe.get_radius_at(x)
        diff_radius = pipe.get_diff_radius_at(x, diff_index)

        rt = (radius * np.sqrt(rhos*Cp/kappas)) * sqrt_omegas
        d_rt = (diff_radius * np.sqrt(rhos*Cp/kappas)) * sqrt_omegas
        coefY = 2*np.sqrt(-1j)/rt + 1j/(rt**2)
        d_coefY = -d_rt*2*np.sqrt(-1j)/(rt**2) - 2*d_rt*1j/(rt**3)

        coef_pressure = pipe.get_coef_pressure_at(x)
        diff_coef_pressure = pipe.get_diff_coef_pressure_at(x, diff_index)

        diff_loss_pressure = (diff_coef_pressure * (gamma - 1) * coefY +
                              coef_pressure * (gamma - 1) * d_coefY)
        return diff_loss_pressure


class MiniKeefe(ThermoviscousModel):
    """Bessel model for truncated Keefe losses.

    Model is given in [1].
    Note that the lossless part is included in the cited equations,
    but excluded from this computation.

    References
    ----------
    [1] Chaigne, A., & Kergomard, J. (2016). Acoustics of musical instruments.
        Springer New York.
    """

    def __wtr__(self):
        return "1st order approx. of ZK losses (from Keefe)"

    @staticmethod
    def get_loss_flow_at(pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)

        rhos, mus = pipe.get_physics().get_coefs(x, 'rho', 'mu')
        radius = pipe.get_radius_at(x)

        rv = (radius * np.sqrt(rhos/mus)) * sqrt_omegas
        coefZ = 2*np.sqrt(-1j)/rv

        coef_flow = pipe.get_coef_flow_at(x)
        coef_loss_flow = coef_flow * coefZ
        return coef_loss_flow

    @staticmethod
    def get_loss_pressure_at(pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        rhos, kappas, Cp, gamma = \
            pipe.get_physics().get_coefs(x, 'rho', 'kappa', 'Cp', 'gamma')
        radius = pipe.get_radius_at(x)

        rt = (radius * np.sqrt(rhos*Cp/kappas)) * sqrt_omegas
        coefY = 2*np.sqrt(-1j)/rt

        coef_pressure = pipe.get_coef_pressure_at(x)
        coef_loss_pressure = coef_pressure * (gamma - 1) * coefY
        return coef_loss_pressure






# Coefficients a_0, a_i, b_i for the model
# with diffusive representation
# formatted as (a0, [a1, ..., aN], [b1, ..., bN])

# N = 0 oscillators (only a_0)
DIFF_REPR_COEFS_0 = (8, [], [])
DIFF_REPR_COEFS_1 = (8, [2.911692e-02], [6.088225e-05])
DIFF_REPR_COEFS_2 = (8, [1.023152e-01, 6.452520e-03], [1.031475e-03,
        4.096967e-06])
DIFF_REPR_COEFS_3 = (8, [1.727801e-01, 2.132782e-02, 2.959091e-03],
        [4.488136e-03, 7.103739e-05, 1.115921e-06])
DIFF_REPR_COEFS_4 = (8, [2.101566e-01, 4.075433e-02, 8.148254e-03,
        1.961590e-03], [1.046286e-02, 4.020925e-04, 1.622093e-05,
        5.688605e-07])
DIFF_REPR_COEFS_5 = (8, [2.181136e-01, 5.786996e-02, 1.551492e-02,
        4.210425e-03, 1.508773e-03], [1.720300e-02, 1.201638e-03,
        8.735695e-05, 6.411291e-06, 3.634377e-07])
DIFF_REPR_COEFS_6 = (8, [2.111089e-01, 7.006312e-02, 2.313580e-02,
        7.696791e-03, 2.590344e-03, 1.245333e-03], [2.329107e-02,
        2.486609e-03, 2.733541e-04, 3.038915e-05, 3.371281e-06,
        2.565221e-07])
DIFF_REPR_COEFS_7 = (8, [1.989030e-01, 7.735631e-02, 2.986941e-02,
        1.156933e-02, 4.498161e-03, 1.783487e-03, 1.069059e-03],
        [2.813858e-02, 4.113576e-03, 6.140065e-04, 9.255009e-05,
        1.400273e-05, 2.093973e-06, 1.914974e-07])
DIFF_REPR_COEFS_8 = (8, [8.063381e-02, 1.864109e-01, 3.520992e-02,
        1.533509e-02, 6.695831e-03, 2.932507e-03, 1.328246e-03,
        9.403661e-04], [5.883906e-03, 3.168418e-02, 1.112007e-03,
        2.116664e-04, 4.045027e-05, 7.735956e-06, 1.444918e-06,
        1.483825e-07])
DIFF_REPR_COEFS_16 = (8, [6.627380e-02, 1.471634e-01, 4.074903e-02,
        1.552206e-02, 2.574291e-02, 9.091941e-03, 6.468480e-03,
        1.024283e-02, 1.053054e-03, 4.081166e-03, 2.575525e-03,
        1.627158e-03, 1.034049e-03, 6.787295e-04, 5.185664e-04,
        5.463057e-04], [1.244692e-02, 3.673293e-02, 4.908436e-03,
        7.628529e-04, 1.953920e-03, 5.002757e-02, 1.217589e-04,
        3.058212e-04, 9.995996e-04, 4.847890e-05, 1.930501e-05,
        7.684006e-06, 3.046646e-06, 1.179583e-06, 3.955228e-07,
        4.831127e-08])

def _get_diff_repr_coefs(name: str):
    """Obtain the coefficients from the name of the model.

    Parameters
    ----------
    name : str
        Should be 'diffrepr' or 'diffreprN' with N an integer.

    Returns
    -------
    coefs : (float, float[], float[])
        Coefficients (a_0, a_i, b_i) to put in the model.
    """
    assert name.startswith("diffrepr")

    if name == "diffrepr":
        # When no number is given
        # Default behavior: 8 coefficients
        return DIFF_REPR_COEFS_8

    try:
        field_name = "DIFF_REPR_COEFS_" + name[8:]
        return globals()[field_name]
    except KeyError:
        raise ValueError("Coefficients for " + name + " are not available.")


class ThermoviscousDiffusiveRepresentation(ThermoviscousModel):
    """Thermoviscous losses model with Diffusive Representation."""

    def __init__(self, diff_repr_coefs='diffrepr'):
        """
        Parameters
        ----------
        pipe : Pipe on which this model is applied
        diff_repr_coefs : (float, float[], float[]) or str
            Coefficients (a_0, a_i, b_i) to put in the model,
            or a string 'diffreprN' where N is the number of
            additionnal variables.
        """
        if isinstance(diff_repr_coefs, str):
            diff_repr_coefs = _get_diff_repr_coefs(diff_repr_coefs)

        self._a0, ai_coefs, bi_coefs = diff_repr_coefs
        assert len(ai_coefs) == len(bi_coefs)
        # First axis is subscript `i`, second axis will broadcast to x
        self._ai = np.array(ai_coefs)[:, np.newaxis]
        self._bi = np.array(bi_coefs)[:, np.newaxis]

    def __str__(self):
        return "Diffusive Representation of losses"

    def get_number_of_dampers(self):
        "Number of indices i used to count additionnal variables V_i or P_i."
        return self._ai.shape[0]

    def get_loss_flow_at(self, pipe, x, omegas_scaled):
        r0, ri, li = self.get_viscous_coefficients_at(pipe, x)
        # Reshape operands so that:
        # axis 0 is subscript i
        # axis 1 is omega
        # axis 2 is space
        ri = ri[:, np.newaxis, :]
        li = li[:, np.newaxis, :]
        omegas_scaled = omegas_scaled[:, np.newaxis]

        li_j_omega = li * 1j * omegas_scaled
        Delta_i = 1 / (1/ri + 1/li_j_omega)
        z_v = r0 + np.sum(Delta_i, axis=0)

        assert z_v.shape == (len(omegas_scaled), len(x))
        return z_v / (1j * omegas_scaled)

    def get_loss_pressure_at(self, pipe, x, omegas_scaled):
        g0, gi, c0, ci = self.get_thermal_coefficients_at(pipe, x)
        # Reshape operands so that:
        # axis 0 is subscript i
        # axis 1 is omega
        # axis 2 is space
        gi = gi[:, np.newaxis, :]
        ci = ci[:, np.newaxis, :]
        omegas_scaled = omegas_scaled[:, np.newaxis]

        c0_j_omega = c0 * 1j * omegas_scaled
        ci_j_omega = ci * 1j * omegas_scaled
        y_theta_tilde = g0 + np.sum(1 / (1/gi + 1/ci_j_omega), axis=0)
        y_theta = 1 / (1/c0_j_omega + 1/y_theta_tilde)

        assert y_theta.shape == (len(omegas_scaled), len(x))
        return y_theta / (1j * omegas_scaled)

    def get_diff_loss_flow(self, pipe, x, omegas_scaled, diff_index):
        raise NotImplementedError()  # TODO ?

    def get_diff_loss_pressure(self, pipe, x, omegas_scaled, diff_index):
        raise NotImplementedError()  # TODO ?

    def get_viscous_coefficients_at(self, pipe, x):
        """Nondimensionalized coefficients R_0(x), R_i(x), L_i(x)."""
        rhos, mus = pipe.get_physics().get_coefs(x, 'rho', 'mu')
        section = pipe.get_section_at(x)
        scaling_l = pipe.get_scaling_flow()
        scaling_r = scaling_l / pipe.get_scaling().get_time()

        # R_0 and R_i have same dimensionality as coef_flow divided by time
        scaled_coef_r = (np.pi * mus / section**2) * pipe.get_length() / scaling_r
        r0 = scaled_coef_r * self._a0
        ri = scaled_coef_r * (self._ai / self._bi)
        # L_i have the same, but multiplied by time.
        li = rhos / section * pipe.get_length() * self._ai / scaling_l
        return r0, ri, li

    def get_thermal_coefficients_at(self, pipe, x):
        """Nondimensionalized coefficients G_0(x), G_i(x), C_0(x), C_i(x)."""
        rhos, kappas, Cp, gamma, cs = \
            pipe.get_physics().get_coefs(x, 'rho', 'kappa', 'Cp', 'gamma', 'c')
        section = pipe.get_section_at(x)
        scaling_c = pipe.get_scaling_pressure()
        scaling_g = scaling_c / pipe.get_scaling().get_time()

        scaled_coef_g = (np.pi * kappas * (gamma-1) * pipe.get_length()
                         / (rhos**2 * cs**2 * Cp)) / scaling_g
        g0 = scaled_coef_g * self._a0
        gi = scaled_coef_g * (self._ai / self._bi)

        scaled_coef_c = (section * (gamma-1) * pipe.get_length() / (rhos * cs**2)
                         / scaling_c)
        c0 = scaled_coef_c
        ci = scaled_coef_c * self._ai

        return g0, gi, c0, ci



class WebsterLokshin(ThermoviscousModel):
    """Webster-Lokshin model of boundary layer losses.

    Losses are applied to the pressure term only,
    and are expressed as a fractional derivative w.r.t. time.
    Formulae are given in [1], eq. (16).

    -  No contribution of losses to the flow term: \
        \( \\text{Losses}_u(\\omega, x)=0\)
    - Fractional derivative on the pressure.

    References
    ----------
    [1] Hélie, Thomas and Hézard, Thomas and Mignot, Rémi and Matignon,
        Denis. One-dimensional acoustic models of horns and comparison
        with measurements. (2013) Acta Acustica united with Acustica,
        vol. 99 (n° 6). pp. 960-974. ISSN 1610-1928
    """

    def __repr__(self):
        return "Webster-Lokshin model of boundary layer losses (from Hélie)"

    def get_loss_flow_at(self, pipe, x, omegas_scaled):
        return _ZERO

    def get_loss_pressure_at(self, pipe, x, omegas_scaled):
        sqrt_omegas = _sqrt_omegas(pipe, omegas_scaled)
        lv, lt, c, gamma = pipe.get_physics() \
                            .get_coefs(x, 'lv', 'lt', 'c', 'gamma')
        epsilon_star = np.sqrt(lv) + (gamma-1) * np.sqrt(lt)
        radius = pipe.get_radius_at(x)
        conicity = pipe.get_conicity_at(x)
        length_factor = np.sqrt(1 + conicity**2)

        epsilon = epsilon_star * length_factor / radius

        # dimensionless loss coefficient
        coefY = 2 * epsilon * np.sqrt(-1j * c) / sqrt_omegas

        coef_pressure = pipe.get_coef_pressure_at(x)
        coef_loss_pressure = coef_pressure * coefY
        return coef_loss_pressure
