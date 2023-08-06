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
from scipy.sparse import coo_matrix, csc_matrix, lil_matrix, vstack, csr_matrix
from scipy.sparse.linalg import splu

from openwind.frequential import FrequentialSolver, FrequentialInterpolation
from openwind.algo_optimization import (Steepest, GaussNewton,
                                        LevenbergMarquardt, QuasiNewtonBFGS)
from openwind.inversion import observation as obs
from openwind.inversion.display_inversion import heatmap, annotate_heatmap
from scipy.optimize import minimize, least_squares


class InverseFrequentialResponse(FrequentialSolver):

    def __init__(self, instru_physics, frequencies, target_impedances,
                 observable='reflection', n_obs=None, diffus_repr_var=False,
                 notes=None, **kwargs):
        self.kwargs = kwargs
        self.n_obs = n_obs
        super().__init__(instru_physics, frequencies,
                         diffus_repr_var=diffus_repr_var,
                         note=None, **kwargs)
        self.instru_physics = instru_physics
        self.set_observation(observable)
        self.set_targets_list(target_impedances, notes)
        self.optim_params = instru_physics.instrument_geometry.optim_params
        self.set_restriction_matrix(n_obs)

    def set_observation(self, observable):
        """ Define the observation made on the impedance in the cost function.
        get_observation: return the observation operator.

        get_diff_observation_wrZ:
        """
        self.is_unwrap = False
        if type(observable) == tuple:
            self.observable = observable
        elif observable == 'impedance':
            self.observable = (obs.impedance, obs.diff_impedance_wrZ)
        elif observable == 'impedance_modulus':
            self.observable = (obs.module_square, obs.diff_module_square_wrZ)
        elif observable == 'reflection':
            self.observable = (obs.reflection, obs.diff_reflection_wrZ)
        elif observable == 'impedance_phase':
            self.observable = (obs.impedance_phase, obs.diff_impedance_phase_wrZ)
        elif observable == 'reflection_phase':
            self.observable = (obs.reflection_phase, obs.diff_reflection_phase_wrZ)
        elif observable == 'reflection_phase_unwraped':
            self.observable = (obs.reflection_phase, obs.diff_reflection_phase_wrZ)
            self.is_unwrap = True
        elif observable == 'reflection_modulus':
            self.observable = (obs.reflection_modulus_square, obs.diff_reflection_modulus_square_wrZ)
        else:
            raise ValueError("Unknown observable. Chose between: \n"
                             "{'impedance', 'impedance_modulus', 'reflection',"
                             "'impedance_phase', 'reflection_phase',"
                             "'reflection_modulus',"
                             " 'reflection_phase_unwraped'}")

    def set_targets_list(self, target_impedances, notes):
        if not type(target_impedances) == list:
            target_impedances = [target_impedances]
        if not type(notes) == list:
            notes = [notes]
        targets_list = []
        for impedance in target_impedances:
            if len(impedance.shape) == 1:
                impedance = np.array([impedance[:]])
            self.target = self.get_observation(impedance)
            targets_list.append(self.target)
        assert len(notes) ==  len(targets_list)
        assert targets_list[0].shape[1] == len(self.frequencies)
        self.targets = targets_list
        self.notes = notes

    def set_restriction_matrix(self, n_obs):
        # TODO: adapter pour des points d'observation quelconques avec interp
        if not n_obs: # by default the observation point is the source entry
            n_obs = [self.source_ref.get_source_index()]
        Nobs = len(n_obs)
        coef_obs = np.ones(Nobs) * self.scaling.get_impedance()
        self.restriction = coo_matrix((coef_obs,
                                      (list(range(Nobs)), n_obs)),
                                     shape=(Nobs, (self.n_tot)))

    def modify_parts(self, new_optim_values):
        self.optim_params.set_active_values(new_optim_values)
        # TODO: include the mesh actualization of pipes
