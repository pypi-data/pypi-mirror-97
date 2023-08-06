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

import warnings

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

import openwind.impedance_tools as tools
from openwind.design import Cone
from openwind.technical import Fingering
from openwind.continuous import (PhysicalRadiation, Excitator, Flow,
                                 JunctionTjoint, JunctionSimple,
                                 ThermoviscousLossless, JunctionDiscontinuity,
                                 ThermoviscousDiffusiveRepresentation,
                                 RadiationPerfectlyOpen)
from openwind.frequential import (FrequentialPipeFEM, FrequentialRadiation,
                                  FrequentialJunctionTjoint,
                                  FrequentialJunctionSimple,
                                  FrequentialJunctionDiscontinuity,
                                  FrequentialSource,
                                  FrequentialInterpolation,
                                  FrequentialPipeDiffusiveRepresentation,
                                  FrequentialPipeTMM,
                                  FrequentialPressureCondition,
                                  FrequentialComponent)
from openwind.tracker import SimulationTracker

__author__ = "Guillaume Castera, Juliette Chabassier, Augustin Ernoult, Alexis Thibault, Robin Tournemenne"
__copyright__ = "Copyright 2019, Inria"
__credits__ = ["Guillaume Castera", "Juliette Chabassier", "Augustin Ernoult", "Alexis Thibault", "Robin Tournemenne"]
__license__ = "GPL 3.0"
__version__ = "2.0"
__maintainer__ = "Juliette Chabassier"
__email__ = "juliette.chabassier@inria.fr"
__status__ = "Dev"

