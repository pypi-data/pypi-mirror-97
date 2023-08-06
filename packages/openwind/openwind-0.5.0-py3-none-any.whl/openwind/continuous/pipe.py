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

from openwind.continuous import Physics
from openwind.continuous import ThermoviscousLossless

class Pipe:
    """A simple waveguide, described by its bore profile (shape) and its
    temperature. It may compute the coefficients of the telegraphist
    equations (wave propagation) with or without losses. It may have a variable
    section and variable temperature.

    In the frequential domain, the telegraphist equations are [1]_:

    .. math::
        Y_t(\\omega, x)  p + d_x u = 0, \\\\
        Z_v(\\omega, x)  u + d_x p = 0.

    where:

    - \(u\) is the scaled flow
    - \(p\) is the scaled pressure
    - \(x\) is the scaled position ( \(0 \\leq x \\leq 1\) ),
    - \(\\omega\) is the scaled angular frequency,

    And the coefficients

    .. math::
        Y_t(\\omega, x) = j \\omega \\left( \\frac{1}{Y_t^{\\ast}} \
        \\frac{S}{\\rho c^2} \\ell + \\text{Losses}_p(\\omega, x)  \\right) \\\\
        Z_v(\\omega, x) = j \\omega\\left( \\frac{1}{Z_v^{\\ast}}  \
        \\frac{\\rho}{S} \\ell + \\text{Losses}_u(\\omega, x) \\right)

    where :

    - \(S(x)\) is the cross section area at the \(x\) position
    - \(\\rho\) is the air density at the \(x\) position
    - \(c\) is the sound celerity at the \(x\) position
    - \(\\ell\) is the length of the pipe
    - \(Y_t^{\\ast}\) is the scaling coefficient of the pressure
    - \(Z_v^{\\ast}\) is the scaling coefficient of the flow
    - \(\\text{Losses}(\\omega, x)\) are the losses terms computed by the \
        `openwind.continuous.thermoviscous_models.ThermoviscousModel` object. \
        It must include the scaling chosen.

    In temporal domain, even if the physical coefficients are similar, the
    equations are slightly different due to the losses reformulation.

    Parameters
    ----------
    design_shape : openwind.design.design_shape.DesignShape
        The shape of the bore profile of the pipe
    temperature : float of callable
        The temperature allong the pipe (if float it is considered uniform)
    label : str
        the label of the pipe
    scaling : openwind.continuous.scaling.Scaling
        object which knows the value of the coefficient used to scale the
        equations
    losses : openwind.continuous.thermoviscous_models.ThermoviscousModel
        How to take into account thermoviscous losses
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

    Attributes
    ---------
    label : str
        The pipe name

    References
    -----------
    .. [1] R. Tournemenne et J. Chabassier, "A comparison of a one-dimensional
       finite element method and the transfer matrix method for the
       computation of wind music instrument impedance." Acta Acustica united
       with Acustica 105.5 (2019): 838-849.
    """

    def __init__(self, design_shape, temperature, label, scaling,
                 losses, convention='PH1', spherical_waves=False):
        self._design_shape = design_shape
        self.label = label
        self._losses = losses
        self._convention = convention
        self._physics = Physics(temperature)
        self._scaling = scaling
        self._spherical_waves = spherical_waves
        if spherical_waves:
            try:
                design_shape.get_diff_shape_wr_x_norm(0.0)
            except NotImplementedError:
                msg = ("Spherical waves not available for "
                       "shape type '{}'.")
                raise ValueError(msg.format(type(design_shape).__name__))

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
        return self._scaling

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
        return self._convention

