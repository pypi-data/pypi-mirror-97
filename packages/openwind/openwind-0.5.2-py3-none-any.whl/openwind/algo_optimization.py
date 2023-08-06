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
import pdb

def stop_message(iteropt, max_iter, cost, step_cost, minstep_cost, gradient,
                 tresh_grad):
    if np.max(np.abs(gradient)) <= tresh_grad:
        print('Algorithm stops: the gradient is below the tolerance treshold ({:.2e})'.format(tresh_grad))
    elif step_cost <= minstep_cost:
        print('Algorithm stops: the cost variation is below the tolerance treshold ({:.2e})'.format(minstep_cost))
    elif iteropt >= max_iter:
        print('Algorithm stops: the maximum iteration number has been reached ({:d})'.format(max_iter))
    else :
        print('Algorithm stops for internal specific reason.')
    print(('    Iterations:{:d} \n    Final cost = {:.2e} \n    '
           'Norm of gradient = {:.2e}').format(iteropt, cost, np.linalg.norm(gradient)))


def print_cost(index_iter, cost, gradient, info=('','')):
    norm_grad = np.linalg.norm(gradient)
    # print('Iteration {:d}; Cost={:.8e}; Gradient={:.8e}'.format(index_iter, cost, norm_grad))
    if index_iter % 20 == 0:
        print('{}\t{:<14}\t{:<14}\t{:<14}'.format('Iteration','Cost',
                                                  'Gradient', info[0]))
    print('{:<10d}\t{:<14.8e}\t{:<14.8e}\t{}'.format(index_iter, cost,
                                                     norm_grad, info[1]))



def __hessianFiniteDiff(get_cost_grad, params_values, stepSize=1e-8):
    Nderiv = len(params_values)
    hessFor = np.zeros((Nderiv, Nderiv))
    hessBack = np.zeros((Nderiv, Nderiv))

    _, grad_init = get_cost_grad(params_values)
    params_init = np.array(params_values, copy=True)
    params = np.array(params_values, copy=True)
    for diff_index in range(Nderiv):
        params[diff_index] = params_init[diff_index] + stepSize
        _, gradFor = get_cost_grad(params)
        hessFor[diff_index, :] = (gradFor - grad_init) / stepSize

        params[diff_index] = params_init[diff_index] - stepSize
        _, gradBack = get_cost_grad(params)
        hessBack[diff_index, :] = (grad_init - gradBack) / stepSize

        params[diff_index] = params_init[diff_index]
    get_cost_grad(params_init)
#    pdb.set_trace()
    return (hessFor + hessBack) / 2


def __hessianBFGS(x0, x1, grad, Bk):
    # equation 6.19 du Nocedal
    sk = x1 - x0
    yk = grad[1] - grad[0]
    sk = sk[:, np.newaxis]
    yk = yk[:, np.newaxis]
    num1 = Bk.dot(sk.dot(sk.T.dot(Bk.T)))
    den1 = sk.T.dot(Bk.dot(sk))
    num2 = yk.dot(yk.T)
    den2 = yk.T.dot(sk)

    Bnew = Bk - num1/den1 + num2/den2
    return Bnew


def __inv__hessianBFGS(x0, x1, grad, Hk):
    # equation 6.17 du Nocedal
    sk = x1 - x0
    yk = grad[1] - grad[0]
    sk = sk[:, np.newaxis]
    yk = yk[:, np.newaxis]
    rho = 1/(yk.T.dot(sk))
    A = np.eye(Hk.shape[0]) - rho * (sk.dot(yk.T))
    Hnew = A.dot(Hk.dot(A)) + rho * (sk.dot(sk.T))
    return Hnew


