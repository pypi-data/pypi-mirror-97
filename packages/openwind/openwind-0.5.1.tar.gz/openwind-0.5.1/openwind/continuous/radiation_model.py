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

from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from openwind.continuous import Physics, Scaling


class RadiationModel(ABC):
    """Choice of a formula to compute a radiation impedance."""

    @abstractmethod
    def get_impedance(self, omegas, radius, rho, c, opening_factor):
        """Radiation impedance.

        Parameters
        ----------
        omegas_scaled : array(float)
            pulsation in s^-1.
        radius : float
            radius of the circular opening.
        rho : float
            air density.
        c : float
            speed of sound in air.
        opening_factor : float
            1 for open pipe, 0 for closed pipe.
        """

    @abstractmethod
    def get_admitance(self, omegas, radius, rho, c, opening_factor):
        """Radiation admitance.

        Parameters
        ----------
        omegas_scaled : array(float)
            pulsation in s^-1.
        radius : float
            radius of the circular opening.
        rho : float
            air density.
        c : float
            speed of sound in air.
        opening_factor : float
            1 for open pipe, 0 for closed pipe.
        """

    @property
    @abstractmethod
    def name(self):
        """Name of this model of radiation.

        Used for plotting, and for repr() unless overridden.
        """

    @abstractmethod
    def get_diff_impedance(self, dr, omegas, radius, rho, c, opening_factor):
        """Variation of impedance with respect to radius."""

    @abstractmethod
    def get_diff_admitance(self, dr, omegas, radius, rho, c, opening_factor):
        """Variation of admitance with respect to radius."""

    def plot_impedance(self, kr0s=np.linspace(0, 4, 200),
                       opening_factor=1.0,
                       axes=None, **kwargs):
        """Plot the radiation impedance of the pipe.

        Parameters
        ----------
        kr0s : array(float)
            Values of omega/c * r0 to use.
        axes : matplotlib Axes, optional
            Where to plot. Default creates a new figure.
        **kwargs :
            Keyword arguments for plt.plot().
        """
        r0 = 1.0
        rho, c = Physics(20).get_coefs(0, 'rho', 'c')
        omegas = kr0s * c/r0
        imped = self.get_impedance(omegas, r0, rho, c, opening_factor)
        imped /= rho*c/(np.pi*r0**2)
        if not axes:
            axes = plt.axes()
        line, = axes.plot(kr0s, np.real(imped), label=self.name, **kwargs)
        axes.plot(kr0s, np.imag(imped), color=line.get_color(), **kwargs)
        axes.set_xlabel('$k r_0$')
        axes.set_ylabel('$Z_R/Z_C$')
        axes.legend()

    def __repr__(self):
        return "{class_}({name})".format(class_=type(self).__name__,
                                         name=repr(self.name))


def __taylor_to_pade(delta, beta_chaigne):
    alpha = 1 / delta
    beta = beta_chaigne / delta**2
    return alpha, beta


def radiation_pade(category):
    """Obtain a RadiationPade model corresponding to a given name.
    """
    if category == 'unflanged_2nd_order':
        return RadiationPade2ndOrder(0.167, 1.393, 0.457)
    elif category == 'flanged_2nd_order':
        return RadiationPade2ndOrder(0.182, 1.825, 0.649)
    else:
        if category == "planar_piston":
            alpha_unscaled, beta = __taylor_to_pade(8/(3*np.pi), 0.5)
        elif category == "unflanged":
            alpha_unscaled, beta = __taylor_to_pade(0.6133, 0.25)
        elif category == "infinite_flanged":
            alpha_unscaled, beta = __taylor_to_pade(0.8236, 0.5)
        elif category == "total_transmission":
            alpha_unscaled, beta = (0, 1)
        elif category == "closed":
            alpha_unscaled = 0
            beta = 0
        else:
            raise ValueError("Unknown radiation type '{}'. Chose between:"
                             "['planar_piston', 'unflanged', 'infinite_flanged',"
                             "'total_transmission', 'closed']".format(category))
        return RadiationPade(alpha_unscaled, beta, category)


class RadiationPade(RadiationModel):
    """Radiation model in Padé form.

    The equation is:
        ZR = Zplus j omega / (alpha + beta j omega).
    """

    def __init__(self, alpha, beta, name=None):
        self.alpha_unscaled, self.beta = \
            alpha, beta
        self._name = name

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return 'alpha={:.3g}, beta={:.3g}'.format(self.alpha_unscaled,
                                                      self.beta)

    def __repr__(self):
        return ("<openwind.continuous.RadiationPade(alpha={:.3g}, beta={:.3g}"
                ", '{}')>".format(self.alpha_unscaled, self.beta, self._name))

    def __str__(self):
        return ("{} radiation model in Padé form: (alpha={:.3g}, "
                "beta={:.3g})".format(self._name, self.alpha_unscaled,
                                      self.beta))

    def _rad_coeff(self, omegas, radius, rho, celerity, opening_factor):
        kr = omegas*radius/celerity
        Zc = rho*celerity / (np.pi*radius**2)
        alpha = self.alpha_unscaled * opening_factor
        beta = self.beta * opening_factor**2
        return kr, Zc, alpha, beta

    def compute_coefs(self, radius, rho, c, scaling, opening_factor):
        """ Used only with the temporal simulation"""
        Zplus = (rho * c / (np.pi * radius**2))/scaling.get_impedance()
        alpha = self.alpha_unscaled * scaling.get_time() * c / radius * opening_factor
        beta = self.beta * opening_factor**2
        return alpha, beta, Zplus

    def get_impedance(self, omegas, radius, rho, celerity, opening_factor):
        kr, Zc, alpha, beta = self._rad_coeff(omegas, radius, rho, celerity,
                                              opening_factor)
        return Zc * 1j*kr / (alpha + 1j*kr*beta)

    def get_diff_impedance(self, dr, omegas, radius, rho, celerity,
                           opening_factor):
        kr, Zc, alpha, beta = self._rad_coeff(omegas, radius, rho, celerity,
                                              opening_factor)
        dZc = -2*dr/radius * Zc
        dkr = omegas*dr/celerity
        return (dZc * 1j*kr / (alpha + 1j*kr*beta)
                + Zc * 1j*dkr*alpha / (alpha + 1j*kr*beta)**2)

    def get_admitance(self, omegas, radius, rho, celerity, opening_factor):
        kr, Zc, alpha, beta = self._rad_coeff(omegas, radius, rho, celerity,
                                              opening_factor)
        return (alpha + 1j*kr*beta) / (Zc * 1j*kr)

    def get_diff_admitance(self, dr, omegas, radius, rho, celerity,
                           opening_factor):
        kr, Zc, alpha, beta = self._rad_coeff(omegas, radius, rho, celerity,
                                              opening_factor)
        dZc = -2*dr/radius * Zc
        dkr = omegas*dr/celerity
        return (dZc*1j*kr*(alpha + beta*1j*kr) + Zc*1j*dkr*alpha) / (Zc*kr)**2

