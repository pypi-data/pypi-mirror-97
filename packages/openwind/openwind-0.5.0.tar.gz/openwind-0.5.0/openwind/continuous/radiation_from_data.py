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


import warnings

import numpy as np

from openwind.continuous import RadiationModel, Physics
from openwind.algo_optimization import QuasiNewtonBFGS
from openwind.impedance_tools import read_impedance

def radiation_from_data(datasource, data_temperature, data_radius):
    """
    Construct a RadiationModel object from radiation data.

    Parameters
    ----------
    datasource : string or tuple of np.array
        The source of the data. It can be a filename in which the data are
        saved, or a tuple of arrays containing the frequencies and the complex
        impedance.
    data_temperature : float
        Temperature of the data.
    data_radius : float
        Radius of the radiating opening of the data.

    .. warning:: The temperature and the radius used for the simulation
                 must be consistant (equal) with the one used to obtain
                 the data!

    Returns
    -------
    RadiationFromData object
        A RadiationModel object build from data.

    """
    if type(datasource)==str:
        data = read_impedance(datasource)
        dataname = datasource
    elif type(datasource)==tuple:
        data = datasource
        dataname = 'array'
    return RadiationFromData(data, data_temperature, data_radius, dataname)

class RadiationFromData(RadiationModel):
    """
    Impose a radiation condition from a data.

    The data contains a radiation impedance (measured or simulated).

    Parameters
    ----------
    data : tuple of np.array
        tuple of two arrays containing: the frequency axis and the complex
        impedance values
    data_temperature : float
        Temperature of the data.

        .. warning:: The temperature and the radius used for the simulation
                     must be consistant (equal) with the one used to obtain
                     the data!
    data_radius : float
        Radius of the radiating opening of the data
    dataname : string, optional
        The name of the data. The default is None.
    name : string, optional
        The name of the object. The default is None
    """

    def __init__(self, data, data_temperature, data_radius, dataname=None, name=None):
        self.dataname = dataname
        self._set_impedance(data, data_temperature, data_radius)
        self._set_pade_coeffs()
        self._name = name

    def _set_impedance(self, data, data_temperature, data_radius):
        data_freq, self.data_imped = data
        rho, c = Physics(data_temperature).get_coefs(0, 'rho', 'c')
        self.data_kr = data_freq * 2*np.pi / c * data_radius

        med_imped = np.median(np.abs(self.data_imped))
        if med_imped > 1e3:
            self.data_imped /= rho * c /(np.pi * data_radius**2)
            msg = ('The radiation impedance modulus is particularly '
                   'high (median={:.2e}), it has been automatically normalized'
                   ' by the characteristics impedance.'.format(med_imped))
            warnings.warn(msg)

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return ('From data:{}, kr range=[{:.2g}, {:.2g}]').format(
                    self.dataname, np.min(self.data_kr), np.max(self.data_kr))

    def __repr__(self):
        return "RadiationFromdata{}".format(self.name)

    def get_impedance(self, omegas, radius, rho, c, opening_factor):
        """
        Radiation impedance value at a given pulsation.

        Compute the radiation condition (impedance or admittance depending on
        the convention) at the given puslation `omegas` by interpolating the
        reference radiation impedance indicated in the data.

        Parameters
        ----------
        omegas : float, np.array of float, list of float
            The pulsations at which are computed the radiation condition (s^-1)
        radius : float
            Radius of the opening.
        rho : float
            Air density at the opening.
        c : float
            Sound celerity at the opening.
        opening_factor : float
            Factor between 0 and 1 which allows to close the opening.

        Raises
        ------
        ValueError
            If some puslations at which the radiation condition must be
            computed are outside the range in which the reference impedance is
            given, an error occurs.

        Returns
        -------
        radiation : np.array
            The radiation impedance at the given pulsations.

        """
        kr = omegas * radius / c
        min_kr = np.min(self.data_kr)
        max_kr = np.max(self.data_kr)
        tresh = 1e-10
        if np.max(kr) > max_kr + tresh or np.min(kr) < min_kr - tresh:
            raise ValueError('The normalized wavenumber range at which must be'
                             ' evaluated the impedance: '
                             '[{:.2g}, {:.2g}]'.format(np.min(kr), np.max(kr))
                             + ' is wider than the range of the given data: '
                             '[{:.2g}, {:.2g}].'.format(min_kr, max_kr))
        Zc = rho*c/(np.pi*radius**2) / opening_factor
        return np.interp(kr, self.data_kr, Zc*self.data_imped)

    def get_admitance(self, omegas, radius, rho, c, opening_factor):
        Zr = self.get_impedance(omegas, radius, rho, c, 1)
        return opening_factor/Zr

    def get_diff_impedance(self, dr, omegas, radius, rho, c, opening_factor):
        raise ValueError('It is impossible to optimize the radius of an '
                         + 'opening the radiation of which is interpolated '
                         + 'from data.')

    def get_diff_admitance(self, dr, omegas, radius, rho, c, opening_factor):
        raise ValueError('It is impossible to optimize the radius of an '
                         + 'opening the radiation of which is interpolated '
                         + 'from data.')
