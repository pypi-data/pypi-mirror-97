# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .background import (perform_mle_background, explore_distribution_background, 
                         dnu_scale, numax_scale)
from .global_pattern import (perform_mle_pattern, explore_distribution_pattern,
                             list_order_to_fit, pattern_to_a2z)
from .peakbagging import peakbagging
from .fit_tools import *


def stellar_framework (freq, psd, r, m, teff, nwalkers=64, dnu=None, back=None, numax=None, Hmax=None, Wenv=None, epsilon=None, 
                       n_harvey=2, low_cut=10., guess_back=None, spectro=False, filename_back='background', 
                       back_mcmc=True, filemcmc_back='mcmc_sampler_background.h5', nsteps_mcmc_back=1000, pattern_mcmc=True, n_order=3, 
                       n_order_peakbagging=3, filename_pattern='pattern',
                       filemcmc_pattern='mcmc_sampler_pattern.h5', nsteps_mcmc_pattern=1000, parallelise=False, 
                       fit_l1=True, fit_l3=False, use_numax_back=False,  
                       progress=False, a2z_file='modes_param.a2z', a2z_in=None, nsteps_mcmc_peakbagging=1000, 
                       mcmcDir='.', instr='geometric', filename_peakbagging='summary_peakbagging.pdf',
                       nopeakbagging=False, coeff_discard_back=5, coeff_discard_pattern=5, coeff_discard_pkb=5, thin_back=1, thin_pattern=1, quickfit=False,
                       num=500, save_only_after_sampling=False, apodisation=False, fit_angle=False, guess_angle=90, fit_splittings=False, guess_split=0.4,
                       frozen_harvey_exponent=False) :

  '''
  Framework for stellar peakbagging considering only a few input parameters.
  Background, global pattern and individual mode parameters are successively fitted.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: real power or power spectral density vector
  :type psd: ndarray

  :param r: stellar radius. Given in solar radius.
  :type r: float

  :param m: stellar mass. Given in solar masses. 
  :type m: float

  :param teff: stellar effective temperature. Given in Kelvins. 
  :type teff: float

  :param nwalkers: number of walkers for the MCMC process. Optional, default 64.
  :type nwalkers: int

  :param dnu: large frequency separation. Must be given in µHz. If ``None``, will be computed through scaling laws. 
    Optional, default ``None``.
  :type dnu: float

  :param back: array of fitted background, of same length as *freq* and *psd*. If given, no fit will be performed on background
    and the pattern step will directly take place. ``Hmax``, ``Wenv`` and ``numax`` must in this case also be given. 
    Optional, default ``None``.
  :type back: ndarray

  :param numax: maximum of power in p-mode envelope. Must be given in µHz. Optional, default ``None``.
  :type numax: float

  :param Hmax: amplitude of p-mode envelope. Optional, default ``None``.
  :type Hmax: float

  :param Wenv: width of p-mode envelope. Optional, default ``None``.
  :type Wenv: float

  :param epsilon: epsilon value of mode patterns. If given, will override the value computed by the automatic guess. 
    Optional, default ``None``.
  :type epsilon: float

  :param n_harvey: number of Harvey laws to use to build the background
    model. Optional, default 2. With more than two Harvey laws, it is strongly recommended
    to manually feed the 'guess' parameter.  
  :type n_harvey: int

  :param guess_back: first guess directly passed by the user. If guess is ``None``, the 
    function will automatically infer a first guess. Optional, default ``None``.
    Backgrounds parameters given in the following order:
    *param_harvey (3* ``n_harvey`` *), param_plaw (2), param_gaussian (3), white noise (1)*. 
  :type guess_back: array-like.

  :param spectro: if set to ``True``, make the plot with unit consistent with radial velocity, else with 
    photometry. Optional, default ``False``.
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
  
  :param n_order: number of orders to consider for the global pattern fit. Optional, default 3. 
  :type n_order: int

  :param n_order_peakbagging: number of orders to fit at the individual mode parameters step. Optional, default 3. 
  :type n_order_peakbagging: int

  :param filename_pattern: name of the pdf file where the fitted global pattern parameters and the plot of the fitted global pattern will be stored.
    Optional, default ``pattern``.
  :type filename_pattern: str
  
  :param filemcmc_pattern: Name of the hdf5 file where the MCMC pattern chain will be stored. Optional, default ``mcmc_sampler_pattern.h5``.
  :type filemcmc_pattern: str

  :param nsteps_mcmc_pattern: number of MCMC steps for the pattern parameters exploration. Optional, default 1000.
  :type nsteps_mcmc_pattern: int

  :param parallelise: if set to ``True``, multiprocessing will be used to sample the MCMC. Optional, default ``False``.
  :type parallelise: bool

  :param fit_l1: set to ``True`` to fit the d01 and b03 param and create guess for l=1 modes. Optional, default ``True``.
  :type fit_l1: bool

  :param fit_l3: set to ``True`` to fit the d03 and b03 param and create guess for l=3 modes. Optional, default ``False``.
    ``fit_l1`` must be set to ``True``. 
  :type fit_l3: bool

  :param use_numax_back: if set to ``True``, the ``numax`` values computed with the background fit will be used as input guess for the pattern fit.
    Otherwise, the initial ``numax`` for the pattern fit will be taken from the ``numax`` argument or computed with the scaling laws. 
  :type use_numax_back: bool

  :param progress: show progress bar in terminal. Optional, default ``False``.
  :type progress: bool

  :param a2z_file: name of the a2z file where the individual parameters will be stored. This will also be used to name the output pkb file.
    Optional, default ``modes_param.a2z``
  :type a2z_file: str

  :param a2z_in: a2z file with guess input for individual parameters. If
    provided, the global pattern step will be ignored and the function will
    directly sample individual modes parameters (after sampling the background if
    it has not been provided too). Optional, default ``None``. 
  :type a2z_in: str

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

  :param quickfit: if set to ``True``, the fit will be performed over a smoothed and logarithmically resampled background.
    Optional, default ``False``. 
  :type quickfit: bool

  :param num: number of point to consider in the degraded PSD if ``quickfit`` is set to True. Optional, default 500.
  :type num: int

  :param save_only_after_sampling: if set to True, hdf5 file with chains information will only be saved at the end of the sampling
    process. If set to False, the file will be saved step by step (see ``emcee`` documentation).
  :type saveon_only_after_sampling: bool

  :param apodisation: if set to ``True``, distort the model to take the apodisation into account. Optional, default ``False``.
  :type apodisation: bool

  :param fit_angle: if set to ``True``, the peakbagging process will include inclination angle of the star in the parameters to fit.
    Optional, default ``False``.
  :type fit_angle: bool

  :param guess_angle: initial guess value for angle. Will be taken into account only if ``fit_angle`` is ``True``. 
    Optional, default 90.
  :type guess_angle: float

  :param fit_splittings: if set to ``True``, the peakbagging process will include mode splittings in the parameters to fit.
    Optional, default ``False``.
  :type fit_splittings: bool

  :param guess_split: initial guess value for splittings. Will be taken into account only if ``fit_splittings`` is ``True``. 
    Optional, default 0.4.
  :type guess_split: float

  :param frozen_harvey_exponent: set to True to have the Harvey models exponent fixed to 4. Optional, default ``False``.
  :type frozen_harvey_exponent: bool

  :return: ``None``
  '''

  if back is None :
    fitted_back, param_back = perform_mle_background (freq, psd, n_harvey=n_harvey, r=r, m=m, teff=teff, guess=guess_back, 
                              dnu=dnu, numax=numax, frozen_param=None, power_law=False,
                              frozen_harvey_exponent=frozen_harvey_exponent, low_cut=low_cut, fit_log=True, quickfit=quickfit,
                              low_bounds=None, up_bounds=None, no_bounds=False, show=False, show_guess=False, filename=filename_back+'.pdf', spectro=spectro,
                              apodisation=apodisation, num=num)
    np.savetxt (filename_back+'_parameters.dat', param_back, fmt='%-s')

    if back_mcmc :
      fitted_back, param_back, sigma_back  = explore_distribution_background (freq, psd,
                                       n_harvey=n_harvey, r=r, m=m, teff=teff, guess=param_back, frozen_param=None, power_law=False,
                                       frozen_harvey_exponent=frozen_harvey_exponent, low_cut=low_cut, fit_log=True, quickfit=quickfit,
                                       low_bounds=None, up_bounds=None, spectro=spectro, show=False, show_guess=False, show_corner=True,
                                       nsteps=nsteps_mcmc_back, filename=filename_back+'.pdf', parallelise=progress, progress=progress, nwalkers=nwalkers, 
                                       filemcmc=filemcmc_back, coeff_discard=coeff_discard_back, thin=thin_back, 
                                       save_only_after_sampling=save_only_after_sampling,
                                       apodisation=apodisation, num=num)
      np.savetxt (filename_back+'_parameters.dat', np.c_[param_back, sigma_back], fmt='%-s')
    
    if use_numax_back :
      numax = param_back[n_harvey*3+3]
    Wenv = param_back[n_harvey*3+4] 

    np.savetxt (filename_back+'.dat', fitted_back, fmt='%-s')

  else :
    fitted_back = back


  if dnu is None :
    dnu = dnu_scale (r, m)

  if numax is None :
    numax = numax_scale (r, m, teff)

  if Hmax is None :
    Hmax = 0.5 * np.max (psd[(freq>0.99*numax)&(freq<1.01*numax)]) 

  if a2z_in is None :
    df_a2z, pattern = perform_mle_pattern (dnu, numax, Hmax, Wenv, teff, freq, psd, back=fitted_back, wdw=None, epsilon=epsilon,
                           n_order=n_order, split=0, angle=90, fit_l1=fit_l1, fit_l3=fit_l3, mass=m, show=False, filename=filename_pattern+'.pdf')

    if pattern_mcmc :
      df_a2z, pattern, sigma_pattern = explore_distribution_pattern (dnu, numax, Hmax, Wenv, teff, freq, psd, back=fitted_back, wdw=None,
                           n_order=n_order, split=0, angle=90, fit_l1=fit_l1, fit_l3=fit_l3, mass=m, guess=pattern, show=False,
                           show_corner=True, nsteps=nsteps_mcmc_pattern, filename=filename_pattern+'.pdf', parallelise=parallelise, progress=progress,
                           nwalkers=nwalkers, filemcmc=filemcmc_pattern, coeff_discard=coeff_discard_pattern, 
                           thin=thin_pattern, save_only_after_sampling=save_only_after_sampling)

    np.savetxt (filename_pattern+'.dat', np.c_[pattern, sigma_pattern], fmt='%-s')

    orders_for_peakbagging = list_order_to_fit (numax, dnu, n_order=n_order_peakbagging) 
    df_a2z = pattern_to_a2z (*pattern, split=guess_split, angle=guess_angle, orders=orders_for_peakbagging, angle_order=fit_angle, 
                             splitting_order=fit_splittings)
    save_a2z (a2z_file, df_a2z)

  if not nopeakbagging :
    if a2z_in is None :
      a2z_to_read = a2z_file
    else :
      a2z_to_read = a2z_in
     
    df_a2z = peakbagging (a2z_to_read, freq, psd, back=fitted_back, wdw=None, spectro=spectro,
                   nsteps_mcmc=nsteps_mcmc_peakbagging, show_corner=True,
                   store_chains=True, mcmcDir=mcmcDir, order_to_fit=None, parallelise=parallelise, progress=progress,
                   strategy='order', nwalkers=nwalkers, normalise=False, instr=instr, filename_summary=filename_peakbagging, show_summary=False,
                   coeff_discard=coeff_discard_pkb, save_only_after_sampling=save_only_after_sampling, restrict=True)

    save_a2z (a2z_file, df_a2z)

  pkb = a2z_to_pkb (df_a2z)
  
  np.savetxt (a2z_file[:len(a2z_file)-3]+'pkb', pkb, fmt='%-s') 

  return 