#        delattr(self, 'source_ref')
#        self._convert_frequential_components(self.netlist, **self.kwargs)
#        self._organize_components()
        self.instru_physics.update_netlist()
        self._convert_frequential_components(**self.kwargs)
        self._organize_components()
        self._construct_matrices_pipes()
        self._construct_matrices()
        self.set_restriction_matrix(self.n_obs)

    def get_observation(self, impedance):
        return self.observable[0](impedance)

    def get_diff_observation_wrZ(self, impedance):
        """return the derivative of the observable w.r. to Z, AND the
        derivative of the CONJUGATE of the observable w.r. to Z.
        Warnings! it is a derivation wr to a complex vector: \
            d/dZ = (d/d(real(Z)) -j*d/d(imag(Z)))/2
        """
        return self.observable[1](impedance)

    def get_impedance_norm(self, Uh):
        return self.restriction.dot(Uh) /self.get_ZC_adim()

    def __get_target_norm(self):
        if self.is_unwrap:
            return np.sqrt(np.sum(np.abs(np.unwrap(self.target))**2))
        else:
            return np.sqrt(np.sum(np.abs(self.target)**2))

    def get_diff_imped_norm_wrUh(self):
        return self.restriction /self.get_ZC_adim()

    def compute_residu(self, Uh, ind_freq):
        impedance = self.get_impedance_norm(Uh)
        observation = self.get_observation(impedance)
        residu = (observation - self.target[:, ind_freq])/self.__get_target_norm()
        return np.append(residu.real, residu.imag)

    def diff_observation_wrU(self, Uh):
        impedance = self.get_impedance_norm(Uh)
        diff_obs_wrZ, diff_conj_obs_wrZ = self.get_diff_observation_wrZ(impedance)
        diff_imped = self.get_diff_imped_norm_wrUh()
        diff_obs = coo_matrix(diff_obs_wrZ).dot(diff_imped)
        diff_conj_obs = coo_matrix(diff_conj_obs_wrZ).dot(diff_imped)
        return diff_obs, diff_conj_obs

    def diff_residu_wrUh(self, Uh):
        diff_obs, diff_conj_obs = self.diff_observation_wrU(Uh)
        diff_real_residu = 0.5*(diff_obs + diff_conj_obs)/self.__get_target_norm()
        diff_imag_residu = -0.5j*(diff_obs - diff_conj_obs)/self.__get_target_norm()
        return vstack([diff_real_residu, diff_imag_residu])

    def compute_cost(self, residu):
        """WARNING: do not change this method or all the gradient computation
        must be modified"""
        cost = 0
        for k in range(len(self.frequencies)):
            cost += 0.5 * np.linalg.norm(residu[:, k])**2
        return cost

    def computedAH(self):
        omegas_scaled = 2*np.pi*self.frequencies * self.scaling.get_time()
        n_tot = self.n_tot
        self.dAh_nodiag_tot = []
        self.dAh_diags_tot = []
        for diff_index in range(len(self.optim_params.get_active_values())):
            # initiate matrices
            dAh_nodiag = csr_matrix((n_tot, n_tot), dtype='complex128')
            dAh_diags = np.zeros((n_tot, len(omegas_scaled)), dtype='complex128')
            # fill the matrices
            for f_comp in self.f_components:
                dAh_nodiag += f_comp.get_contrib_dAh_indep_freq(diff_index)
                dAh_diags += f_comp.get_contrib_dAh_freq(omegas_scaled,
                                                         diff_index)
            assert np.all(dAh_nodiag.diagonal() == 0)
            self.dAh_nodiag_tot.append(dAh_nodiag.tolil())
            self.dAh_diags_tot.append(dAh_diags)

    def __compute_dAhU(self, Uh, diff_index, ind_freq):
        dAh = self.dAh_nodiag_tot[diff_index].copy()
        dAh.setdiag(self.dAh_diags_tot[diff_index][:, ind_freq])
        return  dAh.dot(Uh)

    def __GradAdjoint(self, residu, Ahlu, Uh, ind_freq):
        Nderiv = len(self.optim_params.get_active_values())
        dresidu_dU = 2*self.diff_residu_wrUh(Uh)
        sourceAdj = dresidu_dU.conj().T.dot(residu)
        lambdaAdjconj = Ahlu.solve(-1*sourceAdj.conjugate(), 'T')
        grad = np.zeros([Nderiv])
        for diff_index in range(Nderiv):
            dAhU = self.__compute_dAhU(Uh, diff_index, ind_freq)
            grad[diff_index] = (lambdaAdjconj @ dAhU).real
        return grad

    def __GradFrechet(self, residu, Ahlu, Uh, ind_freq):
        Nderiv = len(self.optim_params.get_active_values())
        dresidu_dU = 2*self.diff_residu_wrUh(Uh)
        grad = np.zeros([Nderiv])
        jacob = np.zeros([self.restriction.shape[0]*2, Nderiv])
        for diff_index in range(Nderiv):
            dAhU = self.__compute_dAhU(Uh, diff_index, ind_freq)
            dU = -1 * Ahlu.solve(dAhU)
            jacob[:, diff_index] = dresidu_dU.dot(dU).T.real
            grad[diff_index] = jacob[:, diff_index].dot(residu)
        hessian = jacob.T.dot(jacob)
        return grad, hessian

    def __GradFiniteDiff(self, cost_init, stepSize=1e-8):
        Nderiv = len(self.optim_params.get_active_values())
        gradFor = np.zeros(Nderiv)
        gradBack = np.zeros(Nderiv)
        params_init = self.optim_params.get_active_values().copy()
        params = self.optim_params.get_active_values().copy()
        for diff_index in range(Nderiv):
            params[diff_index] = params_init[diff_index] + stepSize
            costFor, _, _ = self.get_cost_grad_hessian(params)
            gradFor[diff_index] = (costFor - cost_init) / stepSize

            params[diff_index] = params_init[diff_index] - stepSize
            costBack, _, _ = self.get_cost_grad_hessian(params)
            gradBack[diff_index] = (cost_init - costBack) / stepSize

            params[diff_index] = params_init[diff_index]
        self.get_cost_grad_hessian(params_init)
        return (gradFor + gradBack) / 2

    def __jacobian(self, Ahlu, Uh, ind_freq):
        Nderiv = len(self.optim_params.get_active_values())
        dresidu_dU = 2*self.diff_residu_wrUh(Uh)
        jacobian = np.zeros([self.restriction.shape[0]*2, Nderiv])
        for diff_index in range(Nderiv):
            dAhU = self.__compute_dAhU(Uh, diff_index, ind_freq)
            dU = -1 * Ahlu.solve(dAhU)
            jacobian[:, diff_index] = dresidu_dU.dot(dU).T.real
        return jacobian

