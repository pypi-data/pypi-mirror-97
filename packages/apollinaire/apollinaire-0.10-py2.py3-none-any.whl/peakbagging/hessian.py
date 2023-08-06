import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .modified_optimize import _minimize_powell
from .fit_tools import *
from .likelihood import log_likelihood, log_likelihood_wdw, cond_transf
from .analyse_window import sidelob_param
import sys
import numdifftools as nd
import matplotlib
import matplotlib.pyplot as plt

def evaluate_hessian (df_a2z, freq, psd, back=None, wdw=None, low_bound_freq=1500, up_bound_freq=5000, instr='kepler') : 
  '''
  Evaluate hessian of the log likelihood function according to the parameters set to vary.

  :param df_a2z: input parameters as a pandas DataFrame with the a2z syntax.
  :type df_a2z: pandas DataFrame

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :param back: activity background vector that will be used to complete the model to fit. Optional default None.
  Must have the same length than freq and psd. 
  :type back: ndarray.

  :return: hessian of the likelihood according to the free parameters. 
  :rtype: ndarray
  '''

  param_to_fit, param_type, bounds_to_fit = a2z_df_to_param (df_a2z)

  #only take the log of height and width
  transform = ('height', 'width')
  cond = cond_transf (param_type, transform=transform)
  param_to_fit[cond] = np.log (param_to_fit[cond])
  param_to_fit = np.append (param_to_fit, 1.)

  if back is None :
    back = np.full (psd.size, 1.)

  psd_to_fit = psd / back

  if wdw is not None :
    param_wdw = sidelob_param (wdw, dt=dt)
    # only consider a given interval of frequency (ideally centered around the
    # p-mode region) to compute the likelihood values when performing the fit.
    aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]
    HessLikelihood = nd.Hessian (log_likelihood_wdw)
    hess = HessLikelihood (param_to_fit, param_type, aux_freq, aux_psd, aux_back, 
                           df_a2z, transform, param_wdw, instr)
  else :
    # only consider a given interval of frequency (ideally centered around the
    # p-mode region) to compute the likelihood values when performing the fit.
    aux_freq = freq[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_psd = psd_to_fit[(freq>low_bound_freq)&(freq<up_bound_freq)]
    aux_back = back[(freq>low_bound_freq)&(freq<up_bound_freq)]
    HessLikelihood = nd.Hessian (log_likelihood)
    hess = HessLikelihood (param_to_fit, param_type, aux_freq, aux_psd, aux_back, 
                           df_a2z, transform, instr)
    
  return hess

def evaluate_precision (df_a2z, freq, psd, back=None, wdw=None, show=False,
                 spectro=True, low_bound_freq=1500., up_bound_freq=5000., instr='kepler') : 
  '''
  Evaluate precision of the fitted parameters by computing and inverting the hessian. 
  Be careful, for height and width the standard deviation estimation is given for the logarithm
  of the parameter and not for the parameter itself.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power vector
  :type freq: ndarray

  :return: input DataFrame with precision values updated.
  :rtype: pandasDataFrame
  '''

  hess = evaluate_hessian (df_a2z, freq, psd, back=back, wdw=wdw, 
                           low_bound_freq=low_bound_freq, up_bound_freq=up_bound_freq, instr=instr)
  print ('Hessian')
  print (hess)
  inv_hess = np.linalg.inv (hess)
  print ('Inverted hessian')
  print (inv_hess)
  print ('Diagonal coefficients')
  print (np.diag (inv_hess))
  precision_values = np.sqrt (np.abs ((np.diag (inv_hess))))

  df_a2z.loc[df_a2z[6]==0, 5] = (precision_values[:precision_values.size-1]) 
  # be careful, for height and width the standard deviation estimation is given for the logarithm
  # of the parameter and not for the parameter itself.
  #the last value is just for background slight adjustement and not considered in the DataFrame. 

  if show == True :
    param = a2z_to_pkb (df_a2z)
    plot_from_param (param, freq, psd, back=back, wdw=wdw, smoothing=10, spectro=spectro, correct_width=1.,
                   show=True, save=False)

  return df_a2z


