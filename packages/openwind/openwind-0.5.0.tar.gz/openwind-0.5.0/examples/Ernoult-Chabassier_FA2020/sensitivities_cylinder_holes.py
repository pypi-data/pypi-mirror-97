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
This example is linked to the article:
    Ernoult, Chabassier, "Bore Reconstruction of Woodwind Instruments Using
    the Full Waveform Inversion", e-Forum Acusticum 2020, Lyon
"""


import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.impedance_tools import read_impedance, plot_impedance
from openwind.inversion import InverseFrequentialResponse


font = {'family' : 'serif',
        'size'   : 14}
matplotlib.rc('font', **font)


plt.close('all')

frequencies = np.arange(100, 200, 10)

temperature = 20
losses = True
nondim = True
player = Player()

l_ele = 0.05
order = 10

foldername = 'Measurements/' + 'Impedance_20degC_Cylinder4holes_'
geom_folder = 'Geometries/'
figure_folder = 'Figures/'
os.makedirs(figure_folder, exist_ok=True)
# %% The geometry
common_name = 'Build_tube_Geom_'

# the sensitivity can be computed only on "variable" parameters.
# we load geometry files in which all the parameters are variable
instru_geom = InstrumentGeometry(geom_folder + common_name + 'Bore_Sensitivities.txt',
                          geom_folder + common_name + 'Holes_Sensitivities.txt',
                          geom_folder + 'fingering_chart_Tube_4_holes_all.txt')

notes = instru_geom.fingering_chart.all_notes()

fig_bore = plt.figure()
instru_geom.plot_InstrumentGeometry(figure=fig_bore)

instru_physics = InstrumentPhysics(instru_geom, temperature=temperature,
                                   player=player, losses=losses,
                        nondim=nondim, radiation_category='unflanged')

# %% Construction of the 'Inversion' Problem

# we chose the observable for which we would like to compute the sensitivities
observable = 'reflection'

# the sensitivity is independent on the targets: we defined them arbitrary
Z_target = [np.ones_like(frequencies) for k in notes]
optim_params = instru_geom.optim_params

inverse = InverseFrequentialResponse(instru_physics, frequencies,  Z_target,
                                     notes=notes, observable=observable,
                                     l_ele=l_ele, order=order)

# %% The sensitivity computation

pos_index = [1, 2, 5, 8, 11]
chim_index = [3, 6, 9, 12]
rad_index = [0, 4, 7, 10, 13]

# First of all we would like to compute the sensitivity with respect to
# chimney only

# 1-we activate only these parameters in the OptimizationParameters
optim_params.set_active_parameters(chim_index)

# 2-we compute the sensitivity
sensitivities_chimney, _ = inverse.compute_sensitivity_observable()

# 3- we plot the result we some options
fig_chim, ax_chim = inverse.plot_sensitivities(logscale=True, relative=True,
                                               vmin=-5,  text_on_map=False)
fig_chim.set_figwidth(2.5*fig_chim.get_figwidth())
ax_chim.set_yticklabels(['Hole 1 chimney', 'Hole 2 chimney', 'Hole 3 chimney',
                         'Hole 4 chimney'])
ax_chim.set_xlabel('Fingering')


# Idem for the radii
optim_params.set_active_parameters(rad_index)
sensitivities_radii, _ = inverse.compute_sensitivity_observable()
fig_rad, ax_rad = inverse.plot_sensitivities(logscale=True, relative=True,
                                             param_order=[1,2,3,4,0],
                                             text_on_map=True, vmax=-1, vmin=-5)
fig_rad.set_figwidth(2.5*fig_rad.get_figwidth())
ax_rad.set_yticklabels(['Hole 1 radius', 'Hole 2 radius', 'Hole 3 radius',
                         'Hole 4 radius', 'Right end radius'])
ax_rad.set_xlabel('Fingering')

# and the locations
optim_params.set_active_parameters(pos_index)
sensitivities_positions, _ = inverse.compute_sensitivity_observable()
fig_sens, ax_sens = inverse.plot_sensitivities(logscale=True, relative=True,
                                               vmin=-4,  param_order=[1,2,3,4,0],
                                               text_on_map=False)
# over plot the fingering chart
instru_geom.fingering_chart.plot_chart(figure=fig_sens, markersize=22,
                                       fillstyle='none', color='w',
                                       open_only=False, markeredgewidth=3)


fig_sens.set_figwidth(2.5*fig_sens.get_figwidth())
ax_sens.set_yticklabels(['Hole 1 location', 'Hole 2 location',
                         'Hole 3 location', 'Hole 4 location',
                         'Main bore length'])
ax_sens.set_xlabel('Fingering')
fig_sens.savefig(figure_folder + 'Sensitivity_reflection.pdf')

#%%
# optim_params.set_active_parameters(pos_index[1:])
# sensitivities_positions, gradient_observation = inverse.compute_sensitivity_observable(interp=True, interp_grid=0.01)

# labels = np.array(optim_params.labels)[optim_params.active].tolist()
# ind_example = -3

# inverse.set_note(notes[ind_example])
# inverse.solve()
# fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
# ax[0].plot(frequencies, np.log10(np.abs(inverse.imped)))
# for k in range(len(labels)):
#     ax[1].plot(frequencies, np.log10(np.abs(gradient_observation[ind_example][:, k])))
# ax[1].legend(labels)
# fig.suptitle(notes[ind_example])

# inverse.plot_grad_acoustics_field([notes[ind_example]], var='pressure')