# %% Global cost, gradient, hessian evaluations

    def __residuals_jacobian_1note(self):
        Nderiv = len(self.optim_params.get_active_values())
        Nres = self.target.shape[0]*2  # observation points *2 (real and imag)
        residuals = np.zeros(Nres*self.target.shape[1])
        jacobian = np.zeros((Nres*self.target.shape[1], Nderiv))
        Ah = self.Ah_nodiag
        Lh = self.Lh.toarray()
        self.computedAH()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for nf in range(len(self.frequencies)):
                Ah.setdiag(self.Ah_diags[:, nf])
                Ahlu = splu(Ah, permc_spec='COLAMD')
                Uh = Ahlu.solve(Lh)[:, 0]
                residuals[Nres*nf:Nres*(nf+1)] = self.compute_residu(Uh, nf)
                jacobian[Nres*nf:Nres*(nf+1), :] = self.__jacobian(Ahlu, Uh,
                                                                   nf)
        if self.is_unwrap:
            residuals = (np.unwrap(residuals*self.__get_target_norm())
                         / self.__get_target_norm())
        return residuals, jacobian

    def residuals_jacobian(self, params_values=list()):
        if not not any(params_values):
            self.modify_parts(params_values)
        Nres = (self.targets[0].shape[0]*2*self.targets[0].shape[1])
        Nderiv = len(self.optim_params.get_active_values())
        residuals = np.zeros(Nres*len(self.targets))
        jacobian = np.zeros((Nres*len(self.targets), Nderiv))
        for k_note in range(len(self.notes)):
            self.target = self.targets[k_note]
            self.set_note(self.notes[k_note])
            residuals1, jacobian1 = self.__residuals_jacobian_1note()
            residuals[k_note*Nres:(k_note+1)*Nres] = residuals1
            jacobian[k_note*Nres:(k_note+1)*Nres, :] = jacobian1
        return residuals, jacobian

    def __cost_grad_hessian_1note(self, grad_type=None, stepSize=1e-8):
        gradient = None
        hessian = None
        Nderiv = len(self.optim_params.get_active_values())

        residu = np.zeros((self.target.shape[0]*2, self.target.shape[1]))

        Ah = self.Ah_nodiag
        Lh = self.Lh.toarray()

        if grad_type == 'frechet' or grad_type == 'adjoint':
            self.computedAH()
            gradient = np.zeros([Nderiv])
            if grad_type == 'frechet':
                hessian = np.zeros([Nderiv, Nderiv])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for ind_freq in range(len(self.frequencies)):
                Ah.setdiag(self.Ah_diags[:, ind_freq])
                Ahlu = splu(Ah, permc_spec='COLAMD')
                Uh = Ahlu.solve(Lh)[:, 0]
                residu[:, ind_freq] = self.compute_residu(Uh, ind_freq)
                if self.is_unwrap:
                    residu = np.unwrap(residu*self.__get_target_norm())/self.__get_target_norm()
                if grad_type == 'frechet':
                    grad_temp, hess_temp = self.__GradFrechet(residu[:, ind_freq],
                                                              Ahlu, Uh, ind_freq)
                    hessian += hess_temp
                    gradient += grad_temp
                elif grad_type == 'adjoint':
                    gradient += self.__GradAdjoint(residu[:, ind_freq],
                                                        Ahlu, Uh, ind_freq)
        cost = self.compute_cost(residu)
        return cost, gradient, hessian

    def get_cost_grad_hessian(self, params_values=list(), grad_type=None,
                              stepSize=1e-8):
        gradient = None
        hessian = None
        if not not any(params_values):
            self.modify_parts(params_values)
        Nderiv = len(self.optim_params.get_active_values())

        cost = 0
        if grad_type == 'frechet' or grad_type == 'adjoint':
            gradient = np.zeros([Nderiv])
            if grad_type == 'frechet':
                hessian = np.zeros([Nderiv, Nderiv])

        for note, target in zip(self.notes, self.targets):
            self.target = target
            self.set_note(note)
            (cost_note, gradient_note,
             hessian_note) = self.__cost_grad_hessian_1note(grad_type=grad_type,
                                                              stepSize=stepSize)
            cost += cost_note
            if grad_type == 'frechet' or grad_type == 'adjoint':
                gradient += gradient_note
                if grad_type == 'frechet':
                    hessian += hessian_note
        if grad_type == 'finite diff':
               gradient = self.__GradFiniteDiff(cost, stepSize=stepSize)
        return cost, gradient, hessian

