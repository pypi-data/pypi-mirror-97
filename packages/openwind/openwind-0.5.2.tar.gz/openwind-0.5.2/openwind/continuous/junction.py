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

from numpy import pi, sqrt, sign
import numpy as np
from openwind.continuous import NetlistComponent
import warnings

class PhysicalJunction(NetlistComponent):
    pass


class JunctionSimple(PhysicalJunction):
    """Model a simple junction between two pipes without masses.

    This junction assure the continuity of pression and flow between the two
    pipes.

    Parameters
    ----------
    label : string
        The label of the junction
    scaling : openwind.continuous.scaling.Scaling
        Nondimensionalization coefficients.
    convention : {'PH1', 'VH1'}, optional
        The convention used in this junction. The default is 'PH1'.
    """

    def __init__(self, label, scaling, convention='PH1'):
        super().__init__(label, scaling, convention)


class JunctionDiscontinuity(PhysicalJunction):
    """Model the junction between 2 pipes with a discontinuity of section.

    An acoustic mass is added due to the discontinuity of section.

    The mass takes into account the possible discontinuity of cross section
    between the two pipes.
    The formulation used is the one propose by [[1]_] (Appendix A.3.7). This
    formulation unifiates the two formulations proposed by [[2]_] by assuring
    that the mass and its derivative are null when the two raddi are equal.

    Parameters
    ----------
    label : string
        The label of the junction
    scaling : openwind.continuous.scaling.Scaling
        Nondimensionalization coefficients.
    convention : {'PH1', 'VH1'}, optional
        The convention used in this junction. The default is 'PH1'.

    References
    ----------
    .. [1] P.A.Taillard. 2018. “Theoretical and Experimental Study of the \
    Role of the Reed in Clarinet Playing.” Phd Thesis, Le Mans University. \
    https://tel.archives-ouvertes.fr/tel-01858244/document.

    .. [2] J.Kergomard, and A. Garcia. 1987. "Simple discontinuities in \
    acoustic waveguides at low frequencies: Critical analysis and formulae". \
    JSV 114 (3): 465‑79. https://doi.org/10.1016/S0022-460X(87)80017-2.
    """

    def __init__(self, label, scaling, convention='PH1'):
        super().__init__(label, scaling, convention)

    def get_scaling_masses(self):
        """
        Get the scaling coefficient for acoustic mass.

        Returns
        -------
        flaot
            The scaling coefficient

        """
        return self.scaling.get_impedance() * self.scaling.get_time()

    def compute_masse(self, r1, r2, rho):
        """Compute mass of a Junction from physical parameters.

        Parameters
        ----------
        r1 : float
            Radius of one pipe, at the point of junction
        r2 : float
            Radius of the other pipe, at the point of junction
        rho : float
            Air density, at the point of the junction

        Returns
        -------
        float
            The scaled acoustic mass associated to the junction.

        """
        coef_scaling_masses = self.get_scaling_masses()

        rmin = min(r1, r2)
        rmax = max(r1, r2)
        alpha = rmin/rmax
        mass = (.09616*alpha**6 - .12386*alpha**5 + 0.03816*alpha**4
            + 0.0809*alpha**3 - .353*alpha + .26164)
        return rho/rmin*mass/coef_scaling_masses

    def get_diff_mass(self, r1, r2, rho, dr1, dr2):
        """
        Derivate the mass w.r. to the radii.

        Parameters
        ----------
        r1 : float
            Radius of one pipe, at the point of junction
        r2 : float
            Radius of the other pipe, at the point of junction
        rho : float
            Air density, at the point of the junction
        dr1 : float
            The derivative of the first pipe radius.
        dr2 : float
            The derivative of the first pipe radius.

        Returns
        -------
        float
            The derivative of the mass.

        """
        coef_scaling_masses = self.get_scaling_masses()


        if r1>r2:
            rmin, rmax, drmin, drmax = (r2, r1, dr2, dr1)
        else:
            rmin, rmax, drmin, drmax = (r1, r2, dr1, dr2)

        alpha = rmin/rmax
        dalpha = drmin/rmax - drmax*rmin/rmax**2
        dmass = (6*.09616*alpha**5 - 5*.12386*alpha**4 + 4*0.03816*alpha**3
                + 3*0.0809*alpha**2 - .353)*dalpha

        mass = self.compute_masse(r1, r2, rho)
        return rho/rmin*dmass/coef_scaling_masses - drmin/rmin*mass

