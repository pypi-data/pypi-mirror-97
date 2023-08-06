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
Fingering chart for a given instrument.
"""

import numpy as np
import matplotlib.pyplot as plt
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


class FingeringChart:
    """
    Fingering chart for a given instrument.

    This class instanciates the `Fingering` objects for each fingering of the
    fingering chart.

    Parameters
    ----------
    note_names : list of str, optional
        The list of the note names. The default is an empty list.
    hole_names : list of str, optional
        The list of the hole names. The default is an empty list.
    chart : np.array, optional
        Opening factor for each hole. 0 is closed, 1 is open. Its dimension
        must be consistent with the note_names and hole_names length.
        The default is an empty list.
    other_holes : list of str, optional
        Names of holes that exist in the instrument, but not indicated in the
        fingering chart because always remain open.

    See Also :
    ----------
    `Fingering`

    """

    def __init__(self, note_names=[], hole_labels=[], chart=[],
                 other_holes=[]):
        chart = np.array(chart)
        if (chart.shape != (len(hole_labels), len(note_names))
            and chart.shape != (0,)):
            raise ValueError('The chart dimensions are not consistent with the'
                             ' number of holes and notes.')
        if np.any(chart < 0) or np.any(chart > 1):
            raise ValueError('The chart coefficient must be within 0 and 1')
        self._notes = note_names
        self._holes = hole_labels
        self._chart = chart
        self._other_holes = other_holes
        self._current_note = 'None'

    def fingering_of(self, note):
        """
        Instanciate the `Fingering` object for the given note.

        Parameters
        ----------
        note : str
            The label of the note as indicated in the fingering chart.

        Returns
        -------
        Fingering
            The fingering associate ot the note.

        """
        if note not in self._notes:
            raise ValueError("Unknown note '{}'".format(note))
        self._current_note = note
        opening_factors = self._chart[:, self._notes.index(note)]
        return Fingering(self, opening_factors)

    def get_current_note(self):
        """
        Returns
        -------
        string
            The note name corresponding to the fingering currently applied
        """
        return self._current_note

    def all_notes(self):
        """
        Give the labels of all the note of the fingering chart.

        Returns
        -------
        List of str
            The list of the note labels.

        """
        return self._notes

    def __str__(self):
        if len(self._notes) > 0:
            col_names = ['label'] + self._notes
            chart = [['o' if s else 'x' for s in row] for row in self._chart]
            rows = [[hole] + list(chart_row)
                    for hole, chart_row in zip(self._holes, chart)
                    ]
            return tabulate(rows, col_names)
        else:
            return "None"

    def __repr__(self):
        return '<openwind.technical.FingeringChart(note_names={})>'.format(self._notes)

    def plot_chart(self, figure=None,  open_only=False, **kwargs):
        """
        Plot the fingering chart.

        Each fingering is plotted vertically. The open holes are plotted with
        'o' and the closed ones, with 'x'.

        Parameters
        ----------
        figure : figure, optional
            If indicated the figure one which is plotted the chart. The default
            is None.
        open_only : boolean, optional
            If true, plot only the open holes. The default is False.
        kwargs :
            Additional arguments are passed to the `plt.plot` function..

        Returns
        -------
        None.

        """
        if not figure:
            fig = plt.figure()
        else:
            fig = figure
        ax = fig.get_axes()
        if len(ax) < 1:
            ax.append(fig.add_subplot(1, 1, 1))

        holes_tot = self._holes + self._other_holes
        x = np.arange(0, len(self._notes))
        y = np.arange(0, len(holes_tot))
        xx, yy = np.meshgrid(x, y)

        fing_array = list()
        for note in self._notes:
            finger = self.fingering_of(note)
            one_fing = list()
            for hole in holes_tot:
                one_fing += ([bool(finger.is_hole_open(hole))])
            fing_array.append(one_fing)
        fing_array = np.array(fing_array).T
        ax[0].plot(xx[fing_array], yy[fing_array], 'o', **kwargs)
        if not open_only:
            ax[0].plot(xx[~fing_array], yy[~fing_array], 'x', **kwargs)
        if not figure:
            ax[0].set_xticks(range(len(self._notes)))
            ax[0].set_xticklabels(self._notes)
            ax[0].set_yticks(range(len(holes_tot)))
            ax[0].set_yticklabels(holes_tot)
            ax[0].invert_yaxis()
            ax[0].grid(True)



class Fingering:
    """
    One fingering position.

    To each hole, associates its opening factor
    (0 if closed, 1 if open).
    """
    def __init__(self, chart, opening_factors):
        """
        Parameters
        ----------
        chart: FingeringChart
            The fingering chart from which this fingering derives.
        opening_factors: numpy.array
            The array of opening factor for each hole.

        """
        assert len(chart._holes) == len(opening_factors)
        self._chart = chart
        self._opening_factors = opening_factors

    def apply_to(self, components):
        """Apply this fingering to this dict of components.

        Modify the radiation condition of a set of components by following the
        fingering.
        Assumes the key of the correct radiation components is
        'rad_{hole_label}', and that it has a method
        `set_opening_factor(factor)`.

        Parameters
        ----------
        components: list of [ openwind.frequential.frequential_component.FrequentialComponent ] or [ openwind.temporal.tcomponent.TemporalComponent ]
            List of components at which are apllied the fingering.
        """
        for hole_label, factor in zip(self._chart._holes, self._opening_factors):
            rad_label = 'rad_' + hole_label
            components[rad_label].set_opening_factor(factor)

    def is_hole_open(self, hole_label):
        """Give the opening state of a hole.

        Parameters
        ----------
        hole_label : string
            The name of the hole considered.

        Returns
        -------
        boolean or float within 0 and 1
            The opening factor of the hole..

        """
        if hole_label in self._chart._other_holes:
            return True
        return self._opening_factors[self._chart._holes.index(hole_label)]

    def __str__(self):
        return tabulate([['o' if s else 'x' for s in self._opening_factors]],
                        self._chart._holes)

    def mix(self, other, factor):
        """Create intermediate fingering between this and other.

        Parameters
        ----------
        other : Fingering
            The other fingering with which this one is mixed.
        factor : float
            Mixing factor, between 0 (this fingering) and 1 (other fingering).
        """
        assert isinstance(other, Fingering)
        assert other._chart is self._chart  # Must be from same FingeringChart
        mixed_factors = (factor * other._opening_factors
                         + (1-factor) * self._opening_factors)
        return Fingering(self._chart, mixed_factors)
