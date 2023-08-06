#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for sun-related calculations such as sunrise and sunset.
Adopted from:
https://stackoverflow.com/questions/19615350/calculate-sunrise-and-sunset-times-for-a-given-gps-coordinate-within-postgresql
"""
import sys
import math
import numpy as np
import datetime as dt
import warnings


def calc_sun_time(longitude, latitude, dl=dt.datetime.utcnow(), setrise='sunset', zenith=90.8):
    """Estimate sunset or sunrise in UTC time

    Parameters
    ----------
    longitude : float
        Longitude in degrees
    latitude : float
        Latitude in degrees
    dl : datetime.datetime (optional)
        Day of interest as datetime.datetime object. Defaults to utcnow().
    setrise : str (optional)
        'sunset' or 'sunrise'. Defaults to 'sunset'
    zenith : float (optional)
        Which zenith to use. Defaults to 90.8 degrees.

    Returns
    -------
    sun_dl : datetime.datetime
        datetime in which hour and minutes are either sunset or sunrise depending on input

    Examples
    --------
    >>> sunset = calcSunTime(12, 55, dt.datetime.utcnow(), setrise='sunset')
    >>> sunset = calcSunTime(12, 55, dt.datetime.utcnow(), setrise='sunrise')
    """
    if setrise == 'sunset':
        isRiseTime=False
    elif setrise == 'sunrise':
        isRiseTime=True
    else:
        raise SyntaxError('input argument "setrise" should be either "sunset" or "sunrise"')

    now = dl
    day, month, year = now.day, now.month, now.year

    TO_RAD = math.pi/180

    #1. Calculate the day of the year
    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + day - 30

    #2. Convert the longitude to hour value and calculate an approximate time
    lngHour = longitude / 15

    if isRiseTime:
        t = N + ((6 - lngHour) / 24)
    else:
        t = N + ((18 - lngHour) / 24)

    #3. Calculate the Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    #4. Calculate the Sun's true longitude
    L = M + (1.916 * math.sin(TO_RAD*M)) + (0.020 * math.sin(TO_RAD * 2 * M)) + 282.634
    L = L % 360

    #5a. calculate the Sun's right ascension

    RA = (1/TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD*L))
    RA = RA % 360

    #5b. right ascension value needs to be in the same quadrant as L
    Lquadrant  = (math.floor( L/90)) * 90
    RAquadrant = (math.floor(RA/90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

    #5c. right ascension value needs to be converted into hours
    RA = RA / 15

    #6. calculate the Sun's declination
    sinDec = 0.39782 * math.sin(TO_RAD*L)
    cosDec = math.cos(math.asin(sinDec))

    #7a. calculate the Sun's local hour angle
    cosH = (math.cos(TO_RAD*zenith) - (sinDec * math.sin(TO_RAD*latitude))) / (cosDec * math.cos(TO_RAD*latitude))

    if cosH > 1:
        warnings.warn('Sun never rises, returns None', RuntimeWarning)
        return None

    if cosH < -1:
        warnings.warn('Sun never sets, returns None', RuntimeWarning)
        return None

    #7b. finish calculating H and convert into hours
    if isRiseTime:
        H = 360 - (1/TO_RAD) * math.acos(cosH)
    else:
        H = (1/TO_RAD) * math.acos(cosH)

    H = H / 15

    #8. Calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622

    #9. Adjust back to UTC
    UT = T - lngHour
    UT = UT % 24
    hr = int(UT) % 24
    min = int(round((UT - int(UT))*60,0))

    sun_dl = dt.datetime(year, month, day, hr, min)

    return sun_dl


if __name__ == '__main__':
    dl = calcSunTime(12, 55, dt.datetime.utcnow(), setrise='sunset', zenith=90.8)
    print(dl.strftime('%H:%M'))
