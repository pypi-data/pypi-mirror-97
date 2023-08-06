import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.io
import os
import glob
from tqdm import tqdm
import h5py
import importlib.resources
from apollinaire.psd import series_to_psd
from astropy.stats import mad_std

"""
A library of function dedicated to simplify Solar-SONG data analysis
"""

def get_siod (directory) :
  """
  return list of .siod file in a repertory
  """
  os.chdir (directory)
  list_siod = glob.glob ('*.siod')
  a_siod = np.array (list_siod)
  a_siod = np.sort (a_siod)
  return a_siod

def read_siod (filename, verbose=False) :
  """
  read a .siod file and return the datam structure
  (see Solar-SONG doc for further explanation)
  """
  dum = scipy.io.readsav (filename, verbose=verbose)
  datam = dum['datam']
  return datam

def build_velocity_array (a_siod, sort=True) :
  """
  """
  if sort == True :
    a_siod = np.sort (a_siod)
  ndata = a_siod.size
  velocity = np.empty ((24,22,ndata))
  stamps = np.empty ((24,22,ndata))
  for ii in tqdm (range (ndata)) :
    datam = read_siod (a_siod[ii])
    stamps[:,:,ii] = datam['jd_mid']
    velocity[:,:,ii] = datam['velocity']
  stamps = stamps[0,0,:]
  return stamps, velocity 

def extract_chunk (order, chunk, velocity) :
  return velocity[:,order,chunk]

def read_hdf5 (filename, key='velocity') :
  '''
  Read data previously saved under hdf5 format: 
  extract data and stamps array from a v[date]_out.h5 
  file created by extract.pro.

  :param filename: name of the file to write.
  :type filename: str

  :param key: key to use for the data array in the hdf5 file.
  :type key: str

  :return: stamps and data arrays. 
  :rtype: tuple of ndarray.
  '''

  f = h5py.File (filename, 'r')
  stamps = np.ravel (f['stamps'][()])
  data = f[key][()]
  f.close ()
  return stamps, data

def save_hdf5 (filename, stamps, data, key='velocity', mode='x') :
  '''
  Save data under hdf5 format. 

  :param filename: name of the file to write.
  :type filename: str

  :param stamps: timestamps vector.
  :type stamps: ndarray

  :param data: data vector.
  :type data: ndarray

  :param key: key to use for the data array in the hdf5 file.
  :type key: str

  :param mode: hdf5 file management mode. See h5py doc. 
  :type mode: str
  '''
  f = h5py.File(filename, mode)
  dset_stamps = f.create_dataset ('stamps', stamps.shape, data=stamps)
  dset_data = f.create_dataset (key, data.shape, data=data)
  f.close ()
  return

def jd_to_seconds (stamps) :
  """
  Convert stamps array in julian day
  value into a stamps array in seconds
  with t0 = 0
  """
  stamps_s = stamps - stamps [0]
  stamps_s = stamps_s * 86400.
  return stamps_s

def rebox_stamps (stamps, dt=20.) :
  '''
  Rebox time stamps from daily observation into regular sampled boxes. 

  :param stamps: timestamps vector. Date are expected in Julian day. Must
  correspond to stamp of ONE day of observation. 
  :type stamps: ndarray

  :return: reboxed stamps vector.
  :rtype: ndarray

  CAUTION: dt must divide 86400, otherwise the function will behave wildly.
  '''

  #I want each of daily reboxed series to begin at
  #00.00 Greenwich
  t0 = int (stamps[0]) + 0.5

  #converts dt in days
  dt = dt / 86400.

  #number of boxes for the new sample
  n = int (1. / dt)
  r_stamps = np.linspace (t0, t0+1, n, endpoint=False)

  return r_stamps

