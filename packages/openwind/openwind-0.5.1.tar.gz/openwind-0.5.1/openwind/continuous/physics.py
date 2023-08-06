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


class Physics:
    """
    The actual Physics class.

    Parameters
    ----------
    T :
        temperature in Kelvin
    rho :
        air density
    c :
        air sound speed
    mu :
        viscosity
    Cp :
        specific heat with constant pressure
    kappa :
        thermal conductivity
    gamma :
        ratio of specific heats
    khi :
        isentropic compressibility
    c_lt :
        velocity times a characteristic distance for loss computation
    c_lv :
        velocity times a characteristic distance for loss computation

    """

    def __init__(self, temp):
        """Define the quantitities described above.

        You can find the formulae in the Chaigne and Kergomard book
        """
        T0 = 273.15
        self.T0 = T0
        self.Cp = 240
        self.gamma = 1.402

        if callable(temp):
            self.temp = temp
            self._uniform = False
        else:
            self.temp = lambda x: np.full_like(x, temp, dtype=float)
            self._uniform = True

        self.T = lambda x: self.temp(x) + T0
        self.rho = lambda x: 1.2929 * T0 / self.T(x)
        self.c = lambda x: 331.45 * np.sqrt(self.T(x) / T0)
        self.mu = lambda x: 1.708e-5 * (1 + 0.0029 * self.temp(x))
        self.kappa = lambda x: 5.77 * 1e-3 * (1 + 0.0033 * self.temp(x))
        self.khi = lambda x: 1 / (self.rho(x) * self.c(x) ** 2)
        self.c_lt = lambda x: self.kappa(x) / (self.rho(x) * self.Cp)
        self.c_lv = lambda x: self.mu(x) / self.rho(x)
        self.lt = lambda x: self.c_lt(x) / self.c(x)
        self.lv = lambda x: self.c_lv(x) / self.c(x)

    def get_coefs(self, x, *names):
        """Get the values of several coefficients at the same time.

        Parameters
        ----------
        x : float or array-like
            where to evaluate the coefficients.
        *names : string...
            the names of the coefficients to take

        Returns
        -------
        values : tuple of (float or array-like)
        """
        coefs = tuple(getattr(self, name) for name in names)
        return tuple(coef(x) if callable(coef)
                     else coef
                     for coef in coefs)

    @property
    def uniform(self):
        """Are the coefficients independent of space?

        False if the physical coefficients depend on x, True otherwise.
        """
        return self._uniform
