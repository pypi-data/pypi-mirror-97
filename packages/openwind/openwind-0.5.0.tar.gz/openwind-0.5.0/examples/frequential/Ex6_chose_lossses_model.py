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
How to chose the model used for the thermo-viscous losses.
The different available models and their implementations are described in
[1] Alexis Thibault, Juliette Chabassier, "Viscothermal models for wind musical instruments",
RR-9356, Inria Bordeaux Sud-Ouest (2020) https://hal.inria.fr/hal-02917351
"""

import numpy as np
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation

# %% Variable temperature

# you can apply a variable temperature by defining a function
fs = np.arange(20, 2000, 1)
geom = 'Oboe_instrument.txt'
holes = 'Oboe_holes.txt'

# all physical coefficients follow the temperature profile
# by default the losses are set to True
result = ImpedanceComputation(fs, geom, holes)

# In this case, the temperature variation is along the main axes.
# In the holes the temperature is uniform and equals the one in the main bore
# at their location.
total_length = result.get_bore().get_main_bore_length()
def grad_temp(x):
    T0 = 37
    T1 = 21
    return 37 + x*(T1 - T0)/total_length

# %% Losses

# The losses coefficient also follow the temperature profile
# Losses can be a boolean, or in {'bessel', 'wl', 'keefe', 'minifkeefe','diffrepr', 'diffrepr+'}
#        Whether/how to take into account viscothermal losses. Default is True.
#        True and bessel : Zwikker-Koster model
#        wl : Webster-Lokshin model
#        keefe and mini keefe : approximation of Zwikker-Koster for high Stokes number
#       diffrepr : diffusive representation of Zwikker-Koster
#        If 'diffrepr+', use diffusive representation with explicit
#        additional variables.
# see [1]

# choose the bell and holes radiation model
rad = 'unflanged'

losses_cats = [False,'bessel','wl','keefe','minikeefe','diffrepr','diffrepr+']
markers = ['x','o','s','+','^','v','d']

results= dict()
fig = plt.figure()
for marker, losses in zip(markers, losses_cats):
    result = ImpedanceComputation(fs, geom, holes, temperature=grad_temp,
                                    radiation_category=rad,
                                    losses=losses)
    label = f'losses={losses}'
    result.plot_impedance(figure=fig, label=label, marker=marker, markevery=200)
    results[label] = result
