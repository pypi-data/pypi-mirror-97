import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from apollinaire.psd import series_to_psd, levels
from apollinaire.processing import design_digital_filter, convolve_filter, mirror
from scipy.signal import filtfilt
from tqdm import tqdm
import joblib
import sys
from .songlib import *
from .interval_nan import flux_nan
from .lowess_wrapper import lowess_wrapper

def daily_correction_1d (s, v, f,  
                   dt=20., plot=False, rebox=True,
                   sigma_box=[3.,2.5], thresh=None,
                   origin=2458272.5, size_neighborhood=None,
                   sigma_neighborhood=[8,6], perf_lowess=False) :

    '''
    Function to  make correction over 1d velocity
    array. 
  
    :param s: Julian day timestamps of the series.
    :type s: ndarray
  
    :param v: 1d velocity vector.
    :type v: ndarray
  
    :param f: 1d flux vector.
    :type f: ndarray
  
    :param dt: time sampling wanted in the box. Optional, default 20.
    Caution: 86400 / dt must be an integer. 
    :type dt: float

    :param plot: set to True to plot the series with line of sight corrected in order
    to show which outliers are removed by the neighborhood cleaning step. Optional, default
    False. 
    :type plot: bool.

    :param rebox: if set to True, return timestamps, velocity vector and interpolation
    mask with dt sampling. If False, return only a velocity vector with the original
    sampling. Optional, default True. 
    :type rebox: bool 

    :param sigma_box: the two successive sigma values to use to exclude outliers in each box.
    Optional, default [3, 2.5].
    :type sigma_box: array_like of size 2.

    :param tresh: minimum number of non-zero values in a box. If the number of non-zero values
    in the box is below thresh, the whole box value will be linearly interpolated with its neighbors
    and the box will be flagged in the interpolation mask. Optional, default None.  
    :type thresh: int
  
    :param origin: date of reference from where the date 
    in the plot are computed. Default is 2458272.5, hence
    3rd of June 2018. 
    :type origin: float
  
    :param size_neighborhood: number of box to use before and after
    considered box to flag local outliers. Default None.
    :type size_neighborhood: int

    :param sigma_neighborhood: sigma values used to remove outliers in the neighborhood defined by 
    size_neighborhood. Optional, default [8, 6].
    :type sigma_neighborhood: array_like of size 2.

    :param perf_lowess: set to True to remove low frequency trends in the timeseries before flagging
    the outliers that will be removed by the neighborhood cleaning. Stay aware that the LOWESS process
    is not used to remove low-frequency trends in the timeseries. Optional, default False.  
    :type perf_lowess: bool. 

    :return: if rebox==False, return velocity vector only. If rebox==True, return timestamps of the 
    reboxed series, reboxed velocity vector and interpolation mask flagging the box where real values
    were rejected and replaced by linear interpolation values. 
    :rtype: ndarray or tuple of ndarray
    '''
  
    # creating the timestamps of the boxes
    rs = rebox_stamps (s, dt=dt)
  
    # replacing 0 by nan for convenience
    mask_zero = (v == 0)
    v[mask_zero] = np.nan
  
    # setting to 0 point with nearly 0 measured velocity
    v[v<25.] = np.nan
  
    #INSIDE BOX CORRECTIONS
    for stamp in rs :
      if stamp < s[0] - 0.5*dt/86400. :
        continue
      if stamp > s[-1] + 0.5*dt/86400. :
        continue
      box = v[np.abs (s - stamp) < 0.5*dt / 86400.] 
      box[np.abs (box-np.nanmean (box)) > sigma_box[0] * np.nanstd (box)] = np.nan
      box[np.abs (box-np.nanmean (box)) > sigma_box[1] * np.nanstd (box)] = np.nan
      v[np.abs (s - stamp) < 0.5*dt / 86400.] = box
  
  
    # 1 - centering the noon value at 0
    v = v - np.nanmedian (v[np.abs (s - np.rint(s)) < 5 * dt/86400.])
    # 2 - computing vephem and centering its noon value at 0
    vephem = compute_vephem (s)
    vephem = vephem - np.nanmedian (vephem[np.abs (s - np.rint(s)) < 5 * dt/86400.])
  
    if plot==True :
      fig = plt.figure (figsize=(12,6))
      ax1 = fig.add_subplot (111)
      ax2 = ax1.twinx ()
      ax1.scatter (s-origin, v-vephem, color='black', s=6, marker='.')
      #ax1.scatter (s-origin, vephem, color='blue', s=6, marker='.')
      #ax1.scatter (s-origin, v, color='orange', s=6, marker='.')
      ax2.plot (s-origin, f, color='slategrey')
      ax1.set_xlabel ('Time (day)')
      ax1.set_ylabel ('Velocity (m/s)')
      ax2.set_ylabel ('Photon flux level')
      #plt.show ()
  
  
    #3 - NEIGHBORHOOD OUTLIERS CORRECTION
    if size_neighborhood is not None :
      ns = rebox_stamps (s, dt=dt*size_neighborhood)
  
      # LOWESS
      if perf_lowess==True :
        aux_v = v-vephem
        aux_v = flux_nan (s, aux_v)
        aux_v = lowess_wrapper (s, aux_v, frac=2./3., it=10, subset_size=100)
        if plot==True :
          ax1.scatter (s-origin, aux_v, color='darkred', s=6, marker='.')
        for stamp in ns :
          if stamp < s[0] - 0.5*dt*size_neighborhood/86400. :
            continue
          if stamp > s[-1] + 0.5*dt*size_neighborhood/86400. :
            continue
          neighborhood = v[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.] 
          aux_n = aux_v[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.]
          neighborhood[np.abs (aux_n-np.nanmean (aux_n)) > sigma_neighborhood[0] * np.nanstd (aux_n)] = np.nan
          aux_n[np.abs (aux_n-np.nanmean (aux_n)) > sigma_neighborhood[0] * np.nanstd (aux_n)] = np.nan
          neighborhood[np.abs (aux_n-np.nanmean (aux_n)) > sigma_neighborhood[1] * np.nanstd (aux_n)] = np.nan
          v[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.] = neighborhood 
          if plot==True :
            aux_n[np.abs (aux_n-np.nanmean (aux_n)) > sigma_neighborhood[1] * np.nanstd (aux_n)] = np.nan
            aux_s = s[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.]
            ax1.scatter (aux_s-origin, aux_n, color='goldenrod', s=6, marker='.')
          
  
      # WITHOUT LOWESS
      else :
        for stamp in ns :
          if stamp < s[0] - 0.5*dt*size_neighborhood/86400. :
            continue
          if stamp > s[-1] + 0.5*dt*size_neighborhood/86400. :
            continue
          neighborhood = v[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.] 
          vephem_n = vephem[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.]
          aux_metric = neighborhood - vephem_n
          neighborhood[np.abs (aux_metric-np.nanmean (aux_metric)) > sigma_neighborhood[0] * np.nanstd (aux_metric)] = np.nan
          neighborhood[np.abs (aux_metric-np.nanmean (aux_metric)) > sigma_neighborhood[1] * np.nanstd (aux_metric)] = np.nan
          v[np.abs (s - stamp) < 0.5 * size_neighborhood * dt / 86400.] = neighborhood 
  
    if plot==True :
      ax1.scatter (s-origin, v-vephem, color='deepskyblue', s=6, marker='.')
      plt.show ()
  
    # REBOXING 
    if rebox==True :
       old_s = np.copy (s)
       s, v, mask_interpo = rebox_array (s, v, dt=dt, thresh=thresh, velocity=True, vephem=vephem, return_mask=True)
       s, vephem = rebox_array (old_s, vephem, dt=dt)
       v[v==0] = np.nan
  
    # correcting line of sight
    v = correct_line_of_sight (s, v, vephem=vephem)
  
    if rebox==True :
      return s, v, mask_interpo
    else :
      return v

