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
Deal the temporal evolution of the fingering.
"""


from openwind.technical import Score

class ExecuteScore:
    """
    From a fingering chart and a list of notes, we obtain the
    `openwind.technical.fingering_chart.Fingering` at each moment.

    Parameters
    ----------
    fingering_chart : openwind.technical.fingering_chart.FingeringChart
        The Fingering Chart associated to the played instrument
    note_events : List[Tuple(String, Float)]
        the list of note events (note_name, time) describing the score to play
    fingering_transition_time : float
        the caracteristic time to change fingering from one note to another
    """

    def __init__(self, fingering_chart, t_components):
        self.fingering_chart = fingering_chart
        self.t_components = t_components

        self.set_fingering = self.__set_no_fingering

    def __check_notes(self):
        """
        Check if the score's note names correspond to the chart's ones


        Raises
        ------
        ValueError
            An error if they not correspond.

        """
        fing_notes = self.fingering_chart.all_notes()
        score_notes = self._score.get_all_notes()
        if len(score_notes) > 0 \
           and not any([note in fing_notes for note in score_notes]):
            raise ValueError('The notes of the score must correspond to the '
                             'ones of the fingering chart:\n'
                             'Score:{} \nChart:{}'.format(score_notes,
                                                          fing_notes))

    def set_score(self, score):
        """
        Set the score and update the necessary fields.

        - Check the correspondance between the note names in the score and\
            the ones of the fingering chart .
        - Instanciate how the fingering will be actualized (with nothing if\
        no note is played)

        Parameters
        ----------
        Score : openwind.technical.score.Score

        """
        if not score:
            self._score = Score()
        else:
            self._score = score

        if self._score.is_score():
            self.__check_notes()
            self.set_fingering = self.__set_fingering
        else:
            self.set_fingering = self.__set_no_fingering

    def __get_fingering(self, t):
        """
        Return the fingering at the given instant following the score.


        Parameters
        ----------
        t : float
            The instant at which is read the score.

        Returns
        -------
        openwind.technical.fingering_chart.Fingering
            The fingering at this instant (eventually a mix between two
            fingerings).

        """
        notes = self._score.get_notes_at_time(t)
        if len(notes) == 1:
            return self.fingering_chart.fingering_of(notes[0][0])
        elif len(notes) == 2:
            proportion = notes[1][1]
            prev_note = self.fingering_chart.fingering_of(notes[0][0])
            next_note = self.fingering_chart.fingering_of(notes[1][0])
            return prev_note.mix(next_note, proportion)
        else:
            raise ValueError('Three notes are played together, it is '
                             'impossible to mix: {}'.format(notes))

    def __set_fingering(self, t):
        """
        Set the fingering at given time.

         Parameters
        ----------
        t : float
            The instant at which is read the score.
        """
        fingering = self.__get_fingering(t)
        fingering.apply_to(self.t_components)

    def __set_no_fingering(self, t):
        pass