def __backtracking(get_cost_grad, params_old, direction, cost_old, phi_prime):
    alpha_0 = 1
    rho = 0.75
    c1 = 1e-3

    alpha = alpha_0
    kadapt = 0
    delta_f = c1 * phi_prime
    params_new = params_old + alpha * direction
    cost_new, _ = get_cost_grad(params_new)
    while cost_new > cost_old + alpha * delta_f and kadapt < 100:
        kadapt = kadapt + 1
        alpha = alpha * rho
        params_new = params_old + alpha * direction
        cost_new, _ = get_cost_grad(params_new)
    if kadapt >= 100:
        print('The backtracking process failed to find the step '
              'length in the maximal authorized iterations (100)')
    return params_new


def __linesearch(get_cost_grad, params_old, direction, phi, phi_prime):
    #  linesearch algorithm 3.5 from Nocedal
    c1 = 1e-4  # 1e-3
    c2 = 0.9
    alpha_def = 1  # default value for QuasiNewton

    alpha_k = 0
    alpha_k = np.append(alpha_k, alpha_def)
    alpha_max = 10
    kadapt = 1
    alphaStar = []

    while not alphaStar:
        params_new = params_old + alpha_k[kadapt] * direction
        cost_new, grad_new = get_cost_grad(params_new)

        phi = np.append(phi, cost_new)
        phi_prime = np.append(phi_prime, grad_new @ direction)
        if (phi[kadapt] > phi[0] + c1*alpha_k[kadapt]*phi_prime[0] or
           (phi[kadapt] >= phi[kadapt-1] and kadapt > 1)):
            alphaStar = __zoomLinesearch(get_cost_grad, kadapt-1, kadapt,
                                         alpha_k, phi, phi_prime, direction,
                                         params_old, c1, c2)
        elif np.abs(phi_prime[kadapt]) <= -c2*phi_prime[0]:
            alphaStar = alpha_k[kadapt]
        elif phi_prime[kadapt] >= 0:
            alphaStar = __zoomLinesearch(get_cost_grad, kadapt, kadapt-1,
                                         alpha_k, phi, phi_prime, direction,
                                         params_old, c1, c2)
        else:
            alpha_k = np.append(alpha_k, 0.5*(alpha_k[kadapt]+alpha_max))
            kadapt = kadapt + 1

        if kadapt >= 100:
            print('The linesearch process failed to find the step '
                  'length in the maximal authorized iterations (100)')

    return params_old + alphaStar * direction


def __zoomLinesearch(get_cost_grad, k_lo, k_hi, alpha_k, phi, phi_prime,
                     direction, params_optim, c1, c2):
    a_lo = alpha_k[k_lo]
    a_hi = alpha_k[k_hi]
    phi_lo = phi[k_lo]
    phi_hi = phi[k_hi]
    phi_prime_lo = phi_prime[k_lo]
    alphaStar = []
    niter = 0
    while not alphaStar and niter < 100 and a_lo!=a_hi:
        niter = niter+1
        # quadratic approach
        A = (phi_hi - phi_lo - phi_prime_lo*(a_hi - a_lo) ) / (a_hi - a_lo)**2
        a_j = a_lo - phi_prime_lo/(2*A)
        # limited range
        a_sorted = sorted([.1*a_lo + .9*a_hi, .9*a_lo + .1*a_hi])
        a_j = min(max([a_sorted[0], a_j]), a_sorted[1])
        # a_j = 0.5*(a_lo + a_hi) # simply mean
        params_j = params_optim + a_j * direction
        cost_j, grad_j = get_cost_grad(params_j)

        if cost_j > phi[0] + c1*a_j*phi_prime[0] or (cost_j >= phi_lo):
            a_hi = a_j
            phi_hi = cost_j
        else:
            if np.abs(grad_j @ direction) <= -c2*phi_prime[0]:
                alphaStar = a_j
            elif (grad_j @ direction)*(a_hi - a_lo) >= 0:
                a_hi = a_lo
                phi_hi = phi_lo
            a_lo = a_j
            phi_lo = cost_j
            phi_prime_lo = grad_j @ direction
    if not alphaStar:
        alphaStar = a_j
    return alphaStar


