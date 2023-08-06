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
Pipe the radius of which is defined by a spline (piecewise polynomial curve
twice differentiable).
"""

import numpy as np
import scipy.interpolate as SI

from openwind.design import DesignShape, eval_, diff_


def organize_spline_param(X, R):
    X, R = (np.array(x) for x in zip(*sorted(zip(X, R))))
    return X, R


def construct_spline_matrix(H):
    N = len(H) - 1
    ind = np.arange(N, dtype=int)
    M = np.zeros((N, N))
    M[ind, ind] = (1/3)*(H[ind] + H[ind+1])  # diagonal
    M[ind[:-1], ind[1:]] = (1/6)*H[ind[1:]]
    M[ind[1:], ind[:-1]] = (1/6)*H[ind[1:]]
    return M


def spline_coeff(x, X, R):
    H = np.diff(X)
    N = len(X) - 2  # matrix size

    M = construct_spline_matrix(H)
    dR_H = np.diff(R)/H
    F = np.diff(dR_H)
    Rsec = np.zeros(N+2)
    Rsec[1:-1] = np.linalg.solve(M, F)

    k = np.searchsorted(X, x, side='right')-1
    if k.__class__ == np.int64:  # k is different depending of x type
        k = np.array([k])
    k[k > N] = N
    A = (x - X[k])/H[k]
    B = 1 - A

    return A, B, H, Rsec, k

def spline_deriv_coeff(x, X, R, A, B, H, Rsec, k, pos_deriv):
    dR_H = np.diff(R)/H
    dH = np.zeros(H.shape)
    if pos_deriv < len(dH):
        dH[pos_deriv] = -1.0
    if pos_deriv > 0:
        dH[pos_deriv - 1] = 1.0

    M = construct_spline_matrix(H)
    dM = construct_spline_matrix(dH)
    dF = - dH[1:]/H[1:]*dR_H[1:] + dH[:-1]/H[:-1]*dR_H[:-1]
    dRsec = np.zeros(X.shape)
    dRsec[1:-1] = np.linalg.solve(M, dF - dM.dot(Rsec[1:-1]))
    # differentiation of the coefficient of the polynomial expression
    Hx = H[k]
    kj = (k == pos_deriv)
    if np.isscalar(x):
        dA = np.zeros(1)
    else:
        dA = np.zeros(x.shape)
    dA[kj] = - B[kj]/Hx[kj]
    if pos_deriv > 0:
        kj_minus = (k == (pos_deriv - 1))
        dA[kj_minus] = - A[kj_minus]/Hx[kj_minus]
    return dA, dH, dRsec


def cubicspline(x, X, R):
    """ Calculate cubicspline between x1 and x2 and passing by the knots
    defined in param by using the scipy function.

    Parameters
    ----------
    param : list
        [x_i, ..., y_i, ...]

    """
    X, R = organize_spline_param(X, R)
    spl = SI.CubicSpline(X, R)
    return spl(x)


def spline(x, X, R):
    """ Calculate cubicspline between x1 and x2 and passing by the knots
    defined in param by using a homemade function.

    Parameters
    ----------
    param : list
        [x_i, ..., y_i, ...]

    """
    X, R = organize_spline_param(X, R)
    A, B, H, Rsec, k = spline_coeff(x, X, R)
    spl = (B*R[k] + A*R[k+1] + (H[k]**2)/6*((B**3 - B)*Rsec[k] +
           (A**3 - A)*Rsec[k+1]))
    if np.isscalar(x):
        spl = float(spl)
    return spl

def diff_spline_wr_x(x, X, R):
    """ Calculate the differential of the cubicspline wr to x between x1 and x2
    and passing by the knots defined in param by using a homemade function.

    Parameters
    ----------
    param : list
        [x_i, ..., y_i, ...]

    """
    X, R = organize_spline_param(X, R)
    A, B, H, Rsec, k = spline_coeff(x, X, R)
    diff_spl = (R[k+1] - R[k])/H[k] + H[k]/6*((-3*B**2 + 1)*Rsec[k]
                                              + (3*A**2 - 1)*Rsec[k+1])
    if np.isscalar(x):
        diff_spl = float(diff_spl)
    return diff_spl

def deriv_spline_radius(x, X, R, rad_deriv):
    """Compute the derivative of the cubic spline with respect to one radius

    Parameters
    ----------
    rad_deriv: index of the radius to which is computed the derivative.
    """
    # all the radii are fixed to 0, and the position are kept similar
    new_radii = np.zeros_like(R)
    # the radius of interest is fixed to 1
    new_radii[rad_deriv] = 1
    return spline(x, X, new_radii)

def deriv_spline_position(x, X, R, pos_deriv):
    """ derivation with respect to the position X of a construction point"""
    X, R = organize_spline_param(X, R)
    # linear system to compute the second derivative
    A, B, H, Rsec, k = spline_coeff(x, X, R)
    # linear sys. to compute the variation of the second derivative
    dA, dH, dRsec = spline_deriv_coeff(x, X, R, A, B, H, Rsec, k, pos_deriv)
    Hx = H[k]
    dHx = dH[k]

    dP = (dA * (R[k + 1] - R[k]) +
          dA*Hx**2/6*(-1*(3*B**2 - 1)*Rsec[k] + (3*A**2 - 1)*Rsec[k + 1]) +
          dHx*Hx/3*((B**3 - B) * Rsec[k] + (A**3 - A) * Rsec[k + 1]) +
          (Hx**2)/6 * ((B**3 - B) * dRsec[k] + (A**3 - A) * dRsec[k + 1]))
    if np.isscalar(x):
        dP = float(dP)
    return dP


class Spline(DesignShape):
    """
    Pipe the radius of which is defined by a spline.

    A spline is a piecewise polynomial curve twice differentiable. Here the
    spline is defined by, at least, two points \( (x_1, r_1) \) and
    \( (x_2, r_2) \).

    The piecwise polynomial respect these conditions:

    - The curve passes by all the construction points of coordinates \
        \( (x_i, r_i) \)
    - The second derivative of the curve w.r. to the abscissa is continuous
    - At the two endpoints, the second derivative equals zero

    Parameters
    ----------
    *params : even number (>4) of openwind.design.design_parameter.DesignParameter
        The parameters in this order:
        \(x_1, x_2, \\ldots, x_n,  r_1, r_2, \\ldots, r_n\)

    """
    def __init__(self, *params):
        if len(params) < 4:
            raise ValueError("A spline needs at least 4 parameters.")
        if (len(params) % 2) != 0:
            raise ValueError("A spline needs an even number of parameters.")
        N = len(params)//2
        self.X = params[:N]
        self.R = params[N:]
        self.__check_x_sorted()

    def __str__(self):
        bound = '{} {} {} {} '.format(self.X[0], self.X[-1], self.R[0],
                                      self.R[-1])
        X_int = ''
        for param in self.X[1:-1]:
            X_int += '{} '.format(param)
        R_int = ''
        for param in self.R[1:-1]:
            R_int += '{} '.format(param)
        return '{bound}{class_} {X}{R}'.format(bound=bound, X=X_int, R=R_int,
                                              class_=type(self).__name__)

    def __check_x_sorted(self):
        Xval = eval_(self.X)
        if any(np.diff(Xval) <= 0):
            raise ValueError("The position of the points used to describe " +
                             "the spline must be sorted")

    def get_radius_at(self, x_norm):
        self.__check_x_sorted()
        Xval = eval_(self.X)
        Rval = eval_(self.R)
        x = self.get_position_from_xnorm(x_norm)
        self.check_bounds(x, [Xval[0], Xval[-1]])
        return spline(x, Xval, Rval)

    def get_diff_radius_at(self, x_norm, diff_index):
        self.__check_x_sorted()
        Xval = eval_(self.X)
        Rval = eval_(self.R)
        dXs = diff_(self.X, diff_index)
        dRs = diff_(self.R, diff_index)

        x = self.get_position_from_xnorm(x_norm)
        dx_norm = self.get_diff_position_from_xnorm(x_norm, diff_index)
        diff_radius = diff_spline_wr_x(x, Xval, Rval)*dx_norm
        for k, dX in enumerate(dXs):
            if dX != 0:
                diff_radius += dX * deriv_spline_position(x, Xval, Rval, k)
        for k, dR in enumerate(dRs):
            if dR != 0:
                diff_radius += dR * deriv_spline_radius(x, Xval, Rval, k)
        self.check_bounds(x, [Xval[0], Xval[-1]])
        return diff_radius

    def get_endpoints_position(self):
        return self.X[0], self.X[-1]

    def get_endpoints_radius(self):
        return self.R[0], self.R[-1]

    def get_diff_shape_wr_x_norm(self, x_norm):
        Xval = eval_(self.X)
        Rval = eval_(self.R)
        x = self.get_position_from_xnorm(x_norm)
        dx_dxnorm = (Xval[-1] - Xval[0])
        return dx_dxnorm * diff_spline_wr_x(x, Xval, Rval)
