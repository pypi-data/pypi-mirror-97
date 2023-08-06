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

import numpy as np
from numpy import pi, sqrt, sign
from openwind.continuous import PhysicalJunction, Physics, PhysicalRadiation, ThermoviscousLossless


from openwind.design import Cone
import warnings


class JunctionHoleTMM(PhysicalJunction):


    def __init__(self, design_shape, temperature, label, scaling, losses, rad_model,
                 convention='PH1',
                 spherical_waves=False, matching_volume=False):
        super().__init__(label, scaling, convention)

        self._design_shape = design_shape
        self._losses = losses
        self._physics = Physics(temperature)
        self._spherical_waves = spherical_waves
        self.matching_volume = matching_volume
        self.set_radiation(rad_model)

        if (type(self._design_shape) != Cone or
            not(self._design_shape.is_cylinder())):
            raise ValueError('Only cylindrical chimney can be used.')


    def is_spherical_waves(self):
        """
        Are the wave fronts spherical or plane.

        Returns
        -------
        boolean
            True if spherical waves are assumed, False either.
        """
        return self._spherical_waves

    def get_losses(self):
        """
        Return the losses associated to this pipe.

        Returns
        -------
        openwind.continuous.thermoviscous_models.ThermoviscousModel
            How to take into account thermoviscous losses.
        """
        return self._losses

    def get_scaling(self):
        """
        Return the scaling use for the equations coefficients.

        Returns
        -------
        openwind.continuous.scaling.Scaling
            object which knows the value of the coefficient used to scale the
            equations
        """
        return self.scaling

    def get_physics(self):
        """
        Return the `openwind.continuous.physics.Physics` attached to the pipe.

        Returns
        -------
        `openwind.continuous.physics.Physics`
            This object computes the values of the physical constant (the air
            density, the sound celerity, etc.) along the pipe with respect to
            the temperature.

        """
        return self._physics

    def get_convention(self):
        """
        Return the convention used for this pipe.

        The basis functions for our finite elements must be of regularity
        H1 for one variable, and L2 for the other.
        Regularity L2 means that some degrees of freedom are duplicated
        between elements, whereas they are merged in H1.
        Convention chooses whether P (pressure) or V (flow) is the H1
        variable.

        Returns
        -------
        {'PH1', 'VH1'}
        """
        return self.convention

# %% ----------Geometry------------

    def get_endpoints_position_value(self):
        """
        Return the end points position value in meter along the main bore axis.

        For the holes, the two end points position are equal and correspond to
        the hole position.
        These value are used to construct the graph.

        Returns
        -------
        xmin, xmax : float
            The two end points positions along the main bore axis.
        """
        posmin, posmax = self._design_shape.get_endpoints_position()
        xmin = posmin.get_value()
        xmax = posmax.get_value()
        return xmin, xmax

    def get_radius(self,):
        """ Gives the value of the radius of the chimney hole

        Value is in meters (not nondimensionalized).

        Returns
        -------
        radius: float
            The radius of the chimney hole.
        """
        return self._design_shape.get_radius_at(0)

    def get_length(self):
        """
        Give the length of the pipe in meter.

        Returns
        -------
        float
            The length of the pipe in meter.

        """
        return self._design_shape.get_length()

    def get_scaling_masses(self):
        """
        Get the scaling coefficient for acoustic mass.

        Returns
        -------
        flaot
            The scaling coefficient

        """
        return self.scaling.get_impedance() * self.scaling.get_time()
    # %%

    def set_radiation(self, rad_model):
        rad_label = self.label + '_radiation'
        self.radiation = PhysicalRadiation(rad_model, rad_label,self.scaling,
                                           self.convention)


    def compute_masses(self, r_main, r_side, rho):
        """Compute mass matrix of a Junction from physical parameters.

        Parameters
        ----------
        r_main : float
            Radius of the main pipe, at the point of junction
        r_side : float
            Radius of the side pipe, at the point of junction
        rho : float
            Air density, at the point of the junction
        """
        assert r_main > 0
        assert r_side > 0
        if r_main < r_side:
            msg = ("The radius of the main pipe cannot be smaller"
                   " than that of a side pipe !")
            # raise ValueError(msg)
            warnings.warn(msg)

        coef_scaling_masses = self.get_scaling_masses()
        a = r_main  # Radius of the main pipe
        b = r_side  # Radius of the hole
        d = b/a
        t_s = b*(0.82 - 0.193*d - 1.09*d**2 + 1.27*d**3 - 0.71*d**4)
        if self.matching_volume:
            t_s += b*d/8*(1 + .207*d)
        m_s = rho*t_s/(pi*b**2) / coef_scaling_masses
        t_a = b*(-0.37 + 0.087*d)*d**2
        m_a = rho*t_a/(pi*a**2) / coef_scaling_masses

        m11 = m_s + m_a/4
        m12 = m_s - m_a/4

        return m_s, m_a