def rebox_array (stamps, data, dt=20., thresh=None, velocity=True, vephem=None, return_mask=False) :
  '''
  Rebox values from an 1D input array and its time stamps into regular
  sampled boxes. 

  PLEASE STAY AWARE THAT ALL THE OBSERVATIONS TIME
  GIVEN ARE MID-TIME

  :param stamps: timestamps vector. Date are expected in Julian day. Must
  correspond to stamp of ONE day of observation. 
  :type stamps: ndarray

  :param data: input data array
  :type data: ndarray

  :param thresh: min number of value. 
  Default None. If the number of value is below the threshold
  the velocity value is replaced by the ephemeris values.
  :type thresh: int

  :param velocity: set to True if a velocity array is considered and if a threshold
  is given. Rejected values will then be replaced by ephemeris values. Default True. 
  :type velocity: boolean

  :param vephem: vephem to use for interpolation. Must have the same sampling as the 
  input data. 
  :type vephem: ndarray

  :return: reboxed stamps vector and data aray.
  :rtype: ndarray

  CAUTION: dt must divide 86400, otherwise the function will behave wildly.
  '''

  #I want each of daily reboxed series to begin at
  #00.00 Greenwich
  t0 = int (stamps[0]) + 0.5

  #converts dt in days
  dt = dt / 86400.

  #number of boxes for the new sample
  n = int (1. / dt)
  r_stamps = np.linspace (t0, t0+1, n, endpoint=False)
 
  if return_mask==True :
    mask = np.zeros (r_stamps.size, dtype=bool)

  dim = data.shape 
  if len (dim) == 3 :
    r_data = np.zeros ((r_stamps.size, dim[0], dim[1]))
  else :
    r_data = np.zeros (r_stamps.size)

  for count, boxstamp in enumerate (r_stamps) :
    r_data[count] = np.nanmean (data[np.abs (stamps-boxstamp) < dt/2.], axis=0)
    if thresh is not None :
      flags = ~np.isnan (data[np.abs (stamps-boxstamp) < dt/2.])
      if np.count_nonzero (flags) < thresh : 
        if velocity == True :
          if np.count_nonzero (flags)==0 :
            r_data[count] = np.nanmean (vephem[np.abs (stamps-boxstamp) < dt/2.])
          if return_mask==True :
            mask[count]==True
        else :
          r_data[count] = 0.
          if return_mask==True :
            mask[count]==True

  if return_mask==True :
    return r_stamps, r_data, mask
  else :
    return r_stamps, r_data

def rebox_directory (dir_in, dir_out, key='velocity', dt=20., thresh=None, vephem=None) :
  '''
  Take all hdf5 in directory dir_in, rebox measurements into regular
  dt time sampling and write output (as hdf5 files) in directory
  dir_out

  :param dir_in: directory where to read hdf5 files
  :type: string  

  :param dir_out: directory where to write output hdf5 files
  :type: string  

  :param key: name of the dataset in hdf5 file. Default 'velocity'.
  :type key: str

  :param dt: time sampling for the reboxing
  :type dt: float

  :param chunk: Set to True if the routine will have to deal with chunk array
  and not 1D array.
  :type chunk: bool

  CAUTION: dt must divide 86400, otherwise the function will behave wildly.
  '''

  os.chdir (dir_in)
  list_f = glob.glob ('*.h5')
  for filename in list_f :
    #stamps are in Julian day
    #velocities (if considered) are in km/s
    stamps, data = read_hdf5 (filename, key=key)

    if key == 'velocity' :
      r_s, r_v = rebox_array (stamps, data, dt=dt, velocity=True, thresh=thresh, vephem=vephem)
    else :
      r_s, r_v = rebox_array (stamps, data, dt=dt, velocity=False)
       
    fileout = filename[:len(filename)-7] + '_reboxed_dt' + str (int (dt)) + '.h5'
    save_hdf5 (dir_out+fileout, r_s, r_v, key=key)

  return

def concatene_days (list_subseries, dir_out=None, key='velocity', dt=20., chunk=True) :
  """
  Take a list of subseries of consecutive
  days of observation and concatenes them

  CAUTION : the considered subseries need to
  have been reboxed in the first place
 
  dt is taken in seconds

  :param chunk: Set to True if the routine will have to deal with chunk array
  and not 1D array.
  :type chunk: bool
  """

  ###
  day = int (86400. / dt) 
  n = day * len (list_subseries)
  
  full_stamps = np.zeros (n)
  if chunk==True :
    full_data = np.zeros ((n,24,22)) 
  else :
    full_data = np.zeros (n)

  for ii, elt in enumerate (list_subseries) :
    stamps, data = read_hdf5 (elt, key=key)
    full_stamps[day*ii:day*(ii+1)] = stamps
    if chunk==True :
      full_data[day*ii:day*(ii+1),:,:] = data
    else :
      full_data[day*ii:day*(ii+1)] = data

  if dir_out != None :
      ###
      # Creating filename
      begin = list_subseries[0]
      begin = begin[1:9]
      end   = list_subseries[-1]
      end   = end[1:9]

      filename = key + '_' + begin + '_' + end + '_reboxed_dt' + str(int(dt)) + '.h5' 
      save_hdf5 (dir_out+filename, full_stamps, full_data, key=key)

  return full_stamps, full_data

