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
Create the continuous instrument graph in which each component is associated to
its physical equation.
"""

import numpy as np
import warnings
from openwind.continuous import (PhysicalRadiation, Pipe,
                                 Scaling, Netlist, JunctionTjoint,
                                 JunctionSimple, losses_model, radiation_model,
                                 JunctionDiscontinuity, Flow, Flue, Valve)
from openwind.design import ShapeSlice
from openwind.continuous.tool_slice_temperature import slice_temperature


__author__ = ("Guillaume Castera, Juliette Chabassier, Augustin Ernoult,"
              " Alexis Thibault, Robin Tournemenne")
__copyright__ = "Copyright 2019, Inria"
__credits__ = ["Guillaume Castera", "Juliette Chabassier", "Augustin Ernoult",
               "Alexis Thibault", "Robin Tournemenne"]
__license__ = "GPL 3.0"
__version__ = "2.0"
__maintainer__ = "Juliette Chabassier"
__email__ = "juliette.chabassier@inria.fr"
__status__ = "Dev"



class InstrumentPhysics:


    """Create the continuous instrument graph with physical considerations.

    Create the instrument's graph: an ensemble of pipes (main bore and chimney
    hole) the ends of which being connected to different type of connector:
    - radiation
    - T-joint junction
    - source
    - etc.
    All the connexion of this graph are specified in a
    `openwind.continuous.netlist.Netlist` object.
    Each component of this graph is associated to physical equations (such as
    sound propagation equation for the pipe) an dit computes its own physical
    coefficients.

    Attributes
    ----------
    netlist : openwind.continuous.netlist.Netlist
        Graph of all the connected parts of the instrument.
    scaling : openwind.continuous.scaling.Scaling
        Nondimensionalization coefficients.

    Parameters
    ----------
    instrument_geometry : openwind.technical.instrument_geometry.InstrumentGeometry
        The geometry of the instrument. This object must contain:

        - a list of `openwind.design.design_shape.DesignShape` to describe the\
            main bore
        - a list of `openwind.technical.instrument_geometry.InstrumentGeometry.Hole` to \
            describe the holes
        - a `openwind.technical.fingering_chart.FingeringChart` object
    player : openwind.technical.player.Player
        The control parameters of the instrument. This object must contain:
        - a type of excitator
        - the corresponding series of control curves
        - a list of note_events
        - the transition duration
    temperature : float or callable
        the temperature at which the physical properties are calculated.

        .. warning::

            if the temperature is non constant, it is supposed variate
            along the main tube (main bore). In the holes, the temperature is
            supposed homogeneous.
    source_model : ???, optional
        Model for the exciting mechanism at the entrance of the instrument.
        Can be a ReedModel or a Flow.
    losses : {False, True, 'bessel', 'diffrepr', 'wl', 'keefe' ,'minikeefe'}
        How to take into account the thermoviscous losses.
        See also : `openwind.continuous.thermoviscous_models.losses_model`
    radiation_category : str or openwind.continuous.radiation_model.RadiationModel , optional
        Model of radiation impedance used. Default is 'unflanged'.
        See `openwind.continuous.physical_radiation.radiation_model` for
        available model names.
    nondim : Boolean, optional
        If true all the physical parameters in the equations are
        nondimensionalized (cross section, sound celerity, air density, time).
        The default is False
    convention : {'PH1', 'VH1'}, optional
        The basis functions for our finite elements must be of regularity
        H1 for one variable, and L2 for the other.
        Regularity L2 means that some degrees of freedom are duplicated
        between elements, whereas they are merged in H1.
        Convention chooses whether P (pressure) or V (flow) is the H1
        variable.
        The default is 'PH1'
    spherical_waves : Boolean, optional
        If true, spherical waves are assumed in the pipe. The default is False.
    discontinuity_mass : Boolean, optional
        If true, acoustic mass is included in the junction between two pipe
        with different cross section. The default is True.

    See also :
    ----------
    `openwind.continuous` for all the possible components of the graph
    """

    def __init__(self, instrument_geometry, temperature,  player, losses,
                 radiation_category="unflanged", nondim=False,
                 convention='PH1', spherical_waves=False,
                 discontinuity_mass=True,
                 matching_volume=False):
        self.instrument_geometry = instrument_geometry
        self.player = player
        self.netlist = Netlist()
        self.temperature = temperature
        # initialize the scaling object with all the coeffs to one
        self.scaling = Scaling()
        self.losses = losses_model(losses)
        self.rad_model = radiation_model(radiation_category)
        self.convention = convention
        self.spherical_waves = spherical_waves
        self.discontinuity_mass = discontinuity_mass
        self.matching_volume = matching_volume

        self.__build_netlist()
        self.netlist.set_fingering_chart(instrument_geometry.fingering_chart)

        if nondim:
            _, input_end = self.netlist.get_component_and_ends(self.source_label)
            pipe_ref = input_end[0].get_pipe()
            self.scaling.set_nondimensionalization(pipe_ref)

        self.__check()

    def __repr__(self):
        return ("<openwind.InstrumentPhysics("
                "\n\t{},".format(repr(self.instrument_geometry)) +
                "\n\ttemperature={},".format(repr(self.temperature)) +
                "\n\t{},".format(repr(self.player)) +
                "\n\tlosses={},".format(repr(self.losses)) +
                "\n\t{},".format(repr(self.netlist)) +
                "\n\t{},".format(repr(self.scaling)) +
                "\n\trad_model={},".format(repr(self.rad_model)) +
                "\n\tconvention='{:s}',".format(self.convention) +
                "\n\tspherical_waves={},".format(self.spherical_waves) +
                "\n\tdiscontinuity_mass={},".format(self.discontinuity_mass) +
                "\n\tmatching_volume={}\n)>".format(self.matching_volume))

    def __str__(self):
        return ("InstrumentPhysics:\n" + "="*20 +
                "\nInstrument Geometry:\n{}\n".format(self.instrument_geometry) +"="*20 +
                "\nTemperature: {}°C\n".format(self.temperature) + "="*20 +
                "\nLosses: {}\n".format(self.losses) + "="*20 +
                "\n{}\n".format(self.player) + "="*20 +
                "\n{}\n".format(self.netlist) + "="*20 +
                "\n{}\n".format(self.scaling) + "="*20 +
                "\nRadiation Model: {}\n".format(self.rad_model) + "="*20 +
                "\nOptions:" +
                "\n\tconvention: {:s}".format(self.convention) +
                "\n\tspherical_waves: {}".format(self.spherical_waves) +
                "\n\tdiscontinuity_mass: {}".format(self.discontinuity_mass) +
                "\n\tmatching_volume: {}".format(self.matching_volume))

    def __build_netlist(self):
        """ build the graph of the instrument by assuming a main bore and
        eventually some side holes. Each hole chimney and the main bore shapes
        are converted into pipes connected by junctions and having radiation
        condition.

        1. the holes are localized on the main bore
        2. the entrance is associated to a source condition
        3. each shape constituing the main bore is converted in one or several\
            pipes if holes are localized on it
        4. the last end (the bell) is associated to a radiation condition
        """
        # 1-localize the holes
        self.position_holes = np.array([hole.position.get_value() for hole in
                                        self.instrument_geometry.holes])

        # 2-first shape "entrance"
        entrance_shape = self.instrument_geometry.main_bore_shapes[0]
        (main_end_up,
         main_end_down) = self.__create_main_bore_pipes(entrance_shape, '0')

        self.excitator_model = self._create_excitator()
        self.netlist.add_component(self.excitator_model, main_end_up)

        # 3-entire instrument
        for k, shape in enumerate(self.instrument_geometry.main_bore_shapes[1:]):
            (pipe_end_up,
             pipe_end_down) = self.__create_main_bore_pipes(shape, str(k+1))
            self.__joint_2_main_bore_section(pipe_end_up, main_end_down,
                                             str(k) + '_' + str(k+1))
            main_end_down = pipe_end_down

        # 4-bell
        rad_label = 'bell_radiation'
        rad_bell = PhysicalRadiation(self.rad_model, rad_label,
                                     self.scaling, self.convention)
        self.netlist.add_component(rad_bell, main_end_down)
        self.netlist.check_valid()

    def _create_excitator(self):
        """
        Instanciate the right class according to the excitator_type value
        """
        exc_type = self.player.excitator_type
        self.source_label = "source"

        if exc_type == "Flow":
            return Flow(self.player, self.source_label,
                        self.scaling, self.convention)
        elif exc_type == "Valve":
            return Valve(self.player, self.source_label,
                         self.scaling, self.convention)
        else:
            raise ValueError("Could not convert excitator type %s" % exc_type)


    def _update_player(self):
        self.excitator_model._update_fields(self.player)

    def update_netlist(self):
        """
        Update the graph after a modification of a geometric parameter.

        Particularly useful in inversion, this method actualize the graph after
        a modification of a geometric parameter.

        .. warning::

            This method can modify the instrument topology.
        """
        self.netlist.reset()
        self.__build_netlist()

    def __joint_2_main_bore_section(self, main_end_up, main_end_down, junc_ID):
        """
        Connect two tubes trough a trivial junction without masse.

        Create a connector component of type
        `openwind.continuous.junction.JunctionSimple` and add it to the netlist.

        Parameters
        ----------
        main_end_up : openwind.continuous.netlist.Netlist.PipeEnd
            The end of the "upstream" pipe.
        main_end_down : openwind.continuous.netlist.Netlist.PipeEnd
            The end of the "downstream" pipe.
        junc_ID : str
            The name of the created `openwind.continuous.junction.JunctionSimple`
            object.

        """
        pos_up, _ = main_end_up.get_pipe().get_endpoints_position_value()
        if any(self.position_holes == pos_up):
            hole_ID = np.where(self.position_holes == pos_up)[0][0]
            hole = self.instrument_geometry.holes[hole_ID]
            if hole.position.is_variable():
                warn_msg = ('It is impossible to vary the position of the {}'
                            'placed at the junction of two '
                            'pipes.').format(hole.label)
                warnings.warn(warn_msg)
            self.__create_hole(hole, main_end_down, main_end_up)
        else:
            label = 'junction_' + junc_ID
            if self.discontinuity_mass:
                two_junction = JunctionDiscontinuity(label, self.scaling,
                                                     self.convention)
            else:
                two_junction = JunctionSimple(label, self.scaling,
                                              self.convention)

            self.netlist.add_component(two_junction, main_end_down,
                                       main_end_up)

    def __create_main_bore_pipes(self, shape, pipeID):
        """Convert one shape of the main bore into one pipe or several if holes
        are located on it.

        Parameters
        ----------
        shape : openwind.design.design_shape.DesignShape
            The shape of the considered pipe.
        pipeID : str
            The name of the considered pipe.

        Returns
        -------
        ( openwind.continuous.netlist.Netlist.PipeEnd , openwind.continuous.netlist.Netlist.PipeEnd )
            The main upstream and downstream ends of the created pipe(s) which
            are still unconnected.
        """
        pos_min, pos_max = shape.get_endpoints_position()
        # find the hole on the considered shape
        holes_on_shape = ((self.position_holes > pos_min.get_value()) &
                          (self.position_holes < pos_max.get_value()))
        label = ('bore' + str(pipeID))
        if not any(holes_on_shape):  # if no holes on the shape, no slicing
            pipe_ends = self.__create_pipe(shape, label, pos_min, pos_max,
                                           main_bore=True)
        else:
            pipe_ends = self.__slice_shape(holes_on_shape, shape, label)
        return pipe_ends


    def __create_pipe(self, shape, label, pos_min, pos_max, main_bore=False):
        """
        Create a pipe component of the graph.

        The object `openwind.continuous.pipe.Pipe` created is added to the
        netlist.

        Parameters
        ----------
        shape : openwind.design.design_shape.DesignShape
            The pipe shape.
        label : str
            The pipe name.
        pos_min : openwind.design.design_parameter.DesignParameter
            The upstream end position of the pipe on the main bore axis (used
            for the temperature scale).
        pos_max : openwind.design.design_parameter.DesignParameter
            The downstream end position of the pipe on the main bore axis (used
            for the temperature scale).
        main_bore : bool, optional
            If True, the pipe is considered as a part of the main bore (usefull
            for example for interpolation). The default is False.

        Returns
        -------
        end_up : openwind.continuous.netlist.Netlist.PipeEnd
            The upstream end of the created pipe.
        end_down : openwind.continuous.netlist.Netlist.PipeEnd
            The downstream end of the created pipe.

        """
        temperature_slice = slice_temperature(self.temperature,
                                              pos_min.get_value(),
                                              pos_max.get_value())
        pipe = Pipe(shape, temperature_slice, label, self.scaling,
                    self.losses, self.convention, self.spherical_waves)
        if main_bore:
            pipe.on_main_bore = main_bore
        end_up, end_down = self.netlist.add_pipe(pipe)
        return end_up, end_down

    def __slice_shape(self, holes_on_shape, shape, label):
        """
        Cut the shape at the position of the hole, create the corresponding
        pipe and create the holes pipe and radiation condition

        Parameters
        ----------
        holes_on_shape : np.array of boolean
            If each hole is on the considered part of the main bore or not.
        shape : openwind.design.design_shape.DesignShape
            The main bore shape considered.
        label : str
            The name of the considered shape.

        Returns
        -------
        upstream_end : openwind.continuous.netlist.Netlist.PipeEnd
            The main upstream end of the created pipes (still unconnected).
        end_down : openwind.continuous.netlist.Netlist.PipeEnd
            The main downtream end of the created pipes (stil unconnected).
        """
        pos_min, pos_max = shape.get_endpoints_position()
        index_in = np.argsort(self.position_holes[holes_on_shape])
        # the slicing positions (DesignParameters)
        holes_in = [self.instrument_geometry.holes[nh] for nh in
                    np.where(holes_on_shape)[0][index_in]]
        x_cut = [pos_min] + [hole.position for hole in holes_in] + [pos_max]

        shape_slice = ShapeSlice(shape, x_cut[0:2])
        label_slice = label + '_slice' + str(0)
        upstream_end, end_down = self.__create_pipe(shape_slice, label_slice,
                                                    x_cut[0], x_cut[1],
                                                    main_bore=True)
        for p, hole in enumerate(holes_in):
            shape_slice = ShapeSlice(shape, x_cut[p+1:p+3])
            label_slice = label + '_slice' + str(p+1)
            end_up, end_down_temp = self.__create_pipe(shape_slice,
                                                       label_slice,
                                                       x_cut[p+1], x_cut[p+2],
                                                       main_bore=True)
            self.__create_hole(hole,
                               end_down, end_up)
            end_down = end_down_temp

        return upstream_end, end_down

    def __hole_junction(self, junc_label, end_down, end_up, end_hole):
        """
        Set the T-joint junction between the hole and two main bore pipes.

        Create a `openwind.continuous.junction.JunctionTjoint` object bewteen
        three ends pipe.

        Parameters
        ----------
        junc_label : str
            The name of the junction.
        end_down : openwind.continuous.netlist.Netlist.PipeEnd
            The "downstream" end of the "upstream" pipe.
        end_up : openwind.continuous.netlist.Netlist.PipeEnd
            The "upstream" end of the "downstream" pipe.
        end_hole : openwind.continuous.netlist.Netlist.PipeEnd
            The "upstream" end of the pipe of the hole.
        """
        junction = JunctionTjoint(junc_label, self.scaling, self.convention,
                                  self.matching_volume)
        self.netlist.add_component(junction, end_down, end_up, end_hole)

    def __create_hole(self, hole, end_down, end_up):
        """
        Create the chimney pipe of the hole and connect it to the main bore.

        The chimney hole is associated to a `openwind.continuous.pipe.Pipe`
        and connect to the main bore by a
        `openwind.continuous.junction.JunctionTjoint`. The other end of the
        chimney pipe is connected to a
        `openwind.continuous.physical_radiation.PhysicalRadiation`

        Parameters
        ----------
        hole : openwind.technical.instrument_geometry.Hole
            The hole considered.
        end_down : openwind.continuous.netlist.Netlist.PipeEnd
            The "downstream" end of the "upstream" pipe.
        end_up : openwind.continuous.netlist.Netlist.PipeEnd
            The "upstream" end of the "downstream" pipe.

        """
        # hole chimney
        end_hole_up, end_hole_down = self.__create_pipe(hole.shape, hole.label,
                                                        hole.position,
                                                        hole.position)
        # hole radiation
        rad_label = 'rad_' + hole.label
        hole_rad = PhysicalRadiation(self.rad_model, rad_label,
                                     self.scaling, self.convention)
        self.netlist.add_component(hole_rad, end_hole_down)

        # hole junction
        junc_label = 'junction_' + hole.label
        self.__hole_junction(junc_label, end_down, end_up, end_hole_up)

    def __check(self):
        """
        Check that the number of \
        `openwind.continuous.physical_radiation.PhysicalRadiation` created
        correspond to the number of holes + 1 for the bell.
        """
        # Check how many radiations were created
        assert (len(self.netlist.get_components_of_class(PhysicalRadiation))
                == len(self.instrument_geometry.holes) + 1)