class FrequentialSolver:
    """Compute the impedance of an instrument.

    Methods
    -------

    Parameters
    ----------
    netlist : Netlist
        The netlist describing the instrument.
    frequencies : numpy.array
        Frequencies at which to compute the impedance.
    diffus_repr_var: bool
        Whether to use additional variables when computing the diffusive representation.
    use_tmm: bool
        Whether to use Transfer Matrices in the pipes instead of FEM.
    **discr_params :
        Discretization parameters.
    """

    def __init__(self, instru_physics, frequencies, diffus_repr_var=False, note=None,
                 compute_method='FEM',
                 **discr_params):
        self.netlist = instru_physics.netlist
        self.discr_params = discr_params
        self.check_frequencies(frequencies)
        self.frequencies = np.array(frequencies)
        self.diffus_repr_var = diffus_repr_var   # When using 'diffrepr+'
        self.compute_method = compute_method   # FEM, TMM, or hybrid?
        self._convert_frequential_components()
        self._organize_components()
        self._construct_matrices_pipes()
        self._set_note(note)
        self._construct_matrices()

    def __repr__(self):
        if len(self.frequencies) > 7:
            freq = ("array([{:.2e}, {:.2e}, ..., {:.2e}, "
                    "{:.2e}])".format(self.frequencies[0], self.frequencies[1],
                                     self.frequencies[-2], self.frequencies[-1]))
        else:
            freq = repr(self.frequencies)

        tmm_pipes = len([p for p in self.f_pipes
                         if p.__class__==FrequentialPipeTMM])
        fem_pipes = len(self.f_pipes) - tmm_pipes
        return ("<openwind.frequential.FrequentialSolver("
                "\n\tfrequencies={},".format(freq) +
                "\n\tnetlist={},".format(repr(self.netlist)) +
                "\n\tcompute_method='{:s}',".format(self.compute_method) +
                "\n\tnote='{}',".format(self.netlist.get_fingering_chart().get_current_note()) +
                "\n\tmesh_info:{{{} dof, {} TMM-pipes, {} FEM-pipes,"
                " elements/FEM-pipe:{}, "
                "order/element:{}}}\n)>".format(self.n_tot, tmm_pipes, fem_pipes,
                                          self.get_elements_mesh(),
                                          self.get_orders_mesh()))

    def __str__(self):
        if len(self.frequencies) > 7:
            freq = ("array([{:.2e}, {:.2e}, ..., {:.2e}, "
                    "{:.2e}])".format(self.frequencies[0], self.frequencies[1],
                                     self.frequencies[-2], self.frequencies[-1]))
        else:
            freq = repr(self.frequencies)
        return ("FrequentialSolver:\n" + "="*20 +
                "\nFrequencies:{}\n".format(freq) +"="*20 +
                "\n{}\n".format(self.netlist) + "="*20 +
                "\nCompute Method: '{:s}'\n".format(self.compute_method) + "="*20 +
                "\nCurrent Note: '{}'\n".format(self.netlist.get_fingering_chart().get_current_note()) + "="*20 +
                "\n" + self.__get_mesh_info())


    @staticmethod
    def check_frequencies(frequencies):
        if np.any(np.array(frequencies) <= 0):
            raise ValueError('The frequencies must be strictly positive!')

    def _set_note(self, note):
        if not note:
            return
        if isinstance(note, str):
            fc = self.netlist.get_fingering_chart()
            self.fingering = fc.fingering_of(note)
        elif isinstance(note, Fingering):
            self.fingering = note
        self.fingering.apply_to(self.f_components)

    def set_note(self, note):
        self._set_note(note)
        # Since solve() assumes the matrices are constructed,
        # update the matrices.
        self._construct_matrices()

    def set_frequencies(self, frequencies):
        self.frequencies = np.array(frequencies)
        self._organize_components()
        self._construct_matrices_pipes()
        self._construct_matrices()

    def _convert_pipe(self, pipe):
        """
        Construct an appropriate instance of (a subclass of) FrequentialPipe.

        Parameters
        ----------
        pipe : openwind.continuous.Pipe
            Continuous model of the pipe.
        **discr_params : keyword arguments
            Discretization parameters, passed to the FPipe initializer.

        Returns
        -------
        openwind.temporal.FrequentialPipe.

        """
        # only give to each pipe its corresponding disc value
        params = self.discr_params.copy()
        if ('l_ele' in params and isinstance(params['l_ele'],dict)):
            dict_l_ele = params['l_ele']
            params['l_ele'] = dict_l_ele[pipe.label]
        if ('order' in params and isinstance(params['order'], dict)):
            # only give to each pipe its corresponding disc value
            dict_order = params['order']
            params['order'] = dict_order[pipe.label]

        if self.compute_method == 'FEM':
            if (self.diffus_repr_var and
                isinstance(pipe.get_losses(), ThermoviscousDiffusiveRepresentation)):
                return FrequentialPipeDiffusiveRepresentation(pipe, **params)
            return FrequentialPipeFEM(pipe, **params)
        elif self.compute_method == 'TMM':
            return FrequentialPipeTMM(pipe, **self.discr_params)
        elif self.compute_method == 'hybrid':
            # Use TMM when it is exact,
            # i.e. if the pipe is a cylinder,
            # or a lossless cone.
            # TODO Add test
            shape = pipe.get_shape()
            lossless = isinstance(pipe.get_losses(), ThermoviscousLossless)
            if isinstance(shape, Cone) and \
                (shape.is_cylinder() or lossless):
                return FrequentialPipeTMM(pipe, **self.discr_params)
            return FrequentialPipeFEM(pipe, **params)

        raise ValueError("compute_method must be in {'FEM', 'TMM', 'hybrid'}")

    def _convert_component(self, component, ends):
        """
        Construct the appropriate frequential version of a component.

        Parameters
        ----------
        component : openwind.continuous.NetlistComponent
            Continuous model for radiation, junction, or source.
        ends : List[FPipe.End]
            The list of all `FPipe.End`s this component connects to.

        Returns
        -------
        openwind.temporal.FrequentialComponent.

        """

        if isinstance(component, Excitator):
            # verify that source is a flow
            if not isinstance(component, Flow):
                raise ValueError('The input type of player must be flow for frequential computation')
            f_source = FrequentialSource(component, ends)
        #     # Register the source to know on which d.o.f. to measure impedance
            if (hasattr(self, 'source_ref') and
                f_source.source.label != self.source_ref.source.label):
                raise ValueError('Instrument has several Sources (instead of one).')
            else:
                self.source_ref = f_source
            return f_source
