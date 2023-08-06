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

class ReedModel:
    """Model of reed
    """

    def __init__(self, epsilon, pm, mr, omega02, g, y0, w, sr,
                 theta=0.25, omega_NL=316, alpha_NL=4):

        self.epsilon = epsilon
        self.mr = mr
        self.omega02 = omega02
        self.g = g
        self.y0 = y0
        self.w = w
        self.sr = sr
        self.pm = pm
        self.theta = theta
        self.omega_NL = omega_NL
        self.alpha_NL = alpha_NL

    def __valvetype__(self):
        if self.epsilon == 1:
            return('lip')
        elif self.epsilon == -1:
            return('reed')
        else:
            raise NameError('epsilon must be 1 or -1')

    def __str__(self):
        s = "ReedModel({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
        return s.format(self.valvetype(), self.pm, self.mr, self.omega02,
                        self.omega_NL, self.alpha_NL, self.g, self.y0, self.w,
                        self.sr, self.theta)

    def __repr__(self):
        return self.__str__()
