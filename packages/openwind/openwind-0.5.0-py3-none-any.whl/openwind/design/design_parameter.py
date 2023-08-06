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
Delayed evaluation and differentiation of parameters.

In the context of optimization, equation coefficients must be evaluated
and differentiated for various values of parameters (such as tube length,
hole position, etc.).

These classes allows delayed evaluation of the shape parameters, as well as
their differentiation with respect to the optimization variables.
"""

from abc import ABC, abstractmethod

import numpy as np


def eval_(params):
    """
    Evaluate a list of DesignParameters.

    Parameters
    ----------
    params : list of DesignParameter

    Returns
    -------
    list of float
        The values of each parameter.

    """
    return [p.get_value() for p in params]

def diff_(params, diff_index):
    """
    Differentiate a list of DesignParameters.

    Parameters
    ----------
    params : list of DesignParameter
    diff_index : int
        Index of the optimized parameter considered for the differentiation

    Returns
    -------
    list of float
        The values of the differentiation of each parameter w.r. to the
        designated optimized parameter.

    """
    return [p.get_differential(diff_index) for p in params]

def sigmoid(zeta):
    """
    Sigmoid function for the constraint range parameters.

    Parameters
    ----------
    zeta : float
        Real number

    Returns
    -------
    float
        The value of the sigmoid at zeta. The value is, by definition between 0
        and 1

    """
    return 0.5 + np.arctan(zeta)/np.pi

def diff_sigmoid(zeta):
    """ Derivative of the sigmoid wr to zeta"""
    return 1/(np.pi*(zeta**2 + 1))

def inv_sigmoid(x):
    """
    The inverse of the sigmoid function.

    Parameters
    ----------
    x : float
        The value of the `sigmoid`. Must be between 0 and 1

    Returns
    -------
    zeta : float
        The coordinate at which the `sigmoid` equals x.

    """
    assert np.all(x < 1) and np.all(x > 0)
    zeta = np.tan(np.pi*(x - 0.5))
    return zeta



class OptimizationParameters:
    """Manage the variable parameters for optimization.

    All the variable parameters possibly modified during the optimization
    process are associated to one value of a optimized parameter list.


    Attributes
    ----------
    values : list of float
        The value associated to each parameter
    labels : list of string
        The label of each parameter
    optimized : list of bool
        If the parameter is include (True) or not (False) in the optimization
        process
    geom_value : list of DesignParameter.get_value
        The methods used to compute the geometric value of the parameters from
        the value stored in the `OptimizationParameters.values` list.
    """

    def __init__(self):
        self.values = list()
        self.labels = []
        self.active = []
        """list of `bool` : If the parameter is include (True) or not (False)\
            in the optimization"""
        self.geom_values = []
        """list of `DesignParameter.get_value` : The methods used to compute\
            the geometric value of the parameters from the value stored in the\
            `OptimizationParameters.values` list."""

    def __str__(self):
        msg = '{:20s}|\t{:15s}|\t{:15s}|\t{:6s}\n'.format('Labels',
                                                          'Optim.Values',
                                                          'Geom.Values',
                                                          'Active')
        msg += '-'*70 + '\n'
        for k in range(len(self.labels)):
            msg += ('{:20s}|\t{:+.7e} |\t{:+.7e} |'
                    '\t{:}\n').format(self.labels[k], self.values[k],
                                      self.get_geometric_values()[k],
                                      self.active[k])
        return msg

    def __repr__(self):
        return "<{class_}: {labels}>".format(class_=type(self).__name__,
                                            labels=self.labels)

    def new_param(self, value, label, get_geom_values):
        """
        Add a new optimized parameter.

        Parameters
        ----------
        value : float
            The initial value associated to the new parameter.
        label : str
            The label of the new parameter.
        get_geom_values : DesignParameter.get_value
            The method used to compute the geometric value of the parameter
            from its stored value.

        Returns
        -------
        new_index : int
            The index at which is stored this parameters in the lists of the
            `OptimizationParameters` object.

        """
        new_index = len(self.values)
        self.values.append(value)
        self.labels.append(label)
        self.active.append(True)
        self.geom_values.append(get_geom_values)
        return new_index

    def get_geometric_values(self):
        """
        Evaluate the geometric values of the stored paramters.

        Returns
        -------
        list of float

        """
        return [get_geom() for get_geom in self.geom_values]

    def set_active_parameters(self, indices):
        """
        Chose each stored parameters is include in the optimization process.

        It modifies the `OptimizationParameters.active` attribute.

        Parameters
        ----------
        indices : 'all' or list of int
            If `"all"`, all the stored parameters are included, either only the
            parameters corresponding to the given indices are included.

        """
        if isinstance(indices, str) and indices == 'all':
            active = np.ones_like(self.active)
        else:
            active = np.zeros_like(self.active)
            active[indices] = True
        self.active = active.tolist()

    def get_active_values(self):
        """
        Return the value of the parameters included in the optim. process.

        Returns
        -------
        optim_values : list of float

        """
        optim_values = [value for (value, optim) in
                        zip(self.values, self.active) if optim]
        return optim_values

    def set_active_values(self, new_values):
        """
        Modify the value of the parameters included in the optim. process.

        It is typiccally done at each step of an optimization process.

        Parameters
        ----------
        new_values : list of float
            The list of the new values. Its length must correspond to the
            number of parameters included in the optimization process (True in
            `OptimizationParameters.active`)

        """
        values = np.array(self.values)
        values[self.active] = new_values
        self.values = values.tolist()

    def get_param(self, param_index):
        """
        Get the value of the designated parameter

        Parameters
        ----------
        param_index : int
            The index at which is stored the desired parameter.

        Returns
        -------
        float

        """
        return self.values[param_index]

    def diff_param(self, param_index, diff_index):
        """
        Differentiate the parameter with respect to one parameter.

        The result is typically 1 or 0
        The optimization
        variable designated by "diff_index"

        Parameters
        ----------
        param_index : int
            The parameter which is differentiate.
        diff_index : int
            The index of the parameter w.r. to which the differentiation is
            computed.

        Returns
        -------
        dparam : float
            The value of the differentiate: 1 if the two parameters correspond,
            0 either.
        """
        indices_active = np.where(self.active)[0]
        if param_index == indices_active[diff_index]:
            dparam = 1.
        else:
            dparam = 0.
        return dparam



# === The Different Kinds of Parameters ===


class DesignParameter(ABC):
    """Parameter of a DesignShape.

    Parent class of the different kinds of parameters."""

    @abstractmethod
    def get_value(self):
        """Current geometric value of the parameter."""

    @abstractmethod
    def get_differential(self, diff_index):
        """
        Differentiate the parameter with respect to one optimization variable.

        Parameters
        ----------
        diff_index : int
            Index of the active parameter of the `OptimizationParameters`
            considered for the differentiation.

        Return
        ---------
        float
            The value of the differentiale (Typically 1 or 0).

        """

    @abstractmethod
    def is_variable(self):
        """Variable status (Fixed: False, else: True)."""

    def __str__(self):
        return "{}".format(self.get_value())

    def __repr__(self):
        return '{label}:{class_}({value})'.format(label=self.label,
                                                  class_=type(self).__name__,
                                                  value = self.__str__())


class FixedParameter(DesignParameter):
    """Parameter with a constant value.

    Parameters
    -----------
    value : float
        The geometric value of the parameter
    label : str, optional
        The parameter's name. The default is None.

    Attributes
    ----------
    label
    """

    def __init__(self, value, label=None):
        self._value = value
        self.label = label

    def get_value(self):
        return self._value

    def get_differential(self, diff_index):
        return 0

    def is_variable(self):
        return False



class VariableParameter(DesignParameter):
    """
    Simple variable parameter.

    The geometric value equals the stored optimized value.
    Without external constraint the geometric value is a real (positive or
    negative).

    Parameters
    ----------
    value : float
        The initial geometric value of the parameter
    optim_params : OptimizationParameters
        The object where is stored the variable value
    label : str, optional
        The name of the parameter. the default is None.

    Attributes
    ----------
    label : str
    index : int
        The position at which is stored this parmeter in the
        `OptimizationParameters`
    """

    def __init__(self, value, optim_params, label=None):
        self._optim_params = optim_params
        self.index = optim_params.new_param(value, label, self.get_value)
        self.label = label

    def get_value(self):
        return self._optim_params.get_param(self.index)

    def get_differential(self, diff_index):
        return self._optim_params.diff_param(self.index, diff_index)

    def is_variable(self):
        return True

    def __str__(self):
        return "~{}".format(self.get_value())

class VariableParameterSquare(DesignParameter):
    """
    Variable parameters higher than a minimal value.

    To assure that the geometric value is higher than a minimal value, it is
    defined

    .. math::
        x = \\zeta^2 + x_{min}

    where \(\\zeta\) is the real number (positive or negative) which is stored
    and optimized.

    By this way, it is assure that \( x \\geq x_{min}\)

    Parameters
    ----------
    value : float
        The initial geometric value of the parameter
    optim_params : OptimizationParameters
        The object where is stored the variable value
    min_value : float
        The \(x_{min}\). It is forced to be higher than 1e-10 to avoid
        numerical problem.
    label : str, optional
        The name of the parameter. the default is None.

    Attributes
    ----------
    label : str
    index : int
        The position at which is stored this parmeter in the
        `OptimizationParameters`
    """

    def __init__(self, value, optim_params, min_value, label=None):
        self._optim_params = optim_params
        self.label = label
        self._min_value = np.max([min_value, 1e-10])
        if value <= self._min_value:
            raise ValueError('The initial value must be higher that the '
                             'minimal value.')
        zeta = np.sqrt(value - self._min_value)
        # zeta = np.log(value - self._min_value)
        self.index = optim_params.new_param(zeta, label, self.get_value)

    def get_value(self):
        zeta = self._optim_params.get_param(self.index)
        value = zeta**2 + self._min_value
        # value = np.exp(zeta) + self._min_value
        return value

    def get_differential(self, diff_index):
        d_zeta = self._optim_params.diff_param(self.index, diff_index)
        zeta = self._optim_params.get_param(self.index)
        return 2*zeta*d_zeta  # d_zeta*np.exp(zeta) #

    def is_variable(self):
        return True

    def __str__(self):
        return "{}<~{}".format(self._min_value, self.get_value())

class VariableParameterLimitedRange(DesignParameter):
    """
    Variable parameter limited to an authorized range.

    The parameters is defined as:

    .. math::
        x = (x_{min} - x_{max})\\Sigma(\\zeta) + x_{min}

    with \(\\zeta\) an auxiliary real number (positive or negative) stored
    and optimized. The function \(0<\\Sigma(\\zeta)<1\) is the `sigmoid`..
    By this way, it is assure that \(x \\in ]x_{min} - x_{max}[\)

    Parameters
    ----------
    value : float
        The initial geometric value of the parameter
    optim_params : OptimizationParameters
        The object where is stored the variable value
    authorized_range :  list of two float
        The boundaries \(x_{min}\) and \(x_{max}\) of the authorized range for
        this parameter.
    label : str, optional
        The name of the parameter. the default is None.

    Attributes
    ----------
    label : str
    index : int
        The position at which is stored this parmeter in the
        `OptimizationParameters`
    """

    def __init__(self, value, optim_params, authorized_range, label=None):
        self._optim_params = optim_params
        self.label = label
        self._authorized_range = authorized_range
        if (value <= np.min(authorized_range)
            or value >= np.max(authorized_range)):
            raise ValueError('The initial value is not inside the authorized '
                             'range.')
        zeta = self._get_auxiliary_var(value)
        self.index = optim_params.new_param(zeta, label, self.get_value)

    def _get_auxiliary_var(self, value):
        min_auth = np.min(self._authorized_range)
        max_auth = np.max(self._authorized_range)
        zeta = inv_sigmoid((value - min_auth)/(max_auth - min_auth))
        return zeta

    def get_value(self):
        min_auth = np.min(self._authorized_range)
        max_auth = np.max(self._authorized_range)
        zeta = self._optim_params.get_param(self.index)
        value = (max_auth - min_auth)*sigmoid(zeta) + min_auth
        return value

    def get_differential(self, diff_index):
        min_auth = np.min(self._authorized_range)
        max_auth = np.max(self._authorized_range)
        d_zeta = self._optim_params.diff_param(self.index, diff_index)
        zeta = self._optim_params.get_param(self.index)
        return (max_auth - min_auth) * d_zeta*diff_sigmoid(zeta)

    def is_variable(self):
        return True

    def __str__(self):
        return "{}<~{}<{}".format(np.min(self._authorized_range),
                                  self.get_value(),
                                  np.max(self._authorized_range))

class VariableHolePosition(DesignParameter):
    """
    Variable hole position defined relatively on the main bore pipe.

    The parameters is defined as:

    .. math::
        x = (x_{0} - x_{1})\\Sigma(\\zeta) + x_{0}

    with \(\\zeta\) an auxiliary real number (positive or negative) stored
    and optimized, \(x_{0},x_{1}\) the boundaries of the main bore pipe where
    is placed the considered hole. The function \(0<\\Sigma(\\zeta)<1\) is the
    `sigmoid`. By this way, it is assure that the hole stays on the same pipe:
    \( x \\in ]x_{0} - x_{1}[\)]

    Parameters
    ----------
    init_value : float
        The initial geometric value of the parameter
    optim_params : OptimizationParameters
        The object where is stored the variable value
    main_bore_shape :  openwind.design.design_shape.DesignShape
        The shape of the pipe where is located the hole.
    label : str, optional
        The name of the parameter. the default is None.

    Attributes
    ----------
    label : str
    index : int
        The position at which is stored this parmeter in the
        `OptimizationParameters`
    """
    def __init__(self, init_value, optim_params, main_bore_shape, label=None):
        self._optim_params = optim_params
        self.label = label
        self._main_bore_shape = main_bore_shape
        norm_position = main_bore_shape.get_xnorm_from_position(init_value)
        zeta = inv_sigmoid(norm_position)
        self.index = optim_params.new_param(zeta, label, self.get_value)

    def is_variable(self):
        return True

    def get_value(self):
        zeta = self._optim_params.get_param(self.index)
        x_norm = sigmoid(zeta)
        value = self._main_bore_shape.get_position_from_xnorm(x_norm)
        return value

    def get_differential(self, diff_index):
        d_zeta = self._optim_params.diff_param(self.index, diff_index)
        zeta = self._optim_params.get_param(self.index)

        x_norm = sigmoid(zeta)
        dx_norm = d_zeta * diff_sigmoid(zeta)

        Xmin, Xmax = eval_(self._main_bore_shape.get_endpoints_position())
        d_position = (self._main_bore_shape
                      .get_diff_position_from_xnorm(x_norm, diff_index))
        return dx_norm*(Xmax - Xmin) + d_position

    def __str__(self):
        return "~{}%".format(self.get_value())


class VariableHoleRadius(DesignParameter):
    """
    Variable hole radius defined relatively to the main bore pipe radius.

    The parameters is defined as:

    .. math::
        x = R_{main} \\Sigma(\\zeta)

    with \(\\zeta\) an auxiliary real number (positive or negative) stored
    and optimized, \(R_{main}\) the radius of the main bore pipe at the position of
    the considered hole. The function \(0<\\Sigma(\\zeta)<1\) is the `sigmoid`.
    By this way, it is assure that the hole keeps a radius smaller than the one
    of the main pipe: \(x \\leq R_{main}\)

    Parameters
    ----------
    init_value : float
        The initial geometric value of the parameter
    optim_params : OptimizationParameters
        The object where is stored the variable value
    main_bore_shape :  openwind.design.design_shape.DesignShape
        The shape of the pipe where is located the hole.
    hole_position : DesignParameter
        The position of the hole.
    label : str, optional
        The name of the parameter. the default is None.

    Attributes
    ----------
    label : str
    index : int
        The position at which is stored this parmeter in the
        `OptimizationParameters`
    """

    def __init__(self, init_value, optim_params, main_bore_shape,
                 hole_position, label=None):
        self._optim_params = optim_params
        self.label = label
        self._hole_position = hole_position
        self._main_bore_shape = main_bore_shape

        x_norm = self.__get_x_norm()
        radius_main_pipe = main_bore_shape.get_radius_at(x_norm)
        zeta = inv_sigmoid(init_value/radius_main_pipe)
        self.index = optim_params.new_param(zeta, label, self.get_value)

    def is_variable(self):
        return True

    def get_value(self):
        zeta = self._optim_params.get_param(self.index)
        x_norm = self.__get_x_norm()
        radius_main_pipe = self._main_bore_shape.get_radius_at(x_norm)
        value = radius_main_pipe * sigmoid(zeta)
        return value

    def __get_x_norm(self):
        pos = self._hole_position.get_value()
        return self._main_bore_shape.get_xnorm_from_position(pos)

    def __get_diff_x_norm(self, diff_index):
        dXmin, dXmax = diff_(self._main_bore_shape.get_endpoints_position(),
                             diff_index)
        Xmin, Xmax = eval_(self._main_bore_shape.get_endpoints_position())
        dPos = self._hole_position.get_differential(diff_index)
        Pos = self._hole_position.get_value()
        return (((dPos - dXmin)*(Xmax - Xmin) - (Pos - Xmin)*(dXmax - dXmin))
                / (Xmax - Xmin)**2)

    def get_differential(self, diff_index):
        d_zeta = self._optim_params.diff_param(self.index, diff_index)
        zeta = self._optim_params.get_param(self.index)

        x_norm = self.__get_x_norm()
        r_pipe = self._main_bore_shape.get_radius_at(x_norm)

        dx_norm = self.__get_diff_x_norm(diff_index)
        dr_pipe_dx_norm = self._main_bore_shape.get_diff_shape_wr_x_norm(x_norm)
        dr_pipe_diff_index = (self._main_bore_shape
                              .get_diff_radius_at(x_norm, diff_index))

        return (d_zeta*diff_sigmoid(zeta)*r_pipe
                + sigmoid(zeta)*dr_pipe_dx_norm*dx_norm
                + sigmoid(zeta)*dr_pipe_diff_index)

    def __str__(self):
        return "~{}%".format(self.get_value())