# %% ----------Geometry------------
    def get_shape(self):
        """
        Return the shape of this pipe.

        Returns
        -------
        openwind.design.design_shape.DesignShape
        """
        return self._design_shape

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

    def get_radius_at(self, x):
        """ Gives the value of the radius at the normalized positions 'x'

        Value is in meters (not nondimensionalized).

        Parameters
        ----------
        x : float or array(float)
            Normalized position along the pipe within 0 and 1.

        Returns
        -------
        radius: same shape as `x`
            The radius at positions `x` in meter.
        """
        return self._design_shape.get_radius_at(x)

    def get_conicity_at(self, x):
        """Local variation of radius with respect to position.

        Zero for a cylinder, constant for a cone, 1 for a 45° cone,
        variable for a non-conical shape.
        Conicity is a dimensionless number.

        Parameters
        ----------
        x : float or array(float)
            Normalized position along the pipe.

        Returns
        -------
        conicity: same shape as `x`
            The variation of radius with respect to (absolute) abscissa,
            measured at positions `x`.
        """
        return self._design_shape.get_diff_shape_wr_x_norm(x) / self.get_length()

    def get_section_at(self, x):
        """
        Gives the value of the section at the normalized positions 'x' in m².

        Parameters
        ----------
        x : float or array(float)
            Normalized position along the pipe within 0 and 1.

        Returns
        -------
        same shape as `x`
            The cross section area at positions `x` in meter squared.

        """
        return np.pi * self.get_radius_at(x)**2

    def get_length(self):
        """
        Give the length of the pipe in meter.

        Returns
        -------
        float
            The length of the pipe in meter.

        """
        return self._design_shape.get_length()
# %% ---------- PHYSICAL EQUATION ----------
# ----- SCALING -----
    def get_scaling_flow(self):
        """Scaling coefficient associated to the flow equation.

        This coefficient is used to nondimensionalize \(Z_v\):

        .. math::
            Z_v^{\\ast} = Z_c^{\\ast}  T^{\\ast}

        where:

        - \(Z_c^{\\ast}\) : the reference caracteristic impedance
        - \(T^{\\ast}\) : the reference time

        Returns
        -------
        float
            The coefficient \(Z_v^{\\ast}\)

        See Also:
        --------
        `openwind.continuous.scaling.Scaling`
        """
        return self._scaling.get_impedance() * self._scaling.get_time()

    def get_scaling_pressure(self):
        """
        Scaling coefficient associated to the pressure equation.

        This coefficient is used to nondimensionalize \(Y_t\):

        .. math::
            Y_t^{\\ast} = \\frac{T^{\\ast}}{Z_c^{\\ast}}

        where:

        - \(Z_c^{\\ast}\) : the reference caracteristic impedance
        - \(T^{\\ast}\) : the reference time

        Returns
        -------
        float
            The coefficient \(Y_t^{\\ast}\)

        See Also:
        --------
        `openwind.continuous.scaling.Scaling`
        """
        return self._scaling.get_time() / self._scaling.get_impedance()

# ----- TELEGRAPHISTE EQUATION -----
    def get_coef_flow_at(self, x):
        """
        Coefficient without losses associated to the flow.

        Gives the values of the part of coefficient associated to the flow in
        the scaled telegraphist equations independant of the frequency and
        without losses at the normalized position "x":
        $$ \\frac{1}{Z_v^{\\ast}} \\frac{\\rho}{S} \\ell $$

        .. warning::
            This method is used when the equations solved can not be written
            with a \(Z_v\) e.g. in the temporal domain and/or when the losses
            are include trough auxillary variables.

        Parameters
        ----------
        x : float or array(float)
            Normalized position along the pipe within 0 and 1.

        Returns
        -------
        float or array(float), same shape as x
            The value of the coefficient at positions `x`.

        See Also :
        ----------
        `openwind.frequential.frequential_pipe_diffusive_representation.FrequentialPipeDiffusiveRepresentation`
        `openwind.temporal.tpipe.TemporalPipe`
        """
        section = np.pi * (self.get_radius_at(x))**2
        rho = self._physics.rho(x)
        coef = (rho / section) * self.get_length() / self.get_scaling_flow()
        if self._spherical_waves:
            coef *= np.sqrt(1 + self.get_conicity_at(x)**2)
        return coef

    def get_coef_pressure_at(self, x):
        """
        Coefficient without losses associated to the pressure.

        Gives the values of the part independant of the frequency of the
        coefficient associated to the pressure in the scaled telegraphist
        equations without losses at the normalized position "x":
        $$ \\frac{1}{Y_t^{\\ast}} \\frac{S}{\\rho c^2} \\ell $$

        .. warning::
            This method is used when the equations solved can not be written
            with a \(Y_t\) e.g. in the temporal domain and/or when the losses
            are include trough auxillary variables.

        Parameters
        ----------
        x : float or array(float)
            Normalized position along the pipe within 0 and 1.

        Returns
        -------
        float or array(float), same shape as x
            The value of the coefficient at positions `x`.

        See Also :
        ----------
        `openwind.frequential.frequential_pipe_diffusive_representation.FrequentialPipeDiffusiveRepresentation`
        `openwind.temporal.tpipe.TemporalPipe`
        """
        section = np.pi * (self.get_radius_at(x))**2
        rho_c2 = self._physics.rho(x) * self._physics.c(x)**2
        coef = (section / rho_c2) * self.get_length() / self.get_scaling_pressure()
        if self._spherical_waves:
            coef *= np.sqrt(1 + self.get_conicity_at(x)**2)
        return coef