# Optimization algorithms

    def optimize_freq_model(self, algorithm='LM',
                            max_iter=100, minstep_cost=1e-8, tresh_grad=1e-6,
                            iter_detailed=False, steptype='linesearch'):

        initial_params = self.optim_params.get_active_values()
        if algorithm == 'LM':
            params_evol, cost_evol = LevenbergMarquardt(self._get_cost_grad_hessian_opt,
                                                        initial_params, max_iter,
                                                        minstep_cost, tresh_grad,
                                                        iter_detailed)
        elif algorithm == 'steepest':
            params_evol, cost_evol = Steepest(self._get_cost_grad_opt, initial_params, max_iter,
                                              minstep_cost, tresh_grad,
                                              iter_detailed, steptype)
        elif algorithm == 'QN':
            params_evol, cost_evol = QuasiNewtonBFGS(self._get_cost_grad_opt, initial_params,
                                                     max_iter, minstep_cost,
                                                     tresh_grad, iter_detailed,
                                                     steptype)
        elif algorithm == 'GN':
            params_evol, cost_evol = GaussNewton(self._get_cost_grad_hessian_opt,
                                                 initial_params, max_iter,
                                                 minstep_cost, tresh_grad,
                                                 iter_detailed)
        elif algorithm == 'Newton-CG' or algorithm == 'BFGS':
            params_evol, cost_evol = self._minimize_scipy(algorithm,
                                                          initial_params,
                                                          iter_detailed)
        else:
            print("""Unknown algorithm, choose between:
                  'LM' (Levenberg-Marquardt); 'steepest'; 'QN' (Quasi-Newton);
                  'GN' (Gauss-Newton); 'BFGS' (from scipy);
                  'Newton-CG' (from scipy)""")
        self.get_cost_grad_hessian(params_evol[-1])
        self.solve()
        return params_evol, cost_evol

