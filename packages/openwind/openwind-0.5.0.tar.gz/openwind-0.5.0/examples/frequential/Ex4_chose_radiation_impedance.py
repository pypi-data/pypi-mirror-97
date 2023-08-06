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
How to chose the radiation impedance imposed at the open boundaries.
"""

import numpy as np
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation



fs = np.arange(20, 1000, 1)
temp = 25
geom = 'Geom_trumpet.txt'
holes = 'Geom_holes.txt'

fig = plt.figure()

# You can modify the model used to compute the radiation impedance by using
# the optional keyword 'radiation_category'
# In this version, this model is applied to all radiating opening: you can not
# treat separatly the holes and the "bell"

# WARNING: do not use this to open/close holes!

# %% Default
# by default the radiation category is "unflanged" corresponding to the
# radiation of a pipe with inifinite thin wall.

result = ImpedanceComputation(fs, geom, holes, temperature=temp)
result.plot_impedance(figure=fig, label='Default: unflanged')

# %% Available options
# - 'planar_piston': radiation of planar piston
# - 'unflanged': radiation of an unflanged pipe (default)
# - 'infinite_flanged': radiation of en infinite flanged pipe
# - 'pulsating_sphere': take into account the final conicity to compute the
#                       radiation of the final portion of sphere (use it with
#                       spherical waves cf. Ex6)
# - 'perfectly_open': imposed a zero pressure
# - 'total_transmission': reflection  = 0 (Zrad=Zc)
# - 'closed': perfectly close (do not use that to close hole, it close also
#    the main pipe)

rad_cats = ['planar_piston', 'unflanged', 'infinite_flanged','pulsating_sphere',
           'perfectly_open', 'total_transmission', 'closed']

for rad_cat in rad_cats:
    result = ImpedanceComputation(fs, geom, holes, temperature=temp,
                                  radiation_category=rad_cat)
    result.plot_impedance(figure=fig, label=rad_cat)
