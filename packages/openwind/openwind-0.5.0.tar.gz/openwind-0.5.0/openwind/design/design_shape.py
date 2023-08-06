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
Base class for the shape of a pipe.
"""

from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from openwind.design import eval_, diff_




class DesignShape(ABC):
    """
    Base class for the shape of a section of tube.

    Describe the radius profile r(x) of a length of pipe.
    """

    # %% --- ABSTRACT METHODS ---

    @abstractmethod
    def get_radius_at(self, x_norm):
        """
        Gives the value of the radius at the normalized positions.


        :math:`r(\\tilde{x})`

        Parameters
        ---------
        x_norm : float, array of float
            The normalized position :math:`\\tilde{x}` within 0 and 1 at which
            the radius is computed

        Return
        ------
        float, array of float
            The radii of the shape (same type of `x_norm`)

        """

    @abstractmethod
    def get_diff_radius_at(self, x_norm, diff_index):
        """
        Differentiate the radius w.r. to one parameter.

        .. math::
            \\frac{\\partial r(\\tilde{x})}{\\partial m_i}

        Gives the differentiate of the radius with respect to the
        optimization variable :math:`m_i` at the normalized position
        :math:`\\tilde{x}`.



        Parameters
        ----------
        x_norm : float, array of float
            The normalized position :math:`\\tilde{x}` within 0 and 1 at which the
            radius is computed
        diff_index : int
            The index at which the designated parameters is stored in the
            `openwind.design.design_parameter.OptimizationParameters`.

        Return
        -------
        float, array of float
            The value of the differentiate at each `x_norm`
        """



    @abstractmethod
    def get_endpoints_position(self):
        """
        The design parameters corresponding to the endpoints position.

        Return
        ------
        openwind.design.design_parameter.DesignParameters
            The two paramaters corresponding to the endpoints position
            (abscissa in meters).
        """

    @abstractmethod
    def get_endpoints_radius(self):
        """
        The design parameters corresponding to the endpoints radii.

        Return
        ------
        openwind.design.design_parameter.DesignParameters
            The two paramaters corresponding to the endpoints radii of the
            shape (in meters).
        """



    # %% --- COMMON METHODS ---
    def __repr__(self):
        """Allows readable printing of a list of shapes"""
        positions = self.get_endpoints_position()
        radii = self.get_endpoints_radius()
        return (('{class_}(length={length}cm, bounds positions=[{pos0}, {pos1}]'
                'm, bounds radii=[{rad0}, {rad1}]m)')
                .format(class_=type(self).__name__,
                        length=100*self.get_length(), pos0=positions[0],
                        pos1=positions[1], rad0=radii[0], rad1=radii[1]))

    @staticmethod
    def check_bounds(x, bounds):
        """
        Ensure x is within the given bounds.

        Parameters
        ----------
        x : array
        bounds : list of two floats

        """
        tolerance = 1e-10
        if np.any(x < bounds[0] - tolerance) or np.any(x > bounds[-1] + tolerance):
            raise ValueError('A value is being estimated outside the shape!'
                             'x in [{:.2e},{:.2e}], whereas bounds are '
                             '[{:.2e},{:.2e}]'.format(np.min(x), np.max(x),
                                                      bounds[0], bounds[-1]))

    def is_TMM_compatible(self):
        """
        Is the shape compatible with TMM computation.

        Currently only conical shapes can be used with TMM.

        Returns
        -------
        bool
            The compatibility with TMM computation.

        """
        return False

    def get_length(self):
        """
        Physical length of the pipe in meters.
        """
        X_range = self.get_endpoints_position()
        Xmin, Xmax = eval_(list(X_range))
        return Xmax - Xmin

    def get_diff_length(self, diff_index):
        """
        Differentiate the length w.r.t. an optimization parameter.

        Parameters
        ----------
        diff_index : int
            The index at which the designated parameters is stored in the
            `openwind.design.design_parameter.OptimizationParameters`.

        """
        X_range = self.get_endpoints_position()
        dXmin, dXmax = diff_(list(X_range), diff_index)
        return dXmax - dXmin

    def plot_shape(self, **kwargs):
        """Display this DesignShape.

        Keyword arguments are passed directly to `plt.plot()`.
        """
        x_norm = np.linspace(0, 1, 100)
        x = self.get_position_from_xnorm(x_norm)
        r = self.get_radius_at(x_norm)
        plt.plot(x, r, **kwargs)

    # %% --- CONVERSION X /X_NORM METHODS ---

    def get_position_from_xnorm(self, x_norm):
        """
        Re-scaled the position.

        Give the position on the main bore pipe in meter from a scaled
        position.

        .. math::
            x = (x_{max} - x_{min}) \\tilde{x} + x_{min}

        with :math:`x_{max}, x_{min}` the end points position of the considered
        pipe.

        Parameters
        ----------
        x_norm : float, array of float
            The normalized position :math:`\\tilde{x}` within 0 and 1.

        Return
        ------
        float, array of float
            The physical position in meter.

        """
        Xmin, Xmax = eval_(self.get_endpoints_position())
        return x_norm*(Xmax - Xmin) + Xmin

    def get_xnorm_from_position(self, position):
        """
        Unscaled the position.

        Give the normalized position on the pipe from the physical position in
        meters.

        .. math::
            \\tilde{x} = \\frac{x - x_{min}}{x_{max} - x_{min}}

        with :math:`x_{max}, x_{min}` the end points position of the considered
        pipe.

        Parameters
        ---------
        position : float, array of float
            The physical position in meter.

        Return
        ----------
        x_norm : float, array of float
            The normalized position :math:`\\tilde{x}` within 0 and 1.


        """
        Xmin, Xmax = eval_(self.get_endpoints_position())
        return (position - Xmin) / (Xmax - Xmin)

    def get_diff_position_from_xnorm(self, x_norm, diff_index):
        """
        Differentiate the physical position w.r. to one parameter.

        .. math::
            \\frac{\\partial x(\\tilde{x})}{\\partial m_i} = \
                \\frac{\\partial x_{min}}{\\partial m_i} (1 - \\tilde{x}) + \
                    \\frac{\\partial x_{max}}{\\partial m_i}  \\tilde{x}

        Gives the differentiate of the physical position :math:`x` with respect to
        the optimization variable :math:`m_i` at the normalized position
        :math:`\\tilde{x}`.



        Parameters
        ----------
        x_norm : float, array of float
            The normalized position :math:`\\tilde{x}` within 0 and 1
        diff_index : int
            The index at which the designated parameters is stored in the
            `openwind.design.design_parameter.OptimizationParameters`.

        Return
        -------
        float, array of float
            The value of the differentiate at each `x_norm`
        """
        dXmin, dXmax = diff_(self.get_endpoints_position(), diff_index)
        return dXmin*(1-x_norm) + dXmax*x_norm

    def get_diff_shape_wr_x_norm(self, x_norm):
        """
        Differentiate the radius w.r. to the scaled position.

        .. math::
            \\frac{\\partial r(\\tilde{x})}{\\partial \\tilde{x}} \
        with :math:`r` the radius and :math:`\\tilde{x}` the normalized position.

        Parameters
        ----------
        x_norm : float, array of float
            The normalized position :math:`\\tilde{x}` within 0 and 1.

        Return
        ------
        float, array of float
            The derivative
        """
        raise NotImplementedError
