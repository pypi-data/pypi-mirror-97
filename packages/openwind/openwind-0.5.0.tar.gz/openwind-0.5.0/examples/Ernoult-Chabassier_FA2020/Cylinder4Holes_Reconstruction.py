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
import time
import numpy as np
import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.impedance_tools import read_impedance, plot_impedance
from openwind.inversion import InverseFrequentialResponse
from openwind.inversion.display_inversion import plot_evolution_geometrie

plt.close('all')

temperature = 20
losses = True
nondim = True

l_ele = 0.05
order = 10


foldername = 'Measurements/' + 'Impedance_20degC_Cylinder4holes_'
geom_folder = 'Geometries/'
figure_folder = 'Figures/'

os.makedirs(figure_folder, exist_ok=True)

plot_evolution = True

# %% Measured geometry
common_name = 'Build_tube_Geom_'
target_geom = InstrumentGeometry(geom_folder + common_name + 'Bore_Fixed.txt',
                                 geom_folder + common_name + 'Holes_Fixed.txt',
                                 geom_folder + 'fingering_chart_Tube_4_holes_all.txt')


target_positions = np.array([.2875, .10, .13, .18, .24])
target_chimneys = np.array([17e-4, 13e-4, 15e-4, 14e-4])
target_radius = np.array([2e-3, 1.5e-3, 1.75e-3, 1.75e-3, 1.25e-3])

# %% Impedance Measurements
notes = target_geom.fingering_chart.all_notes()
notes = [notes[k] for k in [0, 1, 2, 4, 8]]

Z_measured = []
f_measured = []

for k, note in enumerate(notes):
    filename = foldername + note + '.txt'
    f_meas, Z_meas = read_impedance(filename, df_filt=None)
    Z_measured.append(Z_meas)
    f_measured.append(f_meas)

# %%  Construction of the inverse problem

# choice of the observable used in the cost function
observable = 'reflection'

# choice of the starting frequency range
frequencies = np.arange(100, 501, 20)

# Construction of the target from measured impedance
Z_target = []
for k in range(len(notes)):
    Z_target_note = np.interp(frequencies, f_measured[k], Z_measured[k])
    Z_target.append(Z_target_note)

# Initial state: all the design parameters must be variable
instru_geom = InstrumentGeometry(geom_folder + common_name + 'Bore_Length_Rad_Var.txt',
                                 geom_folder + common_name + 'Holes_Pos_Chimney_Radius_Var.txt',
                                 geom_folder + 'fingering_chart_Tube_4_holes_all.txt')

# associate physical equations to the different elements
instru_physics = InstrumentPhysics(instru_geom, temperature, Player(), losses,
                                   nondim=nondim,
                                   radiation_category='unflanged',
                                   matching_volume=True)

# Construction of the inverse problem
optim_params = instru_geom.optim_params
inverse = InverseFrequentialResponse(instru_physics, frequencies, Z_target,
                                     notes=notes, observable=observable,
                                     l_ele=l_ele, order=order)

# Index of the different design variables in the global vector
print(optim_params)
pos_index = [0, 2, 5, 8, 11]
chim_index = [3, 6, 9, 12]
rad_index = [1, 4, 7, 10, 13]

# %% Rough estimation: main bore and holes locations

t0 = time.time()
print('\nThe main bore geometry (length and radius)\n' + '_'*70)
# Only the main bore length and radius are set to active
optim_params.set_active_parameters([pos_index[0]] + [rad_index[0]])
print(optim_params)
# Only the all closed fingering is taken into account (select the right target)
inverse.set_targets_list(Z_target[0], notes[0])
# The optimization
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',
                                                     iter_detailed=True)
if plot_evolution:
    plt.close('all')
    plot_evolution_geometrie(inverse, params_evol, target_geom=target_geom,
                             double_plot=False, plot_impedance=False,
                             print_fig=True, save_name=figure_folder + '0_Main_',
                             title='Main Bore: ', linewidth=2,
                             color=[0.236, 0.667, 0.236])


print('\nLocation of Hole 4\n' + '_'*70)
# Only the location of the Hole 4 is set to active
optim_params.set_active_parameters([pos_index[4]])
print(optim_params)
# Include only the fingering 'Hole 4 open' and the corresponding impedance
inverse.set_targets_list(Z_target[1], notes[1])
# The optimization
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',
                                                     iter_detailed=True)
if plot_evolution:
    plt.close('all')
    plot_evolution_geometrie(inverse, params_evol, target_geom=target_geom,
                             double_plot=False, plot_impedance=False,
                             print_fig=True, save_name=figure_folder +'1_Hole4_', title='Hole 4: ',
                             linewidth=2, color=[0.745, .236, .236])

print('\nLocation of Hole 3\n' + '_'*70)
optim_params.set_active_parameters([pos_index[3]])
print(optim_params)
inverse.set_targets_list(Z_target[2], notes[2])
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',
                                                     iter_detailed=True)
if plot_evolution:
    plt.close('all')
    plot_evolution_geometrie(inverse, params_evol, target_geom=target_geom,
                             double_plot=False, plot_impedance=False,
                             print_fig=True, save_name=figure_folder +'2_Hole3_', title='Hole 3: ',
                             linewidth=2, color=[0.157, 0.42, 0.667])

print('\nLocation of Hole 2\n' + '_'*70)
optim_params.set_active_parameters([pos_index[2]])
print(optim_params)
inverse.set_targets_list(Z_target[3], notes[3])
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',

                                                     iter_detailed=True)
