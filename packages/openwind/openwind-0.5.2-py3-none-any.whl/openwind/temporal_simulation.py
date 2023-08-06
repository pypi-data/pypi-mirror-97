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

"""High-level interface to run time-domain simulations."""

import warnings

from openwind import Player, InstrumentGeometry
from openwind.continuous import InstrumentPhysics
from openwind.temporal import (TemporalSolver, RecordingDevice)


def simulate(duration, *files,
             player = None,
             l_ele=None, order=None,
             nondim=False,
             temperature=None,
             losses=False,
             radiation_category='unflanged',
             convention='PH1',
             record_energy=False,
             spherical_waves=False,
             cfl_alpha=0.9, n_steps=None,
             verbosity=1,
             theta_scheme_parameter=0.25):
    """Run time-domain simulation of an instrument.

    Parameters
    ----------
    duration : float
        Duration of the simulation, in (simulated-world) seconds.
    *files : file_bore[, file_holes[, file_fingering_chart]]
        Description of the instrument.
        See also : openwind.InstrumentGeometry
    player : openwind.Player
        Description of the musician's control (embouchure and fingerings)
    l_ele, order :
        Discretization parameters.
        See openwind.discretization.mesh .
    nondim, temperature, losses, radiation_category, convention, spherical_waves :
        Model parameters.
        See openwind.continuous.instrument_physics .
    record_energy: bool
        Whether to calculate and record the energy exchanges during the simulation.
    cfl_alpha, n_steps:
        Temporal simulation parameters. See openwind.temporal.temporal_solver.TemporalSolver.run_simulation .
    verbosity: 0, 1 or 2
        0 does not print anything; 1 prints estimations of the duration
        of the simulation; 2 prints more information.
    theta_scheme_parameter:
        Parameter for reed numerical scheme openwind.temporal.treed .
    """

    if player is None:
        player = Player('IMPULSE_400us')
        warnings.warn("The default player for time simulations is used : %s" % repr(player))
    if temperature is None:
        temperature=25
        warnings.warn('The default temperature is 25 degrees Celsius.')


    instrument_geometry = InstrumentGeometry(*files)
    instru_physics = InstrumentPhysics(instrument_geometry, temperature,
                                       player, losses=losses,
                                       radiation_category=radiation_category,
                                       nondim=nondim, convention=convention,
                                       spherical_waves=spherical_waves,
                                       discontinuity_mass=False)
    t_solver = TemporalSolver(instru_physics, l_ele=l_ele, order=order,
                              cfl_alpha=cfl_alpha,
                              theta_scheme_parameter=theta_scheme_parameter)
    if verbosity>=2:
        print(t_solver)
    rec = RecordingDevice(record_energy=record_energy)
    t_solver.run_simulation(duration, callback=rec.callback,
                            enable_tracker_display=(verbosity>=1),
                            n_steps=n_steps)
    rec.stop_recording()

    return rec
