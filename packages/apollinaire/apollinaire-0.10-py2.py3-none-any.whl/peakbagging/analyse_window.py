import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits

def sidelob_param (win, nu=None, dt=1., threshold=0.1, do_tf=True) :
  """
  :param win: input window
  :type win: ndarray
  :param nu: optional, frequency vector, default None.
  :type nu: ndarray
  :param dt: optional, timeseries sampling, default 1.
  :type dt: float
  :param threshold: limit power ratio to consider the sidelobes. 
  :type threshold: float 
  :param do_tf: set do_tf as True if timeseries is given, as False is the input is already in power
  (in this case, nu must be given as frequency vector), default, True.
  :type do_tf: bool

  :return: sidelob param of the window
  :rtype: list
  """
  if do_tf == True :
    tf_win = np.fft.fft (win) / win.size
    nu = np.fft.fftfreq (win.size, d=dt)
  else :
    tf_win = win
  param = []
  cond = np.abs(tf_win) > np.abs(tf_win[0])*treshold
  indexes, = np.where (cond)
  for ii in indexes :
    #ratio = np.abs (tf_win[ii])/np.abs(tf_win[0])
    ratio = np.abs (tf_win[ii])*np.abs(tf_win[ii])/(np.abs(tf_win[0])*np.abs(tf_win[0]))
    nu_sidelob = nu[ii]
    param.append ((ratio, nu_sidelob))
  return param

def wdw_to_fits (wdw, filename) :
  '''
  Save a window vector into fits file.

  :param wdw: window vector
  :type wdw: ndarray
  :param filename: name of the file to create.
  :type filename: str
  '''

  hdu = fits.PrimaryHDU (wdw)
  hdu.writeto (filename)

  return