class JunctionTjoint(PhysicalJunction):
    """Model a T joint junction where a side tube is branched on a main tube.

    It is done with three parameters m11, m12, m22, computed them through
    empirical formulas given in [[1]_] or [[2]_], by using the short chimney
    height approximation.

    Parameters
    ----------
    label : string
        The label of the junction
    scaling : openwind.continuous.scaling.Scaling
        Nondimensionalization coefficients.
    convention : {'PH1', 'VH1'}, optional
        The convention used in this junction. The default is 'PH1'.
    matching_volume : boolean, optional
        Include or not the matching volume between the main and the side tubes
        in the masses of the junction. The default is False.

    Reference
    ---------
    .. [1] Antoine Chaigne and Jean Kergomard, "Acoustics of Musical \
        Instruments". Springer, New York, 2016.

    .. [2] V Dubos, J. Kergomard, A. Khettabi, J.-P. Dalmont, D. H. Keefe, \
        and C. J. Nederveen, "Theory of sound propagation in a duct with a \
        branched tube using modal decomposition," Acta Acustica united with \
        Acustica, vol. 85, no. 2, pp. 153–169, 1999.



    """

    def __init__(self, label, scaling, convention='PH1', matching_volume=False):
        super().__init__(label, scaling, convention)
        self.matching_volume = matching_volume

    def get_scaling_masses(self):
        return self.scaling.get_impedance() * self.scaling.get_time()

    def is_passive(self, m11, m12, m22):
        """Return True if the junction is passive and False if not
        """
        return abs(m12)**2 < m11 * m22

    def compute_passive_masses(self, r_main, r_side, rho, cond=20):
        """Return a passive version of the junction,
        usable for time simulation.

        Parameters
        ----------
        cond : float
            The largest allowed conditioning number for the mass matrix.

            /!\ Large conditioning means that some parasite modes
            will resonate strongly, resulting in numerical error /!\
        """
        eps = 1/cond
        m11, m12, m22 = self.compute_masses(r_main, r_side, rho)
        large_mass = (m11 + m22)/2 + abs(m12)
        m11_new = max(m11, eps * large_mass)
        m22_new = max(m22, eps * large_mass)
        if abs(m12)**2 >= m11 * m22 * (1-eps):
            m12_new = sqrt(m11_new * m22_new) * sign(m12) * (1-eps)
        else:
            m12_new = m12
        assert abs(m12_new)**2 < m11_new * m22_new
        return m11_new, m12_new, m22_new

    def compute_diagonal_masses(self, r_main, r_side, rho):
        """Diagonalized mass matrix M, and interaction matrix T

        Make mass matrix diagonal, by making variables gamma interact
        with all pipes.

        Evolution equation of the junction variables gamma is :
            M dt gamma - T p_123 = 0
        Contribution to the flow is :
            lbda_123 = T^* gamma

        Returns
        -------
        M : (2,) array
            Diagonal of the new mass matrix
        T : (2, 3) array
            New interaction matrix
        """
        m11, m12, m22 = self.compute_masses(r_main, r_side, rho)

        kappa = (m11 - m22)/(2*m12)
        D = np.sqrt(kappa**2 + 1)
        m_mean = (m11 + m22)/2
        m_plus = m_mean + m12*D
        m_minus = m_mean - m12*D
        tau_plus = -1/np.sqrt(2)*sqrt(1+kappa/D)
        tau_minus = -1/np.sqrt(2)*sqrt(1-kappa/D)

        T_new = np.matrix([[-tau_minus, tau_plus, tau_minus - tau_plus],
                          [tau_plus, tau_minus, -tau_plus - tau_minus]])
        M_new = np.array([m_minus, m_plus])

        return M_new, T_new

    def __compute_length_corr(self, a, b):
        d = b/a
        t_i = b*(0.82 - 0.193*d - 1.09*d**2 + 1.27*d**3 - 0.71*d**4)
        t_mv = 0
        if self.matching_volume:
            t_mv += b*d/8*(1 + .207*d**3)
        t_a = b*(-0.37 + 0.087*d)*d**2
        return t_i, t_mv, t_a

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
        t_i, t_mv, t_a = self.__compute_length_corr(a, b)
        t_s = t_i + t_mv
        m_s = rho*t_s/(pi*b**2) / coef_scaling_masses
        m_a = rho*t_a/(pi*a**2) / coef_scaling_masses

        m11 = m_s + m_a/4
        m12 = m_s - m_a/4

        return m11, m12, m11

    def get_diff_masses(self, r_main, r_side, rho, d_r_main, d_r_side):
        coef_scaling_masses = self.get_scaling_masses()

        a = r_main  # Radius of the main pipe
        b = r_side  # Radius of the hole
        da = d_r_main
        db = d_r_side
        d = b/a
        ddelta = (db/a - da/a*d)

        t_i, t_mv, t_a = self.__compute_length_corr(a, b)

        t_s = t_i + t_mv
        m_s = rho*t_s/(pi*b**2) / coef_scaling_masses

#        d_ts = (db*(0.82 - 2*0.193*d - 3*1.09*d**2 + 4*1.27*d**3 - 5*0.71*d**4)
#                + da*(0.193*d**2 + 2*1.09*d**3 - 3*1.27*d**4 + 4*0.71*d**5))
        d_ti = db/b*t_i + b*ddelta*(-0.193 - 2*1.09*d + 3*1.27*d**2 - 4*0.71*d**3)
        d_tmv = 0
        if self.matching_volume:
            d_tmv += db/b*t_mv + ddelta*b/8*(1 + 4*.207*d**3)
        d_ts = d_ti + d_tmv
        d_ms = (-2*db/b + d_ts/t_s)*m_s

        t_a = b*(-0.37 + 0.087*d)*d**2
        m_a = rho*t_a/(pi*a**2) / coef_scaling_masses
#        d_ta = db*(-3*0.37 + 4*0.087*d)*d**2 + da*(2*0.37 - 3*0.087*d)*d**3
        d_ta = db/b*t_a + b*ddelta*(-2*0.37*d + 3*0.087*d**2)
        d_ma = (-2*da/a + d_ta/t_a)*m_a

        dm11 = d_ms + d_ma/4
        dm12 = d_ms - d_ma/4
        return dm11, dm12, dm11

    def diff_diagonal_masses(self, r_main, r_side, rho, d_r_main, d_r_side):
        """ Computation valid only if m11==m22!!!"""
        dm11, dm12, dm22 = self.get_diff_masses(r_main, r_side, rho, d_r_main,
                                                d_r_side)
        assert dm11 == dm22
        dm_plus = dm11 + dm12
        dm_minus = dm11 - dm12
        dM = np.array([dm_minus, dm_plus])
        dT = np.matrix([[0, 0, 0], [0, 0, 0]])
        return dM, dT