def global_correction (s, v, f, filt=None, sigma_global=[3.5,3.],
                       n_filtering=1, cut_flux=0) :
    '''
    Function to  make global correction over a velocity array
    with regular sampling prealably corrected by the daily_correction_1d
    function. 
  
    :param s: Julian day timestamps of the series.
    :type s: ndarray
  
    :param v: 1d velocity vector.
    :type v: ndarray
  
    :param f: 1d flux vector.
    :type f: ndarray

    :param filt: numerator coefficients of the filter to use. It is recommended
    to use a FIR filter, designed for example with the scipy.signal.firls method.
    :type filt: array-like. 

    :param sigma_global: sigma values used to remove outliers in the whole 
    series. Optional, default [3.5, 3.]. 
    :type sigma_global: array_like of size 2.

    :param n_filtering: number of time the filter will be applied. Optional, default 1.
    :type n_filtering: int

    :param cut_flux: velocity points with corresponding flux values will be set to 0. 
    Optional, default 0.
    :type cut_flux: float. 

    :return: corrected velocity vector.
    :rtype: ndarray.
    '''

    # Low frequency filter
    mask_zero = (np.isnan (v)) | (v==0)
    v[mask_zero] = 0

    if filt is not None :

        # -------------------------------------------------
        # Interpolation strategy
        if v[~mask_zero].size > 0 :
            mask_aux = np.copy (mask_zero)
            if v[0] == 0 : #avoid error in interpolation
                v[0] = v[~mask_zero][0]
                mask_aux = (v==0)
            if v[-1] == 0 : #avoid error in interpolation
                v[-1] = v[~mask_zero][-1]
                mask_aux = (v==0)
            f_interpo = interp1d (s[~mask_aux], v[~mask_aux])
            v[mask_aux] = f_interpo (s[mask_aux])
        # -------------------------------------------------

        for i in range (n_filtering) :
            v = filtfilt (filt, [1.0], v)

    # Applying the global mask to remove filter 
    # effects.
    v[mask_zero] = 0

    #by-hand correction
    v = flux_nan (s, v)

    # Setting  0 at 'early morning'
    v[f < cut_flux] = 0 #those points are normally only at the beginning of the day when the sun is rising
    mask_zero = (np.isnan (v)) | (v==0)

    # GLOBAL CUT #1 
    v[mask_zero] = np.nan
    v[np.abs (v) > sigma_global[0]*np.nanstd(v)] = np.nan
    mask_zero = (np.isnan (v)) | (v==0)

    # GLOBAL CUT #2 
    v[np.abs (v) > sigma_global[1]*np.nanstd(v)] = np.nan

    mask_zero = (np.isnan (v)) | (v==0)
    v[mask_zero] = 0

    n_value = np.count_nonzero (v)
    print (n_value / v.size)

    return v

