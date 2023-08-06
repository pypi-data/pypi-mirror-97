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
This example shows how to use your own instrument geometries in OpenWind
"""

import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry


# In OpenWind, an instrument is described by its bore, i.e., the radius of the
# main pipe along its length.

# For instruments consisting only of conical parts, the information can consist
# in a list of coordinates (x,r), with x the abscissa along the linearized bore
# length (measured from the mouth-end of the instrument), and r the radius at
# this abscissa, in meters.

# Then, use the InstrumentGeometry module to create the OpenWind model of your
# instrument.


# -----------------------------------------------------------------------------
# For example, you can write the geometry directly in the OW code :
#           x [meters]       r [meters]
my_bore = [[0.0000000e+00, 8.4000000e-03],
           [1.2000000e-02, 2.4195678e-03],
           [1.7734052e-02, 1.8250000e-03],
           [8.3704052e-02, 4.2000000e-03],
           [3.0370405e-01, 5.8200000e-03],
           [1.0227041e+00, 7.3900000e-03],
           [1.2977041e+00, 1.4375000e-02],
           [1.4187041e+00, 6.1000000e-02]]

instrument_1 = InstrumentGeometry(my_bore)

# you can visualize the bore :
fig1 = plt.figure(1)  # create new figure
instrument_1.plot_InstrumentGeometry(figure=fig1)  # plot the instrument
plt.title('a simple instrument')  # add a title to the plot


# -----------------------------------------------------------------------------
# For large and/or detailed instruments, this list can grow very fast. OpenWind
# can therefore also import text files to make a model of the instrument.
# Note that the files parsed by this methods must be in csv format, with
# columns separated by spaces and/or tabs. First column is the linearized
# absissa, second column is the radius. Comments start with #. Empty lines are
# ignored.

file = 'Ex1_instrument_2.txt'
instrument_2 = InstrumentGeometry(file)

fig2 = plt.figure(2)  # create new figure
instrument_2.plot_InstrumentGeometry(figure=fig2)  # plot the instrument
plt.title('instrument from file')  # add a title to the plot


# -----------------------------------------------------------------------------
# Some shapes are not easily described by conical parts. OpenWind supports
# different types of shapes, that can easilly be mixed together in the same
# instrument.
# Each of these shape need to be defined in a precise way ('Formatting')
#  The different shapes are :
# - 'linear' : conical portion (same as above). Formatting : [x1, x2, r1, r2] ;
#              Draws a straight line between [x1, r1] and [x2, r2]

# - 'circle' : an arc of a circle. Formatting : [x1, x2, r1, r2, 'circle', R]
#              Draws an arc between [x1, r1] and [x2, r2] with radius R

# - 'exponential' : Formatting [x1, x2, r1, r2, 'exponential'] ;
#              Draws an exponential line between [x1, r1] and [x2, r2]

# - 'Bessel' : Formatting [x1, x2, r1, r2, 'bessel', alpha] ;
#              Draws a line based on a Bessel function, where alpha is the
#              coefficient of the bessel (=power)

# - 'spline' : Smooth function with control points.
#              Formatting [x1, x2, r1, r2, 'spline', x3,..., xN, r3,..., rN] ;
#              Draws a smooth line between [x1, r1] and [x2, r2], passing
#              through the control points (x3, r3) ... (xN, rN)

# load the instrument from the file :
instrument_3 = InstrumentGeometry('Ex1_instrument_3.txt')

fig3 = plt.figure(3)  # create new figure
instrument_3.plot_InstrumentGeometry(figure=fig3)  # plot the instrument
plt.title('a more complicated and smooth instrument')  # add a title


# -----------------------------------------------------------------------------
# Handling instrument side holes is the topic of Example 2 !
