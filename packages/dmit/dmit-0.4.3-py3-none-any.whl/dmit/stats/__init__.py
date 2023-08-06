"""
Module containing simple standard statistics functions
"""
import numpy as np
from scipy.stats.stats import pearsonr

def bias(ref,obs):
    """calculates the bias between two arrays

    Parameters
    ----------
    ref : list
        Reference list
    obs : list
        Comparison list (e.g. Observations)

    Returns
    -------
    bias : float
        Bias from the two lists.
    """
    return np.mean(obs-ref)


def rmse(model,obs):
    """Calculates the Root Mean Square Error

    Parameters
    ----------
    model : list
        List containing model values
    obs : list
        List containing observations (reference)

    Returns
    -------
    rmse : float
        Root mean square error
    """

    N = np.count_nonzero(~np.isnan(obs))
    RMSE = np.sqrt(np.nansum((model-obs)**2)/(N-1))
    return RMSE


def variance(obs):
    """Calculates the variance for a list

    Parameters
    ----------
    obs : list
        list of values (eg. observations)

    Returns
    -------
    var : float
        variance of input list

    """
    return np.var(obs, ddof=1) # ddof = 1 > denominator=n-1


def std(obs):
    """Calculates the standard deviation

    Parameters
    ----------
    obs : list
        List with values (eg. observations)
    Returns
    -------
    std : float
        Standard deviation of input list
    """
    return np.sqrt(variance(obs))


def correlation(x,y):
    """Calculates the pearson correlation coefficient

    Parameters
    ----------
    x : list
        List of values
    y : list
        List of values

    Returns
    -------
    R : float
        Pearson correlation coefficient for input lists
    """
    return pearsonr(x,y)
