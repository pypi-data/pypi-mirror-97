import numpy as np
from .divide_rephase import divide_rephase
import matplotlib

'''
Provides function to compute cross-correlation between
two Fourier transform.

See Elsworth et al. (1993). 
'''

def cross_correlate (tf1, tf2, T) :
  '''
  Compute the cross spectrum between two Fourier transform.

  :param tf1: first Fourier transform to consider.
  :type tf1: ndarray 

  :param tf2: second Fourier transform to consider.
  :type tf2: ndarray

  :param T: resolution of the Fourier transform
  :type T: float

  :return: cross spectrum
  :rtype: ndarray
  '''

  spect = ( tf1 * np.conj (tf2) ) / 2.
  spect = spect * T
  return spect

def coherence (tf1, tf2) :
  '''
  Compute the coherence of the cross spectrum between two Fourier transform.

  :param tf1: first Fourier transform to consider.
  :type tf1: ndarray 

  :param tf2: second Fourier transform to consider.
  :type tf2: ndarray

  :param T: resolution of the Fourier transform
  :type T: float

  :return: coherence vector
  :rtype: ndarray
  '''

  spect = cross_correlate (tf1, tf2, T)
  psd1 = tf_to_psd (tf1)
  psd2 = tf_to_psd (tf2)
  c = spect / np.sqrt (psd1 * psd2)
  return c
  
