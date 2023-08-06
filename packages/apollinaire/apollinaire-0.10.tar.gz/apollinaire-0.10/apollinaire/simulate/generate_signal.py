import numpy as np

"""
Generate a signal with Chi2 degrees of liberty
(amplitude and phase) to simulate seismic data
"""

# Initialize random state
def initialise (seed=567) :
  '''
  Seed the random generator.
  '''
  np.random.seed (seed=seed)
  return

def Lor (A, nu0, Gam, nu) :
  '''
  Compute lorentzian function

  :param A: amplitude of the lorentzian.
  :param nu0: central frequency.
  :param Gam: width of the Lorentzian.
  :param nu: vector of frequency
  :type A: float
  :type nu0: float
  :type Gam: float
  :type nu: ndarray

  :return: Lorentzian computed over nu.
  :rtype: ndarray
  '''
  den = 1 + 4. * (nu - nu0 ) * (nu - nu0) / (Gam * Gam) 
  return A / den

def g (nu) :
  '''
  Compute independant random gaussian value for each frequency contained
  in nu.
  
  :param nu: vector of frequency.
  :type nu: ndarray

  :return: array of gaussian noise
  :rtype: ndarray
  '''
  return np.random.normal (size=nu.size)

# Synthetic Fourier transforms
def gen_tf_1mode (A, nu0, Gam, nu, chi2=True, conv=False, window=None, T=1.) :

  """
  Generate the Fourier transform of the signal with one oscillation mode. 

  :param A: amplitude of the lorentzian.
  :type A: float
  :param nu0: central frequency.
  :type nu0: float
  :param Gam: width of the Lorentzian.
  :type Gam: float
  :param nu: vector of frequency
  :type nu: ndarray
  :param chi2: add chi2 distribution over the frequency range, default True.
  :type chi2: bool
  :param conv: convolute by a given window, default False.
  :type conv: bool
  :param window: window to use for the convolution, default None.
  :type window: ndarray
  :param T: the resolution of the signal, default 1.
  :type T: float

  :return: the synthetical TF computed over the frequency range.
  :rtype: ndarray
  """
  lor = Lor (A,nu0,Gam,nu) 
  if chi2 == True :
    exc_1 = g (nu)
    exc_2 = g (nu)
    lor = exc_1*np.sqrt(lor/2.)+1j*exc_2*np.sqrt(lor/2.)
  else : 
    lor = np.sqrt (lor)
  sig_mod = lor

  if conv == True :
    #process convolution with window 
    # (by equivalence Fourier theorem)
    s = np.fft.irfft (lor) * (lor.size / 2.)
    sig_mod = np.fft.rfft (window*s) / (s.size / 2. )

  return sig_mod

def gen_tf_multmode (param, nu, chi2=True, conv=False, window=None) :

  """
  Generate the Fourier transform of the signal with multiple oscillation mode. 

  :param param: input param of the lorentzians to compute.
  :type param: ndarray

  :param nu: vector of frequency
  :type nu: ndarray
  :param chi2: add chi2 distribution over the frequency range, default True.
  :type chi2: bool
  :param conv: convolute by a given window, default False.
  :type conv: bool
  :param window: window to use for the convolution, default None.
  :type window: ndarray

  :return: the synthetical TF computed over the frequency range.
  :rtype: ndarray

  .. note :: 'param' should be given the following way : [[A_1, nu0_1, Gam_1] [A_2, nu0_2, Gam_2] ... ]
  window should be given as a numpy array of 0 and 1. 
  """

  sig_mod = np.zeros (nu.size, dtype='complex128')
  for elt in param :
    A = elt[0]
    nu0 = elt[1]
    Gam = elt[2]
    lor = Lor (A,nu0,Gam,nu) 
    if chi2 == True :
      exc_1 = g (nu)
      exc_2 = g (nu)
      lor = exc_1*np.sqrt(lor/2.)+1j*exc_2*np.sqrt(lor/2.)
    else : 
      lor = np.sqrt (lor)
    sig_mod += lor

  #process convolution with window 
  # (by equivalence Fourier theorem)
  if conv == True :
    s = np.fft.irfft (sig_mod) * (window.size / 2.)
    sig_mod = np.fft.rfft (window*s) / (window.size / 2. )

  return sig_mod

def extract_window (series) :
  '''
  Extract observation window from a time series.
  
  :param series: input timeseries
  :type series: ndarray

  :return: window array of 0 and 1.
  :rtype: ndarray
  '''
  window = (np.abs (series) > 1.e-6).astype (int)
  return window

def convolute_window (series, model) :

  """
  Allow to convolute synthetic data by the window of a real timeseries.

  :param series: the real timeseries.
  :type series: ndarray

  :param model: should be given as a 1d-vector with only the amplitudes values 
  :type model: ndarray

  :return: the convoluted TF
  :rtype: ndarray
  """

  aux_series = np.fft.irfft (model) * (series.size / 2.)
  aux_series = extract_window (series) * aux_series
  convoluted_tf = np.fft.rfft (aux_series) / (aux_series.size / 2.) 

  return convoluted_tf