def compute_vephem (stamps, interp_kind='linear') :

  '''
  Compute Teide ephemeris velocity for a given timestamps.
  
  :param stamps: timestamps on which to compute the velocity
  :type stamps: ndarray

  :param interp_kind: type of interpolation that will be used
  :type interp_kind: string

  :return: ephemeris velocity
  :rtype: ndarray
  '''

  cm = importlib.resources.path ('apollinaire.songlib.ephemeris', 'sun_teide_20180527_20180725_apparent.csv')

  with cm as pathFile :
      df = pd.read_csv (pathFile, sep=';')

  t_ls = df['Date (undefined)']
  rv_ls = df['RV (km/s)']

  f_ls = interp1d (t_ls, rv_ls, kind=interp_kind)

  rv_ls_series = f_ls (stamps) * 1e3 

  return rv_ls_series

def correct_line_of_sight (stamps, velocity, interp_kind='linear', vephem=None) :

  """
  This routine uses an ephemerid file of 
  60 days sampled at 10 min.
  The first thing it does is interpolate
  and  resampling the ephemeridis 
  to correspond to the Solar-SONG subseries
  to correct.
  """

  mask = velocity != 0.

  if vephem is None :
    cm = importlib.resources.path ('apollinaire.songlib.ephemeris', 'sun_teide_20180527_20180725_apparent.csv')
    with cm as pathFile :
        df = pd.read_csv (pathFile, sep=';')
    t_ls = df['Date (undefined)']
    rv_ls = df['RV (km/s)']
    f_ls = interp1d (t_ls, rv_ls, kind=interp_kind)
    # We keep 0 value at the points where the instrument
    # did not make measurements
    rv_ls_series = f_ls (stamps) 
    vephem = rv_ls_series * mask
    vephem = vephem*1e3

  velocity = velocity - vephem

  return velocity

def compute_weights (mv, cut_up=0.1089, cut_low=1.e-6) :
  '''
  Compute weights of the different chunks following the 
  procedure described in Butler et al. 1996
 
  :param mv: the multi-velocity 24x22 array. Taken in m/s.
  :type mv: ndarray

  :param cut_up: up threshold to reject chunks and set the
  weight to 0. Set to None to avoid making a cut. 
  :type cut_up: float

  :param cut_low: low threshold to reject chunks and set the
  weight to 0. Set to None to avoid making a cut. 
  :type cut_low: float

  :return: weights
  :rtype: ndarray
  '''

  #weights = 1. / (np.nanstd (mv, axis=0)*np.nanstd(mv, axis=0))
  median = np.nanmedian (mv, axis=(1,2)) 
  aux_median = np.zeros (mv.shape)
  dim = mv.shape
  for j in range (dim[1]) :
    for k in range (dim[2]) :
      aux_median[:,j,k] = median
  mv = mv - aux_median
  scatter = mad_std (mv, axis=0, ignore_nan=True) 
  weights = 1. / (scatter*scatter)
  weights[weights==np.inf] = 0.

  if cut_up is not None :
    weights[weights>cut_up] = 0.
  if cut_low is not None :
    weights[weights<cut_low] = 0.
 
  return weights

def integrate_chunk (multi_velocity, mask_chunk=None, weights=None) :

  """
  A tool to compute a series considering the mean 
  values between different chunks from a 24x22
  velocity timeseries of Solar-SONG

  :param multi_velocity: the multi-velocity 24x22 array
  :type multi_velocity: ndarray

  :param mask_chunk:  boolean matrix with 24x22 size, True corresponding 
  to the chunks to consider for the computed velocity
  :type mask_chunk: boolean 24x22 array

  :param weights: attribute weight to average the chunks. 
  (see how to compute the weight of the chunks according to the
  method described in Butler et al. 1996.)
  :type weights: 24x22 ndarray

  :return: 1D velocity vector.
  :rtype: ndarray
  """

  if mask_chunk is None :
    mask_chunk = ~np.zeros ((24,22), dtype=bool)

  velocity = np.zeros (multi_velocity.shape[0])

  if weights is None :
    for ii, elt in enumerate (multi_velocity) :
      aux = elt*mask_chunk
      velocity[ii] = np.nanmean (aux)

  else :
    for ii, elt in enumerate (multi_velocity) :
      aux_w = np.copy (weights)
      aux_w[np.isnan(elt)] = 0.
      elt[np.isnan(elt)] = 0.
      aux = elt*mask_chunk
      if np.sum (aux_w) > 0. :
        velocity[ii] = np.average (aux, weights=aux_w)
      else :
        velocity[ii] = 0.
      del (aux_w)

  return velocity

