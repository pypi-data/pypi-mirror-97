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
Module for TemporalSolver class.
"""

from openwind.continuous import (ThermoviscousLossless,
                                 ThermoviscousDiffusiveRepresentation,
                                 RadiationPade,
                                 PhysicalRadiation,
                                 JunctionTjoint, JunctionSimple,
                                 Valve, Flow,
                                 RadiationPerfectlyOpen
                                 )
from openwind.temporal import (TemporalPipe, TemporalRadiation,
                               TemporalJunction, TemporalLossyPipe,
                               TemporalSimpleJunction,
                               TemporalFlowCondition,
                               TemporalValve,
                               TemporalPressureCondition
                               )
from openwind.temporal import ExecuteScore
from openwind.tracker import SimulationTracker
import numpy as np
import pdb

class TemporalSolver:
    """Prepare an instrument for simulation in time domain.

    This class is responsible for converting a continuous instrument model
    (openwind.continuous.InstrumentPhysics) to objects that can run the
    numerical schemes, and for running said scheme.

    Parameters
    ----------
    instru_physics : openwind.continuous.instrument_physics.IntrumentPhysics
        Description of the instrument.
    cfl_alpha: float
        `dt` will be set to `cfl_alpha * dt_max` or slightly lower.
    **discr_params :
        Discretization parameters. See openwind.discretization.mesh .
    """

    def __init__(self, instru_physics,
                 cfl_alpha=0.9,
                 theta_scheme_parameter=0.25,
                 **discr_params):
        assert 0 < cfl_alpha <= 1, "cfl_alpha must be between 0 and 1"

        self.instru_physics = instru_physics
        self.discr_params = discr_params
        self.theta_scheme_parameter = theta_scheme_parameter
        self._dt = None
        self.__convert_temporal_components()
        self.__compute_dt(cfl_alpha)

        fingering_chart = instru_physics.instrument_geometry.fingering_chart
        self._execute_score = ExecuteScore(fingering_chart,  self.t_components)
        self._current_time = 0.0
        self.energy_check = None

        self.tracker = None

    def __repr__(self):
        return ("<openwind.temporal.TemporalSolver:("
                #"\nTemporalSolver(instr_physics, cfl_alpha, theta_scheme_parameter, **discr_params)\n\n" +
                "\n{},".format(repr(self.instru_physics)) +
                "\ndt={},".format(self.get_dt()) +
                "\ntheta_scheme_parameter={},".format(repr(self.theta_scheme_parameter)) +
                # "\ndisc_params={},".format(repr(self.discr_params)) +
                "\nmesh_info:{{{}pipes, elements/pipe:{}, "
                "order/element:{}}}\n)>".format(len(self.t_pipes),
                                                self.get_elements_mesh(),
                                                self.get_orders_mesh()))

    def __str__(self):
        return ("TemporalSolver:\n" + "="*20 +
                "\nInstrument Physics:\n{}\n".format(self.instru_physics.netlist) +"-"*20 +
                "\n{}\n".format(self.instru_physics.player) +"-"*20 +
                "\nTemperature: {}°C\n".format(self.instru_physics.temperature) +"="*20 +
                "\nTheta scheme parameter: {}\n".format(self.theta_scheme_parameter) + "="*20 +
                "\nTime step: {}\n".format(self.get_dt()) + "="*20 +
                "\n" + self.__get_mesh_info())

    def __convert_temporal_components(self):
        netlist = self.instru_physics.netlist
        self.t_pipes, self.t_connectors = \
            netlist.convert_with_structure(self._convert_pipe,
                                           self._convert_connector)
        self.t_components = self.t_connectors + self.t_pipes


    def _convert_pipe(self, pipe):
        """
        Construct an appropriate instance of (a subclass of) TemporalPipe.

        Parameters
        ----------
        pipe : openwind.continuous.Pipe
            Continuous model of the pipe.
        **discr_params : keyword arguments
            Discretization parameters, passed to the TPipe initializer.

        Returns
        -------
        openwind.temporal.TemporalPipe.

        """
        losses = pipe.get_losses()
        if isinstance(losses, ThermoviscousDiffusiveRepresentation):
            return TemporalLossyPipe(pipe, t_solver=self, **self.discr_params)
        if isinstance(losses, ThermoviscousLossless):
            return TemporalPipe(pipe, t_solver=self, **self.discr_params)
        raise ValueError("Temporal computation only supports "
                          "losses = {False, 'diffrepr'}.")


    def _convert_connector(self, connector, ends):
        """
        Construct the appropriate temporal version of a component.

        Parameters
        ----------
        component : openwind.continuous.NetlistComponent
            Continuous model for radiation, junction, or source.
        ends : List[TPipe.End]
            The list of all `TPipe.End`s this component connects to.

        Returns
        -------
        openwind.temporal.TemporalComponent.

        """

        if isinstance(connector, PhysicalRadiation):
            radiation_model = connector.model
            if isinstance(radiation_model, RadiationPerfectlyOpen):
                return TemporalPressureCondition(connector, ends,
                                                 t_solver=self)
            elif isinstance(radiation_model, RadiationPade):
                return TemporalRadiation(connector, ends,
                                         t_solver=self)
            else:
                raise ValueError("Radiation models usable in temporal are"
                                 " RadiationPerfectlyOpen or"
                                 " RadiationPade.")

        if isinstance(connector, JunctionTjoint):
            return TemporalJunction(connector, ends, t_solver=self)

        if isinstance(connector, JunctionSimple):
            return TemporalSimpleJunction(connector, ends,
                                          t_solver=self)
        if isinstance(connector, Valve):
            return TemporalValve(connector, ends, t_solver=self,
                                theta=self.theta_scheme_parameter)
        if isinstance(connector, Flow):
            return TemporalFlowCondition(connector, ends, t_solver=self)
        raise ValueError("Could not convert %s" % str(connector))



    def __compute_dt(self, cfl_alpha):
        self.cfl_of_components = [(t_comp.label, t_comp.get_maximal_dt())
                                  for t_comp in self.t_components]
        self.cfl_of_components = sorted(self.cfl_of_components,
                                        key=lambda x: x[1])
        _, cfl = self.cfl_of_components[0]
        self._set_dt(cfl_alpha * cfl)

    def _set_dt(self, dt):
        """Change the value of time step dt."""
        self._dt = dt
        for t_pipe in self.t_pipes:
            t_pipe.set_dt(self._dt)
        for t_connector in self.t_connectors:
            t_connector.set_dt(self._dt)

    def get_dt(self):
        """Time step duration."""
        return self._dt

    def reset(self):
        """Reset the simulation."""
        for t_component in self.t_components:
            t_component.reset_variables()
        self._current_time = 0.0

    def get_current_time(self):
        """Current in-simulation physical time in seconds."""
        return self._current_time

    def one_step(self, check_scheme=False):
        """Perform one time step of the numerical scheme.

        See also
        --------
        run_simulation
        """
        # We consider that during the update, current time is (n+1/2)*dt.
        self._current_time += self._dt/2

        self._execute_score.set_fingering(self._current_time)

        # Update connectors first, and pipes afterwards
        for t_connector in self.t_connectors:
            t_connector.one_step()
        for t_pipe in self.t_pipes:
            t_pipe.one_step(check_scheme)

        self._current_time += self._dt/2

    def energy(self):
        """Calculate total numerical energy stored in instrument."""
        return sum(t_comp.energy() for t_comp in self.t_components)

    def dissipated_last_step(self):
        """Calculate total numerical energy dissipated during last step."""
        return sum(t_comp.dissipated_last_step() for t_comp
                   in self.t_components)

    def run_simulation(self, duration,
                       callback=None,
                       enable_tracker_display=True,
                       energy_check=False,
                       n_steps=None):
        """Run the simulation for a given duration.

        Calculates the number of steps needed, changes dt accordingly,
        and runs the simulation.

        .. warning::
            May reset the variables of the t_components.

        Parameters
        ----------
        duration : float
            Duration of the simulation.
            Final time should be `duration` up to numerical error.
        callback : callable, optional
            A function to call after each step, taking this TemporalSolver
            as an argument.
        enable_tracker_display : bool, optional
            Whether to enable printing information on percentage of progression
            and remaining time. Default is `True`. See openwind.tracker .
        energy_check : bool, optional
            Whether to check that the scheme is energy-consistent. More costly.
            See EnergyCheck.
        n_steps : int, optional
            If given, forces the simulation to run in exactly `n_steps` steps.
            Fails if that contradicts stability.

        See also
        --------
        run_simulation_steps:
            To run for a given number of steps instead.
        """
        self._execute_score.set_score(self.instru_physics.player.get_score())
        #pdb.set_trace()
        n_steps_needed = int(np.ceil(duration / self._dt))
        if n_steps is not None:
            print("Custom number of steps:", n_steps)
            if n_steps < n_steps_needed:
                print("WARNING: not enough steps for CFL. Changing to", n_steps_needed)
                n_steps = n_steps_needed
        else:
            n_steps = n_steps_needed
        new_dt = duration / n_steps
        self._set_dt(new_dt)  # Change dt so that the simulation lasts exactly `duration`.
        self.run_simulation_steps(n_steps, callback,
                                  enable_tracker_display, energy_check)

    def run_simulation_steps(self, n_steps,
                             callback=None,
                             enable_tracker_display=True,
                             energy_check=False):
        """Run simulation for a given number of steps.

        Does not change dt.

        See also
        --------
        run_simulation:
            To run for a given duration instead.
        """
        self.tracker = SimulationTracker(n_steps, display_enabled=enable_tracker_display)
        if energy_check:
            self.energy_check = EnergyCheck(self)


        #print(self.t_components['bore0'].PV)

        for _ in range(n_steps):
            self.one_step(check_scheme=True)
            #print(self.t_components['bore0'].PV)


            # All the functions to call after an iteration
            if callback:
                callback(self)
            self.tracker.update()
            if energy_check:
                self.energy_check()

        if self.energy_check:
            self.energy_check.finish()

    def get_lengths_pipes(self):
        return [t_pipe.pipe.get_length() for t_pipe in self.t_pipes]

    def get_orders_mesh(self):
        return [t_pipe.mesh.get_orders().tolist() for t_pipe in self.t_pipes]

    def get_elements_mesh(self):
        return [len(x) for x in self.get_orders_mesh()]

    def __get_mesh_info(self):
        msg = "Mesh info:"
        # msg += '\n\t{:d} degrees of freedom'.format(self.n_tot)
        msg += "\n\tpipes type: {}".format([t for t in self.t_pipes])
        lengths = self.get_lengths_pipes()
        msg += "\n\t{:d} pipes of length: {}".format(len(lengths), lengths)

        # Orders contains one sub-list for each pipe.
        orders = self.get_orders_mesh()
        elem_per_pipe = self.get_elements_mesh()
        msg += ('\n\t{} elements distributed '
                'as: {}'.format(sum(elem_per_pipe), elem_per_pipe))
        msg += '\n\tOrders on each element: {}'.format(orders)
        return msg

    def discretization_infos(self):
        print(self.__get_mesh_info())



class EnergyCheck:
    """Check the global energy balance of the scheme, by computing energy at every time step.

    Used in run_simulation()

    Examples
    --------
    >>> t_solver.run_simulation(duration=0.1, energy_check=True)

    WARNING : Does not take energy sources into account (yet). Will fail if
    a component is a source of energy (for instance a nonzero TFlowCondition).
    """

    def __init__(self, t_solver):
        self.t_solver = t_solver
        self.init_energy = self.prev_energy = self.energy = self.t_solver.energy()
        self.dissipated_total = 0
        print("Initial energy:", self.init_energy)
        self.call_count = 0
        self.max_err = 0
        self.energy_errs = []

    def __call__(self):
        self.call_count += 1
        self.prev_energy = self.energy
        self.energy = self.t_solver.energy()
        dissip_last_step = self.t_solver.dissipated_last_step()
        self.dissipated_total += dissip_last_step
        #print(self.energy)
        #print(self.t_solver.get_dt())
        residual = (self.energy - self.prev_energy + dissip_last_step) \
            / (self.t_solver.get_dt() * self.energy)
        #print(residual)
        err = abs(residual)
        self.energy_errs.append(residual)

        # print("t = {:.3e} ; energy = {} ; dissipated_total = {} ; energy+dissip = {} ; error on energy balance = {}".format(self.t_solver.get_current_time(),
        #       self.energy, self.dissipated_total, self.energy+self.dissipated_total, err))
        if err > self.max_err:
            self.max_err = err
        if err > 1:         # When huge error, stop the program
            raise Exception("Energy balance failed (very badly)!")

    def finish(self):
        """Finalize the energy check at the end of the simulation.

        Raises
        ------
        Exception
            If the energy balance was not verified, but the error was
            not large enough to raise an Exception earlier.
        """
        print("EnergyCheck was called {} times.".format(self.call_count))
        print("Final values:")
        print("t = {:.3e} ; energy = {} ; dissipated_total = {} ; energy+dissip = {} ; maximal error on energy balance = {}".format(self.t_solver.get_current_time(),
              self.energy, self.dissipated_total, self.energy+self.dissipated_total, self.max_err))
        if self.max_err > 1e-8:  # If there was error, say it in the end
            raise Exception("Energy balance failed! (but not too badly)")