#            return(FrequentialSource(component, ends))
        elif isinstance(component, PhysicalRadiation):
            if isinstance(component.model, RadiationPerfectlyOpen):
                return FrequentialPressureCondition(0, ends)
            else:
                return FrequentialRadiation(component, ends)
        elif isinstance(component, JunctionTjoint):
            return FrequentialJunctionTjoint(component, ends)
        elif isinstance(component, JunctionSimple):
            return FrequentialJunctionSimple(component, ends)
        elif isinstance(component, JunctionDiscontinuity):
            return FrequentialJunctionDiscontinuity(component, ends)

        raise ValueError("Could not convert component %s" % str(component))


    def _convert_frequential_components(self, **kwargs):
        self.f_pipes, self.f_connectors = \
            self.netlist.convert_with_structure(self._convert_pipe,
                                                self._convert_component)

        self.f_components = self.f_pipes + self.f_connectors
        assert all([isinstance(f_comp, FrequentialComponent)
                    for f_comp in self.f_components])

        if not hasattr(self, 'source_ref'):
            raise ValueError('The input emplacement is not identified: '
                             'it is impossible to compute the impedance.')
        self.scaling = self.source_ref.get_scaling()


    def _organize_components(self):
        n_dof_cmpnts = self.get_dof_of_components()
        self.n_tot = sum(n_dof_cmpnts)
        # place the components
        beginning_index = np.zeros_like(self.f_components)
        beginning_index[1:] = np.cumsum(n_dof_cmpnts[:-1])
        for k, f_comp in enumerate(self.f_components):
            f_comp.set_first_index(beginning_index[k])
            f_comp.set_total_degrees_of_freedom(self.n_tot)

    def _construct_matrices_of(self, components):
        omegas_scaled = 2*np.pi*self.frequencies * self.scaling.get_time()
        # initiate matrices
        n_tot = self.n_tot
        Ah_comp_nodiag = csr_matrix((n_tot, n_tot), dtype='complex128')
        Ah_comp_diags = np.zeros((n_tot, len(omegas_scaled)), dtype='complex128')
        Lh_comp = csr_matrix((n_tot, 1), dtype='complex128')
        # fill the matrices
        for f_comp in components:
            Ah_comp_nodiag += f_comp.get_contrib_indep_freq()
            Ah_comp_diags += f_comp.get_contrib_freq(omegas_scaled)
            Lh_comp += f_comp.get_contrib_source()

        # Transfer the diagonal of Ah_nodiag onto Ah_diags
        # so that the diagonal data of Ah_nodiag can be replaced
        # by each column of Ah_diags
        Ah_comp_diags[:, :] += Ah_comp_nodiag.diagonal()[:, np.newaxis]
        return Ah_comp_nodiag, Ah_comp_diags, Lh_comp

    def _construct_matrices_pipes(self):
        nodiag, diag, Lh = self._construct_matrices_of(self.f_pipes)
        self.Ah_pipes_nodiag = nodiag
        self.Ah_pipes_diags = diag
        self.Lh_pipes = Lh

    def _construct_matrices(self):
        (Ah_conect_nodiag, Ah_conect_diags,
         Lh_conect) = self._construct_matrices_of(self.f_connectors)
        self.Ah_nodiag = self.Ah_pipes_nodiag + Ah_conect_nodiag
        self.Ah_diags = self.Ah_pipes_diags + Ah_conect_diags
        self.Lh = self.Lh_pipes + Lh_conect


    def get_dof_of_components(self):
        n_dof_cmpts = np.array([f_cmpnt.get_number_dof()
                                for f_cmpnt in self.f_components], dtype='int')
        return n_dof_cmpts

    def solve_FEM(self, interp=False, pipes_label='main_bore', interp_grad=False,
                  interp_grid='original', observe_radiation=False):
        """
        An overlay of solve()
        """
        self.solve(interp, pipes_label, interp_grad, interp_grid,
                       observe_radiation)
        warnings.warn('The method FrequentialSolver.solve_FEM() is deprecated, please use solve() instead.')


    def solve(self, interp=False, pipes_label='main_bore', interp_grad=False,
                  interp_grid='original', observe_radiation=False,
                  enable_tracker_display=False):
        """ Parameters
        ----------
        interp : bool, optional
            to interpolate the results on other points than GaussLobato points.
            Default is False
        interp_grad : bool, optional
            if you yant to interpolate the matrix of the gradient too
            default is false
        interp_grid : {float, array(float), 'original'}
            you can give either a list of points on which to interpolate, or a
            float which is the step of the interpolation grid, or if you want
            to keep the GaussLobato grid, put 'original'.
            Default is 'original'.
        """

        # TODO Mieux séparer l'adimensionalisation / redimensionalisation
        # de la résolution du problème.

        # Mettre dans des méthodes indépendantes :
        # 1. Calcul des coefficients du modèle initial
        # 2. Changement de variable/scaling qui donne de nouveaux coefficients
        # 3. Résolution du problème
        # 4. Redimensionalisation des résultats
        # Si on ne veut pas adimensionner, il suffit de bypass 2. et 4.

        redim_imped = self.scaling.get_impedance()
        redim_pressure = self.scaling.get_scaling_pressure()
        redim_flow = self.scaling.get_scaling_flow()
        convention = self.source_ref.get_convention()
        ind_source = self.source_ref.get_source_index()

        self.imped = np.empty(self.frequencies.shape, dtype=np.complex128)
        if interp or interp_grad:
            self.flow = []
            self.pressure = []
            self.dpressure = []
            interpolation = FrequentialInterpolation(self, pipes_label,
                                                     interp_grid)
            self.x_interp = interpolation.x_interp

        if observe_radiation:
            self.pressure_rad = list()
            self.flow_rad = list()

        tracker = SimulationTracker(len(self.frequencies), display_enabled=enable_tracker_display)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Ah = self.Ah_nodiag.copy()
            for cpt in range(len(self.frequencies)):
                Ah.setdiag(self.Ah_diags[:, cpt])
                Uh = spsolve(Ah, self.Lh, permc_spec='COLAMD')
                tracker.update()
                if convention == 'PH1':
                    self.imped[cpt] = redim_imped * Uh[ind_source]
                    if interp:
                        self.pressure.append(interpolation.interpolate_H1(Uh)
                                             * redim_pressure)
                        self.flow.append(interpolation.interpolate_L2(Uh)
                                         * redim_flow)
                    if interp_grad:
                        self.dpressure.append(interpolation
                                              .interpolate_gradH1(Uh)
                                              * redim_pressure)
                    if observe_radiation:
                        self.pressure_rad.append(self.rad_mat_H1.dot(Uh)*redim_pressure)
                        self.flow_rad.append(self.rad_mat_L2.dot(Uh)*redim_flow)
                elif convention == 'VH1':
                    self.imped[cpt] = redim_imped / Uh[ind_source]
                    if interp:
                        self.pressure.append(interpolation.interpolate_L2(Uh)
                                             * redim_pressure)
                        self.flow.append(interpolation.interpolate_H1(Uh)
                                         * redim_flow)
                    if observe_radiation:
                        self.pressure_rad.append(self.rad_mat_L2.dot(Uh)*redim_pressure)
                        self.flow_rad.append(self.rad_mat_H1.dot(Uh)*redim_flow)
