#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tools for different geographical procedures often used.
"""
import numpy as np
from numpy import deg2rad, sin, cos, arctan2, sqrt, rad2deg, radians, arccos


__author__ = "Kasper Hintz"
__version__ = "0.1"
__email__ = "kah@dmi.dk"


def find_nearest_gridpoint(grid_lat, grid_lon, olat, olon, nx, ny, dx, dy, data):
    """Find nearest gridpoint in a regular grid

    Parameters
    ----------
    grid_lat : list
        List of latitudes in regular grid
    grid_lon : list
        List of longitudes in regular grid
    olat : float
        Latitude of point of interest
    olon : float
        Longitude of point of interest
    nx : integer
        Number of gridpoints in x-direction
    ny : integer
        Number of gridpoints in y-direction
    dx : float
        Horisontal resolution in degrees in x-direction
    dy : float
        Horisontal resolution in degrees in y-direction
    data : list
        List of data

    Returns
    -------
    datapoint : float
        The nearest value from data
    """
    i = int((olon - grid_lon[0]) / dx)
    j = int((olat - grid_lat[0]) / dy * nx)

    nearest_index = int((i % nx) + (j - (j % nx)))
    return data[nearest_index]


def point_inside_polygon(x, y, poly):
    """Checks if a point (x,y) is inside a polygon

    Parameters
    ----------
    x : float
        x-coordinate
    y : float
        y-coordinate
    poly : list
        List of tuples with points of the polygon

    Returns
    -------
    inside : boolean
        True if inside, False if outside
    """
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def distance(lon1, lat1, lon2, lat2):
    """Calculate great-circle distance in kilometers

    Parameters
    ----------
    lon1 : float
        Longitude of first point in degrees
    lat1 : float
        Latitude of first point in degrees
    lon2 : float
        Longitude of second point in degrees
    lat2 : float
        Latitude of second point in degrees

    Returns
    -------
    d : float
        Great-circle distance in kilometers
    """
    pi = np.pi
    radius = 6371.  # Earth radius
    dlat = deg2rad(lat2 - lat1) / 2.0
    dlon = deg2rad(lon2 - lon1) / 2.0

    a = sin(dlat)**2 + cos(deg2rad(lat1)) * cos(deg2rad(lat2)) * sin(dlon)**2
    d = 2.0 * radius * arctan2(sqrt(a), sqrt(1 - a))
    return d

# def coordinate_from_distance(lon1, lat1, dx, dy):
#     """
#     Calculate the point from a reference dx, dy km away
#     dx<0 = westwards
#     dy<0 = southwards
#     """
#     pi = np.pi
#     radius = 6371.
#     lat = deg2rad(lat1)
#     lon = deg2rad(lon1)


def bearing(lon1, lat1, lon2, lat2):
    """Calculate bearing between two points

    Parameters
    ----------
    lon1 : float
        Longitude of first point in degrees
    lat1 : float
        Latitude of first point in degrees
    lon2 : float
        Longitude of second point in degrees
    lat2 : float
        Latitude of second point in degrees

    Returns
    -------
    bearing : float
        Bearing in radians
    """
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)
    lon1 = deg2rad(lon1)
    lon2 = deg2rad(lon2)

    dlon = lon2 - lon1

    bearing = arctan2(sin(lon2 - lon1) * cos(lat2),
                      cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1))

    return bearing


def lon_lat_to_cartesian(lon, lat, R=1):
    """Calculates cartesian coordinates of a point on a sphere with radius R

    Parameters
    ----------
    lon : float
        Longitude
    lat : float
        Latitude
    R : float (optional)
        Radius of sphere, defaults to 1.

    Returns
    -------
    x : float
        x-coordinate
    y : float
        y-coordinate
    z : float
        z-coordinate
    """
    lon_r = radians(lon)
    lat_r = radians(lat)

    x = R * cos(lat_r) * cos(lon_r)
    y = R * cos(lat_r) * sin(lon_r)
    z = R * sin(lat_r)
    return x, y, z
