import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

'''
Module to compute power spectra density (PSD) from
  timeseries (series_to_psd) or Fourier transform 
  (tf_to_psd).

PSD can then be saved as fits file with the psd_to_fits
  function.

PSD saved into fits file can be directly plotted with the 
  plot_fits function.

The echelle_diagram function allow to compute and optionnally
  plot the echelle diagram of the PSD.
'''

def tf (series, dt) :

  """
  Take a timeseries and compute its properly normalised
  Fourier transform.

  :param series: input timeseries
  :type series: ndarray

  :param dt: sampling of the timeseries
  :type dt: float

  :return: frequency and psd array
  :rtype: tuple of ndarray
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)

  return freq, tf

def series_to_psd (series, dt, correct_dc=False) :

  """
  Take a timeseries and compute its PSD

  :param series: input timeseries
  :type series: ndarray

  :param dt: sampling of the timeseries
  :type dt: float

  :param correct_dc: if set to True, will compute the duty_cycle
    to adjust the psd values. Optional, default False.
  :type correct_dc: bool

  :return: frequency and psd array
  :rtype: tuple of ndarray
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)
  T = series.size * dt
  PSD = np.abs (tf) * np.abs (tf) * T / 2.

  if correct_dc :
    dc = np.count_nonzero (series) / series.size
    PSD = PSD / dc

  return freq, PSD

def tf_to_psd (tf, T) :

  '''
  :param tf: complex Fourier transform from which to
    compute the PSD.
  :type tf: ndarray 

  :param T: resolution of the Fourier transform.
  :type T: float

  :return: corresponding PSD
  :rtype: ndarray
  '''

  PSD = np.abs (tf) * np.abs (tf) * T / 2.
  return PSD 


def psd_to_fits (freq, psd, filename) :
  '''
  Save frequency and power vector into a fits file.

  :param freq: frequency vector.
  :type freq: ndarray
  :param psd: psd vector.
  :type psd: ndarray
  :param filename: name of the fits file to create.
  :type filename: str
  '''

  data = np.c_[freq,psd]
  hdu = fits.PrimaryHDU (data)
  hdu.writeto (filename)

  return

def plot_psd_fits (filename, rv=True, index=0) :
  '''
  Plot the PSD of a fits file containing frequency and power 
  array. The frequency in the file are supposed to be in Hz and
  the power in (m/s)^2/Hz (spectroscopy) or ppm^2/Hz (photometry)

  :param filename: name of the fits file
  :type filename: str

  :param rv: set to True if it is a radial velocity PSD, to False
    if it is a photometric PSD.
  :type rv: bool

  :param index: index of the hdulist of the fits file where the PSD can
    be found. Default is 0.
  :type index: int
  '''

  hdu = fits.open (filename) [index]
  data = np.array (hdu.data)
  fig = plt.figure (figsize=(12,6))
  ax = fig.add_subplot (111)
  ax.plot (data[:,0]*1.e6, data[:,1]*1.e-6)
  ax.set_xlabel (r'Frequency ($\mu$Hz)')
  if rv==True :
     ax.set_ylabel (r'PSD ((m/s)$^2$/$\mu$Hz)')
  else :
     ax.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)')

  return

def echelle_diagram (freq, PSD, dnu, plot=True, twice=False,
                   smooth=10, cmap='inferno') :

  '''
  Build the echelle diagram of a given PSD. It is preferable that the
  PSD has been prealably slice around the p-modes region. 

  :param freq: input vector of frequencies.
  :type freq: ndarray

  :param PSD: input vector of power. Must be of same size than freq.
  :type PSD: ndarray

  :param dnu: the large frequency separation use to cut slices 
    into the diagram. 
  :type dnu: float

  :param plot: plot the echelle diagram directly, default True.
  :type plot: bool

  :param twice: slice using 2 x *dnu* instead of *dnu*, default False.
  :type twice: bool

  :param smooth: size of the rolling window used to smooth the PSD. Default 10.
  :type smooth: int

  :param cmap: select one available color map provided by matplotlib, default ``inferno``
  :type cmap: str

  :return: the echelle diagram matrix.
  :rtype: ndarray
  '''


  if smooth != 1 :
    PSD = pd.Series(data=PSD).rolling (window=smooth, min_periods=1, 
                             center=True).mean().to_numpy()

  if twice==True :
    dnu = 2.*dnu

  res = freq[2]-freq[1]
  start = int (freq[0]*1.e6 / dnu + 1.) * dnu
  stop = int (freq[-1]*1.e6 / dnu) * dnu
 
  ind, = np.where ((freq > start*1e-6) & (freq < stop*1e-6))
  freq = freq[ind]
  PSD = PSD[ind]

  n_slice = int (round (freq.size*res*1.0e6 / dnu))
  len_slice = int (round ((freq[-1]-freq[0]) / (n_slice*res)))

  if (n_slice*len_slice > PSD.size) :
    len_slice -= 1

  ed = PSD[:len_slice*n_slice]
  ed = np.reshape (ed, (n_slice, len_slice))

  freq_ed = freq[:len_slice*n_slice]
  freq_ed = np.reshape (freq_ed, (n_slice, len_slice))
  x_freq = freq_ed[0,:] - freq_ed[0,0]
  y_freq = freq_ed[:,0]

  if plot==True :
    fig = plt.figure ()
    ax = fig.add_subplot (111)
    ax.pcolormesh (x_freq*1.e6, y_freq*1.e6, ed, cmap=cmap)
    ax.set_xlabel (r'Frequency mod. ' + str('%.1f' % dnu) + r' $\mu$Hz')
    ax.set_ylabel (r'Frequency ($\mu$Hz)')
    plt.show ()

  return ed