# %%

    def _get_flow_pressure_rad_1note(self, note, f_interest):


        if isinstance(f_interest, float):
            f_interest = np.array([f_interest])
        else:
            f_interest = np.array(f_interest)
        self.set_frequencies(f_interest)
        self.set_note(note)

        self.solve(observe_radiation=True)

        return np.array(self.flow_rad), np.array(self.pressure_rad)


    def _build_observe_radiation_matrix(self):
        from scipy.sparse import lil_matrix
        rad_component = [comp for comp in self.f_connectors
                         if type(comp).__name__ == 'FrequentialRadiation']
        rad_labels = [comp.rad.label for comp in rad_component]
        pipes_end = [comp.freq_end for comp in rad_component]

        freq_pipes = [freq_end.f_pipe for freq_end in pipes_end]

        self.rad_mat_L2 = lil_matrix((len(rad_component), self.n_tot))
        self.rad_mat_H1 = lil_matrix((len(rad_component), self.n_tot))

        for k, f_pipe in enumerate(freq_pipes):
            x_rad_local = np.array([pipes_end[k].pos.x])
            self.rad_mat_L2[k, :] = f_pipe.place_interp_matrix(x_rad_local)
            self.rad_mat_H1[k, :] = f_pipe.place_interp_matrix(x_rad_local,
                                                               variable='H1')

    def get_flow_pressure_radiation(self, notes, f_interest):
        assert len(notes) == len(f_interest)
        flow_radiations = list()
        pressure_radiations = list()

        self._build_observe_radiation_matrix()

        for note, freq in zip(notes, f_interest):
            flow_rad, press_rad = self._get_flow_pressure_rad_1note(note, freq)
            flow_radiations.append(flow_rad)
            pressure_radiations.append(press_rad)

        self.rad_labels = [comp.rad.label for comp in self.f_connectors
                           if type(comp).__name__ == 'FrequentialRadiation']
        self.flow_radiations = np.array(flow_radiations)
        self.pressure_radiations = np.array(pressure_radiations)
        return flow_radiations, pressure_radiations