# %% Fit the pade development
    @staticmethod
    def __radiation_pade(beta, gamma, kr):
        return 1j*kr / (gamma + 1j*kr*beta)

    @staticmethod
    def __diff_rad_pade(beta, gamma, kr):
        diff_gamma = -1j*kr / (gamma + 1j*kr*beta)**2
        diff_beta = (kr / (gamma + 1j*kr*beta))**2
        return diff_beta, diff_gamma

    def _set_pade_coeffs(self):
        fit_kr = self.data_kr[self.data_kr <= 1]  # The pade approximation is valid for kr<1
        fit_imped = self.data_imped[self.data_kr <= 1]

        def get_cost_grad(params):
            Zr_pade = self.__radiation_pade(params[0], params[1], fit_kr)
            residu = Zr_pade - fit_imped
            cost = 0.5*np.sum(np.abs(residu)**2)
            diff_beta, diff_gamma = self.__diff_rad_pade(params[0], params[1],
                                                         fit_kr)
            grad = np.zeros([2])
            grad[0] = np.real(residu.T.conjugate() @ diff_beta)
            grad[1] = np.real(residu.T.conjugate() @ diff_gamma)
            return cost, grad

        delta = 0.6133
        beta = 0.25/(delta**2)
        params_init = [beta, 1/delta]  # initiated with unflanged parameters
        params_evol, _ = QuasiNewtonBFGS(get_cost_grad, params_init)
        params_opt = params_evol[-1]
        self.beta = params_opt[0]
        self.alpha_unscaled = params_opt[1]

    def compute_coefs(self, radius, rho, c, scaling, opening_factor):
        """
        Compute the coefficients of the Pade developpement of the radiation.

        The radiation impedance is model by the following development

        .. math:: Z_r = Z_c (j \omega)/(alpha + j \omega beta)

        This method returns the three coefficients :math:`Z_c, alpha` (which
        depend on the radius) and :math:`beta`.

        Parameters
        ----------
        radius : float
            Radius of the opening.
        rho : float
            Air density at the opening.
        c : float
            Sound celerity at the opening.
        opening_factor : float
            Factor between 0 and 1 which allows to close the opening.

        Returns
        -------
        alpha, beta : float
            Coefficients of the pade developpement
        Zplus : float
            Characteristics impedance of the opening.

        Warnings
        -------
        The coefficients are obtained here by fitting the impedance given in
        the data. Precautions must be taken if the radius is different that the
        one used to obtain the reference impedance.
        """
        alpha = (self.alpha_unscaled * scaling.get_time() * c / radius
                 * opening_factor)
        beta = self.beta*opening_factor**2
        Zplus = (rho * c / (np.pi * radius**2))/scaling.get_impedance()
        return alpha, beta, Zplus
