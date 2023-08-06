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

"""Record selected data during time-domain simulation."""

from collections import defaultdict

import numpy as np


class RecordingDevice:
    """Record simulation data throughout the instrument.

    The instants at which the recording is done are stored in
    `recording.ts`, and the recorded values are in
    `recording.values[label]`,
    where `label` is the name of the radiating end, for example
    `'bell_radiation_pressure'` for the bell.

    A typical use is:
    ```
    rec = simulate(...)  # Returns a RecordingDevice
    bell_pressure = rec.values['bell_radiation_pressure']
    ```
    """

    def __init__(self, record_energy=False):
        self.ts = []
        self.y = []
        self.values = defaultdict(list)
        self.dt = None
        self.record_energy = record_energy
        self._stopped = False

    def callback(self, t_solver):
        assert not self._stopped
        if not self.dt:
            self.dt = t_solver.get_dt()
            self.t_solver = t_solver
        # Recording saves values from time t = dt*(n-1/2)
        self.ts.append(t_solver.get_current_time() - self.dt/2)
        for t_comp in t_solver.t_components:
            for name, value in t_comp.get_values_to_record().items():
                self.values[t_comp.label+"_"+name].append(value)

            if self.record_energy:
                self._do_record_energies_of(t_comp)

    def _do_record_energies_of(self, t_comp):
        # Find all methods starting with 'energy'
        for attr in dir(t_comp):
            if attr.startswith('energy') and callable(getattr(t_comp, attr)):
                value = getattr(t_comp, attr)()
                short_name = attr.replace('energy', 'E')
                self.values[t_comp.label+"_"+short_name].append(value)
        q = t_comp.dissipated_last_step()
        self.values[t_comp.label+"_Q"].append(q)

    def stop_recording(self):
        """Notify the device that the simulation is over.

        Converts all recorded values to numpy arrays, so that we can
        manipulate them easily.
        """
        self._stopped = True
        self.ts = np.array(self.ts)
        for key in self.values:
            self.values[key] = np.array(self.values[key])

    def __repr__(self):
        return ("<openwind.temporal.RecordingDevice ({}, t={:.3e}); "
                "values.keys()={}>").format(
                    "running" if not self._stopped else "stopped",
                    self.ts[-1] if len(self.ts) > 0 else 0,
                    list(self.values.keys()))