# %%
    def get_ZC_adim(self):
        return self.source_ref.get_Zc0()


    # --- Plotting functions ---

    def plot_flow(self, freq=0):
        """Plot the flow for a given frequency inside the entire instrument
        """
        ifreq = np.where(self.frequencies >= freq)[0][0]
        plt.plot(self.x_interp, np.real(self.flow[ifreq]))

    def plot_pressure(self, freq=0):
        """Plot the pressure for a given frequency inside the entire instrument
        """
        ifreq = np.where(self.frequencies >= freq)[0][0]
        plt.plot(self.x_interp, np.real(self.pressure[ifreq]))

    def plot_impedance(self, **kwargs):
        tools.plot_impedance(self.frequencies, self.imped,
                             self.get_ZC_adim(), **kwargs)

    def plot_var3D(self, dbscale=True, var='pressure'):
        try:
            import plotly.graph_objs as go
            import plotly.offline as py
        except ImportError as err:
            msg = "Function plot_var3D() requires plotly."
            raise ImportError(msg) from err

        """Plot either the pressure or the flow for every frequency inside the
        entire instrument.
        """
        X = self.x_interp
        Y = self.frequencies
        if var == 'pressure':
            Z = self.pressure
            filename = 'pressure_3D.html'
        elif var == 'flow':
            Z = self.flow
            filename = 'flow_3D.html'
        else:
            raise ValueError("possible values are pressure or flow")
        if dbscale:
            Zplot = 20*np.log10(np.abs(Z))
        else:
            Zplot = np.real(Z)
        try:
            layout_3D = go.Layout(scene=dict(xaxis=dict(title='Position',
                                                        autorange='reversed'),
                                             yaxis=dict(title='Frequency',
                                                        autorange='reversed'),
                                             zaxis=dict(title='Field')))

            data_u3D = [go.Surface(x=X, y=Y, z=Zplot,
                                   contours=go.surface.Contours(
                                           x=go.surface.contours.X(
                                                   highlightcolor="#42f462",
                                                   project=dict(x=True)),
                                           y=go.surface.contours.Y(
                                                   highlightcolor="#42f462",
                                                   project=dict(y=True))
                                                                 )
                                   )
                        ]
            fig_u3D = go.Figure(data=data_u3D, layout=layout_3D)
            py.plot(fig_u3D, filename=filename)
        except:
            print('Impossible to load plotly: no 3D plot')

    def plot_acoustics_radiation(self, notes, variable='power', logscale=False,
                                 scaled=False, **kwargs):
        if variable == 'flow':
            ac_field = np.linalg.norm(self.flow_radiations, axis=1)
            title = 'Acoustic flow'
        elif variable == 'pressure':
            ac_field = np.linalg.norm(self.pressure_radiations, axis=1)
            title = 'Acoustic pressure'
        elif variable == 'power':
            ac_field = np.linalg.norm(self.flow_radiations
                                      * self.pressure_radiations, axis=1)
            title = 'Acoustic power'

        if scaled:
            ac_field = (np.abs(ac_field) /
                        np.sum(np.abs(ac_field), 1)[:, np.newaxis])

        if logscale:
            Z = np.log10(ac_field.T)

        else:
            Z = ac_field.T

        x = np.arange(0, len(self.rad_labels))

        fig_test, ax_test = plt.subplots()
        im = ax_test.imshow(Z, **kwargs)
        ax_test.set_yticks(x)
        ax_test.set_yticklabels(self.rad_labels)
        ax_test.set_yticks(np.append(-.5, x+0.5), minor=True)

        ax_test.set_xticks(np.arange(0, len(notes), 1))
        ax_test.set_xticks(np.arange(-.5, len(notes)+.5, 1), minor=True)
        ax_test.set_xlim(-.5, len(notes)-.5)
        ax_test.set_xticklabels(notes)

        fig_test.suptitle(title)
        ax_test.xaxis.tick_top()
        ax_test.grid(which='minor', color='k', linestyle='-', linewidth=1.5)

        divider = make_axes_locatable(ax_test)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig_test.colorbar(im, cax=cax)

    # --- Post-processing functions ---

    def write_impedance(self, filename):
        tools.write_impedance(self.frequencies, self.imped, filename)

    def resonance_frequencies(self, k=5):
        return tools.resonance_frequencies(self.frequencies, self.imped, k)

    def antiresonance_frequencies(self, k=5):
        return tools.antiresonance_frequencies(self.frequencies, self.imped, k)

    def get_lengths_pipes(self):
        return [f_pipe.pipe.get_length() for f_pipe in self.f_pipes]

    def get_orders_mesh(self):
        return [f_pipe.mesh.get_orders().tolist() for f_pipe in self.f_pipes
                if f_pipe.__class__ != FrequentialPipeTMM]

    def get_elements_mesh(self):
        return [len(x) for x in self.get_orders_mesh()]

    def __get_mesh_info(self):
        msg = "Mesh info:"
        msg += '\n\t{:d} degrees of freedom'.format(self.n_tot)
        msg += "\n\tpipes type: {}".format([t for t in self.f_pipes])
        lengths = self.get_lengths_pipes()
        msg += "\n\t{:d} pipes of length: {}".format(len(lengths), lengths)

        # Orders contains one sub-list for each pipe.
        orders = self.get_orders_mesh()
        elem_per_pipe = self.get_elements_mesh()
        msg += ('\n\t{} elements distributed on FEM-pipes '
                'as: {}'.format(sum(elem_per_pipe), elem_per_pipe))
        msg += '\n\tOrders on each element: {}'.format(orders)
        return msg

    def discretization_infos(self):
        print(self.__get_mesh_info())