# ------ FULL FREQUENTIAL COEFFICIENTS ------

    def get_Zv_at(self, x, omegas_scaled):
        """
        Flow coefficent in the frequential equation.

        Give the value of the flow coefficient \(Z_v\) estimated at the given
        normalized positions for the given normalized angular frequencies:
        $$Z_v(\\omega, x) = j \\omega \\left( \\frac{1}{Z_v^{\\ast}} \
            \\frac{\\rho}{S} \\ell + \\text{Losses}_u(\\omega, x) \\right)$$


        .. warning::
            The losses must include the scaling term \(Z_v^{\\ast}\)

        Parameters
        ----------
        x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        omegas_scaled : float or array(float)
            Normalized angular frequencies.

        Returns
        -------
        np.array(float)
            The value of the coefficient at each position and each angular
            frequency.

        """
        Zv_wo_losses = self.get_coef_flow_at(x)[np.newaxis, :]
        losses_u = self.get_losses().get_loss_flow_at(self, x, omegas_scaled)
        return 1j*omegas_scaled[:, np.newaxis]*(Zv_wo_losses + losses_u)

    def get_Yt_at(self, x, omegas_scaled):
        """
        Pressure coefficent in the frequential equation.

        Give the value of the pressure coefficient \(Y_t\) estimated at the given
        normalized positions for the given normalized angular frequencies:
        $$Y_t(\\omega, x) = j \\omega \\left( \\frac{1}{Y_t^{\\ast}} \
        \\frac{S}{\\rho c^2} \\ell + \\text{Losses}_p(\\omega, x)  \\right)$$

        .. warning::
            The losses must include the scaling term \(Y_t^{\\ast}\)

        Parameters
        ----------
        x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        omegas_scaled : float or array(float)
            Normalized angular frequencies.

        Returns
        -------
        np.array(float)
            The value of the coefficient at each position and each angular
            frequency.

        """
        Yt_wo_losses = self.get_coef_pressure_at(x)[np.newaxis, :]
        losses_p = self.get_losses().get_loss_pressure_at(self, x,
                                                          omegas_scaled)
        return 1j*omegas_scaled[:, np.newaxis]*(Yt_wo_losses + losses_p)

