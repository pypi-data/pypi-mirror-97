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
Slice a temperature function and change its variable
"""

def slice_temperature(temperature, pos_min, pos_max):
    """
    Extract the temperature evolution allong a portion of pipe.

    Return a temperature function which verifies

    .. math::
        y(0) = T(x_{min}) \\\\
        y(1) = T(x_{max})

    with

    - \(T(x)\) : the temperature evolution with respect to the position
    - \(x_{min}, x_{max}\) the two endpoints position of the slice.

    It is used to associate a temperature evolution for each part of the
    instrument.

    Parameters
    ----------
    temperature : float or callable
        The temperature with respect to the position.
    pos_min : float
        The minimal position used for the change of variable.
    pos_max : float
        The maximal position used for the change of variable..

    Returns
    -------
    float or callable
        The sliced temperature function.

    """
    if callable(temperature):
        slice_temp = lambda x: temperature(x*(pos_max - pos_min) + pos_min)
        return slice_temp
    else:
        return temperature