def _search_step_length(get_cost_grad, params_old, direction, cost_old,
                        gradient_old, steptype='linesearch'):
    phi_prime = gradient_old @ direction
    if steptype == 'backtracking':
        newparams = __backtracking(get_cost_grad, params_old,
                                   direction, cost_old, phi_prime)
    else:
        newparams = __linesearch(get_cost_grad, params_old,
                                 direction, cost_old, phi_prime)
    return newparams


# %% Algorithms
def _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                          initial_params, max_iter=100, minstep_cost=1e-8,
                          tresh_grad=1e-10, iter_detailed=False,
                          steptype='linesearch', hessiantype=None):
    step_cost = np.inf
    iteropt = 0

    if hessiantype == 'BFGS':
        cost, gradient, direction, Hk = get_cost_grad_direction(initial_params,
                                                                0., 0., 0., 0.)
    else:
        cost, gradient, direction = get_cost_grad_direction(initial_params)

    params_evol = [np.array(initial_params)]
    cost_evol = [cost]
    if iter_detailed:
        print_cost(iteropt,cost, gradient)
    while (iteropt < max_iter and step_cost > minstep_cost
           and np.linalg.norm(gradient) > tresh_grad):
        iteropt = iteropt + 1
        newparams = _search_step_length(get_cost_grad, params_evol[iteropt-1],
                                        direction, cost, gradient,
                                        steptype=steptype)
        if hessiantype == 'BFGS':
            (cost, gradient, direction,
             Hk) = get_cost_grad_direction(newparams, params_evol[-1],
                                           gradient, iteropt, Hk)
        else:
            cost, gradient, direction = get_cost_grad_direction(newparams)

        params_evol.append(newparams)
        cost_evol.append(cost)
        if iter_detailed:
            print_cost(iteropt, cost, gradient)
        step_cost = (cost_evol[-2] - cost_evol[-1])/(cost_evol[-1] + minstep_cost) # np.abs(cost_evol[-2] - cost_evol[-1])/cost_evol[-1]

    stop_message(iteropt, max_iter, cost, step_cost, minstep_cost, gradient,
                 tresh_grad)
    return params_evol, cost_evol


def QuasiNewtonBFGS(get_cost_grad, initial_params, max_iter=100,
                    minstep_cost=1e-8, tresh_grad=1e-10, iter_detailed=False,
                    steptype='linesearch'):

    def get_cost_grad_direction(x, x0, old_grad, iteropt, old_Hk):
        cost, gradient = get_cost_grad(x)
        if np.mod(iteropt, 10) == 0:
            hessian = __hessianFiniteDiff(get_cost_grad, x)
            try:
                Hk = np.linalg.inv(hessian)
            except:
                Hk = np.eye(len(hessian))
        else:
#            hessian = __hessianBFGS(x0, x, [old_grad, gradient], np.linalg.inv(old_Hk))
            Hk = __inv__hessianBFGS(x0, x, [old_grad, gradient], old_Hk)
        direction = -1 * Hk.dot(gradient)
        if (gradient @ direction) >= 0:
            direction = -1*gradient
        return cost, gradient, direction, Hk

    return _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                                 initial_params, max_iter, minstep_cost,
                                 tresh_grad, iter_detailed, steptype,
                                 hessiantype='BFGS')


def Steepest(get_cost_grad, initial_params, max_iter=100, minstep_cost=1e-8,
             tresh_grad=1e-10, iter_detailed=False,
             steptype='linesearch'):

    def get_cost_grad_direction(x):
        cost, gradient = get_cost_grad(x)
        direction = -1 * gradient
        return cost, gradient, direction

    return _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                                 initial_params, max_iter, minstep_cost,
                                 tresh_grad, iter_detailed, steptype)


