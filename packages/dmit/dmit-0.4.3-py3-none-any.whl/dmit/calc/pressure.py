#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tools for computing ps and slp
"""
import sys
import numpy as np


def netatmo_pressure_correction(p0, h):
    """Convert SLP reported by Netatmo to Surface pressure.
    Necessary because Netatmo uses a very crude formula.

    Parameters
    ----------
    p0 : float
        Netatmo SLP in hPa
    h : float
        Altitude of station in meters

    Returns
    -------
    ps : float
        Surface pressure
    """
    L = 0.0065  # K/m
    cp = 1007.  # J/(kg*K)
    T0 = 288.15  # K
    g = 9.82  # m/s**2
    M = 0.0289644  # kg/mol
    R = 8.31447  # J/(mol*K)

    ps = p0 * (1 - L * h / T0)**(g * M / (R * L))

    return ps


def wmo_ps_to_slp(Ps, H, T, RH=None, Td=None):
    """Correction to Sea Level Pressure using WMO recommendations

    Parameters
    ----------
    T : float
        2 m Temperature at station in Celcius
    Ps : float
        Station pressure in hPa
    Hp : float
        Station elevation in gpm
    RH : float (optional)
        Relative Humidity
    Td : float (optional)
        2 m Dewpoint temperature at station in Celcius

    Returns
    -------
    slp : float
        Sea level pressure in hPa

    Notes
    -----
    Either RH or Td must be specified. Otherwise a very bad guess is made.

    Following:
    https://www.wmo.int/pages/prog/www/IMOP/meetings/SI/ET-Stand-1/Doc-10_Pressure-red.pdf
    """

    Hp = H  # meters:
    # For now it is assumed that geopotentiel meters are close to meters
    # (which) is nearly true for the boundary layer.

    if Td is None:
        if RH is None:
            print('WARNING, None of Td and RH are set\nContinuing with guessed numbers')
            Td = T - 3.  # 3 is chosen randomly


    if not RH is None:
        es = 6.11 * 10**((7.5 * T) / (237.3 + T))
        e = RH * es

        A = 17.625
        B = 243.04  # C
        C = 610.94  # Pa

        # http://climate.envsci.rutgers.edu/pdf/LawrenceRHdewpointBAMS.pdf
        Td = (B * np.log(e / C)) / (A - np.log(e / C))

    if not Td is None:
        # Temperatures in C
        e = 6.11 * 10**((7.5 * Td) / (237.3 + Td))
        es = 6.11 * 10**((7.5 * T) / (237.3 + T))
        RH = e / es

    a = 0.0065  # K/gpm
    Ch = 0.12  # K/hPa
    Kp = 0.0148275  # K/gpm
    g = 9.80665  # m/s**2
    R = 287.05  # J/kg/K

    Ts = 273.15 + T

    slp = Ps * np.exp((g * Hp / R) / (Ts + 0.5 * a * Hp + e * Ch))

    if H < 50:  # meters
        Tv = (273.15 + T) / (1 - 0.379 *
                             (6.11 * 10**((7.5 * Td) / (237.7 + Td)) / Ps))
        C = Ps * Hp / (29.27 * Tv)
        slp = Ps + C

    return slp


def altimeter_setting(ps, altitude):
    """Follows computation from Madaus and Mass 2017 p. 513.
    It computes the altimeter setting from bias corrected values

    Parameters
    ----------
    ps : float
        Surface pressure in hPa
    altitude : float
        Altitude in m

    Returns
    -------
    slp : float
        Sea level pressure in hPa
    """
    data = ps

    k1 = 8.4228807 * 10**(-5)
    k2 = 0.190284

    slp = np.zeros(len(data))
    counter = 0
    i = 0
    for P in data:
        h = altitude[i]
        if h == -999.:
            slp[i] = np.nan
        else:
            Palt = (P - 0.3) * (1 + k1 * h / ((P - 0.3)**k2))**(1 / k2)
            slp[i] = Palt
        i += 1

    return slp