# For scipy.otimize.least_squares
    def _update_residuals_jacobian(self, x):
        if any(np.asarray(x) != self.optim_params.get_active_values()):
            self._residuals, self._jacobian = self.residuals_jacobian(x)
            self._params_evol.append(x)
            cost = 0.5*self._residuals.dot(self._residuals)
            self._cost_evol.append(cost)
            if self._iter_detail:
                index_iter = len(self._cost_evol)-1
                if index_iter % 20 == 0:
                    print('{:<12}{:<16}{:<16}'.format('Iteration','Cost','Gradient'))
                norm_grad = np.linalg.norm(self._jacobian.T.dot(self._residuals[:, np.newaxis]))
                print('{:<12d}{:<16.8e}{:<16.8e}'.format(index_iter, cost,
                                                         norm_grad))

    def _get_residuals(self, x):
        self._update_residuals_jacobian(x)
        return self._residuals

    def _get_jacobian(self, x):
        self._update_residuals_jacobian(x)
        return self._jacobian

    def least_squares_freq_model(self, algorithm='lm',
                            max_iter=100, minstep_cost=1e-8, tresh_grad=1e-6,
                            iter_detailed=False):
        initial_params = self.optim_params.get_active_values()
        self._residuals, self._jacobian = self.residuals_jacobian(initial_params)
        self._iter_detail = iter_detailed
        self._params_evol = [initial_params]
        self._cost_evol = [0.5*self._residuals.dot(self._residuals)]
        if self._iter_detail:
            index_iter = len(self._cost_evol)-1
            if index_iter % 20 == 0:
                print('{:<12}{:<16}{:<16}'.format('Iteration','Cost','Gradient'))
            norm_grad = np.linalg.norm(self._jacobian.T.dot(self._residuals[:, np.newaxis]))
            print('{:<12d}{:<16.8e}{:<16.8e}'.format(index_iter,
                                                     self._cost_evol[-1],
                                                     norm_grad))
        res = least_squares(self._get_residuals, initial_params,
                            jac=self._get_jacobian, verbose=1,
                            method=algorithm, ftol=minstep_cost,
                            gtol=tresh_grad)
        return self._params_evol, self._cost_evol



# For scipy.optimize.minimize
    def _update_cost_grad_hessian(self, x):
        if any(np.asarray(x) != self.optim_params.get_active_values()):
            self._cost, self._grad, self._hessian = \
                self.get_cost_grad_hessian(x, grad_type=self._grad_type)
            self._params_evol.append(x)
            self._cost_evol.append(self._cost)
            if self._iter_detail:
                index_iter = len(self._cost_evol)-1
                if index_iter % 20 == 0:
                    print('{:<12}{:<16}{:<16}'.format('Iteration','Cost','Gradient'))
                norm_grad = np.linalg.norm(self._grad)
                print('{:<12d}{:<16.8e}{:<16.8e}'.format(index_iter, self._cost,
                                                         norm_grad))

    def _get_cost(self, x):
        self._update_cost_grad_hessian(x)
        return self._cost

    def _get_grad(self, x):
        self._update_cost_grad_hessian(x)
        return self._grad

    def _get_hessian(self, x):
        self._update_cost_grad_hessian(x)
        return self._hessian

    def _minimize_scipy(self, algorithm, initial_params, iter_detailed=False,
                        max_iter=None, tresh_grad=1e-6):
        if algorithm == 'Newton-CG':
            self._grad_type = 'frechet'
        else:
            self._grad_type = 'adjoint'
        self._cost, self._grad, self._hessian = \
            self.get_cost_grad_hessian(initial_params, grad_type=self._grad_type)
        self._iter_detail = iter_detailed
        self._params_evol = [initial_params]
        self._cost_evol = [self._cost]
        if self._iter_detail:
             print('{:<12}{:<16}{:<16}'.format('Iteration','Cost','Gradient'))
             norm_grad = np.linalg.norm(self._grad)
             print('{:<12d}{:<16.8e}{:<16.8e}'.format(0, self._cost,
                                                      norm_grad))
        if  algorithm == 'Newton-CG':
            res = minimize(self._get_cost, initial_params, method=algorithm,
                           jac=self._get_grad,
                           hess=self._get_hessian,
                           options={'disp': True, 'maxiter': max_iter})
        elif algorithm == 'BFGS':
            res = minimize(self._get_cost, initial_params, method=algorithm,
                           jac=self._get_grad,
                           options={'disp': True, 'maxiter': max_iter, 'gtol': tresh_grad})
        return self._params_evol, self._cost_evol

# For home made algorithms

    def _get_cost_grad_hessian_opt(self, x):
        return self.get_cost_grad_hessian(x, grad_type='frechet')

    def _get_cost_grad_opt(self, x):
        return self.get_cost_grad_hessian(x, grad_type='adjoint')[0:2]



