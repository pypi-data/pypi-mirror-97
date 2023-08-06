import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from astropy.stats import mad_std

def smooth (psd, smoothing=50) :

  if smoothing!=1 :
    psd = pd.Series(data=psd).rolling (window=smoothing, min_periods=1, win_type='triang', 
                             center=True).mean().to_numpy()

  return psd

def create_log_freq (freq, num=1000) :

  '''
  Take an array with frequency linearly spaced and returns an array
  with frequency logarithmically spaced
  '''

  log_freq = np.logspace (np.log10 (freq[1]), np.log10 (freq[-1]), num=num, endpoint=False) 
  # I use the 2nd bin and not the first to avoid a check_bound error in the interpolation

  return log_freq

def rebox_psd (freq, psd, new_freq, return_mad=True) :
  '''
  Create a new PSD vector using box defined by the ``new_freq`` vector
  and taking the median of the value inside the box as new value.
  '''
    
  new_psd = np.zeros (new_freq.size)
  new_psd_mad = np.zeros (new_freq.size)
  
  for ii in range (new_freq.size) :
    f = new_freq[ii]      
    if ii==0 :
      cond = np.abs (freq-f) < np.abs (freq-new_freq[ii+1])
      box = psd[cond]
    if ii==new_freq.size-1 :
      cond = np.abs (freq-f) < np.abs (freq-new_freq[ii-1])
      box = psd[cond]
    else :
      cond1 = np.abs (freq-f) < np.abs (freq-new_freq[ii-1])
      cond2 = np.abs (freq-f) < np.abs (freq-new_freq[ii+1])
      box = psd[cond1&cond2]
    new_psd[ii] = np.median (box)
    new_psd_mad[ii] = mad_std (box)
  
  new_freq = new_freq[~np.isnan(new_psd)]
  new_psd_mad = new_psd_mad[~np.isnan(new_psd)]
  new_psd = new_psd[~np.isnan(new_psd)]

  
  if return_mad :
    return new_freq, new_psd, new_psd_mad
  else :
    return new_freq, new_psd

def degrade_psd (freq, psd, num=1000, behaviour='reboxing') :
  '''
  Take a psd linearly sampled, smooth it, interpolate it
  and return a psd logarithmically sampled.

  :param freq: frequency array.
  :type freq: ndarray

  :param psd: power array
  :type psd: ndarray

  :param num: number of point in the output arrays.
  :type num: int

  :param smoothing: coeff used to smooth the input psd.
  :type smoothing: int

  :return: freq and psd logarithmically sampled.
  :rtype: tuple of ndarray
  '''

  log_freq = create_log_freq (freq, num=num)

  if behaviour=='smoothing' :
    psd = smooth (psd)
    f = interp1d (freq, psd)
    log_psd = f (log_freq)
  if behaviour=='reboxing' :
    log_freq, log_psd = rebox_psd (freq, psd, log_freq, return_mad=False)

  return log_freq, log_psd
