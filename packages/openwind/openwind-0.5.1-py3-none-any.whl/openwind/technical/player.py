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
Module for the Player class
"""

import matplotlib.pyplot as plt
import numpy as np
import pdb
from openwind.technical import default_excitator_parameters as EXCITATOR_DEFAULTS
from openwind.technical import Score


AVAILABLE_DEFAULTS = [p for p in EXCITATOR_DEFAULTS.__dict__.keys() if
                      p[0] != "_" and p not in
                      ["np","constant_with_initial_ramp", "dirac_flow",
                       "triangle"]]


class Player:
    """
    class for a player

    Parameters
    ----------
    dict_key: str, optional
        This is the name of the default dictionnary that will be given to Player
        Default dictionnary can be found in technical/parameters.py
        Player's constructor will parse the default dictionnary entries into
        attributes. The default is 'UNITARY_FLOW'.
    note_events : List[(string, float)], optional
        List of note events: tuples with the note name and the starting
        time of the note. The default is an emtpy list.
    transition_duration: float, optional
        The transition duration between notes. The default is 0.02
    """

    def __init__(self, dict_key='UNITARY_FLOW', note_events=[],
                 transition_duration=.02):
        # read the default_dict from parameters that has the name dict_key
        for label, curve in getattr(EXCITATOR_DEFAULTS, dict_key).items():
            # creates attibutes whose names are the keys of the default dict
            # eg. "opening", "mass" for the dict_key "REED"
            setattr(self, label, curve)
        self._score = Score(note_events, transition_duration)

    def set_defaults(self, dict_key):
        """
        Method which updates the player attributes values with a default dict
        stored in technical/parameters.py

        """
        # Check that user input exists
        try:
            for label, curve in getattr(EXCITATOR_DEFAULTS, dict_key).items():
                self.update_curve(label, curve)
        except AttributeError as e:
            raise ValueError(
                "Available default parameters are %s" %AVAILABLE_DEFAULTS
                ) from e

    def update_score(self, note_events, transition_duration=None):
        """
        Update the score

        Parameters
        ----------
        note_events : List[(string, float)]
            List of note events: tuples with the note name and the starting
            time of the note
        transition_duration : float, optional
            The new transition duration between notes, if none, do not change
            the value. The default is None.
        """
        self._score.set_note_events(note_events)
        if transition_duration:
            self._score.set_transition_duration(transition_duration)

    def get_score(self):
        """
        Return the score

        Returns
        -------
        openwind.technical.score.Score
        """
        return self._score

    def update_curve(self, label, new_curve):
        # first we check that we update an existing label:
        if hasattr(self, label):
            # check if we are updating "excitator_type" (label == "excitator_type")
            if label == "excitator_type":
                # Prevent user from changing the excitator_type
                if self.excitator_type != new_curve:
                    raise ValueError(
                          "ERROR: you are trying to change the excitator type "
                          "from %s to %s, but this is forbidden. "
                          "You must create a new Player instance and add it to "
                          "your InstrumentPhysics instance instead"
                          %(self.excitator_type, new_curve))
            else:
                setattr(self, label, new_curve)
        else:
            raise ValueError("%s has no attribute %s, please check your label"
                             %(self,label))

    def update_curves(self, dict_):
        """Update several curves."""
        for label, new_curve in dict_.items():
            self.update_curve(label, new_curve)

    @classmethod
    def print_defaults(cls):
        #pdb.set_trace()
        print("Available default parameters are %s" %AVAILABLE_DEFAULTS)
        # print("\n Advanced usage : you can add your own default dictionnary to"
        #       " openwind/technical/parameters.py\n")

    def plot_one_control(self, label, time, ax=None):
        """
        Plot one control curve

        Parameters
        ----------
        label : string
            The name of the control plotted.
        time : np.array
            The time axis.
        ax : matplotlib.axes, optional
            The axes on which plot the curve. The default is None.
        """
        _curve = getattr(self, label)
        if callable(_curve):
            ys = _curve(time)
        else:
            ys = _curve * np.ones_like(time)
        if not ax:
            fig = plt.figure()
            ax = fig.add_subplot()
        ax.plot(time, ys)
        ax.set_xlabel('Time')
        ax.set_ylabel(label)

    def plot_controls(self, time):
        """
        Plot all the controle curves of the player.

        Parameters
        ----------
        time : np.array
            The time axis.
        """
        title = self.excitator_type
        if title.lower() == 'valve':
            title += ', ' + self.model
        curves = [p for p in self.__dict__.keys() if p != "_score"
                  and p != "excitator_type" and p != "model"]
        n_row = len(curves) + 1
        fig = plt.figure()
        ax = [fig.add_subplot(n_row, 1, 1)]
        self._score.plot_score(time, ax[0])
        for k, label in enumerate(curves):
            ax.append(fig.add_subplot(n_row, 1, k+2, sharex=ax[0]))
            self.plot_one_control(label, time, ax[k+1])
        plt.show()
        fig.suptitle(title)

    def __repr__(self):
        msg = 'dict_key={'
        excitator_labels = [p for p in self.__dict__.keys() if p != "_score"]
        for label in excitator_labels[:-1]:
            msg += "{}:{}, ".format(label, self.__dict__[label])
        msg += "{}:{}}}".format(excitator_labels[-1], self.__dict__[excitator_labels[-1]])
        return "<openwind.Player({}, {})>".format(msg, repr(self._score))

    def __str__(self):
        msg = "Player:\nExcitator:\n"
        excitator_labels = [p for p in self.__dict__.keys() if p != "_score"]
        for label in excitator_labels:
            msg += "\t{}: {}\n".format(label, self.__dict__[label])
        msg += str(self._score)
        return msg

    def display(self):
        print(repr(self))
