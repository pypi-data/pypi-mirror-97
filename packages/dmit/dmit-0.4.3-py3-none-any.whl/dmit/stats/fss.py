import sys
import numpy as np
from scipy import stats as ss

def calculate_fss(obs,mod,percentile=None,threshold=None,nmax=50):
    """Calculates FSS

    Parameters
    ----------
    obs : array
        Input array of truth (eg. observations)
    mod : array
        Input array of model (eg. model data)
    percentile : float (optional)
        Which percentile to use. Defaults to None
    threshold : float (optional)
        Which threshold to use. Defaults to None
    nmax : integer (optional)
        How many gridpoints to consider. Defaults to 50.

    Returns
    -------
    FSS : list
        List with FSS for different scales
    f0 : float
        FSS value for random values

    Notes
    -----
    Either percentile or threshold should be set.
    """

    if (percentile == None) and (threshold==None):
        sys.exit('All input to calculate_fss was None')

    FSS_NMAX  = nmax
    FSS_NSTOP = int(FSS_NMAX/2+1)
    FSS_RANGE = range(1,FSS_NMAX+2,2)
    FSS = np.zeros(FSS_NSTOP)

    # FZERO = (100. - percentile)/100. # Random Forecast FSS

    OBS_BIN = np.zeros(obs.shape)
    MOD_BIN = np.zeros(mod.shape)

    NY, NX = obs.shape

    # Create Binary Field
    if threshold==None:
        print('Using percentile', flush=True)
        OBS_CUTOFF = ss.scoreatpercentile(obs.flatten(),percentile)
        MOD_CUTOFF = ss.scoreatpercentile(mod.flatten(),percentile)
    if percentile==None:
        print('Using threshold', flush=True)
        OBS_CUTOFF = threshold
        MOD_CUTOFF = threshold

    OBS_WET = obs >= OBS_CUTOFF
    MOD_WET = mod >= MOD_CUTOFF

    OBS_BIN[OBS_WET] = 1.
    MOD_BIN[MOD_WET] = 1.

    f0 =  np.sum(OBS_BIN) / len(OBS_BIN.flatten())

    print('FSS_RANDOM = '+str(f0), flush=True)

    print('OBS,CUTOFF:'+str(OBS_CUTOFF),'MOD,CUTOFF:'+str(MOD_CUTOFF), flush=True)
    print('OBS,SUM:'+str(np.sum(OBS_BIN)),'MOD,SUM:'+str(np.sum(MOD_BIN)), flush=True)

    OBS_FRACTION = np.zeros(obs.shape)
    MOD_FRACTION = np.zeros(mod.shape)

    # print('Percent done with outer loop, cpu time for outer loop iteration')
    for i in range(FSS_NSTOP):

        n = FSS_RANGE[i]

        for iy in range(0,NY):
            YRS = int(iy-(n-1)/2)   # start
            YRE = int(iy-(n-1)/2+n) # end
            if YRS<0: YRS = 0
            if YRE>NY: YRE = NY

            for ix in range(0,NX):
                XRS = int(ix-(n-1)/2)
                XRE = int(ix-(n-1)+n)
                if XRS < 0: XRS = 0
                if XRE > NX: XRE = NX

                OBS_FRACTION[iy,ix] = 1./(n*n) * np.sum(OBS_BIN[YRS:YRE,XRS:XRE])
                MOD_FRACTION[iy,ix] = 1./(n*n) * np.sum(MOD_BIN[YRS:YRE,XRS:XRE])

        OBS_PROVINCIAL = np.sum(OBS_FRACTION*OBS_FRACTION)
        MOD_PROVINCIAL = np.sum(MOD_FRACTION*MOD_FRACTION)

        MSE     = np.sum((OBS_FRACTION-MOD_FRACTION)**2)
        MSE     = MSE*1./(NX*NY)

        MSE_REF = 1./(NX*NY) * (MOD_PROVINCIAL+OBS_PROVINCIAL)

        if MSE_REF != 0.:
            FSS[i] = 1. - (float(MSE)/float(MSE_REF))


    return FSS, f0
