import numpy as np

'''
This file provides tools to :
- divide a timeseries in two and cross-correlate the two obtained Fourier
transform (divide_rephase).
- compute Fourier transform from a timeseries and change its phase (fft_rephase)
- rephase a given Fourier transform (rephase)
'''


def divide_rephase (s, dt, step=2) : #Takes series and sampling as input
  '''
  Divide a time series in two independent one,
  compute Fourier transforms and corrects phase

  .. warning :: for now, makes sure that the length of
  the series is a multiple of two
  (in order to obtain two subseries of same length
  and Fourier transform with exact same resolution)
  .. note :: if series length is odd, s2 will be shorter
  However, numpy.fft.fft seems to be able to remedy
  this problem with facultative parameter n

  :param s: series to take as input
  :type s: ndarray

  :param dt: sampling of the series
  :type dt: float

  :param step: step used to divide between the series
  :type step:
  ''' 
  if step == 1 :
    TF = np.fft.rfft (s) / (s.size/2.)
    freq = np.fft.rfftfreq (s.size, d=dt)
    return freq, TF, TF 
  
  if step%2 != 0 :
    raise ValueError ('step should not be odd (step=1 is only accepted for test purpose)')
  
  if step != 2 :
    aux = step//2
    s = s [:s.size-s.size%aux]
    s = np.reshape (s, (s.size//aux, aux))
    s = np.mean (s, axis=1)

  # ------------------------------------------------------
  # Divide and compute Fourier transform

  s1 =np.ravel (s[0::2])
  s2 =np.ravel (s[1::2])
  n = s2.size
  
  TF1 = np.fft.rfft (s1, n=n) / (n/2.)
  TF2 = np.fft.rfft (s2, n=n) / (n/2.)
  freq = np.fft.rfftfreq (n, d=dt*step)
  
  # -------------r-----------------------------------------
  # Rephase step
  TF2 = np.exp (- 1j * 2. * np.pi * (step//2) * dt * freq) * TF2

  return freq, TF1, TF2

def fft_rephase (s, dt, T) :
  """
  Compute the Fourier transform of a timeseries and
  rephase the FFT. 

  :param s: series to take as input
  :type s: ndarray

  :param dt: sampling of the series
  :type dt: float

  :param T: rephasing time
  :type T: float
  """
  TF = np.fft.rfft (s) / (s.size/2.)
  freq = np.fft.rfftfreq (s.size, d=dt)
  TF = np.exp (- 1j * 2. * np.pi * T * freq) * TF
  return freq, TF

def rephase (freq, tf, T) :
  """
  Compute the Fourier transform of a timeseries and
  rephase the FFT. 

  :param freq: frequency vector
  :type freq: ndarray 

  :param tf: Fourier transform to consider.
  :type tf: ndarray

  :param T: rephasing time
  :type T: float
  """
  tf = np.exp (- 1j * 2. * np.pi * T * freq) * tf
  return tf