if plot_evolution:
    plt.close('all')
    plot_evolution_geometrie(inverse, params_evol, target_geom=target_geom,
                             double_plot=False, plot_impedance=False,
                             print_fig=True, save_name=figure_folder +'3_Hole2_', title='Hole 2: ',
                             linewidth=2, color=[0.745, .236, .236])

print('\nLocation of Hole 1\n' + '_'*70)
optim_params.set_active_parameters([pos_index[1]])
print(optim_params)
inverse.set_targets_list(Z_target[4], notes[4])
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',
                                                     iter_detailed=True)
if plot_evolution:
    plt.close('all')
    plot_evolution_geometrie(inverse, params_evol, target_geom=target_geom,
                             double_plot=False, plot_impedance=False,
                             print_fig=True, save_name=figure_folder +'4_Hole1_', title='Hole 1: ',
                             linewidth=2, color=[0.157, 0.42, 0.667])

t1 = time.time()
total = t1-t0

print('\n' + '='*70 + '\n' + '='*70)
print('Rough estimation results:')
print('- Computation Time: {:.2f} sec.'.format(total))
pos_dev = np.abs(np.asarray(optim_params.get_geometric_values())[pos_index] - target_positions)
print('- The absolute error on the position are (in mm)\n {}'.format(pos_dev*1e3))
print('='*70 + '\n' + '='*70 + '\n')


# %% Refining

# change the frequency range
frequencies = np.arange(100, 3001, 100)
inverse.set_frequencies(frequencies)

# redefine the targets from measurements with this new frequency range
Z_target = []
for k in range(len(notes)):
    Z_target_note = np.interp(frequencies, f_measured[k], Z_measured[k])
    Z_target.append(Z_target_note)

t0 = time.time()

print('\nSecond step: all parameters few frequencies\n' + '_'*70)
# all the design variables are set active
optim_params.set_active_parameters('all')
print(optim_params)
# all the note and the impedance are included
inverse.set_targets_list(Z_target, notes)
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',
                                                     iter_detailed=True)

t1 = time.time()
total = t1-t0

if plot_evolution:
    plt.close('all')
    plot_evolution_geometrie(inverse, params_evol, target_geom=target_geom,
                             double_plot=False, plot_impedance=False,
                             print_fig=True, save_name=figure_folder +'5_total_', title='Total: ',
                             linewidth=3, color=[0.236, 0.667, 0.236])

final_pos = np.asarray(optim_params.get_geometric_values())[pos_index]
final_chim = np.asarray(optim_params.get_geometric_values())[chim_index]
final_rad = np.asarray(optim_params.get_geometric_values())[rad_index]

pos_dev = np.abs(final_pos - target_positions)
chem_dev = np.abs(final_chim - target_chimneys)
rad_dev = np.abs(final_rad - target_radius)

print('\n' + '='*70 + '\n' + '='*70)
print('Refining results:')
print('- Computation Time: {:.2f} sec.'.format(total))
print('- The geometrie \n\t+Positions: {} \n\t+Chimneys: {} '
      '\n\t+Diameters: {}'.format(final_pos*1e3, final_chim*1e3,
                                  final_rad*2e3))
print('- The absolute error on the locations (in mm):\n{}'.format(pos_dev*1e3))
print('- The absolute error on the chimneys (in mm):\n{}'.format(chem_dev*1e3))
print('- The absolute error on the radii (in mm):\n{}'.format(rad_dev*1e3))
print('='*70 + '\n' + '='*70 + '\n')

# np.save('Params_reconstruct_new_geom_3_param', params_evol)
# np.save('Cost_reconstruct_new_geom_3_param', cost_evol)


# %% Final refingin

# more frequencies included
frequencies = np.arange(100, 3001, 10)
inverse.set_frequencies(frequencies)

# update targets
Z_target = []
for k in range(len(notes)):
    Z_target_note = np.interp(frequencies, f_measured[k], Z_measured[k])
    Z_target.append(Z_target_note)

print('\nComplete\n' + '_'*70)
optim_params.set_active_parameters('all')
inverse.set_targets_list(Z_target, notes)

t0 = time.time()
params_evol, cost_evol = inverse.optimize_freq_model(algorithm='LM',
                                                     iter_detailed=True)
t1 = time.time()
total = t1-t0

final_pos = np.asarray(optim_params.get_geometric_values())[pos_index]
final_chim = np.asarray(optim_params.get_geometric_values())[chim_index]
final_rad = np.asarray(optim_params.get_geometric_values())[rad_index]

pos_dev = np.abs(final_pos - target_positions)
chem_dev = np.abs(final_chim - target_chimneys)
rad_dev = np.abs(final_rad - target_radius)

print('\n' + '='*70 + '\n' + '='*70)
print('Final results with a lot of frequencies:')
print('- Computation Time: {:.2f} sec.'.format(total))
print('- The geometrie \n\t+Positions: {} \n\t+Chimneys: {} '
      '\n\t+Diameters: {}'.format(final_pos*1e3, final_chim*1e3,
                                  final_rad*2e3))
print('- The absolute error on the locations (in mm):\n{}'.format(pos_dev*1e3))
print('- The absolute error on the chimneys (in mm):\n{}'.format(chem_dev*1e3))
print('- The absolute error on the radii (in mm):\n{}'.format(rad_dev*1e3))
print('='*70 + '\n' + '='*70 + '\n')