def GaussNewton(get_cost_grad_hessian, initial_params, max_iter=100,
                minstep_cost=1e-8, tresh_grad=1e-10, iter_detailed=False):

    def get_cost_grad(x):
        cost, gradient, _ = get_cost_grad_hessian(x)
        return cost, gradient

    def get_cost_grad_direction(x):
        cost, gradient, hessian = get_cost_grad_hessian(x)
        direction = np.linalg.solve(hessian, -1 * gradient)
        if (gradient @ direction) >= 0:
            direction = -1*gradient
        return cost, gradient, direction

    return _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                                 initial_params, max_iter, minstep_cost,
                                 tresh_grad, iter_detailed)



def LevenbergMarquardt(get_cost_grad_hessian, initial_params, max_iter=100,
                       minstep_cost=1e-8, tresh_grad=1e-10,
                       iter_detailed=False, method='3'):
    """
    Levenberg Marquardt algorithm.

    This algorithm can be used only with least-square problems for which the
    cost function is writting as:

        .. math::
            F = \\frac{1}{2} ||\\mathbf{r}||_{L2}

    where :math:`\\mathbf{r}` is the residual. The three implementation
    presented here are inspired from the one proposed by H.Gavin [[1]_, [2]_]



    Parameters
    ----------
    get_cost_grad_hessian : callable
        A method which return the cost, the gradient and the estimation of the\
        hessian.
    initial_params : np.array()
        The initial values.
    max_iter : int, optional
        The maximum iterations authorized. The default is 100.
    minstep_cost : float, optional
        the minimal step cost authorized. The default is 1e-8.
    tresh_grad : float, optional
        The minimal authorized value for gradient. The default is 1e-10.
    iter_detailed : boolean, optional
        Display or not the detail of each iterations. The default is False.
    method : string, optional
        The method used between {'1', '2', '3'}, see [[1]_]. The default is '3'.
        1. the historical LM method
        2. Quadratic approximation
        3. Method proposed by [[2]_]

    Returns
    -------
    (params_evol, cost_evol): list
        List of the parameters and cost evolution along the optimization
        procedure.

    References
    ----------
    .. [1] http://people.duke.edu/~hpgavin/m-files/lm.pdf

    .. [2] K.Madsen, H. B. Nielsen, and O. Tingleff, Methods For Non-Linear\
    Least Squares Probems, Informatics and Mathematical Modelling, Technical \
    University of Denmark. 2004.


    """

    lambda0 = 1e-2 # 1e-8  # 1e-5 #
    eps_4 = 1e-1#1e-1 # 0 #
    nui0 = 2
    lambdaMin = 1e-7 # ??1e-10  #
    lambdamax = 1e7 # 1e10 #
    iter_lambda_max = 100

    Lup = 11
    Ldown = 9

    # print('WARNING ARTIFICIAL MIN AND MAX')
    # p_min = -10*np.abs(initial_params)
    # p_max =  10*np.abs(initial_params)

    if method == '1':
        # cf document by H.P. Gavin method 1: method from LM
        def one_step_LM(hessian, lambdai, minusgrad):
            diag_hess = np.diag(hessian)
            step_i = np.linalg.solve(hessian + lambdai*np.diag(diag_hess),
                                        minusgrad)  # eq(13)
            params_test = params_evol[-1] + step_i
            # params_test = np.array([min(max(pi, p_min[k]), p_max[k]) for k, pi in enumerate(params_test)])
            cost, gradient, hessian = get_cost_grad_hessian(params_test)
            DeltaCost = cost_evol[-1] - cost
            expected =  0.5*(step_i @ (lambdai*diag_hess*step_i + minusgrad))
            rho = DeltaCost / min(cost_evol[-1], expected)  # eq(16)
            if rho > eps_4:
                lambdai = np.maximum(lambdai/Ldown, lambdaMin)
            else:
                lambdai = np.minimum(lambdai*Lup, lambdamax)
            return params_test, cost, gradient, hessian, rho, lambdai

    elif method == '2':
        # cf document by H.P. Gavin method 2: quadratic Method

        def one_step_LM(hessian, lambdai, minusgrad):
            direction = np.linalg.solve(hessian + lambdai*np.identity(Nparam),
                                        minusgrad)  # eq(12)
            params_test = params_evol[-1] + direction
            cost, gradient, hessian = get_cost_grad_hessian(params_test)
            alpha = minusgrad @ direction / ((cost - cost_evol[-1])/2
                                                 + 2*minusgrad @ direction)
            if alpha > 0:
                step_i = alpha * direction
                params_test = params_evol[-1] + step_i
                cost, gradient, hessian = get_cost_grad_hessian(params_test)
            else :
                alpha = 1
                step_i = direction
            DeltaCost = cost_evol[-1] - cost
            expected = 0.5 * step_i @ (lambdai*step_i +  minusgrad)
            rho = DeltaCost / min(cost_evol[-1], expected)  # eq(15)
            if rho > eps_4:
                lambdai = np.maximum(lambdai/(1 + alpha), lambdaMin)
            else:
                lambdai = lambdai + np.abs(DeltaCost)/(2*alpha)
            return params_test, cost, gradient, hessian, rho, lambdai

    elif method == '3':
        # cf document by H.P. Gavin method 3: from Nielsen 1999
        def one_step_LM(hessian, lambdai, minusgrad):
            step_i = np.linalg.solve(hessian + lambdai*np.identity(Nparam),
                                        minusgrad)  # eq(12)
            params_test = params_evol[-1] + step_i

            cost, gradient, hessian = get_cost_grad_hessian(params_test)

            DeltaCost = cost_evol[-1] - cost
            expected = 0.5 * step_i @ (lambdai*step_i +  minusgrad)
            rho = DeltaCost / min(cost_evol[-1], expected)  # eq(15)
            if rho > eps_4:
                lambdai *= np.maximum(1/3, 1 - (2 * rho - 1)**3)
            else:
                lambdai *= nui
            return params_test, cost, gradient, hessian, rho, lambdai

    Nparam = len(initial_params)
    step_cost = np.inf
    rho = np.inf
    iteropt = 0
    iter_lambda = 0
    nui = nui0

    params_evol = [np.array(initial_params)]
    cost, gradient, hessian = get_cost_grad_hessian(params_evol[iteropt])
    cost_evol = [cost]
    minusgrad = -1 * gradient

    if method == '2' or method == '3':
        lambdai = lambda0*np.max(np.diag(hessian))
    else:
        lambdai = lambda0
    if iter_detailed:
        print_cost(iteropt, cost, gradient,
                   info=('lambda', '{:.8e}'.format(lambdai)))

    while (iteropt < max_iter and step_cost > minstep_cost
           and (rho <= eps_4 or np.linalg.norm(gradient) > tresh_grad)
           and iter_lambda < iter_lambda_max):

        (new_param, cost, gradient,
         hessian, rho, lambdai) = one_step_LM(hessian, lambdai, minusgrad)
        if rho > eps_4:
            iteropt += 1
            iter_lambda = 0
            nui = nui0
            minusgrad = -1 * gradient
            cost_evol.append(cost)
            params_evol.append(new_param)
            step_cost = (cost_evol[-2] - cost_evol[-1])/(cost_evol[-1] + minstep_cost)
            if iter_detailed:
                print_cost(iteropt, cost, gradient,
                           info=('lambda', '{:.8e}'.format(lambdai)))
        else:
            if iter_detailed:
                print('\tAdapt lambda: {:.8e}'.format(lambdai))
            iter_lambda += 1
            nui *= 2

    _, _, _ = get_cost_grad_hessian(params_evol[-1])
    if iter_lambda >= iter_lambda_max:
        print('The LM process failed to adapt the lambda in the'
              ' maximal authorized iterations ({})'.format(iter_lambda_max))
    stop_message(iteropt, max_iter, cost, step_cost, minstep_cost, gradient,
                 tresh_grad)
    return params_evol, cost_evol
