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


from abc import ABC, abstractmethod
import numpy as np

class TemporalComponent(ABC):
    """Abstract class representing a component of an instrument in a temporal simulation."""

    def __init__(self, component, t_solver):
        self.label = component.label
        self._t_solver = t_solver

    def get_current_time(self):
        return self._t_solver.get_current_time()

    @abstractmethod
    def one_step(self):
        """Advance one time step."""

    @abstractmethod
    def reset_variables(self):
        """Reinitialize all variables to start the simulation over.

        Implementing classes should ensure that after a call to this method,
        the object behaves like a fresh instance
        with with same __init__ parameters.
        """

    @abstractmethod
    def energy(self):
        """Compute amount of energy currently stored in element."""

    @abstractmethod
    def dissipated_last_step(self):
        """Amount of energy dissipated by this component during the last time step."""

    @abstractmethod
    def get_maximal_dt(self):
        """Get the largest time step allowed by CFL condition."""
        return np.infty

    @abstractmethod
    def set_dt(self):
        """Set the time step of the component."""

    def get_values_to_record(self):
        """Extract the current value of data that we want to record.

        Returns
        -------
        values : Dict[str, float]
            The names and values of the data.
        """
        return {}



class TemporalComponentExit(TemporalComponent):
    """An exit is a point where we can record one pressure and one flow.

    A TemporalComponent which connects to a single pipe will
    usually be an exit, but it may connect to several
    (e.g. a possible future component "tonehole", including junction,
    chimney and radiation, would connect to two pipes, but we can
    measure the pressure/flow at the end of the chimney).


    16/01/2020: I think this method of recording is hacky and bad,
    because it entails bad object-oriented programming and shotgun surgery.
    If all we want is the flow and pressure at some PipeEnds,
    we should probably rather mark the PipeEnds that we want to record.
    -- Alexis
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_flow = None
        self._last_pressure = None
        self._last_y = None

    def remember_flow_and_pressure(self, pipe_end):
        self._last_flow = pipe_end.get_w_nph()
        self._last_pressure = pipe_end.get_q_nph()

    def remember_y(self, y):
        self._last_y = y

    def get_exit_flow(self):
        """Measure flow w^{n+1/2} at this exit."""
        assert self._last_flow is not None
        return self._last_flow

    def get_exit_pressure(self):
        """Measure pressure q^{n+1/2} at this exit."""
        assert self._last_pressure is not None
        return self._last_pressure

    def get_values_to_record(self):
        assert self._last_pressure is not None
        return {'pressure': self._last_pressure,
                'flow': self._last_flow,
                'y': self._last_y}
