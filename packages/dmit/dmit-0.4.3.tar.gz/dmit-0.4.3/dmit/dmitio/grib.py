#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 \nUtility to read grib data
"""
import eccodes as ec
import pygrib
import xarray as xr
import numpy as np
import datetime as dt

class grib_reader:
    """Class to read and get data from gribfile
    """

    def __init__(self, namelist):
        """Init for grib_reader

        Parameters
        ----------
        namelist : dict
            dictionary containing namelist
        """
        variables = [k for k in namelist['grib_translators'].keys()]

        self.search_t2m = True if "t2m" in variables else False
        self.search_tp  = True if "precip" in variables else False

        self.found_t2m = False
        self.found_tp = False
        
        return


    def get_latlons(self, gribfile):
        """Uses pygrib to get coordinates
        Parameters
        ----------
        gribfile : str
            path to gribfile

        Returns
        -------
        array
            array with latitudes
        array
            array with longitudes
        """
        gr = pygrib.open(gribfile)
        lats, lons = gr[1].latlons()
        gr.close()
        return lats, lons


    def get_data(self, gribfiles, namelist, stepunit="m"):
        """Get data from gribfiles according to a namelist

        Parameters
        ----------
        gribfiles : list
            list with paths to gribfiles
        namelist : dict
            namelist of job

        Returns
        -------
        xarray.Dataset
            Dataset with data from gribfile
        """

        gribfiles = list(gribfiles)

        lats, lons = self.get_latlons(gribfiles[0])

        Nt = len(gribfiles)
        time = np.empty(Nt, dtype='i8')

        init = True
        k=0
        for gribfile in gribfiles:

            f = open(gribfile, 'rb')

            while True:

                gid = ec.codes_grib_new_from_file(f)
                if gid is None:
                    break

                ec.codes_set(gid, 'stepUnits', stepunit)

                if init:
                    latdim = ec.codes_get(gid, 'Ny')
                    londim = ec.codes_get(gid, 'Nx')
                    if self.search_t2m: t2m = np.zeros([Nt,latdim,londim])
                    if self.search_tp: tp = np.zeros([Nt,latdim,londim])
                    init=False

                shortName = ec.codes_get(gid, 'shortName')
                level = ec.codes_get(gid, 'level')
                dataDate = ec.codes_get(gid, 'dataDate')
                dataTime = ec.codes_get(gid, 'dataTime')
                leadTime = ec.codes_get(gid, 'step')

                
                ct = dt.datetime.strptime('{}{:02d}'.format(dataDate,dataTime), '%Y%m%d%H%M') + dt.timedelta(minutes=leadTime)
                time[k] = int((ct - dt.datetime(1970,1,1,0)).total_seconds())

                if (self.search_t2m) and (shortName=='t') and (level==2):
                    values = ec.codes_get_values(gid)
                    t2m[k,:,:] = values.reshape((latdim,londim))
                    self.found_t2m = True
                if (self.search_tp) and (shortName=='tp') and (level==0):
                    values = ec.codes_get_values(gid)
                    tp[k,:,:] = values.reshape((latdim,londim))
                    self.found_tp = True
                
                    
                ec.codes_release(gid)

            f.close()
            k+=1


        ds = xr.Dataset(
            data_vars=dict(
            ),
                coords=dict(
                    lon=(["y", "x"], lons),
                    lat=(["y", "x"], lats),
                    time=time,
                    )
            )

        if self.found_t2m: 
            t2m[np.where(t2m==0)] = np.nan
            ds = ds.assign(t2m= (("time", "y", "x"), t2m))
        if self.found_tp: 
            ds = ds.assign(tp= (("time", "y", "x"), tp))

        ds.attrs['starttime'] = time[0]
        
        return ds