class RadiationPade2ndOrder(RadiationModel):
    """
    Radiation model in Padé form at the second order as proposed by [1] .

    Following the correction proposed in the Corrigendum and with the good
    complex convention, the equation is:

    .. math::
        Z_r = \\frac{- (n_1 - d_1) jkr + d_2 (j k r)^2}\
            {2 + (d_1 + n_1) jkr + d_2 (jkr)^2}.


    Parameters
    ----------
    d1, n1, d2 : float
        The coefficient values, depending of the radiation type (flanged,
        unflanged)
    name : string, optional
        The label of the object. The default is None.

    Reference
    --------
    .. [1] F.Silva, P.Guillemain, J.Kergomard, B.Mallaroni, and A.N.Norris, \
        "Approximation formulae for the acoustic radiation impedance of a \
        cylindrical pipe", Journal of Sound and Vibration, vol.322, no.1–2, \
        pp.255–263, Apr.2009, doi: 10.1016/j.jsv.2008.11.008.

    """

    def __init__(self, n1, d1, d2, name=None):
        self.n1, self.d1, self.d2 = n1, d1, d2
        self._name = name

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return 'n1={:.5f}, d1={:.5f}, d2={:.5f}'.format(self.n1, self.d1,
                                                            self.d2)

    def __repr__(self):
        return ("<openwind.continuous.RadiationPade2ndOrder(n1={:.3g}, "
                "d1={:.3g},  d2={:.3g},'{}')>".format(self.n1, self.d1,
                                                      self.d2, self._name))

    def _rad_coeff(self, omegas, radius, rho, celerity, opening_factor):
        # TODO: include the opening factor in the radiation coefficients
        if opening_factor != 1:
            raise ValueError('The opening factor is not yet implemented for' +
                             ' this version of radiation')
        kr = omegas*radius/celerity
        Zc = rho*celerity / (np.pi*radius**2)
        n1 = self.n1 #* opening_factor
        d1 = self.d1 #* opening_factor
        d2 = self.d2 #* opening_factor**2
        return kr, Zc, n1, d1, d2

    def compute_coefs(self, radius, rho, c, scaling, opening_factor):
        """ Method Used only with the temporal simulation.
        TODO: implement the temporal version of this radiation
        """
        raise NotImplementedError

    def get_impedance(self, omegas, radius, rho, celerity, opening_factor):
        kr, Zc, n1, d1, d2 = self._rad_coeff(omegas, radius, rho, celerity,
                                             opening_factor)
        return Zc*((n1 - d1)*-1j*kr - d2*kr**2)/(2 + (d1 + n1)*1j*kr - d2*kr**2)

    def get_diff_impedance(self, dr, omegas, radius, rho, celerity,
                           opening_factor):
        # kr, Zc, alpha, beta = self._rad_coeff(omegas, radius, rho, celerity,
        #                                       opening_factor)
        # dZc = -2*dr/radius * Zc
        # dkr = omegas*dr/celerity
        # return (dZc * 1j*kr / (alpha + 1j*kr*beta)
        #         + Zc * 1j*dkr*alpha / (alpha + 1j*kr*beta)**2)
        raise NotImplementedError

    def get_admitance(self, omegas, radius, rho, celerity, opening_factor):
        kr, Zc, n1, d1, d2 = self._rad_coeff(omegas, radius, rho, celerity,
                                             opening_factor)
        return 1/Zc*(2 + (d1 + n1)*1j*kr - d2*kr**2)/((n1 - d1)*-1j*kr - d2*kr**2)

    def get_diff_admitance(self, dr, omegas, radius, rho, celerity,
                           opening_factor):
        # kr, Zc, alpha, beta = self._rad_coeff(omegas, radius, rho, celerity,
        #                                       opening_factor)
        # dZc = -2*dr/radius * Zc
        # dkr = omegas*dr/celerity
        # return (dZc*1j*kr*(alpha + beta*1j*kr) + Zc*1j*dkr*alpha) / (Zc*kr)**2
        raise NotImplementedError


class RadiationPerfectlyOpen(RadiationModel):
    """Z_R=0"""
    @property
    def name(self):
        return "perfectly_open"
    def get_impedance(self, *args, **kwargs):
        return 0
    def get_diff_impedance(self, *args, **kwargs):
        return 0
    def get_admitance(self, *args, **kwargs):
        return np.infty
    def get_diff_admitance(self, *args, **kwargs):
        return 0