def order_psd (mv, n_order, cut_global=4., dt=20., plot=True, window=60,
                correct=True) :

  '''
  CAUTION: This function needs to be updated with the right digital filter.
  For now it uses a triangle filtering. 

  Select an order from the multi-velocity chunk-by-chunk corrected array,
  make final corrections, compute and optionnaly plot PSD.  

  :param mv: multi-velocity array. It is assumed that chunk by chunk corrections
  have already been processed.
  :type mv: ndarray

  :param n_order: order to analyse, must be an integer between 1 and 24
  :type order: int

  :param cut_global: value in m/s to reject values considered as outliers
  :type cut_global: float

  :param dt: time sampling, must be given in seconds
  :type dt: float

  :param plot: set to True to automatically plot the PSD of the considered
  order
  :type plot: bool

  :param window: size of the window used to apply the low-frequency filter
  :type window: int

  :param correct: apply the global corrections on the order integrated data
  :type correct: int

  :return: frequency and power spectral density (PSD) spectrum
  :rtype: ndarray
  '''

  day = int (86400 / dt)

  order = mv[:,n_order-1,:]
  order[order==0] = np.nan
  order = np.nanmean (order, axis=1)

  if correct==True :
    for ii in range (int (order.size / day)) :
        aux = order[ii*day:(ii+1)*day]
        aberrant = np.abs (aux - np.nanmean (aux)) > cut_global
        aux[aberrant] = 0
        order[ii*day:(ii+1)*day] = aux

    order = order - pd.Series(data=order).rolling(window=window, win_type='triang', center=True).mean()

    order[np.isnan(order)] = 0

  f, p = series_to_psd (order, dt=20.)

  if plot==True :
    fig = plt.figure ()
    ax = fig.add_subplot (111) 
    ax.plot (f*1e6, p*1e-6, color='black', label=n_order)
    ax.legend ()
    ax.set_xlabel ('Frequency ($\mu$Hz)')
    ax.set_xlabel ('PSD ((m/s)$^2$/$\mu$Hz)')

  return f, p 

def plot_weights (mv, cut_up=None, cut_low=None, invert=False) :

  '''
  Compute and plot weights for each chunk
  
  :param mv: the multi-velocity 24x22 array
  :type mv: ndarray

  :param cut_up: up threshold to reject chunks and set the
  weight to 0. Set to None to avoid making a cut. 
  :type cut_up: float

  :param cut_low: low threshold to reject chunks and set the
  weight to 0. Set to None to avoid making a cut. 
  :type cut_low: float

  :param invert: set to True to plot velocity standard deviation
  and not weights.
  :type invert: bool
  '''
  
  weights = compute_weights (mv, cut_up=cut_up, cut_low=cut_low)

  fig = plt.figure ()
  ax = fig.add_subplot (111)
  ax.set_xlabel ('Chunks')
  ax.set_ylabel ('Weight (m/s)$^{-1}$')

  order = 0
  for elt in weights : 
    if invert==False :
      ax.bar (range (order*elt.size+1, (order+1)*elt.size+1), elt)
    else :
      ax.bar (range (order*elt.size+1, (order+1)*elt.size+1), 1./elt)
    order = order+1

  return

def plot_flux (mf) :

  '''
  Plot mean photon flux for each chunk, considering a given
  Solar-SONG timeseries.
  
  :param mf: the multi-flux 24x22 array
  :type mf: ndarray
  '''
  
  mean_flux = np.nanmean (mf, axis=0) 
  
  fig = plt.figure ()
  ax = fig.add_subplot (111)
  ax.set_xlabel ('Chunks')
  ax.set_ylabel ('Photon fluxlevel')

  order = 0
  for elt in mean_flux : 
    ax.bar (range (order*elt.size+1, (order+1)*elt.size+1), elt)
    order = order+1

  return