# %% Sensitivity

    def __build_window(self, window):
        if not window:
            window_pond = np.ones_like(self.frequencies)
        else:
            f0, Deltaf = window
            Deltaf_Hz = f0 * (2**(Deltaf/1200) - 1)
            window_pond = np.zeros(self.frequencies.shape, dtype=float)
            sin = 0.5 + 0.5*np.cos(np.pi*(self.frequencies - f0)/Deltaf_Hz)
            ind = np.logical_and(self.frequencies >= f0 - Deltaf_Hz,
                                 self.frequencies <= f0 + Deltaf_Hz)
            window_pond[ind] = sin[ind]
        return window_pond

    def __sensitivity_observable_1note(self, note=None, window=None,
                                     interp=False, pipes_label='main_bore',
                                     interp_grid='original'):
        """
        Sensitivity of the observable w.r. to the design parameters for 1 note.

        The sensitivity is here defined as the L2 norm of the gradient of the
        observable. This gradient is estimated by the Frechet Derivative,
        giving the possibility to have the gradients of the acoustics fields.

        Parameters
        ----------
        note : string, optional
            Name of the note idicated in the fingering chart. The default value
            is 'None' (all the holes opened)

        window: tuple, optional
            Parameters to window the observable:
                (central frequency, frequency width in cents)
            If not defined, no window is applied. The default is None.

        interp: logical, optional
            Indicates if the variation of the acoustics fields (pressure and
            flow) wrt tthe design parameters must be interpolated along the
            instrument. The default is 'False'

        pipes_label: string, optional
            The labels of the pipes on which the acoustics fields must be
            interpolated. If it is "main_bore" all the pipes of the main bore
            (all excepted chimney holes) are included. Not used if
            `interp=False`. The default is 'main_bore'

        interp_grid : {float, array(float), 'original'}
            you can give either a list of points on which to interpolate, or a
            float which is the step of the interpolation grid, or if you want
            to keep the GaussLobato grid, put 'original'. Not used if
            `interp=False`. Default is 'original'.


        Returns
        -------
        sensitivity : np.array
            The norm (along the frequency axes) of the gradient for each design
            parameters.

        grad_observation : np.array
            The gradient of the observation at each frequency for each design
            parameters

        grad_flow, grad_pressure : np.array
            The gradient of the acoustics fields at each point of the
            interpolation grid, for each frequency and for each design parameters

        """
        self.set_note(note)
        Nderiv = len(self.optim_params.get_active_values())
        Nfreq = len(self.frequencies)

        redim_pressure = self.scaling.get_scaling_pressure()
        redim_flow = self.scaling.get_scaling_flow()
        convention = self.source_ref.get_convention()

        grad_observation = np.zeros((Nfreq, Nderiv), dtype='complex')
        observation = np.zeros(Nfreq, dtype='complex')
        Ah = lil_matrix(self.Ah_nodiag)
        Lh = self.Lh.toarray()
        if interp:
            interpolation = FrequentialInterpolation(self, pipes_label,
                                                     interp_grid)
            self.x_interp = interpolation.x_interp
            Nx = len(self.x_interp)
            grad_flow = np.zeros((Nx, Nfreq, Nderiv), dtype='complex')
            grad_pressure = np.zeros((Nx, Nfreq, Nderiv), dtype='complex')
        else:
            grad_flow = np.array([])
            grad_pressure = np.array([])

        window_pond = self.__build_window(window)
        self.computedAH()

        for ind_freq in range(Nfreq):
            Ah.setdiag(self.Ah_diags[:, ind_freq])
            Ahlu = splu(csc_matrix(Ah), permc_spec='COLAMD')
            Uh = Ahlu.solve(Lh)[:, 0]

            impedance = self.get_impedance_norm(Uh)
            observation[ind_freq] = self.get_observation(impedance)

            diff_obs, diff_conj_obs = self.diff_observation_wrU(Uh)
            diff_real_obs = 0.5*(diff_obs + diff_conj_obs)
            diff_imag_obs = -0.5j*(diff_obs - diff_conj_obs)
            dobservation_dU = vstack([diff_real_obs, 1j*diff_imag_obs])

            # sourceAdj = dobservation_dU.conj().T.dot(np.array([1., 1.]))
            # lambdaAdjconj = Ahlu.solve(-1*sourceAdj.conjugate(), 'T')
            grad = np.zeros([Nderiv], dtype='complex')
            for diff_index in range(Nderiv):
                dAhU = self.__compute_dAhU(Uh, diff_index, ind_freq)
                # grad[diff_index] = (lambdaAdjconj @ dAhU)
                dU = -1 * Ahlu.solve(dAhU)
                jacob = dobservation_dU.dot(dU).T
                grad[diff_index] = jacob.dot(np.array([1., 1.]))
                if interp:
                    if convention == 'PH1':
                        diff_P = interpolation.interpolate_H1(dU)
                        diff_interp_P = (interpolation.
                                          diff_interpolate_H1(Uh, diff_index))
                        P = interpolation.interpolate_H1(Uh)
                        grad_pressure[:, ind_freq,
                                      diff_index] = (diff_P + diff_interp_P)/P
                        diff_F = interpolation.interpolate_L2(dU)
                        diff_interp_F = (interpolation.
                                          diff_interpolate_L2(Uh, diff_index))
                        F = interpolation.interpolate_L2(Uh)
                        grad_flow[:, ind_freq,
                                      diff_index] = (diff_F + diff_interp_F)/F
                    elif convention == 'VH1':
                        diff_P = interpolation.interpolate_L2(dU)
                        diff_interp_P = (interpolation.
                                          diff_interpolate_L2(Uh, diff_index))
                        P = interpolation.interpolate_L2(Uh)
                        grad_pressure[:, ind_freq,
                                      diff_index] = (diff_P + diff_interp_P)/P
                        diff_F = interpolation.interpolate_H1(dU)
                        diff_interp_F = (interpolation.
                                          diff_interpolate_H1(Uh, diff_index))
                        F = interpolation.interpolate_H1(Uh)
                        grad_flow[:, ind_freq,
                                      diff_index] = (diff_F + diff_interp_F)/F
            grad_observation[ind_freq, :] = grad #/observation

        gradient_window = grad_observation*window_pond[:, np.newaxis]
        sensitivity = np.sqrt(np.sum(gradient_window.real**2
                                     + gradient_window.imag**2, axis=0))

        sensitivity /= np.linalg.norm(observation)
        return sensitivity, grad_observation, grad_flow, grad_pressure

    def compute_sensitivity_observable(self, windows=None, interp=False,
                                       pipes_label='main_bore',
                                       interp_grid='original'):
        """
        Sensitivity of the observable w.r. to the design parameters.

        The sensitivity of each fingering \[n\] w.r. to each parameter \[m_i\]
        is here defined as the L2 norm of the gradient of the observable
        \[\\mathcal{O}(\\omega)\] normalized by the norm of the observable
        along the frequency axis:

        .. math::
            \\sigma_i = \\frac{|| \\frac{\\partial \\mathcal{O}(\\omega)} \
            {\\partial m_i}||_{L_2} }{||\\mathcal{O}(\\omega)||_{L_2}}


        This gradient is estimated by the Frechet Derivative,
        giving the possibility to have the gradients of the acoustics fields.


        Parameters
        ----------
        note : string, optional
            Name of the note idicated in the fingering chart. The default value
            is 'None' (all the holes opened)

        window: tuple, optional
            Parameters to window the observable: \
                (central frequency, frequency width in cents)
            If not defined, no window is applied. The default is None.

        interp: logical, optional
            Indicates if the variation of the acoustics fields (pressure and
            flow) wrt tthe design parameters must be interpolated along the
            instrument. The default is 'False'

        pipes_label: string, optional
            The labels of the pipes on which the acoustics fields must be
            interpolated. If it is "main_bore" all the pipes of the main bore
            (all excepted chimney holes) are included. Not used if
            `interp=False`. The default is 'main_bore'

        interp_grid : {float, array(float), 'original'}
            you can give either a list of points on which to interpolate, or a
            float which is the step of the interpolation grid, or if you want
            to keep the GaussLobato grid, put 'original'. Not used if
            `interp=False`. Default is 'original'.


        Returns
        -------
        sensitivity : np.array
            The norm (along the frequency axes) of the gradient for each design
            parameters and each note.

        grad_observation : np.array
            The gradient of the observation at each frequency for each design
            parameters

        """
        sensitivities = list()
        grad_observation = list()
        grad_flow, grad_pressure = (list(), list())
        if not windows:
            windows = [None]*len(self.notes)
        else:
            assert len(windows) == len(self.notes)

        for note, window in zip(self.notes, windows):
            (sensi_note, grad_note, grad_flow_note,
             grad_pressure_note) = self.__sensitivity_observable_1note(note, window, interp, pipes_label, interp_grid)
            sensitivities.append(sensi_note)
            grad_observation.append(grad_note)
            grad_flow.append(grad_flow_note)
            grad_pressure.append(grad_pressure_note)
        self.grad_flow = grad_flow
        self.grad_pressure = grad_pressure
        self.sensitivities = np.array(sensitivities)
        return np.array(sensitivities), grad_observation

