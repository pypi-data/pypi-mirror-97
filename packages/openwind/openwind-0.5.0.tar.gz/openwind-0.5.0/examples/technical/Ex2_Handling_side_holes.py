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
This example shows how to add side holes to your instrument
"""

import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry

# In Ex1, we have learned how to import a geometry from a file :

# my_instrument = InstrumentGeometry("Ex2_instrument.txt")

# Most wind instruments have side holes. In OpenWind, you can define your own
# side holes for your instrument.
# This can be done either directly in the code or in a independent file.

# This file must be written in an adequate format. Please refer directly to the
# example file Ex2_holes.txt or to the help page for InstrumentGeometry for more
# information.

# To add holes to your instrument, simply add the file with the holes info in
# your InstrumentGeometry. Make sure the file with the holes is second after the main
# bore geometry.

instrument_with_holes = InstrumentGeometry("Ex2_instrument.txt", "Ex2_holes.txt" )


fig1 = plt.figure(1)
instrument_with_holes.plot_InstrumentGeometry(figure=fig1)
plt.suptitle('wind instrument with side holes')

# -----------------------------------------------------------------------------

# Side holes are useful for calculating the impedance or simulating the sound
# of your instrument for a given note, i.e., fingering. For this you need to
# specify which holes are open and which are closed.
# You can add a 'fingering chart' file to your instrument to make this step
# easier.
# Please refer to the example file Ex2_fingering_chart.txt or to the help page
# for InstrumentGeometry for more information about the formatting of this file.


# Simply add the fingering chart as third file for the InstrumentGeometry :
complete_instrument = InstrumentGeometry("Ex2_instrument.txt",
                                 "Ex2_holes.txt",
                                 "Ex2_fingering_chart.txt")

# With a fingering chart, you can plot the instrument for a given note :

fig2 = plt.figure(2)
complete_instrument.plot_InstrumentGeometry(figure=fig2, note='E')
plt.suptitle('wind instrument with side holes (closed holes are filled)')


# -----------------------------------------------------------------------------
# This instrument is now fully ready to be used in simulations !
