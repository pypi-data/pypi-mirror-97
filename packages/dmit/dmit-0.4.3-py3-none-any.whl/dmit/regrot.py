"""Conversion between regular and rotated spherical coordinates.
Original Source: Fortran SUBROUTINE regrof.F, by J.E. Haugen, 1992.
"""
from __future__ import division
import numpy as np
import sys

__author__ = "Kasper Hintz"
__credits__ = ["J.E. Haugen"]
__version__ = "0.2"
__email__ = "kah@dmi.dk"

pi = np.pi
rad = pi / 180.
radinv = 1. / rad


def rot_to_reg(pole_lon, pole_lat, lon, lat):
    """Rotates from rotated grid to regular grid

    Parameters
    ----------
    pole_lon : float
        Longitude of pole in degrees
    pole_lat : float
        Latitude of pole in degrees
    lon : float, list
        Longitudes of points in grid. Can also be a single point.
    lat : float, list
        Latitudes of points in grid. Can also be a single point.

    Returns
    -------
    lon1 : float, list
        Longitudes of regular grid. Same shape as input.
    lat1 : float, list
        Latitudes  of regular grid. Same shape as input.
    """
    sin_pole = np.sin(rad * (pole_lat + 90.))
    cos_pole = np.cos(rad * (pole_lat + 90.))

    sin_lon = np.sin(rad * lon)
    cos_lon = np.cos(rad * lon)
    sin_lat = np.sin(rad * lat)
    cos_lat = np.cos(rad * lat)

    lat_tmp = cos_pole * sin_lat + sin_pole * cos_lat * cos_lon

    try:
        lat_tmp[np.where(lat_tmp < -1.)] = -1.
        lat_tmp[np.where(lat_tmp > 1.)] = 1.
    except TypeError:
        if lat_tmp < -1.:
            lat_tmp = -1.
        if lat_tmp > 1.:
            lat_tmp = 1.

    lat2 = np.arcsin(lat_tmp) * radinv

    cos_lat2 = np.cos(lat2 * rad)

    cos_tmp = (cos_pole * cos_lat * cos_lon - sin_pole * sin_lat) / cos_lat2

    try:
        cos_tmp[np.where(cos_tmp < -1.)] = -1.
        cos_tmp[np.where(cos_tmp > 1.)] = 1.
    except TypeError:
        if cos_tmp < -1.:
            cos_tmp = -1.
        if cos_tmp > 1.:
            cos_tmp = 1.

    tmp_sin_lon = cos_lat * sin_lon / cos_lat2
    tmp_cos_lon = np.arccos(cos_tmp) * radinv

    try:
        tmp_cos_lon[np.where(tmp_sin_lon < 0.)] = - \
            tmp_cos_lon[np.where(tmp_sin_lon < 0.)]
    except IndexError:
        if tmp_sin_lon < 0.:
            tmp_cos_lon = -tmp_cos_lon

    lon2 = tmp_cos_lon + pole_lon

    return lon2, lat2


def reg_to_rot(pole_lon, pole_lat, lon, lat):
    """Rotates from regular grid to rotated grid

    Parameters
    ----------
    pole_lon : float
        Longitude of pole in degrees
    pole_lat : float
        Latitude of pole in degrees
    lon : float, list
        Longitudes of points in grid. Can also be a single point.
    lat : float, list
        Latitudes of points in grid. Can also be a single point.

    Returns
    -------
    lon1 : float, list
        Longitudes of rotated grid. Same shape as input.
    lat1 : float, list
        Latitudes  of rotated grid. Same shape as input.

    """
    sin_pole = np.sin(rad * (pole_lat + 90.))
    cos_pole = np.cos(rad * (pole_lat + 90.))

    tmp_lon = rad * (lon - pole_lon)

    sin_lon = np.sin(tmp_lon)
    cos_lon = np.cos(tmp_lon)
    sin_lat = np.sin(rad * lat)
    cos_lat = np.cos(rad * lat)

    lat_tmp = cos_pole * sin_lat - sin_pole * cos_lat * cos_lon

    try:
        lat_tmp[np.where(lat_tmp < -1.)] = -1.
        lat_tmp[np.where(lat_tmp > 1.)] = 1.
    except TypeError:
        if lat_tmp < -1:
            lat_tmp = -1.
        if lat_tmp > 1:
            lat_tmp = 1.

    lat2 = np.arcsin(lat_tmp) * radinv

    cos_tmp = np.cos(lat2 * rad)

    tmp_lon_rot = (cos_pole * cos_lat * cos_lon + sin_pole * sin_lat) / cos_tmp

    try:
        tmp_lon_rot[np.where(tmp_lon_rot < -1.)] = -1.
        tmp_lon_rot[np.where(tmp_lon_rot > 1.)] = 1.
    except TypeError:
        if tmp_lon_rot < -1.:
            tmp_lon_rot = -1.
        if tmp_lon_rot > 1.:
            tmp_lon_rot = 1.

    rot_check = cos_lat * sin_lon / cos_tmp

    lon2 = np.arccos(tmp_lon_rot) * radinv

    try:
        lon2[np.where(rot_check < 0.)] = -lon2[np.where(rot_check < 0.)]
    except IndexError:
        if rot_check < 0.:
            lon2 = -lon2

    return lon2, lat2
