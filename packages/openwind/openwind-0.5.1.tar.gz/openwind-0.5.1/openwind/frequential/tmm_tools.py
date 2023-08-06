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


def compute_beta_S(R0,R1,lcur,sph):
    if sph in [True]:
        DR = R1 - R0
        beta = DR / R0 * (lcur ** 2 + DR ** 2) ** (-1 / 2)
        S = np.pi * R0 ** 2
    elif sph in ['spherical_tmm']:
        DR = R1 - R0
        beta = DR / R0 * (lcur ** 2 + DR ** 2) ** (-1 / 2)
        h = DR * R0 / ((lcur ** 2 + DR ** 2) ** (1 / 2) + lcur)
        S = np.pi * (R0 ** 2 + h ** 2)
    else:
        beta = (R1 - R0) / lcur / R0
        S = np.pi * R0 ** 2
    return beta, S

def cone_lossy(physics, lpart, R0, R1, omegas, nbSub=1, sph=False, loss_type='bessel'):
    assert physics.uniform # constant temperature only

    Rbeg = R0
    Rend = R1
    if Rbeg == Rend:  # test cylindrique
        subPart = 1
    else:
        subPart = nbSub
    lcur = lpart / subPart
    for i in range(subPart):
        R0 = Rend + (Rbeg - Rend) * (lpart - i * lcur) / lpart
        R1 = Rend + (Rbeg - Rend) * (lpart - (i + 1) * lcur) / lpart

        L = np.sqrt(lcur ** 2 + (R0 - R1) ** 2)
        beta, S = compute_beta_S(R0,R1,lcur,sph)
        Zc = physics.rho(0) * physics.c(0) / S

        # Rmoy = (R0 + R1) / 2  # half
        # Rmoy = (2 * R0 + R1) / 3  # first third, better according to Jean-Pierre Dalmont
        rmoy = (2 * min(R0, R1) + max(R0, R1)) / 3  # adapted to converging and diverging pipes

        # TODO(Augustin) Better formula for rmoy

        Zv, Yt = zv_yt_TMM(rmoy, S, omegas, physics, loss_type)
        Gamma = np.sqrt(Zv * Yt)
        Zcc = np.sqrt(Zv / Yt)
        if sph:
            length = L
        else:
            length = lcur
        A = R1 / R0 * np.cosh(Gamma * length) - \
            beta / Gamma * np.sinh(Gamma * length)
        B = R0 / R1 * Zcc * np.sinh(Gamma * length)
        C = 1 / Zcc * ((R1 / R0 - beta ** 2 / Gamma ** 2) *
                       np.sinh(Gamma * length) + length * beta ** 2 /
                       Gamma * np.cosh(Gamma * length))
        D = R0 / R1 * (np.cosh(Gamma * length) + (beta / Gamma) *
                       np.sinh(Gamma * length))

        matrixLocal = A, B, C, D
        if i == 0:
            mat = matrixLocal
        else:
            mat = multmat(mat, matrixLocal)
    return mat


def cone_lossless(physics, lpart, R0, R1, omegas, sph=False):
    assert physics.uniform # constant temperature only
    ks = omegas/physics.c(0)
    L = np.sqrt(lpart ** 2 + (R0 - R1) ** 2)
    beta, S = compute_beta_S(R0,R1,lpart,sph)

    if sph:
        length = L
    else:
        length = lpart

    Zc = physics.rho(0) * physics.c(0) / S
    A = R1 / R0 * np.cos(ks * length) - beta / ks * np.sin(ks * length)
    B = R0 / R1 * 1j * Zc * np.sin(ks * length)
    C = 1j / Zc * ((R1 / R0 + beta ** 2 / ks ** 2) * np.sin(ks * length) -
                   length * beta ** 2 / ks * np.cos(ks * length))
    D = R0 / R1 * (np.cos(ks * length) + (beta / ks) * np.sin(ks * length))
    return A, B, C, D


# def multmat(mguide, matrix):
#     N = int(mguide.shape[0] / 4)
#     A = mguide[0:N] * matrix[0:N] + \
#         mguide[N:2 * N] * matrix[2 * N:3 * N]
#     B = mguide[0:N] * matrix[N:2 * N] + \
#         mguide[N:2 * N] * matrix[3 * N:4 * N]
#     C = mguide[2 * N:3 * N] * matrix[0:N] + \
#         mguide[3 * N:4 * N] * matrix[2 * N:3 * N]
#     D = mguide[2 * N:3 * N] * matrix[N:2 * N] + \
#         mguide[3 * N:4 * N] * matrix[3 * N:4 * N]
#     return np.concatenate([A, B, C, D])

def multmat(mguide, matrix):
    A1, B1, C1, D1 = mguide
    A2, B2, C2, D2 = matrix
    A = A1*A2 + B1*C2
    B = A1*B2 + B1*D2
    C = C1*A2 + D1*C2
    D = C1*B2 + D1*D2
    return A, B, C, D

def impedance(mguide, Zr):
    N = int(mguide.shape[0] / 4)
    return (mguide[0:N] * Zr +
            mguide[N:2 * N]) / (mguide[2 * N:3 * N] * Zr + mguide[3 * N:4 * N])

def zv_yt_TMM(rmoy, S, omega, physics, loss_type):
    rv = rmoy * np.sqrt(physics.rho(0) * omega / physics.mu(0))
    rt = rmoy * np.sqrt(omega * physics.rho(0) * physics.Cp / physics.kappa(0))
    if loss_type in ['bessel']:
        kvr = rv / np.sqrt(1j)
        ktr = rt / np.sqrt(1j)
        #    jv = 2 * sp.jve(1, kvr) / (kvr * sp.jve(0, kvr))
        Zv = (1j * omega * physics.rho(0) / S) * (1 / ( 1 - 2 * sp.jve(1, kvr) / (kvr * sp.jve(0, kvr))))
        #    jt = 2 * sp.jve(1, ktr) / (ktr * sp.jve(0, ktr))
        Yt = 1j * omega * S / (physics.rho(0) * physics.c(0)**2) * (1 + (physics.gamma - 1) * 2 * sp.jve(1, ktr) / (ktr * sp.jve(0, ktr)))
    elif loss_type in ['keefe']:
        Zv = (1j * omega * physics.rho(0) / S) * (1 + 2*np.sqrt(-1j)/rv - 3*1j/(rv**2))
        Yt = 1j * omega * S / (physics.rho(0) * physics.c(0)**2) * (1 + (physics.gamma - 1)*(2*np.sqrt(-1j)/rt + 1j/(rt**2)))
    elif loss_type in ['minikeefe']:
        Zv = (1j * omega * physics.rho(0) / S) * (1 + 2*np.sqrt(-1j)/rv )
        Yt = 1j * omega * S / (physics.rho(0) * physics.c(0)**2) * (1 + (physics.gamma - 1)*(2*np.sqrt(-1j)/rt ))
    return Zv, Yt
