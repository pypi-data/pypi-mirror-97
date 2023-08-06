#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 \nUtility to write netcdf files
"""
import xarray as xr
import numpy as np
import datetime as dt
import netCDF4 as nc

class netcdf_write:
    """Class to write netCDF files
    """

    def __init__(self, namelist):
        """Init function for netcdf_write class

        Parameters
        ----------
        namelist : dict
            Dictionary holding namelist
        """
        self.write_t2m = False
        self.write_tp = False

        return


    def write_data(self, ds, outputfile):
        """Writes data to netCDF file

        Parameters
        ----------
        ds : xarray.Dataset
            Dataset holding data should be written
        outputfile : str
            Path of the outputfile
        """

        variable_list = list(ds.keys())

        if 't2m' in variable_list: self.write_t2m = True
        if 'tp' in variable_list: self.write_tp = True


        ncf = nc.Dataset(outputfile,'w')
        ncf.institution = 'DMI'
        ncf.source = 'DMI'
        ncf.start_time = ds.attrs['starttime']

        dim_time = ncf.createDimension("time", ds.dims['time'])
        dim_lat  = ncf.createDimension("latitude", ds.dims['y'])
        dim_lon  = ncf.createDimension("longitude", ds.dims['x'])

        ncvar_time = ncf.createVariable('time', np.float64, ('time'), zlib=True)
        ncvar_time[:] = ds['time']
        ncvar_time.units = 'seconds since 1970-1-1 0:00:00'
        ncvar_time.coordinates = 'time'

        ncvar_lat = ncf.createVariable('latitude', np.float32, ('latitude','longitude'), zlib=True)
        ncvar_lat[:,:] = ds['lat']
        ncvar_lat.long_name = 'latitude, south is negative'
        ncvar_lat.units = 'degrees'

        ncvar_lon = ncf.createVariable('longitude', np.float32, ('latitude','longitude'), zlib=True)
        ncvar_lon[:,:] = ds['lon']
        ncvar_lon.long_name = 'longitude, west is negative'
        ncvar_lon.units = 'degrees'


        if self.write_t2m:
            ncvar_t2m = ncf.createVariable('air_temperature_2m', np.float32, ('time', 'latitude', 'longitude'), zlib=True)
            ncvar_t2m[:,:,:] = ds['t2m']
            ncvar_t2m.units = 'K'
            ncvar_t2m.long_name = 'air_temperature_2m'
        if self.write_tp:
            ncvar_tp = ncf.createVariable('total_precipitation', np.float32, ('time', 'latitude', 'longitude'), zlib=True)
            ncvar_tp[:,:,:] = ds['tp']
            ncvar_tp.units = 'mm'
            ncvar_tp.long_name = 'total_precipitation'

        ncf.close()

        return