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

#--------------------------
def impedance(Z):
    return Z

def diff_impedance_wrZ(Z):
    diff_obs = 1
    diff_conj_obs = 0
    return diff_obs, diff_conj_obs

# -----------------------------------
def module_square(Z):
    return np.abs(Z)**2

def diff_module_square_wrZ(Z):
    """ return the derivative of the observation w.r. to Z, and the derivative
    of the CONJUGATE of the observation w.r. to Z.
    Warnings! it is a derivation wr to a complex vector: \
                  d/dZ = (d/d(real(Z)) -j*d/d(imag(Z)))/2
    """
    diff_obs = Z.conj().T
    diff_conj_obs = diff_obs
    return diff_obs, diff_conj_obs

# -----------------------------------
def reflection(Z):
    return (Z - 1)/(Z + 1)

def diff_reflection_wrZ(Z):
    """
    return the derivative of the observation w.r. to Z, and the derivative
    of the CONJUGATE of the observation w.r. to Z.
    Warnings! it is a derivation wr to a complex vector: \
                  d/dZ = (d/d(real(Z)) -j*d/d(imag(Z)))/2
    """
    diff_obs = 2/(Z + 1)**2
    diff_conj_obs = 0
    return diff_obs, diff_conj_obs

# ------------------------
def impedance_phase(Z):
    return np.angle(Z)

def diff_impedance_phase_wrZ(Z):
    diff_obs = -1j * Z.conjugate() / (2 * np.abs(Z)**2)
    diff_conj_obs = diff_obs
    return diff_obs, diff_conj_obs

# --------------------------
def reflection_phase(Z):
    return (np.angle(reflection(Z)))

def diff_reflection_phase_wrZ(Z):
    diff_R_wrZ, _ = diff_reflection_wrZ(Z)
    diff_obs_wrR, diff_conj_obs_wrR = diff_impedance_phase_wrZ(reflection(Z))
    return diff_obs_wrR*diff_R_wrZ, diff_conj_obs_wrR*diff_R_wrZ

# --------------------------
def reflection_modulus_square(Z):
    return np.abs(reflection(Z))**2

def diff_reflection_modulus_square_wrZ(Z):
    diff_R_wrZ, _ = diff_reflection_wrZ(Z)
    diff_obs_wrR, diff_conj_obs_wrR = diff_module_square_wrZ(reflection(Z))
    return diff_obs_wrR*diff_R_wrZ, diff_conj_obs_wrR*diff_R_wrZ
