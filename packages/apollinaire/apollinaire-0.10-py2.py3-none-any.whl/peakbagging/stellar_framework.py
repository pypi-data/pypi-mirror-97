import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .background import perform_mle_background, explore_distribution_background, dnu_scale
from .global_pattern import perform_mle_pattern, explore_distribution_pattern
from .peakbagging import peakbagging
from .fit_tools import *


def stellar_framework (freq, psd, r, m, teff, dnu=None, back=None, numax=None, Hmax=None, Wenv=None, n_harvey=2, low_cut=10., guess_back=None, spectro=True, filename_back='background', 
                       back_mcmc=True, filemcmc_back='mcmc_sampler_background.h5', nsteps_mcmc_back=1000, pattern_mcmc=True, n_order=3, filename_pattern='pattern',
                       filemcmc_pattern='mcmc_sampler_pattern.h5', nsteps_mcmc_pattern=1000, parallelise=False, fit_l1=True,  
                       progress=False, a2z_file='modes_param.a2z', nsteps_mcmc_peakbagging=1000, mcmcDir='.', instr='geometric', filename_peakbagging='summary_peakbagging.pdf',
                       nopeakbagging=False, coeff_discard_back=50, coeff_discard_pattern=50, coeff_discard_pkb=50, thin_back=10, thin_pattern=10) :

  '''
  Framework for stellar peakbagging considering only a few input parameters.
  Background, global pattern and individual mode parameters are successively fitted.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power or power spectral density vector
  :type freq: ndarray

  :param r: stellar radius. Given in solar radius.
  :type r: float

  :param m: stellar mass. Given in solar masses. 
  :type m: float

  :param teff: stellar effective temperature. Given in Kelvins. 
  :type teff: float

  :param dnu: large frequency separation. Must be given in muHz. If ``None``, will be computed through scaling laws. 
    Optional, default ``None``.
  :type dnu: float

  :param back: array of fitted background, of same length as *freq* and *psd*. If given, no fit will be performed on background
    and the pattern step will directly take place. Hmax, Wenv and numax must in this case also be given. Optional, default ``None``.
  :type back: ndarray

  :param numax: maximum of power in p-mode envelope. Must be given in muHz.
  :type numax: float

  :param Hmax: amplitude of p-mode envelope
  :type Hmax: float

  :param Wenv: width of p-mode envelope
  :type Wenv: float

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. With more than two Harvey laws, it is strongly recommended
    to manually feed the 'guess' parameter.  
  :type n_harvey: int

  :param guess_back: first guess directly passed by the user. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Backgrounds parameters given in the following order:
    *param_harvey (3), param_plaw (2), param_gaussian (3), white noise (1)*. 
  :type guess_back: array-like.

  :param spectro: if set to ``True``, make the plot with unit consistent with radial velocity, else with 
    photometry. Optional, default ``True``.
  :type spectro: bool

  :param filename_back: name of the of the dat file of the fitted background, the background parameters pdf file where the plot will be stored.
    Optional, default ``background``.
  :type filename_back: str

  :param back_mcmc: If set to ``False``, no MCMC sampling will be performed for the background. Optional, default ``True``.
  :type back_mcmc: bool
  
  :param filemcmc_back: Name of the hdf5 file where the MCMC background chain will be stored. Optional, default ``mcmc_sampler_background.h5``.
  :type filemcmc_back: str

  :param nsteps_mcmc_back: number of MCMC steps for the background parameters exploration. Optional, default 1000.
  :type nsteps_mcmc_back: int

  :param pattern_mcmc: If set to ``False``, no MCMC sampling will be performed for the pattern. Optional, default ``True``.
  :type pattern_mcmc: bool
  
  :param n_order: number of fitted orders. Optional, default 3. 
  :type n_order: int
  :type back: ndarray.

  :param filename_pattern: name of the pdf file where the fitted global pattern parameters and the plot of the fitted global pattern will be stored.
    Optional, default ``pattern``.
  :type filename_pattern: str
  
  :param filemcmc_pattern: Name of the hdf5 file where the MCMC pattern chain will be stored. Optional, default ``mcmc_sampler_pattern.h5``.
  :type filemcmc_pattern: str

  :param nsteps_mcmc_pattern: number of MCMC steps for the pattern parameters exploration. Optional, default 1000.
  :type nsteps_mcmc_pattern: int

  :param parallelise: if set to ``True``, multiprocessing will be used to sample the MCMC. Optional, default ``False``.
  :type parallelise: bool

  :param fit_l1: set to ``True`` to fit the d01 param and create guess for l=1 modes. Optional, default ``True``.
  :type fit_l1: bool

  :param progress: show progress bar in terminal. Optional, default ``False``.
  :type progress: bool

  :param a2z_file: name of the a2z file where the individual parameters will be stored. This will also be used to name the output pkb file.
    Optional, default ``modes_param.a2z``
  :type a2z_file: str

  :param nsteps_mcmc_peakbagging: number of MCMC steps for the peakbagging parameters exploration. Optional, default 1000.
  :type nsteps_mcmc_peakbagging: int

  :param mcmcDir: Name of the directory where the MCMC of the individual parameters should be stored. Optional, default ``.``.
  :type mcmcDir: str

  :param instr: name of the instrument for which m-amplitude ratios will be computed. ``geometric``, ``golf`` and ``virgo`` are available.
  :type instr: str
  
  :param filename_peakbagging: name of the file where the plot summary of the individual mode parameters peakbagging will be stored.
    Optional, default ``summary_peakbagging.pdf``.
  :type filename_peakbagging: str

  :param nopeakbagging: if set to ``True``, individual modes parameters will not be fitted. Optional, default ``False``.
  :type nopeakbagging: bool

  :param coeff_discard_back: coefficient used to compute the number of values to discard at the beginning
    of each MCMC sampled by the background step : total amount of sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :param coeff_discard_pattern: coefficient used to compute the number of values to discard at the beginning
    of each MCMC sampled by the pattern step : total amount of sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :param coeff_discard_pkb: coefficient used to compute the number of values to discard at the beginning
    of each MCMC sampled by the peakbagging step : total amount of sampled values will be divided by coeff_discard. Optional, default 50.
  :type coeff_discard: int

  :param thin_back: take only every ``thin`` steps from the chain sampled for backgrounds parameters. Optional, default 10. 
  :type thin_back: int

  :param thin_pattern: take only every ``thin`` steps from the chain sampled for pattern parameters. Optional, default 10. 
  :type thin_pattern: int

  :return: ``None``
  '''

  if back is None :
    fitted_back, param_back = perform_mle_background (freq, psd, n_harvey=n_harvey, r=r, m=m, 
                              teff=teff, guess=guess_back, frozen_param=None, power_law=False,
                              frozen_harvey_exponent=False, fmin=None, fmax=None, low_cut=low_cut, fit_log=True,
                              low_bounds=None, up_bounds=None, no_bounds=False, show=False, show_guess=False, filename=filename_back+'.pdf', spectro=spectro)
    np.savetxt (filename_back+'_parameters.dat', param_back, fmt='%-s')

    if back_mcmc :
      fitted_back, param_back, sigma_back  = explore_distribution_background (freq, psd,
                                       n_harvey=n_harvey, r=r, m=m, teff=teff, guess=param_back, frozen_param=None, power_law=False,
                                       frozen_harvey_exponent=False, fmin=None, fmax=None, low_cut=low_cut, fit_log=True,
                                       low_bounds=None, up_bounds=None, spectro=spectro, show=False, show_guess=False, show_corner=True,
                                       nsteps=nsteps_mcmc_back, filename=filename_back+'.pdf', parallelise=progress, progress=progress, nwalkers=64, 
                                       filemcmc=filemcmc_back, coeff_discard=coeff_discard_back, thin=thin_back)
      np.savetxt (filename_back+'_parameters.dat', np.c_[param_back, sigma_back], fmt='%-s')
    
    numax = param_back[n_harvey*3+3]
    Hmax = 0.5 * np.max (psd[(freq>0.99*numax)&(freq<1.01*numax)]) 
    Wenv = param_back[n_harvey*3+4] 

    np.savetxt (filename_back+'.dat', fitted_back, fmt='%-s')

  else :
    fitted_back = back


  if dnu is None :
    dnu = dnu_scale (r, m)

  df_a2z, pattern = perform_mle_pattern (dnu, numax, Hmax, Wenv, teff, freq, psd, back=fitted_back, wdw=None, 
                         n_order=n_order, split=0, angle=0, fit_l1=fit_l1, mass=m, show=False, filename=filename_pattern+'.pdf',
                         fit_log=False)

  if pattern_mcmc :
    df_a2z, pattern = explore_distribution_pattern (dnu, numax, Hmax, Wenv, teff, freq, psd, back=fitted_back, wdw=None,
                         n_order=n_order, split=0, angle=0, fit_l1=fit_l1, mass=m, guess=pattern, show=False,
                         fit_log=False, show_corner=True, nsteps=nsteps_mcmc_pattern, filename=filename_pattern+'.pdf', parallelise=parallelise, progress=progress,
                         nwalkers=64, filemcmc=filemcmc_pattern, coeff_discard=coeff_discard_pattern, thin=thin_pattern)

  np.savetxt (filename_pattern+'.dat', pattern, fmt='%-s')
  save_a2z (a2z_file, df_a2z)

  if not nopeakbagging :
    df_a2z = peakbagging (a2z_file, freq, psd, back=fitted_back, wdw=None, spectro=spectro,
                   compute_hessian=False, fit_splittings=False, nsteps_mcmc=nsteps_mcmc_peakbagging, show_corner=True,
                   store_chains=True, mcmcDir=mcmcDir, order_to_fit=None, parallelise=parallelise, progress=progress,
                   strategy='order', nwalkers=64, normalise=False, instr=instr, filename_summary=filename_peakbagging, show=False,
                   coeff_discard=coeff_discard_pkb)

    save_a2z (a2z_file, df_a2z)

  pkb = a2z_to_pkb (df_a2z)
  
  np.savetxt (a2z_file[:len(a2z_file)-3]+'pkb', pkb, fmt='%-s') 

  return 
