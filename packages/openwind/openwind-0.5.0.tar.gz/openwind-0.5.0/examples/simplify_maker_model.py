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
This example present a way to obtained a simplified geometry from a complex
geometry: here a simple spline from 10 conical parts
"""

import numpy as np
import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry, AdjustInstrumentGeometry


# creation of an arbitrary series of conical parts:
# it is the geometry which must be simplified
x_targ = np.linspace(0,.5,10)
r_targ = np.linspace(5e-3,1e-2,10) + 2e-3*np.sin(x_targ*2*np.pi)
Geom = np.array([x_targ, r_targ]).T.tolist()

# creation of a geometry which will be adjusted on the prevous one
geom_adjust = [[0, .5, 5e-3, '~5e-3', 'spline', '.15', '.3', '~5e-3', '~5e-3']]
# here it is only one spline, the parameters which are adjusted are preceded by '~'

# the corresponding InstrumentGeometry object are instanciated
mm_target_test = InstrumentGeometry(Geom)
mm_adjust_test = InstrumentGeometry(geom_adjust)

fig = plt.figure()
mm_target_test.plot_InstrumentGeometry(figure=fig, label='target')
mm_adjust_test.plot_InstrumentGeometry(figure=fig, label='initial', linestyle='--')

# the AdjustInstrumentGeometry is instanciated from the two maker models
test = AdjustInstrumentGeometry(mm_adjust_test, mm_target_test)
# the optimization process is carried out
adjusted = test.optimize_mkm(iter_detailed=False)
adjusted.plot_InstrumentGeometry(figure=fig, label='final', linestyle=':')
