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
Parse instrument geometry and fingering into OpenWind classes.
"""

import collections
import warnings

try:
    from tabulate import tabulate
except ImportError:
    # Backup (less-)pretty-printing function for when package is missing
    def tabulate(data, col_names):
        """ Adjust column width in a string. """
        data = [col_names] + data
        data = [[str(d) for d in row] for row in data]
        maxlength = max(max(len(d) for d in row) for row in data)
        format_per_element = "{:>%d}" % (maxlength+1)
        format_per_row = format_per_element * len(data[0])
        rows = [format_per_row.format(*row) for row in data]
        return '\n'.join(rows)

import numpy as np
import matplotlib.pyplot as plt

from openwind.design import (FixedParameter, OptimizationParameters,
                             VariableParameter, VariableParameterSquare,
                             VariableParameterLimitedRange,
                             VariableHolePosition, VariableHoleRadius)
from openwind.design import Spline, Cone, Bessel, Circle, Exponential
from openwind.technical import FingeringChart

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


class InstrumentGeometry:
    """
    Parse instrument geometry and fingering into OpenWind classes.

    Create an instrument with the bore shape and holes given by the
    geometry described in the files.
    Up to three files can be provided :

    * main bore geometry
    * side holes
    * fingering chart


    Attributes
    ----------
    main_bore_shapes: list[ openwind.design.design_shape.DesignShape ]
        The description of the main bore
    holes: list[ openwind.technical.instrument_geometry.InstrumentGeometry.Hole ]
        The description of the tone holes
    fingering_chart: openwind.technical.fingering_chart.FingeringChart
        The fingerings of the various notes.
    optim_params: openwind.design.design_parameter.OptimizationParameters
        Used only for inverse problem. Organized the variable parameters which
        are modified during the optimization process.

    Methods
    -------
    `plot_InstrumentGeometry(figure=None, note=None, **kwargs)` :
        Plot the instrument.

    `print_files(generic_name, extension='.txt')` :
        Print the files corresponding to this InstrumentGeometry.

    `get_main_bore_radius_at(position)` :
        Return the radius of the main bore at given position.

    `get_bore_list()` :
        Return the lists of data of the geometry.

    `get_main_bore_length()` :
        Return the total length of the main bore.

    `print_main_bore_shape(filename=None)` :
        Print the main bore shape.

    `print_holes(filename=None)` :
        Print the holes information.

    See Also:
    --------
    `openwind.design.design_parameter.DesignParameter` : Mother class of design
    parameters

    `openwind.design.design_shape.DesignShape` : Mother class of design shapes

    `openwind.design.design_parameter.OptimizationParameters`

    `openwind.technical.fingering_chart.FingeringChart`

    Structure of the files
    -----------------------
    -----------------------

    In all of the files, data are separated by whitespace.
    Comments start with a `#` and extend to the end of the line.
    Blank lines are ignored.

    Instead of giving a filename, it is possible (and equivalent) to give
    the list of already-split lines, for instance:

        >>> InstrumentGeometry([[0.0, 2e-3], [0.2, 0.01]])
        <openwind.InstrumentGeometry at ...>


    * Main bore geometry file *

    The instrument bore is assumed to be aligned along one axis `x`.
    Abscissae `x` are absolute, with `x = 0` corresponding to the
    entrance of the instrument, and increasing `x` along its length.

    Each line describes one section of the instrument,
    which can be of one of several basic shapes.
    Measurements are given in meters.

    The line must be of the form, either:

    * `x1 x2 r1 r2 type [param...]`
        where

        * x1, x2 are the beginning and end abscissae of the part,
        * r1, r2 are the radii at the beginning and end,
        * `type` is one of `{'linear', 'spline', 'circle', 'exponential', 'bessel'}`,
        * `param...` are the parameters of the shape, if necessary:
            - radius of the `circle`
            - `alpha` parameter of the `bessel` function
            - `x_i... r_i...` internal points of the `spline`

    * `x r`
        in which case the radius is assumed to evolve linearly from the
        last specified point.

    .. code-block:: shell

        # This is my favorite instrument
        # x1    x2     r1      r2     type         param
          0     0.1    0.02    0.03   linear
          0.1   1.2    0.03    0.015  circle       -10   # slightly fat curve
          1.2   2.6    0.015   0.02   exponential
        # x     r
          2.7   2.1e-2   # the bell is smaller than usual



    * Holes file *

    A new format for holes file has been introduced:
    First line of the file contains column titles,
    the following lines contain the data.

    Possible column names are : 'label', 'position', 'chimney', 'radius', 'type'.
    Columns 'position', 'chimney', 'radius' are mandatory, 'label' and 'type'
    are optional.
    If 'label' is provided, each hole will be labeled by the given name.
    Currently the only supported 'type' is 'linear'.

    .. code-block:: shell

        label       position type    radius  chimney
        #----------------------------------------
        g_hole      0.1      linear  1e-3    0.021
        b_flat_hole 0.23     linear  4.2e-3  2e-3
        ...


    Alternate (old) format : `x l r type`.
    This format is deprecated and may give inconsistent hole labels.

    * Fingering chart file *

    First line of the file must be:
        `label [note_name...]`
    The following lines are:
        `hole_name ['x' or 'o' ...]`
        specifying for each note, whether this hole is
        open ('o') or closed ('x').

    .. code-block:: shell

        label        C1    do    re    fa    open    closed    fork
        #----------------------------------------------------------
        g_hole       x     x     x     x     o       x         o
        b_flat_hole  o     o     o     o     o       x         x
        ...


    * Type of design parameters for the inversion *

    For the inversion, it is necessary to indicate which parameters are fixed,
    and which parameters is variable and can be modified by the algorithm. This
    is done directly in the MainBore and Holes files by adding information on
    the numerical values.

    Several types of variable parameters can be used:

    * `0.01`: The numerical value only is a fixed parameters.
            A ``FixedParameter`` object is instantiated.

    * `~0.01`: The '~' indicates a variable parameters (unlimited range).
            A ``VariableParameter`` object is instantiated.

    * `1e-3<~0.01`: The range of the variable parameter is limited by a low bound.
            A ``VariableParameterSquare`` object is instantiated.

    * `1e-3<~0.01<1e-1`: The range of the variable parameter is limited by low and upper bounds.
            A ``VariableParameterLimitedRange`` object is instantiated.

    * `~0.01%`: Only valid for hole position and hole radius!
            The parameter is defined relatively to the main bore shape on which
            the hole is placed.
            A `VariableHolePosition` or `VariableHoleRadius` object is instantiated.
    """

    Hole = collections.namedtuple('Hole', ['shape', 'position', 'label'])
    # Collection used to instanciate a subclass `Hole`.
    #
    # Attributes
    # ----------
    # shape : openwind.design.design_shape.DesignShape
    #     The shape of the chimney.
    # position : openwind.design.design_parameter.DesignParameter
    #     The position of the Hole on the main bore.
    # label : string
    #     The name of the hole.

    def __init__(self, *files):
        self.optim_params = OptimizationParameters()
        self._create_main_bore_shapes(files[0])

        self.holes = list()
        if len(files) >= 2:
            self._create_holes_shapes(files[1])

        if len(files) >= 3:
            self.fingering_chart = self._create_fingering_chart(files[2])
        else:
            self.fingering_chart = self._create_fingering_chart(None)


    def __repr__(self):
        return '<openwind.InstrumentGeometry({} main bore parts, {} holes, ' \
               '{})>'.format(len(self.main_bore_shapes),
                                            len(self.holes),
                                            repr(self.fingering_chart))

    def __str__(self):
        return(('-'*30 + '\nMain Bore:\n{} \n' + '-'*30 + '\nHoles:\n{} \n' +
                '-'*30 + '\nFingering Chart:\n{}\n')
               .format(self.print_main_bore_shape(), self.print_holes(),
                       self.fingering_chart))

    def get_hole_labels(self):
        return [hole.label for hole in self.holes]

# %% creation of lists of shape and fingering chart
    def _create_main_bore_shapes(self, data):
        """
        Construct the "DesignShapes" of the main bore from the data.

        The possible format of the data are speciefied in the main docstring.
        The data are interpreted by the method ```_parse_geometry```.

        Parameters
        ----------
        data : list or string
            `data` is either direct data, or a filename containing the data.

        Attributes
        ----------
        main_bore_shapes : list of [ openwind.design.design_shape.DesignShape ]
            list of DesignShape

        """
        self.main_bore_shapes = list()
        """A list of `openwind.design.design_shape.DesignShape` which describe
        the main bore of the instrument."""
        main_bore_list = self._interpret_data(data)
        Xlast = None
        Rlast = None
        for k, raw_part in enumerate(main_bore_list):
            label = 'bore_' + str(k)
            X, R, shape_type, Geom_param = self._parse_geometry(raw_part, Xlast,
                                                                Rlast, label)

            if Xlast is not None and \
                min([x.get_value() for x in X]) < Xlast.get_value():
                raise ValueError("Some abscissae x are going backwards, "
                                 "there must be a mistake in the instrument"
                                 " file.")
            if min([r.get_value() for r in R]) < 0:
                raise ValueError("Radius must be positive.")

            if shape_type is not None:
                new_shape = self._build_shape(X, R, shape_type, Geom_param)
                self.main_bore_shapes.append(new_shape)
            Xlast = X[-1]
            Rlast = R[-1]
        #     if (k==0):
        #         self.Rinput = R[0].get_value()
        # self.ltot = self.main_bore_shapes[-1].get_position_from_xnorm(1)



    def _create_holes_shapes(self, data):
        """
        Construct the DesignShape of each hole from the data.

        The possible format of the data are speciefied in the main docstring.
        The data are interpreted by the method ```_parse_holes_new_format``` or
        ```_parse_holes_old_format```.

        .. warning::
            The current version accept only one DesignShape by hole

        Parameters
        ----------
        data : list or string
            `data` is either direct data, or a filename containing the data.

        """
        try:
            holes_list = InstrumentGeometry._interpret_data(data)
            if len(holes_list) == 0:  # No holes
                return
            if str(holes_list[0][0]).isalpha():
                self._parse_holes_new_format(holes_list)
            else:
                self._parse_holes_old_format(holes_list)
        except (ValueError, IndexError) as err:
            msg = ("\nImpossible to read the file. See documentation of InstrumentGeometry.")
            raise ValueError(str(err) + msg).with_traceback(err.__traceback__)



    def _create_fingering_chart(self, data):
        """
        Construct the ```FingeringChart``` from the data.

        Parameters
        ----------
        data : list or string or None
            `data` is either direct data, or a filename containing the data.
            If data is not specified, the default fingering with all holes open
            is assumed

        Attributes
        -------
        fingering_chart: FingeringChart
            The FingeringChart object containing the information on the
            fingerings.

        """
        if not data:
            return FingeringChart()
        data = InstrumentGeometry._interpret_data(data)
        # First line should be 'label'
        # followed by the names of all the notes
        column_titles, remaining_lines = data[0], data[1:]
        assert column_titles[0] == 'label'
        note_names = column_titles[1:]
        number_of_holes = len(remaining_lines)
        chart = -np.ones((number_of_holes, len(note_names))) # Initialize at -1
        hole_labels = []
        for hole_i, line in enumerate(remaining_lines):
            hole_label = line[0]
            if hole_label not in self.get_hole_labels():
                raise ValueError("Hole '{}' was not defined in holes file. Chose between: {}"
                                 .format(hole_label, self.get_hole_labels()))
            hole_labels.append(hole_label)

            for note_j, s in enumerate(line[1:]):
                factor = InstrumentGeometry._parse_opening_factor(s)
                chart[hole_i, note_j] = factor

        # Check if fingering chart is valid
        if np.any(chart == -1):
            raise ValueError("Invalid fingering chart: missing data.")
        # Check if all holes from holes file
        # have been defined in fingering chart
        missing = [hole for hole in self.get_hole_labels()
                        if hole not in hole_labels]
        if missing:
            warnings.warn(('Holes {} missing from fingering chart.\n'
                           'They will be assumed to remain open.').format(missing))

        return FingeringChart(note_names, hole_labels, chart,
                              other_holes=missing)

# %% Reading external files

    @staticmethod
    def _interpret_data(data):
        """
        Interpret the input data as a list of data.

        It is a very general method.
        If the data is a string  it is supposed to be the name of the file
        containing the data, wich is read by the method ```_read_file```.
        If it is a list, it is return identically.

        Parameters
        ----------
        data : list or string
            List of data or a filename.

        Returns
        -------
        List
            List of raw of data.

        """
        if isinstance(data, list):  # We can chose to take real csv files as inputs
            return data             # or using directly lists
        else:
            return InstrumentGeometry._read_file(data)

    @staticmethod
    def _read_file(filename):
        """
        Read file and transcript it in a list of data raw.

        It is a very general method which only read the file, split the
        text w.r. to lines and whitespaces and organise it in a list of list.

        Parameters
        ----------
        filename : string
            The name of the file containing the data.

        Returns
        -------
        raw_parts : List
            List of raw data.

        """
        with open(filename) as file:
            lines = file.readlines()
        raw_parts = []
        for line in lines:
            contents = InstrumentGeometry._parse_line(line)
            if len(contents) > 0:
                raw_parts.append(contents)
        return raw_parts

    @staticmethod
    def _parse_line(line):
        """
        Interpret each line as a list of string.

        Split the lines according to whitespace.
        Anything after a '#' is considered to be a comment

        Parameters
        ----------
        line : string
            A line string.

        Returns
        -------
        List
            List of string obtained from the line.

        """
        # Anything after a '#' is considered to be a comment
        line = line.split('#')[0]
        # Split the lines according to whitespace
        return line.split()

    @staticmethod
    def _parse_opening_factor(s):
        """
        Interpret the opening factor in the fingering chart data.

        Each hole is:
            - open if 'o' or 'open'
            - closed if 'x' or 'closed'
            - semi-closed if '0.5' or '.5'

        Parameters
        ----------
        s : string
            string containing the information about the opening of the hole

        Returns
        -------
        float
            The opening factor between 0 (entirely closed) and 1 (entirely
            opened)

        """
        opening_factor_from_str = {
                'open': 1, 'o': 1,
                'closed': 0, 'x': 0, 'c': 0,
                '0.5': 0.5, '.5': .5
                }

        if s.lower() in opening_factor_from_str:
            return opening_factor_from_str[s.lower()]

        try:
            # Legacy behavior: 1 is closed, 0 is open
            factor = 1 - float(s)
            warnings.warn("Please use 'o' or 'open' for open holes"
                          " and 'x' or 'closed' for closed")
            return factor
        except ValueError:
            raise ValueError("Invalid string for open/close: {}"
                             .format(s))

# %% Creating DesignParameters / DesignShapes

    def __estim_value(self, param):
        """
        Get the numerical value associated to a parameters.

        The numerical value `x` is extracted from `param`, following
        the different format possible (see the class docstring):
            - a float: `x`
            - the string: `'~x'`
            - the string: `'x_min<~x'`
            - the string: `'x_min<~x<x_max'`
            - the string: `'~x%'`

        Parameters
        ----------
        string : float or string
            Float or string containing the parameters value.

        Returns
        -------
        float
            The numerical value of the parameter.

        """
        if isinstance(param, str):
            string_split = param.split(sep='<')
            if len(string_split) == 1 and param.startswith('~'):
                if param.endswith('%'):
                    return float(param[1:-1])
                else:
                    return float(param[1:])
            elif len(string_split) == 1:
                return float(param)
            elif len(string_split) == 2 and string_split[1].startswith('~'):
                return float(string_split[1][1:])
            elif len(string_split) == 3 and string_split[1].startswith('~'):
                return float(string_split[1][1:])
            else:
                raise ValueError(("the parameters format: '{:s}' is not "
                                  "recognized").format(param))
        else:
            return float(param)

    def __designparameter(self, param, label):
        """
        Create the DesignParameter associated to the format specified in the
        input parameter (except for holes parameters).

        The subclass of `openwind.design.design_parameter.DesignParameter`
        instanciated depend of the format of `param`. The different format
        possible are (see the class docstring):

        - a float:      `x`                 => FixedParameter
        - the string:   `'~x'`              => VariableParameter
        - the string:   `'x_min<~x'`        => VariableParameterSquare
        - the string:   `'x_min<~x<x_max'` => VariableParameterLimitedRange

        Parameters
        ----------
        param : float or string
            Float or string containing the parameters value.
        label : string
            the label of the parameter

        Returns
        -------
        openwind.design.design_parameter.DesignParameter
            The DesignParameter object associated to the parameter
        """
        if isinstance(param, str):
            string_split = param.split(sep='<')
            if len(string_split) == 1 and param.startswith('~'):
                return VariableParameter(float(param[1:]), self.optim_params,
                                         label)
            elif len(string_split) == 1:
                return FixedParameter(float(param), label)
            elif len(string_split) == 2 and string_split[1].startswith('~'):
                min_value = float(string_split[0])
                return VariableParameterSquare(float(string_split[1][1:]),
                                               self.optim_params, min_value,
                                               label)
            elif len(string_split) == 3 and string_split[1].startswith('~'):
                authorized_range = [float(string_split[0]),
                                    float(string_split[2])]
                return VariableParameterLimitedRange(float(string_split[1][1:]),
                                                     self.optim_params,
                                                     authorized_range, label)
            else:
                raise ValueError(("the parameters format: '{:s}' is not "
                                  "recognized").format(param))
        else:
            return FixedParameter(float(param), label)

    def __localize_hole(self, x):
        """
        Localize the hole on the main bore.

        Estimate the main bore shape on which is placed the hole, from its
        position

        Parameters
        ----------
        x : string, float
            The hole position data.

        Returns
        -------
        openwind.design.design_shape.DesignShape
            The design shape of the main bore part on which is placed the hole.

        """
        hole_position = self.__estim_value(x)
        main_bore_bound = [shape.get_position_from_xnorm(0)
                           for shape in self.main_bore_shapes]
        main_bore_bound.append(self.main_bore_shapes[-1]
                               .get_position_from_xnorm(1))
        if hole_position > np.max(main_bore_bound):
            raise ValueError('One hole is placed outside the main bore!')
        index_main_bore_shape = np.max([0, np.searchsorted(main_bore_bound,
                                                           hole_position) - 1])
        return self.main_bore_shapes[index_main_bore_shape]

    def __hole_position_designparameter(self, x, main_bore_shape, hole_label):
        """
        Create the adequate DesignParameter for a hole position.

        The subclass of `openwind.design.design_parameter.DesignParameter`
        instanciated depend of the format of `param`. The different format
        possible are (see the class docstring):

        - if '~x%' => VariableHolePosition
        - else : it is treat like other parameters.

        Parameters
        ----------
        x : string, float
            The data corresponding to the hole positon.
        main_bore_shape : openwind.design.design_shape.DesignShape
            The design shape of the main bore part on which is placed the hole.
        hole_label : string
            The hole label.

        Returns
        -------
        openwind.design.design_parameter.DesignParameter
            The DesignParameter object associated to the parameter
        """
        label = hole_label + '_position'
        if isinstance(x, str) and x.startswith('~') and x.endswith('%'):
            return VariableHolePosition(float(x[1:-1]), self.optim_params,
                                        main_bore_shape, label)
        else:
            return self.__designparameter(x, label)

    def __hole_radius_designparameter(self, r_data, main_bore_shape,
                                      hole_position, hole_label):
        """
        Create the adequate DesignParameter for a hole radius.

        The subclass of `openwind.design.design_parameter.DesignParameter`
        instanciated depend of the format of `r_data`. The different format
        possible are (see the class docstring):

        - if '~x%' => VariableHoleRadius
        - else : it is treat like other parameters.

        Parameters
        ----------
        r_data : string, float
            The data corresponding to the hole radius.
        main_bore_shape : openwind.design.design_shape.DesignShape
            The design shape of the main bore part on which is placed the hole.
        hole_position : openwind.design.design_parameter.DesignParameter
            The design parameter of the hole position
        hole_label : string
            The hole label.

        Returns
        -------
        openwind.design.design_parameter.DesignParameter
            The DesignParameter object associated to the parameter
        """
        label = hole_label + '_radius'

        if (isinstance(r_data, str) and r_data.startswith('~')
            and r_data.endswith('%')):
            return VariableHoleRadius(float(r_data[1:-1]), self.optim_params,
                                      main_bore_shape, hole_position, label)
        else:
            return self.__designparameter(r_data, label)

    def _build_shape(self, X, R, shape_type, Geom_param):
        """
        Construct a DesignShape from DesignParamters

        Parameters
        ----------
        X : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends position of the shape.
        R : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends radius of the shape.
        shape_type : string
            The type of the shape.
        Geom_param : list of [ openwind.design.design_parameter.DesignParameter ]
            The eventual supplementary parameters (necessary for Circle,
            Bessel and Spline). Empty list if not necessary


        Returns
        -------
        shape : openwind.design.design_shape.DesignShape
            The design shape of the considered tube.

        """
        shape_type = shape_type.lower()
        if (shape_type == 'linear' or shape_type == '' or shape_type == 'cone'
            or shape_type == 'cylinder'):
            shape = Cone(*(X + R))
        elif shape_type == 'exponential':
            shape = Exponential(*(X + R))
        elif shape_type == 'circle':
            shape = Circle(*(X + R + Geom_param))
        elif shape_type == 'bessel':
            shape = Bessel(*(X + R + Geom_param))
        elif shape_type == 'spline':
            shape = Spline(*(X + R))
        else:
            msg = ("The shape '" + shape_type + "' is unknown. Please " +
                   "chose between: 'cone'(default), 'spline', 'circle', " +
                   "'exponential' and 'bessel'")
            raise ValueError(msg)
        return shape


# %% Parsing geometry data
    def _parse_geometry(self, raw_part, Xlast, Rlast, label):
        """
        Interpret a list of data to design the main bore shape.

        The list of data is treated differently following to format:
            - 'x r': two columns, a conical part from the last ending point
            is created
            - else: the list is treated independently to build a new shape

        Parameters
        ----------
        raw_part : list
            the list of the data.
        Xlast : openwind.design.design_parameter.DesignParameter or None
            The last ending position.
        Rlast : openwind.design.design_parameter.DesignParameter or None
            The last ending point radius.
        label : string
            The label of the shape.

        Returns
        -------
        X : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends position of the shape.
        R : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends radius of the shape.
        shape_type : string
            The type of the shape.
        Geom_param : list of [ openwind.design.design_parameter.DesignParameter ]
            The eventual supplementary parameters (necessary for Circle,
            Bessel and Spline).

        """
        if len(raw_part) == 2:  # if the input contains only x and r
            return self._parse_x_r(raw_part, Xlast, Rlast, label)
        else:
            return self._parse_detailed_geometry(raw_part, Xlast, Rlast, label)

    def _parse_x_r(self, raw_part, Xlast, Rlast, label):
        """
        Treat the list of data in the forme: position radius

        In this format each couple of value (position, radius) is used to
        create a conical part from the last ending point position and radius.

        Parameters
        ----------
        raw_part : list
            List of two data.
        Xlast : openwind.design.design_parameter.DesignParameter or None
            The last ending position.
        Rlast : openwind.design.design_parameter.DesignParameter or None
            The last ending point radius..
        label : string
            The label of the shape.

        Returns
        -------
        X : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends position of the shape.
        R : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends radius of the shape.
        shape_type : None
            Here it is the default type: 'linear'.
        Geom_param : []
            For this type no supplementary parameter is needed.

        """
        # X, R = [self.__designparameter(value) for value in raw_part]
        X = self.__designparameter(raw_part[0], label+'_pos_plus')
        R = self.__designparameter(raw_part[1], label+'_radius_plus')
        if Xlast is None:  # for the first line only create the design parameter
            return [X], [R], None, []
        elif X.get_value() == Xlast.get_value():  # discontinuity: change only the radius
            return [X], [R], None, []
        else:
            return [Xlast, X], [Rlast, R], 'linear', []

    def _parse_detailed_geometry(self, raw_part, Xlast, Rlast, label):
        """
        Treat the list of data associated to detailed geometry.

        Each list must contains at least four elements in this order:
            - the left end position
            - the right end postion
            - the left end radius
            - the right end radius
        It can also contains the type which is a string chosen between
        {linear, cone, cylinder, exponential, spline, bessel, circle}
        The default type is 'linear' (or 'cone')

        For some shape type other parameters are necessary, added after this
        five first elements.

        .. warning::
            The right end position must correspond to the left end position of
            the last tube (Xlast).

            If the right end radius is equal to the left end radius they are
            treated as a common design parameter, else, a discontinuity of
            section is created.


        Parameters
        ----------
        raw_part : list
            the list of the data (at list 4 elements: len(raw_part>=4)).
        Xlast : openwind.design.design_parameter.DesignParameter or None
            The last ending position. None for the first shape
        Rlast : openwind.design.design_parameter.DesignParameter or None
            The last ending point radius. None for the first shape
        label : string
            The label of the shape.

        Returns
        -------
        X : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends position of the shape.
        R : list of [ openwind.design.design_parameter.DesignParameter ]
            The 2 ends radius of the shape.
        shape_type : string
            The type of the shape.
        Geom_param : list of [ openwind.design.design_parameter.DesignParameter ]
            The eventual supplementary parameters (necessary for Circle,
            Bessel and Spline).
        """
        if Xlast is None:  # For the first line, the first column is the begining of the main bore
            X = [self.__designparameter(raw_part[0], label + '_pos_minus')]
        elif np.isclose(self.__estim_value(raw_part[0]), Xlast.get_value()):  # the parts of the main bore must be connected
            X = [Xlast]
        else:
            msg = ('The main bore parts are not connected! '
                   'It is impossible to construct the instrument.')
            raise ValueError(msg)

        if (Rlast is None or not
            np.isclose(self.__estim_value(raw_part[2]), Rlast.get_value())):  # begining or discontinuity
            R = [self.__designparameter(raw_part[2], label + '_radius_minus')]
        else:
            R = [Rlast]
        shape_type = raw_part[4].lower()
        if shape_type == 'spline':
            params = raw_part[5:]
            N = len(params)//2
            X.extend([self.__designparameter(value, label + '_spline_x' + str(k))
                      for k, value in enumerate(params[:N])])
            R.extend([self.__designparameter(value, label + '_spline_r' + str(k))
                      for k, value in enumerate(params[N:])])
            # spline_points = [self.__designparameter(value, label + '_param')
            #                  for value in raw_part[5:]]
            # N = len(spline_points)//2
            # X.extend(spline_points[:N])
            # R.extend(spline_points[N:])
        X.append(self.__designparameter(raw_part[1], label + '_pos_plus'))
        R.append(self.__designparameter(raw_part[3], label + '_radius_plus'))
        if shape_type == 'circle' or shape_type == 'bessel':
            Geom_param = [self.__designparameter(raw_part[5], label + '_param')]
        else:
            Geom_param = []
        return X, R, shape_type, Geom_param

#%% Parsing hole data
    def _parse_holes_old_format(self, raw_holes):
        """
        Treat the old hole file in format: `position chimney radius type`.

        In this file format each columns is supposed to contains in this order:
            - the position of the hole on the main bore
            - the chimney length
            - the radius of the hole
            - the shape type (only linear is accept)

        Parameters
        ----------
        raw_holes : List
            the list of the data list for each hole.
        """
        warnings.warn("`position chimney radius type` hole file format is deprecated. "
                      "Use the file format with column headers instead.",
                      DeprecationWarning)
        for i, raw_hole in enumerate(raw_holes):
            label = "hole{}".format(i+1)
            if len(raw_hole)>3:
                position, chimney, radius, type_ = raw_hole
                self._add_hole(position, chimney, radius, type_, label)
            else:
                position, chimney, radius = raw_hole
                self._add_hole(position, chimney, radius, label=label)

    def _parse_holes_new_format(self, raw_holes):
        """
        Treat the hole file with column headers.

        The first line of this file must be column headers which can be:
            - 'position' or 'x' : the position of the hole on the main pipe (NEEDED)
            - 'radius' or 'r' : the radius of the hole (NEEDED)
            - 'chimney' or 'l' : the chimney height (NEEDED)
            - 'label' : the label of the hole (optional)
            - 'type' : the shape type of the chimney tube (optional), only
            'linear' is accepted.


        Parameters
        ----------
        raw_holes : List of [List]
            the list of the data list for each hole.

        """
        unifiate_column_name = {'x': 'position', 'position': 'position',
                                'r': 'radius', 'radius': 'radius',
                                'l': 'chimney', 'chimney':'chimney',
                                'type':'type_', 'label':'label'}
        column_names = list()
        for col in raw_holes[0]:
            column_names += [unifiate_column_name.get(col)]
        mandatory_columns = ['position', 'chimney', 'radius']
        if not all(col in column_names for col in mandatory_columns):
            raise ValueError("Hole file must contain columns 'position',"
                             " 'chimney', 'radius'. See documentation of "
                             "openwind hole files.")

        for i, line in enumerate(raw_holes[1:]):
            hole_data = dict(zip(column_names, line))
            self._add_hole(**hole_data)


    def _add_hole(self, position, chimney, radius, type_='linear', label=None):
        """
        Create a hole from the data.

        Generate the design shape and the design parameters associated to the
        hole corresponding to the specified data.

        Parameters
        ----------
        position : string or float
            The data corresponding to the hole position.
        chimney : string or float
            The data corresponding to the chimney height.
        radius : string or float
            The data corresponding to the hole radius..
        type_ : string, optional
            The shape type of the chimney tube (only `linear` is accepted).
            The default is 'linear'.
        label : string, optional
            The hole label. Given automatically if None. The default is None.

        Attribute
        --------
        holes: list
            list of the Hole object.

        """
        if type_ != 'linear' and type_ != 'cone' and type_ != 'cylinder':
            raise ValueError("Only cylindrical holes are implemented (type='linear')")
        if label is None:
            raise ValueError("Hole needs a label")
        if label in self.get_hole_labels():
            raise ValueError("Several holes were defined with the same label.")
        main_bore_shape = self.__localize_hole(position)
        # hole_position = self.__designparameter(x, label + '_position')
        hole_position = self.__hole_position_designparameter(position, main_bore_shape,
                                                             label)
        shape_X = [self.__designparameter(0.0, label + '_chimney_start')]
        shape_X.append(self.__designparameter(chimney, label + '_chimney'))
        # r_param = self.__designparameter(r, label + '_radius')
        r_param = self.__hole_radius_designparameter(radius, main_bore_shape,
                                                     hole_position, label)
        shape_R = [r_param, r_param]
        new_shape = self._build_shape(shape_X, shape_R, 'linear', [])
        self.holes.append(InstrumentGeometry.Hole(new_shape, hole_position, label))

# %% Plots

    def get_bore_list(self):
        """
        Return the list of data of the geometry.

        Returns
        -------
        List
            The list of the data of the main bore.
        List
            The list of data for the holes.

        """
        bore_list = []
        for shape in self.main_bore_shapes:
            bore_list.append(self._parse_line(str(shape)))
        holes_list = []
        for hole in self.holes:
            _, chimney = hole.shape.get_endpoints_position()
            _, radius = hole.shape.get_endpoints_radius()
            holes_list.append([str(hole.label), str(hole.position), str(chimney), str(radius)])
        return bore_list, holes_list

    def get_main_bore_length(self):
        """
        Return the total length of the main bore.

        Returns
        -------
        float
            Total length of the main bore (or position of the last end of the
            main bore).

        """
        return self.main_bore_shapes[-1].get_position_from_xnorm(1)

    def get_main_bore_radius_at(self, position):
        """
        Return the radius of the main bore at given position.

        Parameters
        ----------
        position : float or array of float
            Position at which is estimated the radius.

        Returns
        -------
        radius : array of float
            Radius at the given position.

        """
        radius = np.zeros_like(position, dtype=float)
        for shape in self.main_bore_shapes:
            x_norm = np.array(shape.get_xnorm_from_position(position))
            is_in = (x_norm >= 0) & (x_norm <= 1)
            if np.any(is_in):
                radius[is_in] = shape.get_radius_at(x_norm[is_in])
        return radius

    def plot_InstrumentGeometry(self, figure=None, note=None, double_plot=True, **kwargs):
        """Display the geometry and holes of the instrument.

        If a note name is given, also display the fingering of that note.

        Parameters
        ----------
        figure: matplotlib.figure.Figure, optional
            Which figure to use. By default opens a new figure.
        note: str, optional
            If a note name is given, closed holes are filled, whereas
            open holes are outlined.
            By default all holes are outlined.
        kwargs:
            Additional arguments are passed to the `plt.plot` function.
        """
        if self.holes == []:
            double_plot = False
        # double_plot = (self.holes != [])

        if not figure:
            fig = plt.figure()
        else:
            fig = figure
        ax = fig.get_axes()
        if len(ax) < 2 and double_plot:
            ax = [fig.add_subplot(2, 1, 1)]
            ax.append(fig.add_subplot(2, 1, 2, sharex=ax[0]))
        elif len(ax) < 1:
            ax.append(fig.add_subplot(1, 1, 1))

        x = np.linspace(0, 1, 1000)
        for shape in self.main_bore_shapes:
            radius = np.append(shape.get_radius_at(x), np.nan)
            position = np.append(shape.get_position_from_xnorm(x), np.nan)
            ax[0].plot(np.append(position, np.flip(position)),
                     np.append(radius, np.flip(-radius)), **kwargs)
            if double_plot:
                ax[1].plot(np.append(position, np.flip(position)),
                         np.append(radius, np.flip(-radius)), **kwargs)

        if note:
            fingering = self.fingering_chart.fingering_of(note)
            def plot_or_fill(axes, hole):
                if fingering.is_hole_open(hole.label):
                    return axes.plot
                else:
                    return axes.fill
        else:
            def plot_or_fill(axes, hole):
                return axes.plot

        for hole in self.holes:
            position = hole.position.get_value()
            radius = hole.shape.get_radius_at(x)
            chimney = hole.shape.get_position_from_xnorm(x)
            main_bore = self.__localize_hole(position)
            pos_norm = main_bore.get_xnorm_from_position(position)
            main_radius = main_bore.get_radius_at(pos_norm)
            x_plot = position + np.append(radius, np.flip(-radius))
            y_plot = main_radius + np.append(chimney, np.flip(chimney))
            hole_plot = plot_or_fill(ax[0], hole)(x_plot, y_plot, **kwargs)
            if type(hole_plot[0]).__name__ == 'Polygon':
                hole_plot[0].set_edgecolor(hole_plot[0].get_facecolor())

            if double_plot:
                theta = np.linspace(0,2*np.pi,100)
                hole_plot = plot_or_fill(ax[1], hole)(position + np.mean(radius)*np.cos(theta),
                                                      np.mean(radius)*np.sin(theta), **kwargs)
                if type(hole_plot[0]).__name__ == 'Polygon':
                    hole_plot[0].set_edgecolor(hole_plot[0].get_facecolor())
        ax[-1].set_xlabel('Position (m)')
        ax[0].set_ylabel('Radius (m)')
        ax[0].axis('equal')
        if double_plot:
            ax[1].axis('equal')
            ax[1].set_ylabel('Radius (m)')

# %% print files

    def print_files(self, generic_name, extension='.txt'):
        """
        Print the files corresponding to this InstrumentGeometry.

        Print the three files (MainBore, Holes and FingeringChart) associated
        to this maker model.

        Parameters
        ----------
        generic_name : string
            The generic name for the three files which will be named
            "generic_name_MainBore", "generic_name_Holes" and
            "generic_name_FingeringChart".
        extension : string, optional
            The extension used for the filenames. The default is '.txt'.
        """
        if generic_name.endswith('.txt'):
            generic_name = generic_name[:-4]
        elif generic_name.endswith('.csv'):
            generic_name = generic_name[:-4]
            extension = '.csv'
        self.print_main_bore_shape(generic_name + '_MainBore' + extension)
        if self.holes:
            self.print_holes(generic_name + '_Holes' + extension)
        if len(self.fingering_chart.all_notes()) > 0:
            filename = generic_name + '_FingeringChart' + extension
            f = open(filename, "w")
            f.write('{}'.format(self.fingering_chart))

    def print_main_bore_shape(self, filename=None):
        """
        Print the main bore shape

        Parameters
        ----------
        filename : string, optional
            If indicated, the filename in which the main bore shape is written.
            The default is None.

        Returns
        -------
        msg : str
            The string corresponding to the main bore shape.

        """
        msg = '# x_0\t x_1\t r_0\t r_1\t type\t param\n'
        for shape in self.main_bore_shapes:
            msg += '{}\n'.format(shape)
        if not filename:
            return msg
        else:
            f = open(filename, "w")
            f.write(msg)

    def print_holes(self, filename=None):
        """
        Print the holes information.

        Parameters
        ----------
        filename : string, optional
            If indicated, the filename in which the holes informatiions are
            written. The default is None.

        Returns
        -------
        msg : str
            The string corresponding to the holes information.

        """
        if self.holes:
            col_names = ['label', 'position', 'chimney', 'radius']
            rows = []
            for hole in self.holes:
                _, chimney = hole.shape.get_endpoints_position()
                _, radius = hole.shape.get_endpoints_radius()
                rows.append([hole.label, hole.position, chimney, radius])
            msg = tabulate(rows, col_names)
        else:
            msg = 'None'
        if not filename:
            return msg
        else:
            f = open(filename, "w")
            f.write(msg)
