import matplotlib
import numpy as np
import sys
import matplotlib.pyplot as plt
from pycorrelate import ucorrelate
from astropy.io import fits
from scipy.signal import hilbert 
from scipy.optimize import curve_fit

'''
This module provides tools to compute and fit cross
correlation between two timeseries.

'''

#AUX FUNCTIONS FOR THE FIT
def gaussian (x, A, alpha, beta) :
  '''
  Gaussian function that will be used to perform the fit.

  :param x: variable to consider
  :type x: ndarray

  :param A: amplitude factor
  :type A: float

  :param alpha: center value of the Gaussian
  :type alpha: float

  :param: beta: denominator parameter
  :type beta: float

  :return: Gaussian function corresponding to the x array.
  :rtype: ndarray
  '''
  return A * np.exp ( - (x - alpha) * (x - alpha) / beta )

def cos_gauss (x, alpha, f) :
  '''
  Gaussian cosinus that will be used to perform the fit. 

  :param x: variable to consider
  :type x: ndarray

  :param alpha: center value of the Gaussian
  :type alpha: float
 
  :param f: frequency of the cosinus
  :type f: float

  :return: Gaussian cosinus function corresponding to the x array.
  :rtype: ndarray
  '''
  global aux_beta
  global aux_A
  return gaussian (x, aux_A, alpha, aux_beta) * np.cos ( 2*np.pi*f * (x - alpha))

def cos_gauss_to_plot (x, alpha, f, A, beta) :
  '''
  Gaussian cosinus function needed for the plot in the verification plot
  in the compute shift function. 

  :param x: variable to consider
  :type x: ndarray

  :param alpha: center value of the Gaussian
  :type alpha: float
 
  :param f: frequency of the cosinus
  :type f: float

  :return: Gaussian cosinus function corresponding to the x array.
  :rtype: ndarray
  '''
  return gaussian (x, A, alpha, beta) * np.cos ( 2*np.pi*f * (x - alpha))

#----------------------------------------------------------

def compute_shift (sub1, sub2, maxlag, freq_init, shiftmax, lags=None, plot=False,
                   subindex=0) :
  '''
  Compute the cross correlation between two timeseries, fit a gaussian cosinus
  on it and compute a shift value between the two subseries.

  Refer to Appourchaux et al. 2018 for more precise explanation on the way the fit
  is performed.

  :param sub1: first subseries to consider.
  :type sub1: ndarray

  :param sub1: second subseries to consider.
  :type sub1: ndarray

  :param maxlag: maximum lag to consider between the two subseries.
  :type maxlag: float

  :param freq_init: first frequency guess to use for the gaussian cosinus fit.
  :type freq_init: float

  :param shiftmax: maximum possible shift between the two timeseries (shift will
  be computed modulo this value).
  :type shiftmax: float

  :param lags: lag array defined as : 
  lags = np.array ([i for i in range (-maxlag+1, maxlag)])
  Default to None (the function will compute it itself).
  May be given as an optional argument when looping over the function, 
  may save some memory.
  :type lags: ndarray

  :param plot: set to True to plot the result of the gaussian cosinus fit. Default False.
  :type plot: bool

  :param subindex: index of the subseries to compare. Default 0.
  :type subindex: float

  :return: shift between the two subseries.
  :rtype: float

  Example of parameters to give :
  if sampling==60 :
    maxlag=14 
    freq_init = 0.2
    shiftmax = 1
  if sampling==20 :
    maxlag=40 
    freq_init = 0.06
    shiftmax = 3
  if sampling==10 :
    maxlag=79 
    freq_init = 0.035
    shiftmax = 6
  if sampling==5 :
    maxlag=157 
    freq_init = 0.017
    shiftmax = 12
  '''
  if lags.all()==None :
    lags = np.array ([i for i in range (-maxlag+1, maxlag)])

  #COMPUTING CROSS CORRELATION
  corr_vec_1 = ucorrelate (sub2, sub1, maxlag=maxlag)
  corr_vec_1 = np.delete (corr_vec_1, 0)
  corr_vec_1 = corr_vec_1 [::-1]
  corr_vec_2 = ucorrelate (sub1, sub2, maxlag=maxlag)
  cc = np.concatenate ((corr_vec_1, corr_vec_2), axis=0)
  #normalisation step
  cc = cc / (sub2.std () * sub1.std () * sub2.size)
  cc = np.nan_to_num (cc, copy=False)
  h_cc = hilbert (cc)
  envelope = np.abs (h_cc)
  #FITTING STEP
  try :
    popt, pcov = curve_fit (gaussian, lags, envelope, p0=[1., 0., 1.], maxfev=10000) 
  except RuntimeError:
    print ('Subseries '  + str(subindex) + ': envelope fitting failed')
    popt = [0., 0., 0.]
  global aux_A
  global aux_beta
  aux_A = popt [0]
  cp_A = popt [0]
  aux_beta = popt [2]
  try :
    popt_cos, pcov_cos = curve_fit (cos_gauss, lags, cc, p0=np.array ([popt[1], freq_init]), maxfev=10000) 
  except RuntimeError:
    popt_cos = [0., 0.]
    print ('Subseries '  + str(subindex) + ': cos fitting failed')
  aux_A = - popt [0]
  try :
    popt_cos_2, pcov_cos_2 = curve_fit (cos_gauss, lags, cc, p0=np.array ([popt[1], freq_init]), maxfev=10000) 
  except RuntimeError:
    popt_cos_2 = [0., 0.]
    print ('Subseries '  + str(subindex) + ': cos fitting failed')

  if plot==True :
    lags_plot = np.linspace (-maxlag, maxlag, 500)
    plt.plot (lags, cc, color='orange')
  
  if np.abs (popt_cos_2 [0]) < np.abs (popt_cos [0]) :
    if plot==True :
      plt.plot (lags_plot, cos_gauss_to_plot (lags_plot, popt_cos_2[0], popt_cos_2 [1], aux_A, aux_beta), '--r')
      plt.show ()
    return popt_cos_2 [0] 
  else :
    if plot==True :
      plt.plot (lags_plot, cos_gauss_to_plot (lags_plot, popt_cos[0], popt_cos[1], cp_A, aux_beta), '--r')
      plt.show ()
    return popt_cos[0] 
