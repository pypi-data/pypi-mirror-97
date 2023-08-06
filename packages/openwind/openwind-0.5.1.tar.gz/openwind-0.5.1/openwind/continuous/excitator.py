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

"""Module for the exitator classes"""

from abc import ABC, abstractmethod
import warnings

from openwind.continuous import NetlistComponent


## FLUTE
# List of flute parameters
FLUTE_PARAM = []

## FLOW
FLOW_PARAM = ["input_flow"]

## VALVE
VALVE_PARAM = ["opening", "mass","section","pulsation","dissip","width",
               "mouth_pressure","model","contact_pulsation","contact_exponent"]


class ExcitatorParameter(ABC):
    """
    Abstract class for excitator parameter
    """
    @abstractmethod
    def get_value(self,t):
        """
        Method which returns the curve value for a given t

        Parameters
        ----------
        t : float
            The time for which we want to get the curve value
        """
        pass


class VariableParameter(ExcitatorParameter):
    """
    Class for variable excitator parameter

    Parameters
    ----------
    curve : callable
        time dependant function

    """
    def __init__(self,curve):
        self._variable_value = curve

    def get_value(self,t):
        """
        Returns
        ----------
        Curve value at t: float
        """
        return self._variable_value(t)


class FixedParameter(ExcitatorParameter):
    """
    Class for fixed excitator parameter
    Parameters
    ----------
    fixed_value : float
        Fixed value for the FixedParameter
    """
    def __init__(self, curve):
        self._fixed_value = curve


    def get_value(self,t):
        """
        Returns
        ----------
        constant value : float
        """
        return self._fixed_value


class Excitator(ABC, NetlistComponent):
    def __init__(self, label, scaling, convention):
        super().__init__(label, scaling, convention)

    @abstractmethod
    def _update_fields(self, player):
        """
        This method will update all fields according to the
        player attributes

        Returns
        ----------
        default_list: list
            list of all parameters that were updated
            (for debug / verbose purpose)
        """
        pass


class Flow(Excitator):
    """
    class for a constant flow exitator
    Parameters
    ----------
    player : openwind.Player
    """
    def __init__(self, player, label, scaling, convention):
        super().__init__(label, scaling, convention)
        updated = self._update_fields(player)

    def _update_fields(self, player):
        """
        This method will update all fields according to the
        player attributes

        Returns
        ----------
        default_list: list
            list of all parameters that were updated
            (for debug / verbose purpose)
        """
        updated_list = list()
        excitator_parameters = [p for p in player.__dict__.keys()
                                if p != "_score"]
        for label in excitator_parameters:
            curve = getattr(player, label)
            if label in FLOW_PARAM:
                # must test to check if curve is constant or not
                if callable(curve):
                    setattr(self, label, VariableParameter(curve))
                else:
                    setattr(self, label, FixedParameter(curve))
                updated_list.append(label)
            elif label not in ["excitator_type"]:
                raise ValueError("Parameter '%s' not valid, must be in %s"
                      %(label, FLOW_PARAM))
        return updated_list


# TODO : write this class methods
class Flue(Excitator):
    """class for a flue excitator, to define"""
    def __init__(self, player, label, scaling, convention):
        raise NotImplementedError()


class Valve(Excitator):
    """class for valve excitator
    Parameters
    ----------
    player : openwind.Player
    """
    def __init__(self, player, label, scaling, convention):
        super().__init__(label, scaling, convention)
        updated = self._update_fields(player)

    def _update_fields(self, player):
        """
        This method will update all fields according to the
        attributes of player

        Returns
        ----------
        default_list: list
            list of all parameters that were updated
            (for debug / verbose purpose)
        """
        # TODO : ici interdire les param variables pour l instant
        updated_list = list()
        excitator_parameters = [p for p in player.__dict__.keys()
                                if p != "_score"]
        for label in excitator_parameters:
            curve = getattr(player, label)
            if label in VALVE_PARAM and label != "model":
                # must test to check if curve is constant or not
                if callable(curve):
                    # prompts an error unless the curve is mouth_pressure
                    if label != 'mouth_pressure' :
                        raise ValueError(f"Parameter {label} of Valve Excitator not supported yet, must be a constant value")
                    setattr(self, label, VariableParameter(curve))
                else:
                    setattr(self, label, FixedParameter(curve))
            elif label == "model":
                if curve in ["lips","inwards"]:
                    model_value = 1
                elif curve in ["reed","outwards"]:
                    model_value= -1
                else:
                    warnings.warn("WARNING : your model is %s, but it must "
                          "be in {'lips', 'inwards', 'reed', 'outwards'}, it "
                          "will be set to default (lips)"
                          %label)
                    model_value = 1
                setattr(self, label, FixedParameter(model_value))
            elif label not in ["excitator_type"]:
                raise ValueError("Parameter '%s' not valid, must be in %s"
                      %(label, VALVE_PARAM))

            updated_list.append(label)
        return updated_list

    def get_all_values(self, t):
        Sr = self.section.get_value(t)
        Mr = self.mass.get_value(t)
        g = self.dissip.get_value(t)
        omega02 = self.pulsation.get_value(t)**2
        w = self.width.get_value(t)
        y0 = self.opening.get_value(t)
        epsilon = self.model.get_value(t)
        pm= self.mouth_pressure.get_value(t)

        return (Sr, Mr, g, omega02, w, y0, epsilon, pm)