# %% ---------- DIFFERENTIATION ----------

    def get_diff_length(self, diff_index):
        """
        Differentiate the length w.r. to the designated optimization parameter.

        Parameters
        ----------
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float
            The value of the differential, in meters per unit of diff_index.

        """
        return self._design_shape.get_diff_length(diff_index)

    def get_diff_radius_at(self, x, diff_index):
        """
        Differentiate the radius w.r. to the designated optimization parameter.

        Gives the differential of the radius with respect to the design
        variables designated by "diff_index" at the normalized positions "x".

        Parameters
        ----------
         x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float
            The value of the differential, in meters per unit of diff_index.
        """
        return self._design_shape.get_diff_radius_at(x, diff_index)

    def get_diff_endpoints_position(self, diff_index):
        """
        Differentiate the end points w.r. to the designated optimization
        parameter.

        The end points position along the main bore axis are differentiated
        with respect to the designated optimization parameter.

        Parameters
        ----------
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float
            The value of the differential, in meters per unit of diff_index.

        """
        posmin, posmax = self._design_shape.get_endpoints_position()
        dxmin = posmin.get_differential(diff_index)
        dxmax = posmax.get_differential(diff_index)
        return dxmin, dxmax

    def get_diff_coef_flow_at(self, x, diff_index):
        """
        Differentiate the flow coefficient without losses.

        Gives the differential with respect to the design variables
        designated by "diff_index", of the coefficient associated to the flow
        in the scaled telegraphist equations without lossesat the normalized
        positions "x".

        Parameters
        ----------
        x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float or array(float), same shape as x
            The value of the differential at the given positions.
        """
        radius = self.get_radius_at(x)
        diff_radius = self.get_diff_radius_at(x, diff_index)
        partial_wr_radius = -2*diff_radius/radius * self.get_coef_flow_at(x)

        diff_length = self.get_diff_length(diff_index)
        partial_wr_length = diff_length/self.get_length() * self.get_coef_flow_at(x)
        return partial_wr_radius + partial_wr_length

    def get_diff_coef_pressure_at(self, x, diff_index):
        """
        Differentiate the pressure coefficient without losses.

        Gives the differential with respect to the design variables
        designated by "diff_index" of the coefficient associated to the
        pressure in the scaled telegraphist equations without losses at the
        normalized positions "x".

        Parameters
        ----------
        x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float or array(float), same shape as x
            The value of the differential at the given positions.
        """
        radius = self.get_radius_at(x)
        diff_radius = self.get_diff_radius_at(x, diff_index)
        partial_wr_radius = 2*diff_radius/radius * self.get_coef_pressure_at(x)

        diff_length = self.get_diff_length(diff_index)
        partial_wr_length = diff_length/self.get_length() * self.get_coef_pressure_at(x)
        return partial_wr_radius + partial_wr_length

    def get_diff_Zv_at(self, x, omegas_scaled, diff_index):
        """
        Differentiate the flow coefficient with losses in frequential equation.

        Give the differential of the coefficient \(Z_v\) in the telegraphist
        equations with respect to the designated optimization parameter at the
        given normalized positions and normalized angular frequencies.

        Parameters
        ----------
         x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        omegas_scaled : float or array(float)
            Normalized angular frequencies.
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float or array(float), same shape as x
            The value of the differential at the given positions and angular
            frequencies.

        """
        d_Zv_wo_losses = self.get_diff_coef_flow_at(x, diff_index)[np.newaxis, :]
        d_losses_u = self.get_losses().get_diff_loss_flow(self, x,
                                                          omegas_scaled,
                                                          diff_index)
        return 1j*omegas_scaled[:, np.newaxis]*(d_Zv_wo_losses + d_losses_u)

    def get_diff_Yt_at(self, x, omegas_scaled, diff_index):
        """
        Differentiate the pressure coefficient with losses.

        Give the differential of the coefficient \(Y_t\) in the telegraphist
        equations with respect to the designated optimization parameter at the
        given normalized positions and normalized angular frequencies.

        Parameters
        ----------
         x : float or array(float)
            Normalized positions along the pipe within 0 and 1.
        omegas_scaled : float or array(float)
            Normalized angular frequencies.
        diff_index : int
            The index of the desire design parameter in the \
            `openwind.design.design_parameter.OptimizationParameters`.

        Returns
        -------
        float or array(float), same shape as x
            The value of the differential at the given positions and angular
            frequencies.
        """
        d_Yt_wo_losses = self.get_diff_coef_pressure_at(x, diff_index)[np.newaxis, :]
        d_losses_p = self.get_losses().get_diff_loss_pressure(self, x,
                                                              omegas_scaled,
                                                              diff_index)
        return 1j*omegas_scaled[:, np.newaxis]*(d_Yt_wo_losses + d_losses_p)
