# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from __future__ import division
from math import log, pi, exp
from scipy.constants import inch, foot, hour, Btu, degree_Fahrenheit

__all__ = ['R_to_k', 'k_to_R', 'k_to_thermal_resistivity',
'thermal_resistivity_to_k', 'R_value_to_k', 'k_to_R_value', 'R_cylinder']


def R_to_k(R, t, A=1.):
    r'''Returns the thermal conductivity of a substance given its thickness
    and thermal resistance.

    .. math::
        k = \frac{t}{RA}

    Parameters
    ----------
    R : float
        Thermal resistance of a substance [K/W or m^2*K/W]
    t : float
        Thickness of the substance used in the measurement of R, [m]
    A : float, optional
        Area; normally 1, [m^2]

    Returns
    -------
    k : float
        Thermal conductivity of a substance [W/m/K]

    Examples
    --------
    >>> R_to_k(R=0.05, t=0.025)
    0.5

    Notes
    -----
    When solving problems of changing areas, this value may be calculated with
    an area other than 1 m^2. Values in tables reported as properties of
    materials are often divided by area already; the conversion holds if A is 1.


    References
    ----------
    .. [1] Bergman, Theodore L., Adrienne S. Lavine, Frank P. Incropera, and
       David P. DeWitt. Introduction to Heat Transfer. 6E. Hoboken, NJ:
       Wiley, 2011.
    '''
    k = t/(A*R)
    return k


def k_to_R(k, t, A=1.):
    r'''Returns the thermal resistance of a substance given its thickness
    and thermal conductivity.

    .. math::
        R = \frac{t}{kA}

    Parameters
    ----------
    k : float
        Thermal conductivity of a substance [W/m/K]
    t : float
        Thickness of the substance for a given value of R, [m]
    A : float, optional
        Area; normally 1, [m^2]

    Returns
    -------
    R : float
        Thermal resistance of a substance [K/W]

    Examples
    --------
    >>> k_to_R(k=0.5, t=0.025)
    0.05

    Notes
    -----
    When solving problems of changing areas, this value may be calculated with
    an area other than 1 m^2. Values in tables reported as properties of
    materials are often divided by area already; the conversion holds if A is 1.

    References
    ----------
    .. [1] Bergman, Theodore L., Adrienne S. Lavine, Frank P. Incropera, and
       David P. DeWitt. Introduction to Heat Transfer. 6E. Hoboken, NJ:
       Wiley, 2011.
    '''
    R = t/(k*A)
    return R


def k_to_thermal_resistivity(k):
    r'''Returns the thermal resistivity of a substance given its thermal
    conductivity.

    .. math::
        r = \frac{1}{k}

    Parameters
    ----------
    k : float
        Thermal conductivity of a substance [W/m/K]

    Returns
    -------
    r : float
        Thermal resistivity of a substance [m*K/W]

    Examples
    --------
    >>> k_to_thermal_resistivity(0.25)
    4.0

    Notes
    -----
    Do not confuse this with thermal resistance! Often not introduced in heat
    transfer textbooks to avoid further confusion. Used almost exclusively
    as a desrciption of solids. Thermal resistivity has different units than
    R-value, but is of the same dimensionality.

    References
    ----------
    .. [1] Gesellschaft, V. D. I., ed. VDI Heat Atlas. 2nd edition.
       Berlin; New York:: Springer, 2010.
    '''
    r = 1./k
    return r


def thermal_resistivity_to_k(r):
    r'''Returns the thermal resistivity of a substance given its thermal
    conductivity.

    .. math::
        k = \frac{1}{r}

    Parameters
    ----------
    r : float
        Thermal resistivity of a substance [m*K/W]

    Returns
    -------
    k : float
        Thermal conductivity of a substance [W/m/K]

    Examples
    --------
    >>> thermal_resistivity_to_k(4)
    0.25

    Notes
    -----
    Do not confuse this with thermal resistance! Often not introduced in heat
    as a desrciption of solids. Thermal resistivity has different units than
    R-value, but is of the same dimensionality.

    References
    ----------
    .. [1] Gesellschaft, V. D. I., ed. VDI Heat Atlas. 2nd edition.
       Berlin; New York:: Springer, 2010.
    '''
    k = 1./r
    return k


