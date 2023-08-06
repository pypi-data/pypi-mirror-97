import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import interp1d

def lowess_wrapper (s, v, frac=2./3., it=3, subset_size=None) :
    '''
    A lowess wrapper to use lowess on series with NaN
    values

    :param s: Julian day timestamps of the series.
    :type s: ndarray
  
    :param v: 1d velocity vector.
    :type v: ndarray

    :param fracfloat: between 0 and 1. i
    The fraction of the data used when estimating each y-value.
    Optional, default 2/3. 
    :type fracfloat: float.
    
    :param it: number of residual-based reweightings to perform.
    :type it: int

    :param subset_size: If a value is given, the input series
    will be divided in subset of size subset_size to perform 
    LOWESS operation. Optional, default None.
    :type subset_size: int
    ''' 

    # Interpolation strategy
    mask_zero = (v==0) | (np.isnan (v))
    v[mask_zero] = 0
    if v[~mask_zero].size > 0 :
        if v[0] == 0 : #avoid error in interpolation
            v[0] = v[~mask_zero][0]
            mask_zero = (v==0) | (np.isnan (v))
        if v[-1] == 0 : #avoid error in interpolation
            v[-1] = v[~mask_zero][-1]
            mask_zero = (v==0) | (np.isnan (v))
        f_interpo = interp1d (s[~mask_zero], v[~mask_zero])
        v[mask_zero] = f_interpo (s[mask_zero])
    
    if subset_size is None :
        subset_size = v.size
    n_subset = int (v.size / subset_size) + 1
    for ii in range (n_subset) :
        v_sub = v[ii*subset_size:min ((ii+1)*subset_size, v.size)]
        sub = s[ii*subset_size:min ((ii+1)*subset_size, v.size)]
        trend = lowess (v_sub, sub, frac=frac, it=it, is_sorted=True) [:,1]
        v_sub = v_sub - trend 
        v[ii*subset_size:min ((ii+1)*subset_size, v.size)] = v_sub
  
    v[mask_zero] = np.nan

    return v
