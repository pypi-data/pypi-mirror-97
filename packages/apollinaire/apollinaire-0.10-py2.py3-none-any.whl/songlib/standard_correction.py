import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy.io
import os
import glob
from tqdm import tqdm
import h5py
import sys
import apollinaire as apn
from .songlib import *
from .interval_nan import flux_nan, manual_nan

def standard_correction (dir_velocity, dir_corrected, dir_flux_out=None,
                         dir_long=None,  dir_flux=None, iSONG=False, dt=20., pop_end=0, pop_beginning=0, save=False,
                         correct=True, test=False, test_length=2, weighted=True, perf_lowess=False,
                         remove_interval_manually=True, plot_flux=False, 
                         cut_rising=12000, sigma_box=[3.,2.5], size_neighborhood=50, sigma_neighborhood=[3.5,3.],
                         sigma_global=[4.,3.], scatter_min=3., scatter_max=1000., thresh=2, n_filtering=1, 
                         plot_final=False, plot_intermediate=False, plot_response=False, 
                         harmonics=False, s_comp=None, v_comp=None, origin=0, origin_comp=0) :

  
  '''
  Read raw daily velocity files into their repertory, save corrected daily file and return the concatenated corrected series.

  :param dir_velocity: name of the repertory where to read velocity files (saved in text format if iSONG is True, in
  hdf5 otherwise)
  :type dir_velocity: string

  :param dir_corrected: name of the repertory where to write corrected velocity files
  :type dir_corrected: string

  :param dir_long: name of the repertory where to write the concatenated series files if save set to True.
  Optional, default None. 
  :type dir_long: string.

  :param dir_flux: name of the repertory where to read flux files. Needs to be specified if iSONG is False. 
  Optional, default None. 
  :type dir_flux: string

  :param dir_flux_out: name of the repertory where to write output flux files of plot_flux is set to True. Optional,
  default None. 
  :type dir_flux_out: string

  :param iSONG: set to True if the data to use are outputs (with chunks already integrated) from the iSONG pipeline.
  Optional, default False.
  :type iSONG: bool

  :param dt: time sampling of the wanted corrected timeseries. Optional, default 20. Caution: 86400/dt must be an integer.
  :type dt: float

  :param pop_beginning: number of daily file to remove at the beginning of the list from the files read in dir_velocity.
  :type pop_beginning: int

  :param pop_end: number of daily file to remove at the end of the list from the files read in dir_velocity.
  :type pop_end: int

  :param save: if set to True, the final corrected concatenated series will be saved in dir_long.
  Optional, default False.
  :type save: bool

  :param correct: if set to True, the full correction pipeline will be executed. If set to False, the function will only
  read preexisting daily files in dir_corrected and create the concatenated timeseries. Optional, default True.
  :type correct: bool.

  :param test: if set to True, will only perform corrections on the first files to correct. The number of files to correct
  is given by test_length. Optional, default False.
  :type test: bool

  :param test_length: number of daily files to correct when test is set to True. Optional, default 2.
  :type test_length: int

  :param weighted: if set to True, the weighting process will be applied when integrating chunks. Not weighting the chunks
  will give an output result with a much more important level of noise. Optional, default True.
  :type weighted: bool

  :param perf_lowess: set to True to remove low frequency trends in the timeseries before flagging
  the outliers that will be removed by the neighborhood cleaning. Stay aware that the LOWESS process
  is not used to remove low-frequency trends in the timeseries. Optional, default False.  
  :type perf_lowess: bool. 

  :param remove_interval_manually: if set to True, some pre-determined noisy interval will be set to 0 at the end of the
  correction process. Optional, default True.
  :type remove_interval_manually: bool

  :param plot_flux: if set to True flux arrays (only read if iSONG is True, integrated from chunks otherwise) will be saved
  in dir_flux_out in order to plot the concatenated final array with the concatenated timeseries. 

  :param plot_final: set to True to plot the full corrected timeseries at the end of the correction process
  Optional, default False. 
  :type plot_final: bool

  :param plot_intermediate: For each daily series, plot velocity before reboxing steps and shows the outliers points that
  will be removed by the nighborhood cleaning. Optional, default False. 
  :type plot_intermediate: bool

  :param plot_response: if set to True, plot the response function of the high pass filter used. Optional, default False.
  :type plot_response: bool

  :param size_neighborhood: number of box to use before and after
  considered box to flag local outliers. Default None.
  :type size_neighborhood: int

  :param sigma_neighborhood: sigma values used to remove outliers in the neighborhood defined by 
  size_neighborhood. Optional, default [8, 6].
  :type sigma_neighborhood: array_like of size 2.

  :param cut_rising: velocity values with corresponding flux values inferior to cut_rising will
  be removed. Optional, default 12000. Those values corresponds most of the time to measurements
  taken at the beginning of the day while the sun is rising.
  :type float:

  :param sigma_box: the two successive sigma values to use to exclude outliers in each box.
  Optional, default [3, 2.5].
  :type sigma_box: array_like of size 2.

  :param tresh: minimum number of non-zero values in a box. If the number of non-zero values
  in the box is below thresh, the whole box value will be linearly interpolated with its neighbors
  and the box will be flagged in the interpolation mask. Optional, default None.  
  :type thresh: int

  :param sigma_global: sigma values used to remove outliers in the whole 
  series. Optional, default [3.5, 3.]. 
  :type sigma_global: array_like of size 2.

  :param scatter_min: Chunks with scatter below this limit will not be used for the integration
  of global velocity value.
  :type scatter_min: float

  :param scatter_max: Chunks with scatter below this limit will not be used for the integration
  of global velocity value.
  :type scatter_max: float

  :param n_filtering: number of time the filter will be applied. Optional, default 1.
  :type n_filtering: int

  :param harmonics: if set to True, harmonics due to residual Earth rotation signal
  will be spotted by vertical lines.
  :type harmonics: bool

  :param s_comp: Julian day timestamps of the series to compare with.
  Optional, default None.
  :type s_comp: ndarray
  
  :param v_comp: 1d velocity vector of the series to compare with.
  Optional, default None. 
  :type v_comp: ndarray

  :param origin: origin to consider for the s time stamps. On the plot, the first
  point of the timeseries s, v will be represented at the abscisse 
  s[0] - origin. Optional, default 0.
  :type origin: float 

  :origin_comp: origin to consider for the s_comp time stamps. On the plot, the first
  point of the timeseries s_comp, v_comp will be represented at the abscisse 
  s_comp[0] - origin_comp. Optional, default 0.
  :type origin_comp: float 

  :return: timestamps and velocity vector of the final corrected and concatenated timeseries.
  :rtype: tuple of ndarray
  '''

  dir_src = os.path.abspath ('.') + '/'
  
  day = int (86400 / dt)
  cut_up = 1. / (scatter_min*scatter_min) 
  cut_low = 1. / (scatter_max*scatter_max)
  
  # ------------------------------------------------------------------------------------------------
  
  if correct == True :

    #Designing high pass filter 
    desired = [0,0,0,1,1,1]
    dt==20. 
    bands = [0, 400e-6, 400e-6, 900e-6, 900e-6, 1/(2*dt)]
    numtaps = 1101
    filt = design_digital_filter (numtaps=numtaps, bands=bands, desired=desired,
                                  plot_response=plot_response, fs=1/dt)
  
    os.chdir (dir_velocity)
    if iSONG==True :
      list_velocity = glob.glob ('*.cln')
    else :
      list_velocity = glob.glob ('*.h5')
      list_flux = glob.glob ('*.h5')
    for ii in range (pop_end) : 
      list_velocity.pop ()
    for ii in range (pop_beginning) : 
      list_velocity.pop (0)

    if iSONG==False : 
      os.chdir (dir_flux)
      for ii in range (pop_end) :
        list_flux.pop ()
      for ii in range (pop_beginning) : 
        list_flux.pop (0)
  
    os.chdir (dir_src)
  
    if test==True :
      list_velocity = list_velocity[0:test_length]
      if iSONG==False :
        list_flux = list_flux[0:test_length]
  
   # ------------------------------------------------------------------------------------------------
   # ------------------------------------------------------------------------------------------------
    # CORRECTION OVER iSONG VELOCITY FILES
    if iSONG==True :
      for file_v in list_velocity :
        print (file_v)
        file_id = file_v[:13]
        fileout = dir_corrected + file_id + '_corrected.h5'
        # usecols=(1,4,7) for BVC velocities - (1,3,7) otherwise
        # The ephemeris files seems to already have barycentric correction
        # ie better use second solution. 
        daily_data = np.loadtxt (dir_velocity+file_v, usecols=(1,3,7))
        s = daily_data[:,0]
        v = daily_data[:,1]
        f = daily_data[:,2]
  
        rs = rebox_stamps (s, dt=dt)
        aux_s, rf = rebox_array (s, f, dt=dt, velocity=False)
        rs, v, mask_interpo = daily_correction_1d (s, v, f, rs, plot=plot_intermediate, dt=dt, rebox=True, 
                                     sigma_box=sigma_box, thresh=thresh, perf_lowess=perf_lowess,  
                                     size_neighborhood=size_neighborhood, sigma_neighborhood=sigma_neighborhood)
        v = global_correction (rs, v, rf, filt=filt, sigma_global=sigma_global, n_filtering=n_filtering, cut_flux=cut_rising)
        v[mask_interpo] = 0. 
        save_hdf5 (fileout, rs, v, key='velocity', mode='x')
  
   # ------------------------------------------------------------------------------------------------
   # ------------------------------------------------------------------------------------------------
    # CORRECTION OVER RAW VELOCITY FILES
    else :
      for file_v, file_f in zip (list_velocity, list_flux) :
        print (file_v, file_f)
        file_id = file_v[:9]
        fileout = dir_corrected + file_id + '_corrected.h5'
        if plot_flux == True :
          fileout_flux = dir_flux_out + file_id + '_corrected.h5'
        file_v = dir_velocity + file_v
        file_f = dir_flux + file_f
        s, mf = read_hdf5 (file_f, key='fluxlevel')
        s, mv = read_hdf5 (file_v, key='velocity')
  
        mv = mv*1e3
  
        if weighted == True :
          weights = compute_weights (mv, cut_up=cut_up, cut_low=cut_low)
        else :
          weights = None
  
        # ------------------------
        #TEST : FLUX THRESHOLD
        weights[np.nanmean(mf, axis=0) < cut_flux] = 0
        # ------------------------
        
        mean_flux = np.nanmean (mf, axis=0)
        v = integrate_chunk (mv, weights=weights) 
        f = integrate_chunk (mf, weights=weights)
  
        #rs = rebox_stamps (s, dt=dt)
        aux_s, rf = rebox_array (s, f, dt=dt, velocity=False)
        rs, v, mask_interpo = daily_correction_1d (s, v, f, plot=plot_intermediate, dt=dt, rebox=True, 
                                     sigma_box=sigma_box, thresh=thresh, perf_lowess=perf_lowess,  
                                     size_neighborhood=size_neighborhood, sigma_neighborhood=sigma_neighborhood)
        v = global_correction (rs, v, rf, filt=filt, sigma_global=sigma_global, n_filtering=n_filtering, cut_flux=cut_rising)
        v[mask_interpo] = 0. 
        save_hdf5 (fileout, rs, v, key='velocity', mode='x')
        if plot_flux==True :
          save_hdf5 (fileout_flux, rs, rf, key='fluxlevel', mode='x')
  
   # ------------------------------------------------------------------------------------------------
   # ------------------------------------------------------------------------------------------------
    
  
  # CONCATENING DAILY CORRECTED SERIES 
  # FINAL CORRECTIONS AND PLOT
  # ------------------------------------------------------------------------------------------------
  os.chdir (dir_corrected) 
  list_corrected = glob.glob ('*.h5')
  s, v = concatene_days (list_corrected, chunk=False, dt=dt)
  
  if plot_flux==True :
    os.chdir (dir_flux_out) 
    list_flux_corrected = glob.glob ('*.h5')
    xxx, f = concatene_days (list_flux_corrected, chunk=False, dt=dt, key='fluxlevel')
  
  os.chdir (dir_src)
  
  # flux correction (already done in previous steps)
  v = flux_nan (s, v)
  v[np.isnan(v)]=0.
  
  if remove_interval_manually==True :
    v = manual_nan (s, v)
    v[np.isnan(v)]=0.
  
  if plot_final==True :
    if plot_flux == False :
      plot_result_reduction (s, v, s_comp=s_comp, v_comp=v_comp, dt=dt, dt_comp=32, harmonics=harmonics,
                             test=test, test_length=test_length, origin_comp=0, origin=s[0])
    else :
      plot_result_reduction (s, v, f=f, s_comp=s_comp, v_comp=v_comp, dt=dt, dt_comp=32, harmonics=harmonics,
                             test=test, test_length=test_length, origin_comp=0, origin=s[0])
    plt.show ()
  
  if save==True :
    save_hdf5 (dir_long + 'solar_song_long_corrected.h5', s, v, key='velocity', mode='x') 
    np.savetxt (dir_long + 'solar_song_long_corrected.dat', np.c_[s,v], fmt='%-s')
    print ('Concatenated series saved in', dir_long + 'solar_song_long_corrected.h5') 

  return s, v
      
  