def R_value_to_k(R_value, SI=True):
    r'''Returns the thermal conductivity of a substance given its R-value,
    which can be in either SI units of m^2 K/(W*inch) or the Imperial units
    of ft^2 deg F*h/(BTU*inch).

    Parameters
    ----------
    R_value : float
        R-value of a substance [m^2 K/(W*inch) or ft^2 deg F*h/(BTU*inch)]
    SI : bool, optional
        Whether to use the SI conversion or not

    Returns
    -------
    k : float
        Thermal conductivity of a substance [W/m/K]

    Notes
    -----
    If given input is SI, it is divided by 0.0254 (multiplied by 39.37) and
    then inversed. Otherwise, it is multiplied by 6.93347 and then inversed.

    Examples
    --------
    >>> R_value_to_k(0.12), R_value_to_k(0.71, SI=False)
    (0.2116666666666667, 0.20313787163983468)

    >>> R_value_to_k(1., SI=False)/R_value_to_k(1.)
    5.678263341113488

    References
    ----------
    .. [1] Gesellschaft, V. D. I., ed. VDI Heat Atlas. 2nd edition.
       Berlin; New York:: Springer, 2010.
    '''
    if SI:
        r = R_value/inch
    else:
        r = R_value*foot**2*degree_Fahrenheit*hour/Btu/inch
    k = thermal_resistivity_to_k(r)
    return k

#print [R_value_to_k(0.12), R_value_to_k(0.71, SI=False)]
#print [R_value_to_k(1., SI=False)/R_value_to_k(1.)]


def k_to_R_value(k, SI=True):
    r'''Returns the R-value of a substance given its thermal conductivity,
    Will return R-value in SI units unless SI is false. SI units are
    m^2 K/(W*inch); Imperial units of R-value are ft^2 deg F*h/(BTU*inch).

    Parameters
    ----------
    k : float
        Thermal conductivity of a substance [W/m/K]
    SI : bool, optional
        Whether to use the SI conversion or not

    Returns
    -------
    R_value : float
        R-value of a substance [m^2 K/(W*inch) or ft^2 deg F*h/(BTU*inch)]

    Notes
    -----
    Provides the reverse conversion of R_value_to_k.

    Examples
    --------
    >>> k_to_R_value(R_value_to_k(0.12)), k_to_R_value(R_value_to_k(0.71, SI=False), SI=False)
    (0.11999999999999998, 0.7099999999999999)

    References
    ----------
    .. [1] Gesellschaft, V. D. I., ed. VDI Heat Atlas. 2nd edition.
       Berlin; New York:: Springer, 2010.
    '''
    r = k_to_thermal_resistivity(k)
    if SI:
        R_value = r*inch
    else:
        R_value = r/(foot**2*degree_Fahrenheit*hour/Btu/inch)
    return R_value

#print [k_to_R_value(R_value_to_k(0.12)), k_to_R_value(R_value_to_k(0.71, SI=False), SI=False)]

#print k_to_R_value(0.7, SI=False)



def R_cylinder(Di, Do, k, L):
    r'''Returns the thermal resistance `R` of a cylinder of constant thermal
    conductivity `k`, of inner and outer diameter `Di` and `Do`, and with a
    length `L`.

    .. math::
        (hA)_{\text{cylinder}}=\frac{k}{\ln(D_o/D_i)} \cdot 2\pi L\\
        R_{\text{cylinder}}=\frac{1}{(hA)_{\text{cylinder}}}=
        \frac{\ln(D_o/D_i)}{2\pi Lk}

    Parameters
    ----------
    Di : float
        Inner diameter of the cylinder, [m]
    Do : float
        Outer diameter of the cylinder, [m]
    k : float
        Thermal conductivity of the cylinder, [W/m/K]
    L : float
        Length of the cylinder, [m]

    Returns
    -------
    R : float
        Thermal resistance [K/W]

    Examples
    --------
    >>> R_cylinder(0.9, 1., 20, 10)
    8.38432343682705e-05

    References
    ----------
    .. [1] Bergman, Theodore L., Adrienne S. Lavine, Frank P. Incropera, and
       David P. DeWitt. Introduction to Heat Transfer. 6E. Hoboken, NJ:
       Wiley, 2011.
    '''
    hA = k*2*pi*L/log(Do/Di)
    R = 1./hA
    return R
