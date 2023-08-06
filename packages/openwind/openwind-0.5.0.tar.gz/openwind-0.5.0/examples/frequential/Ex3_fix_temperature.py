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
How to fix the temperature.
"""

import numpy as np
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation

fs = np.arange(20, 2000, 1)
geom = 'Geom_trumpet.txt'
holes = 'Geom_holes.txt'
# %% Default computation

# by default the temperature is 25°C
result = ImpedanceComputation(fs, geom, holes)
result.plot_instrument()

fig = plt.figure()
result.plot_impedance(figure=fig, label='Default Temp.: 25°C')

# %% if you want you can also fix a uniform temperature
result_30 = ImpedanceComputation(fs, geom, holes, temperature=30)
result_30.plot_impedance(figure=fig, label='30°C')

# %% you can also apply a variable temperature by defining a function

# In this case, the temperature variation is along the main axes.
# In the holes the temperature is uniform and equals the one in the main bore
# at their location.
total_length = result.get_bore().get_main_bore_length()
def grad_temp(x):
    T0 = 37
    T1 = 21
    return 37 + x*(T1 - T0)/total_length
result_var = ImpedanceComputation(fs, geom, holes, temperature=grad_temp)
result_var.plot_impedance(figure=fig, label='Variable Temp.')
