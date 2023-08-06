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

from collections import UserDict
import enum

from openwind.technical import FingeringChart


class MyDict(UserDict):
    """
    A dictionary that iterates over values, and allows union through '+'.
    """
    def __iter__(self):
        return iter(self.data.values())

    def __add__(self, other):
        assert isinstance(other, MyDict)
        return MyDict({**self.data, **other.data})


class EndPos(enum.Enum):
    """
    Position of a pipe-end (POS_MINUS is the first end, POS_PLUS is the second).
    """
    MINUS = 0
    PLUS = 1

    @property
    def array_pos(self):
        """
        Relative position of the end in an array representing the pipe's data.
        """
        if self == EndPos.MINUS:
            return 0
        if self == EndPos.PLUS:
            return -1
        raise ValueError

    @property
    def x(self):
        """
        Relative abscissa x in the pipe.
        """
        if self == EndPos.MINUS:
            return 0.0
        if self == EndPos.PLUS:
            return 1.0
        raise ValueError


class Netlist:
    """Represent the connexions in the instrument as a netlist.

    The Pipes are stored aside. Each of them has two pipe-ends.

    The other components may each be connected to one or several pipe-ends:
        * A Radiation is connected to one pipe-end
        * A Junction may be connected to two or three (or maybe more soon?)

    The order of connection is important
    (just like on the pins of an electronic component, you can't reverse a
    diode or shuffle the connections to an op-amp), and should be given in the
    order that is conventional for the component.
    """

    class PipeEnd:
        """A netlist-kind PipeEnd.

        Knows which pipe it is part of, and which component it is connected to.
        """
        def __init__(self, pipe, pos):
            self.pipe = pipe
            self.pos = pos
            self.component = None

        def set_component(self, component):
            if self.is_connected():
                raise ValueError("PipeEnd already connected to {}".format(self.component))
            self.component = component

        def get_component(self):
            return self.component

        def get_pipe(self):
            return self.pipe

        def is_connected(self):
            return self.component != None

        def __repr__(self):
            return 'PipeEnd({},{})'.format(self.pipe, self.component)
        def __str__(self):
            return self.__repr__()




    def __init__(self):
        # self._netlist : dict string -> (Component, list[pipe_end])
        self._pipes = dict()
        self._components = dict()
        self._ends = []
        self._fingering_chart = FingeringChart()

    def reset(self):
        self._pipes = dict()
        self._components = dict()
        self._ends = []

    def _new_pipe_end(self, pipe, pos):
        """Get a new pipe_end, to which stuff can be connected."""
        pipe_end = Netlist.PipeEnd(pipe, pos)
        self._ends.append(pipe_end)
        return pipe_end

    def add_pipe(self, pipe):
        """Add a Pipe to the netlist, and return the labels of its ends."""
        if pipe.label in self._pipes:
            raise ValueError(("A Pipe with label '{}' has already been "
                             "added to the netlist").format(pipe.label))
        pipe_ends = [self._new_pipe_end(pipe, pos) for pos in EndPos]
        self._pipes[pipe.label] = (pipe, pipe_ends)
        return pipe_ends

    def add_component(self, component, *pipe_ends):
        """Add a component to the netlist"""
        if component.label in self._components:
            raise ValueError(("A Component with label '{}' has already been "
                             "added to the netlist").format(component.label))
        for pipe_end in pipe_ends:
            pipe_end.set_component(component)
        self._components[component.label] = (component, pipe_ends)

    def get_component_and_ends(self, label):
        """Get a component and its pipe_ends from its label."""
        component, ends = self._components.get(label)
        return component, ends

    def get_pipe_and_ends(self, label):
        """Get a pipe and its pipe_ends from its label."""
        pipe, ends = self._pipes.get(label)
        return pipe, ends

    def get_free_ends(self):
        """List of all the ends that are not connected to a component."""
        free_ends = []
        for pipe_end in self._ends:
            if not pipe_end.is_connected():
                free_ends.append(pipe_end)
        return free_ends

    def check_valid(self):
        """Check if the netlist is valid for building a music instrument,
        i.e. that each pipe_end is between one pipe and one component.
        """
        free_ends = self.get_free_ends()
        if len(free_ends) > 0:
            raise ValueError('Some pipe-ends are not connected to '
                             'a component!\n'
                             + str(free_ends))


    def get_components_of_class(self, class_):
        """List all the components of a given class in this netlist."""
        return [comp for comp, ends in self._components.values()
                if isinstance(comp, class_)]

    def set_fingering_chart(self, fingering_chart):
        self._fingering_chart = fingering_chart
    def get_fingering_chart(self):
        return self._fingering_chart

    def convert_with_structure(self, convert_pipe, convert_component):
        """
        Create specialized components while preserving graph structure.

        We assume that for each netlist component, we want to build exactly
        one "specialized component" (such as FComponent or TComponent).
        To do so, one factory function must be given for pipes,
        and one for other components.

        The following diagram illustrates how this method operates. \
            1. Convert Pipes to "SpecialPipes" \
            (i.e. TemporalPipes or FrequentialPipes) \
            2. Obtain the ends of the SpecialPipes \
            3. Create the SpecialComponents and connect them \
            to the correct ends. \


          Pipe <--------> PipeEnd <-------------> NetlistComponent \
             |       (2)           (n)                  | \
          1. |                                          | \
             |                                          | \
             v                                          | 3. \
        SpecialPipe                                     | \
                \                                       | \
              2. \                                      | \
                  v (2)                                 v \
                SpecialPipeEnd <--------------> SpecialComponent \
                                (n)


        Parameters
        ----------
        convert_pipe: Callable[Pipe, SpecialPipe]
            Function that constructs the appropriate SpecialPipe.
        convert_component: Callable[(NetlistComponent, Tuple[SpecialPipeEnd]),
                                     SpecialComponent]
            Function that constructs the appropriate SpecialComponent and
            connects it to the given SpecialPipeEnds.

        Returns
        -------
        special_pipes, special_components : list, list
            The converted pipes and components

        """
        self.check_valid()
        special_pipes = MyDict()
        special_ends = dict()
        for label in self._pipes:
            pipe, ends = self._pipes[label]
            s_pipe = convert_pipe(pipe)
            special_pipes[label] = s_pipe
            try:
                for end, s_end in zip(ends, s_pipe.get_ends()):
                    special_ends[end] = s_end
            except TypeError:
                raise ValueError("Failure in conversion of pipe: object %s "
                                 "does not define .get_ends()")

        special_components = MyDict()
        for label in self._components:
            comp, ends = self._components[label]
            s_ends = [special_ends[end] for end in ends]
            s_comp = convert_component(comp, s_ends)
            special_components[label] = s_comp

        return special_pipes, special_components

    def __repr__(self):
        return ("<openwind.continous.Netlist(pipes={}, "
                "connectors={}, fingering_chart={})>").format(
                    list(self._pipes.keys()),
                    list(self._components.keys()),
                    self._fingering_chart.all_notes())

    def __str__(self):
        return ("Netlist:\n\tPipes = {};\n"
                "\tConnectors = {};\n\tFingering Chart = {}").format(
                    list(self._pipes.keys()),
                    list(self._components.keys()),
                    self._fingering_chart.all_notes())