# %% Plots
    def plot_sensitivities(self, logscale=False, scaling=False, relative=True,
                           text_on_map=True, param_order=None, **kwargs):
        import matplotlib.pyplot as plt
        width = 1/(len(self.notes)+1)
        x = np.arange(0, len(self.optim_params.get_active_values()))
        labels = np.array(self.optim_params.labels)[self.optim_params.active].tolist()

        if relative:
            Z = self.sensitivities * np.array(self.optim_params.get_active_values())
            z_legend = 'Relative Sensitivity'
        else:
            Z = self.sensitivities
            z_legend = 'Sensitivity'

        if param_order:
            Z = Z[:, param_order]
            labels = np.array(labels)[param_order].tolist()

        if scaling:
            Z = Z / np.sum(Z, 1)[:, np.newaxis]

        if logscale:
            Z_plot = np.log10(np.abs(Z.T))
            z_legend += ' (log)'
        else:
            Z_plot = np.abs(Z.T)

        fig_sens, ax_sens = plt.subplots()
        im, cbar = heatmap(Z_plot, labels, self.notes, ax=ax_sens,
                           cbarlabel=z_legend, **kwargs)
        if text_on_map:
            cbar.remove()
            annotate_heatmap(im, data=np.abs(Z.T)*100, threshold=Z_plot.max()/2)
        return fig_sens, ax_sens

    def plot_grad_acoustics_field(self, notes=None, dbscale=True,
                                  var='pressure'):
        try:
            import plotly.graph_objs as go
            import plotly.offline as py
        except:  # ImportError as err:
            import matplotlib.pyplot as plt
            from matplotlib import cm
            msg = "The 3D plot are nicer with the module plotly."
            # raise ImportError(msg) from err
            print(msg)

        """Plot either the pressure or the flow for every frequency inside the
        entire instrument.
        """
        X = self.x_interp
        Y = self.frequencies

        optim_labels = (np.array(self.optim_params.labels)
                        [self.optim_params.active].tolist())
        if not notes:
            notes = self.notes
        for note in notes:
            ind_note = self.notes.index(note)
            for diff_index, param_label in enumerate(optim_labels):
                if var == 'pressure':
                    Z = self.grad_pressure[ind_note][:, :, diff_index].T
                    filename = 'grad_pressure_{}_{}.html'.format(note, param_label)
                elif var == 'flow':
                    Z = self.grad_flow[ind_note][:, :, diff_index].T
                    filename = 'grad_flow_{}_{}.html'.format(note, param_label)
                else:
                    raise ValueError("possible values are pressure or flow")
                if dbscale:
                    Zplot = 20*np.log10(np.abs(Z))
                else:
                    Zplot = np.real(Z)
                try:
                    xaxis = dict(title='Position', autorange='reversed')
                    yaxis = dict(title='Frequency', autorange='reversed')
                    zaxis = dict(title='Relative variation')
                    layout_3D = go.Layout(scene=dict(xaxis=xaxis, yaxis=yaxis,
                                                     zaxis=zaxis))

                    x_go = go.surface.contours.X(highlightcolor="#42f462",
                                                 project=dict(x=True))
                    y_go = go.surface.contours.Y(highlightcolor="#42f462",
                                                 project=dict(y=True))
                    contours = go.surface.Contours(x=x_go, y=y_go)
                    data_u3D = [go.Surface(x=X, y=Y, z=Zplot,
                                           contours=contours)]
                    fig_u3D = go.Figure(data=data_u3D, layout=layout_3D)
                    py.plot(fig_u3D, filename=filename)
                except:
                    fig = plt.figure()
                    ax = fig.gca(projection='3d')
                    Xplot, Yplot = np.meshgrid(X, Y)
                    surf = ax.plot_surface(Xplot, Yplot, Zplot, cmap=cm.plasma, antialiased=True)
                    ax.set_xlabel('Position')
                    ax.set_ylabel('Frequency')
                    ax.set_zlabel('Relative variation')
                    fig.colorbar(surf, shrink=0.5, aspect=5)
                    fig.suptitle('{}\n{}'.format(note, param_label))