def plot_result_reduction (s, v, f=None, s_comp=None, v_comp=None, dt=20., dt_comp=20, 
                           origin=0, origin_comp=0, harmonics=False, test=False, test_length=2,
                           alpha_comp=0.8, color_comp='firebrick') :
    '''
    Plot the timeseries and its power spectral density.

    :param s: Julian day timestamps of the series.
    :type s: ndarray
  
    :param v: 1d velocity vector.
    :type v: ndarray
  
    :param f: 1d flux vector. Optional, default None.
    :type f: ndarray

    :param s_comp: Julian day timestamps of the series to compare with.
    Optional, default None.
    :type s_comp: ndarray
  
    :param v_comp: 1d velocity vector of the series to compare with.
    Optional, default None. 
    :type v_comp: ndarray

    :param dt: sampling of the timeseries. Optional, default 20.
    :type dt: float

    :param dt_comp: sampling of the timeseries to compare with. Optional, default 20.
    :type dt_comp: float

    :param origin: origin to consider for the s time stamps. On the plot, the first
    point of the timeseries s, v will be represented at the abscisse 
    s[0] - origin. Optional, default 0.
    :type origin: float 

    :origin_comp: origin to consider for the s_comp time stamps. On the plot, the first
    point of the timeseries s_comp, v_comp will be represented at the abscisse 
    s_comp[0] - origin_comp. Optional, default 0.
    :type origin_comp: float 

    :param harmonics: if set to True, harmonics due to residual Earth rotation signal
    will be spotted by vertical lines.
    :type harmonics: bool

    :param test: if set to True, only the first test_length days of the series will
    be plotted. 
    :type test: bool 

    :param test_length: number of day that will be plotted if test is True.
    :type test_length: int

    :param alpha_comp: alpha of the plot linked to s_comp, v_comp timeseries. Between 0 and 1.
    :type alpha_comp: float

    :param color_comp: color of the plot linked to s_comp, v_comp timeseries. 
    :type color_comp: string
    '''

    day_length = int (86400 / dt)

    if test==True :
      s=s[:test_length*day_length]
      v=v[:test_length*day_length]

    #removing possible nan to avoid a bug when computing psd
    mask = np.isnan (v)
    v[mask] = 0
    freq, psd = series_to_psd (v, dt=dt)
    
    #noise_metric = levels (freq, psd, verbose=True) 
    #correcting psd with duty cycle
    dc = np.count_nonzero (v) / v.size
    psd = psd / dc
    noise_metric = levels (freq, psd, verbose=True) 
    
    fig = plt.figure (figsize=(12,6))
    ax1 = fig.add_subplot (211)
    ax2 = fig.add_subplot (223)
    ax3 = fig.add_subplot (224)

    if f is not None :
      axflux = ax1.twinx ()
      axflux.plot (s-origin, f, color='darkorange')
      axflux.set_ylabel ('Photon flux level')

    if harmonics==True :
      fond = 1 / 86400.
      a_harmonics = np.array ([fond*i for i in range (500)])
      ax2.vlines (x=a_harmonics*1e6, ymin=0, ymax=0.01, color='red', linestyle='--')
      ax3.vlines (x=a_harmonics*1e6, ymin=0, ymax=0.01, color='red', linestyle='--')
    
    ax1.plot (s-origin, v, color='black')
    ax2.plot (freq*1e6, psd*1e-6, color='black')
    ax3.plot (freq*1e6, psd*1e-6, color='black')
    
    if (s_comp is not None) and (v_comp is not None) :
      if test==True :
        s_comp=s_comp[:test_length*int(86400./dt_comp)]
        v_comp=v_comp[:test_length*int(86400./dt_comp)]
      freq_comp, psd_comp = series_to_psd (v_comp, dt=dt_comp)
      dc_comp = np.count_nonzero (v_comp) / v_comp.size
      psd_comp = psd_comp / dc_comp
      ax1.plot (s_comp-origin_comp, v_comp, color=color_comp)
      ax2.plot (freq_comp*1e6, psd_comp*1e-6, color=color_comp, alpha=alpha_comp)
      ax3.plot (freq_comp*1e6, psd_comp*1e-6, color=color_comp, alpha=alpha_comp)
      noise_metric = levels (freq_comp, psd_comp, verbose=True)
      
       
    ax2.set_xscale ('log')
    ax2.set_yscale ('log')
    
    ax1.set_xlabel ('Time (days)')
    ax2.set_xlabel (r'Freq ($\mu$Hz)')
    ax3.set_xlabel (r'Freq ($\mu$Hz)')
    
    ax1.set_ylabel ('Velocity (m/s)')
    ax2.set_ylabel (r'PSD ((m/s)$^2$/$\mu$Hz)')
    ax3.set_ylabel (r'PSD ((m/s)$^2$/$\mu$Hz)')
    
    ax3.set_xlim (2000, 4500)

    return


