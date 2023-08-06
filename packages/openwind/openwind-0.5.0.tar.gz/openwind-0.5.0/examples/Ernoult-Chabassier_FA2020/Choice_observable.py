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
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.impedance_tools import read_impedance, plot_impedance
from openwind.inversion import InverseFrequentialResponse
from openwind.inversion import observation

font = {'family' : 'serif',
        'size'   : 14}
matplotlib.rc('font', **font)
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

# %% Measured geometry
common_name = 'Build_tube_Geom_'

instru_geom = InstrumentGeometry(geom_folder + common_name + 'Bore_Sensitivities.txt',
                         geom_folder + common_name + 'Holes_Sensitivities.txt',
                         geom_folder + 'fingering_chart_Tube_4_holes.txt')
optim_params = instru_geom.optim_params
notes = instru_geom.fingering_chart.all_notes()

# frequencies = np.arange(100, 3001, 290)
frequencies = np.arange(100, 501, 20)

# %% chose what to observe
index_param = 4 # chose between [0, 1, 2, 3, 4]

# only this parameters is can now be changed, all the other are fixed
optim_params.set_active_parameters(index_param)
param_label = np.array(optim_params.labels)[optim_params.active][0]
target_geom = optim_params.get_active_values()[0]
print("The studied parameters is '{}'".format(param_label))
print("Its measured geometric value is {:.2f}mm".format(target_geom*1000))

n_values = 50

if param_label == 'bore_0_pos_plus':  # Main Bore length
    notes = [notes[0]]
    values = np.linspace(0.241, 0.5, n_values).tolist()
elif param_label == 'bore_0_radius_plus':  # Main Bore radius
    notes = [notes[0]]
    values = np.linspace(1.65e-3, 4e-3, n_values).tolist()
elif param_label == 'hole1_position':
    notes = [notes[4]]
    values = np.linspace(0.01, 0.129, n_values).tolist()
elif param_label == 'hole1_chimney':
    notes = [notes[4]]
    values = np.linspace(1e-5, 4e-3, n_values).tolist()
elif param_label == 'hole1_radius':
    notes = [notes[4]]
    values = np.linspace(1e-5, 2e-3, n_values).tolist()

print("The considered fingering is '{}'".format(notes[0]))

figure_name = (param_label
               + '_{:}_{:.0f}_{:}'.format(min(frequencies),
                                          np.mean(np.diff(frequencies)),
                                          max(frequencies))
               + '.pdf')
# %% Instanciate the inverse problem
Z_target = []
for k, note in enumerate(notes): #
    filename = foldername +  note + '.txt'
    f_measured, Z_measured = read_impedance(filename, df_filt=None)
    Z_target_note = np.interp(frequencies, f_measured, Z_measured)
    Z_target.append(Z_target_note)

instru_physics = InstrumentPhysics(instru_geom, temperature, Player(), losses,
                        nondim=nondim, radiation_category='unflanged')
inverse = InverseFrequentialResponse(instru_physics, frequencies,
                                  Z_target, notes=notes,
                                  observable='impedance', l_ele=l_ele, order=order)

# %% The main loop which computes the different costs at each values
impedance = np.zeros(len(values), dtype=float)
impedance_modulus =  np.zeros(len(values), dtype=float)
impedance_phase =  np.zeros(len(values), dtype=float)
reflection =  np.zeros(len(values), dtype=float)
reflection_modulus =  np.zeros(len(values), dtype=float)
reflection_phase =  np.zeros(len(values), dtype=float)
reflection_phase_unwraped =  np.zeros(len(values), dtype=float)

grad_impedance = np.zeros(len(values), dtype=float)
grad_impedance_modulus =  np.zeros(len(values), dtype=float)
grad_impedance_phase =  np.zeros(len(values), dtype=float)
grad_reflection =  np.zeros(len(values), dtype=float)
grad_reflection_modulus =  np.zeros(len(values), dtype=float)
grad_reflection_phase =  np.zeros(len(values), dtype=float)
grad_reflection_phase_unwraped =  np.zeros(len(values), dtype=float)

for k, length in enumerate(values):
    print('Value {}/{}'.format(k+1, len(values)))
    inverse.set_observation('impedance')
    inverse.set_targets_list(Z_target, notes)
    impedance[k], grad_impedance[k], _ = inverse.get_cost_grad_hessian([length], grad_type='adjoint')

    inverse.set_observation('impedance_modulus')
    inverse.set_targets_list(Z_target, notes)
    impedance_modulus[k], grad_impedance_modulus[k], _  = inverse.get_cost_grad_hessian(grad_type='adjoint')

    inverse.set_observation('impedance_phase')
    inverse.set_targets_list(Z_target, notes)
    impedance_phase[k], grad_impedance_phase[k], _  = inverse.get_cost_grad_hessian(grad_type='adjoint')

    inverse.set_observation('reflection')
    inverse.set_targets_list(Z_target, notes)
    reflection[k], grad_reflection[k], _  = inverse.get_cost_grad_hessian(grad_type='adjoint')

    inverse.set_observation('reflection_modulus')
    inverse.set_targets_list(Z_target, notes)
    reflection_modulus[k], grad_reflection_modulus[k], _  = inverse.get_cost_grad_hessian(grad_type='adjoint')

    inverse.set_observation('reflection_phase')
    inverse.set_targets_list(Z_target, notes)
    reflection_phase[k], grad_reflection_phase[k], _  = inverse.get_cost_grad_hessian(grad_type='adjoint')

    inverse.set_observation('reflection_phase_unwraped')
    inverse.set_targets_list(Z_target, notes)
    reflection_phase_unwraped[k], grad_reflection_phase_unwraped[k], _  = inverse.get_cost_grad_hessian(grad_type='adjoint')


# %% the plot

plt.figure()

plt.semilogy(np.asarray(values)/target_geom, impedance, label='Impedance')
plt.semilogy(np.asarray(values)/target_geom, impedance_modulus, label='Impedance Modulus')
plt.semilogy(np.asarray(values)/target_geom, impedance_phase, label='Impedance Phase')
plt.semilogy(np.asarray(values)/target_geom, reflection, label='Reflection')
plt.semilogy(np.asarray(values)/target_geom, reflection_modulus, label='Reflection Modulus' )
plt.semilogy(np.asarray(values)/target_geom, reflection_phase, label='Reflection Phase')
plt.semilogy(np.asarray(values)/target_geom, reflection_phase_unwraped, label='Reflection Unwrap')
plt.grid(True)
plt.legend()
plt.xlabel('Relative position variation')
plt.ylabel('Cost')

plt.savefig(figure_folder + 'Cost_' + figure_name)


plt.figure()

plt.plot(np.asarray(values)/target_geom, grad_impedance, label='Impedance')
plt.plot(np.asarray(values)/target_geom, grad_impedance_modulus, label='Impedance Modulus')
plt.plot(np.asarray(values)/target_geom, grad_impedance_phase, label='Impedance Phase')
plt.plot(np.asarray(values)/target_geom, grad_reflection, label='Reflection')
plt.plot(np.asarray(values)/target_geom, grad_reflection_modulus, label='Reflection Modulus' )
# plt.plot(np.asarray(values), grad_reflection_phase, label='Reflection Phase')
# plt.plot(np.asarray(values), grad_reflection_phase_unwraped, label='Reflection Unwrap')
plt.legend()
plt.grid(True)
plt.xlabel('Relative position variation')
plt.ylabel('Grad')
plt.ylim(((-50,50)))
plt.savefig(figure_folder + 'Gradients_' + figure_name)
