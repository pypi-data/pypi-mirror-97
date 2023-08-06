import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from .analyse_window import sidelob_param
from .ampl_mode import ampl_mode
from os import sys
from os import path

def read_a2z (a2z_file) :
  '''
  Read a file with a a2z standard syntax (doc to be written) and return
  a2z-style parameters.

  :param a2z_file: name of the file to read the parameters.
  :type a2z_file: string

  :return: input parameters as a pandas DataFrame with the a2z syntax.
  :rtype: pandas DataFrame
  '''

  df_a2z = pd.read_csv (a2z_file, sep=' ', header=None)

  return df_a2z

def save_a2z (filename, df) :
  '''
  Write with a a2z standard syntax (doc to be written).

  :param filename: name of the file where to write the parameters.
  :type filename: string
  '''

  df.to_csv (filename, sep=' ', header=False, index=False)
  
  return

def a2z_df_to_param (df, give_degree=False) :
  '''
  Convert df_a2z to param_a2z tuple useful to feed the log_likelihood and the
  scipy minimize function.

  :param df: input parameters as a pandas DataFrame with the a2z syntax.
  :type df: pandas DataFrame

  :param give_degree: if set to True, will also send back a vector with the
  degree of the corresponding parameters. Optional, default False. 
  :type give_degrees: bool
  '''
  df_to_fit = df.loc[df[6]==0].copy ()
  param_to_fit = df_to_fit[4].to_numpy ()
  param_type = df_to_fit[2].to_numpy ()
  bounds_to_fit = df_to_fit [[7,8]].to_numpy ()

  if give_degree :
    degrees = df_to_fit[1].to_numpy ()
    return param_to_fit, param_type, bounds_to_fit, degrees
  else :
    return param_to_fit, param_type, bounds_to_fit

def a2z_to_pkb (df_a2z) :
  '''
  Take a2z dataframe and return pkb_style parameters useful to feed the compute_model.
  function. IMPORTANT: Everywhere frequency units are muHz and not Hz. 
  parameters=[n,l,nu,nu_error,height,height_error,width,width_error,angle,angle_error,split,split_error, asym, asym_error]
  units=[integer,integer,uHz,uHz,poweruHz,poweruHz,uHz,uHz,deg,deg,uHz,uHz, ., .]

  :param df_a2z: input parameters as a pandas DataFrame with the a2z syntax.
  :type df_a2z: pandas DataFrame

  :return: input parameter using pkb syntax
  :rtype: ndarray
  '''
  modes = df_a2z.loc[df_a2z[2]=='freq'].copy ()
  height = df_a2z.loc[df_a2z[2]=='height'].copy ()
  width = df_a2z.loc[df_a2z[2]=='width'].copy ()
  amp_l = df_a2z.loc[df_a2z[2]=='amp_l'].copy ()
  asym = df_a2z.loc[df_a2z[2]=='asym'].copy ()
  n_elt = modes.index.size

  #converting columns 
  modes.loc[:,0] = modes.loc[:,0].map (np.int_)
  modes.loc[:,1] = modes.loc[:,1].map (np.int_)
  height.loc[:,0] = height.loc[:,0].map (np.int_)
  width.loc[:,0] = width.loc[:,0].map (np.int_)
  amp_l.loc[:,1] = amp_l.loc[:,1].map (np.int_)
  asym.loc[:,0] = asym.loc[:,0].map (np.int_)

  # computing height and width with a line for each mode
  # ------------------------------------------------------------------------
  aux_height = modes[[0,1]].copy () 
  aux_width = modes[[0,1]].copy ()
  amp_l = amp_l.rename (columns={4:'ratio'})
  if (height[1]=='a').any () : #height are fitted order by order
    # 'correcting' order in order to have the right height and width value when performing the
    # join step.
    aux_height.loc[aux_height[1]>1, 0] = aux_height.loc[aux_height[1]>1, 0] + 1
    aux_height = aux_height.set_index(aux_height[0]).join (height[[4,5]].set_index(height[0]))
    aux_height = aux_height.set_index (aux_height[1]).join (amp_l[['ratio']].set_index(amp_l[1]))
    aux_height.loc[:,4] = aux_height[4].to_numpy() * aux_height['ratio'].to_numpy ()
    aux_height.loc[:,5] = aux_height[5].to_numpy() * aux_height['ratio'].to_numpy ()
    aux_height = aux_height.reset_index (drop=True)
    aux_height.loc[aux_height[1]>1, 0] = aux_height[0].loc[aux_height[1]>1] - 1
    aux_height = aux_height.rename (columns={4:'height', 5:'height_error'})
  else : #case where heights are fitted degree to degree
    height.loc[:,1] = height.loc[:,1].map (np.int_)
    height = height.set_index([0,1])
    aux_height = aux_height.set_index([0,1]).join (height[[4,5]])
    aux_height = aux_height.reset_index ()
    aux_height = aux_height.rename (columns={4:'height', 5:'height_error'})
  if (width[1]=='a').any () : #width are fitted order to order
    # 'correcting' order in order to have the right height and width value when performing the
    # join step.
    aux_width.loc[aux_width[1]>1, 0] = aux_width.loc[aux_width[1]>1, 0] + 1
    aux_width = aux_width.set_index(aux_width[0]).join (width[[4,5]].set_index(width[0]))
    aux_width = aux_width.reset_index (drop=True)
    aux_width.loc[aux_width[1]>1, 0] = aux_width[0].loc[aux_width[1]>1] - 1
    aux_width = aux_width.rename (columns={4:'width', 5:'width_error'})
  else : #case where widths are fitted degree to degree
    width.loc[:,1] = width.loc[:,1].map (np.int_)
    width = width.set_index([0,1])
    aux_width = aux_width.set_index([0,1]).join (width[[4,5]])
    aux_width = aux_width.reset_index ()
    aux_width = aux_width.rename (columns={4:'width', 5:'width_error'})

  # extracting angle, angle_error, split and split_error
  cond_split = (df_a2z.loc[df_a2z[2]=='split'].index.size > 1) 
  if cond_split :
    split = df_a2z.loc[df_a2z[2]=='split'].copy ()
    split.loc[:,0] = split.loc[:,0].map (np.int_)
    aux_split = modes[[0,1]].copy ()
    if (split[1]=='a').any () : #splitting are fitted order to order
      aux_split.loc[aux_split[1]>1, 0] = aux_split[0] + 1
      aux_split = aux_split.set_index(aux_split[0]).join (split[[4,5]].set_index(split[0]))
      aux_split = aux_split.reset_index (drop=True)
      aux_split.loc[aux_split[1]>1, 0] = aux_split[0].loc[aux_split[1]>1] - 1
      aux_split = aux_split.rename (columns={4:'split', 5:'split_error'})
    else : #splitting are fitted degree to degree
      split.loc[:,1] = split.loc[:,1].map (np.int_)
      split = split.set_index([0, 1])
      aux_split = aux_split.set_index([0, 1]).join (split[[4,5]])
      aux_split = aux_split.reset_index ()
      aux_split.loc[aux_split[1]==0, 4] = 0   #set splitting for l=0 to 0 instead of NaN
      aux_split.loc[aux_split[1]==0, 5] = 0
      aux_split = aux_split.rename (columns={4:'split', 5:'split_error'})
  else :
    split = df_a2z.loc[df_a2z[2]=='split', 4].values[0]
    split_error = df_a2z.loc[df_a2z[2]=='split', 5].values[0]

  #asymetry extraction
  if not asym.empty : 
    if (asym[1]=='a').any () : #asym are fitted order to order
      aux_asym = modes[[0,1]].copy ()
      aux_asym.loc[aux_asym[1]>1, 0] = aux_asym[0] + 1
      aux_asym = aux_asym.set_index(aux_asym[0]).join (asym[[4,5]].set_index(asym[0]))
      aux_asym = aux_asym.reset_index (drop=True)
      aux_asym.loc[aux_asym[1]>1, 0] = aux_asym[0].loc[aux_asym[1]>1] - 1
      aux_asym = aux_asym.rename (columns={4:'asym', 5:'asym_error'})
    else : #asym are fitted degree to degree
      asym.loc[:,1] = asym.loc[:,1].map (np.int_)
      aux_asym = modes[[0,1]].copy ()
      asym  = asym.set_index([0,1])
      aux_asym = aux_asym.set_index([0, 1]).join (asym[[4,5]])
      aux_asym = aux_asym.reset_index ()
      aux_asym = aux_asym.rename (columns={4:'asym', 5:'asym_error'})

  #joining height and width on the main frame
  modes = modes.set_index ([0,1])
  aux_height = aux_height.set_index ([0,1])
  aux_width = aux_width.set_index ([0,1])
  modes = modes.join (aux_height)
  modes = modes.join (aux_width)
  # joining splits
  if cond_split :
    aux_split = aux_split.set_index ([0,1])
    modes = modes.join (aux_split)
  #joining asymetries
  if not asym.empty :
    aux_asym = aux_asym.set_index ([0,1])
    modes = modes.join (aux_asym)
  modes = modes.reset_index ()

  angle = df_a2z.loc[df_a2z[2]=='angle', 4].values[0]
  angle_error = df_a2z.loc[df_a2z[2]=='angle', 5].values[0]
  # ------------------------------------------------------------------------

  # Filling pkb array 
  param_pkb = np.zeros ((n_elt, 14))
  param_pkb[:,0] = modes[0].to_numpy () #n - order
  param_pkb[:,1] = modes[1].to_numpy () #l - degree
  param_pkb[:,2] = modes[4].to_numpy () #nu - freq
  param_pkb[:,3] = modes[5].to_numpy () #nu_error - freq
  # height are given in ***^2/muHz
  param_pkb[:,4] = modes['height'].to_numpy ()  
  param_pkb[:,5] = modes['height_error'].to_numpy () 
  #
  param_pkb[:,6] = modes['width'].to_numpy () 
  param_pkb[:,7] = modes['width_error'].to_numpy () 
  param_pkb[:,8] = angle
  param_pkb[:,9] = angle_error
  if cond_split :
    param_pkb[:,10] = modes['split'].to_numpy ()  
    param_pkb[:,11] = modes['split_error'].to_numpy () 
  else :
    param_pkb[:,10] = split
    param_pkb[:,11] = split_error
  if not asym.empty :
    param_pkb[:,12] = modes['asym'].to_numpy ()
    param_pkb[:,13] = modes['asym_error'].to_numpy ()

  return param_pkb


def input_to_pkb (param_to_fit, df_info_modes, df_global) :
  '''
  Take a2z parameter and corresponding auxiliary array (giving modes information
  that are not supposed to change when minimising, e.g. order, degree, etc.) 
  and return pkb_style parameters useful to feed the compute_model
  function.

  :return: input parameter using pkb syntax
  :rtype: ndarray
  '''
  df_info_modes[4] = param_to_fit
  df_a2z = pd.concat([df_info_modes, df_global])
  param_pkb = a2z_to_pkb (df_a2z)

  return param_pkb


def smooth (vector, smoothing) :
  '''
  Smooth routines. Uses boxcar smoothing. 

  :param vector: vector to smooth.
  :type vector: ndarray

  :param smoothing: size of the rolling window used for the smooth.
  :type smoothing: int

  :return: smoothed vector
  :rtype: ndarray
  '''
  smoothed = pd.Series (data=vector)
  smoothed = smoothed.rolling (smoothing, min_periods=1, center=True).mean ()
  return smoothed

def read_pkb (pkb_file) :
  '''
  Read a pkb file and return the parameters.
  :param pkb_file: name of the pkb file.
  :type pkb_file: str

  :return: an array with the parameters given by the file.  
  :rtype: ndarray

  ..note:: format reminder :
  parameters=[n,l,nu,nu_error,height,height_error,width,width_error,angle,angle_error,split, split_error]
  units=[integer,integer,uHz,uHz,ppm2uHz,ppm2uHz,uHz,uHz,deg,deg,uHz,uHz]
  '''
  param_pkb = np.loadtxt (pkb_file, skiprows=4)
  return param_pkb

def compute_model (freq, param_pkb, param_wdw=None, correct_width=1., instr='kepler') :

  '''
  Compute the model to compare with observed PSD.
  The asymetries are computed after Korzennik 2005. 

  :param freq: vector of frequency
  :type freq: ndarray

  :param param_pkb: parameters contained in the pkb files.
  :type param_pkb: ndarray

  :param param_wdw: parameters given by the analysis of the window.
  :type param_wdw: ndarray

  :param correct_width: param to adjust the width of the Lorentzian if it has been manually modified 
  during the fitting
  :type correct_width: float 

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str
 
  :return: computed model
  :rtype: ndarray
  '''

  model = np.zeros (freq.size)

  for elt in param_pkb :
    for m in range (int(-1*elt[1]), int (elt[1]) + 1) :
      if param_wdw is not None :
        for elt_wdw in param_wdw :
          nu0 = elt[2] + m*elt[10] + elt_wdw[1] 
          G = elt[6] * correct_width
          angle = elt[8]
          xxx = (freq - nu0) / G
          asym = elt[12]
          A = ampl_mode (int(elt[1]), m, angle, np.sin (angle), np.cos (angle), instr=instr) * elt[4] * elt_wdw[0] 
          num = A * (1 + asym*(xxx - asym/2.))
          if np.any (num) < 0 :
            return np.inf #avoid case where asymetries make a negative height
          model += num / (1. + 4. * xxx * xxx) 

      else :
        nu0 = elt[2] + m*elt[10]
        G = elt[6]
        angle = elt[8]
        xxx = (freq - nu0) / G
        asym = elt[12]
        A = ampl_mode (elt[1], m, angle, np.sin (angle), np.cos (angle), instr=instr) * elt[4] 
        num = A * (1 + asym*(xxx - asym/2.))
        if np.any (num) < 0 :
          return np.inf #avoid case where asymetries make a negative height
        model += num / (1. + 4. * xxx * xxx) 

  return model

def plot_from_param (param_pkb, freq, psd, back=None, wdw=None, smoothing=50, spectro=True, correct_width=1.,
                   show=False, filename=None, instr='kepler') :
  """
  Plot the results of a fit according to the pkb file.

  :param param_pkb: parameters contained in the pkb files.
  :type param_pkb: ndarray

  :param freq: frequency vector, must be given in muHz.
  :type freq: ndarray

  :param psd: real power vector, must be given in ***2/muHz. 
  :type freq: ndarray

  :param wdw: set to True if the mode have been fitted using the sidelobes fitting method, default False
  :type wdw: bool

  :param smoothing: size of the rolling window used to smooth the psd in the plot.
  :type smoothing: int

  :param spectro: set to True if the instruments uses spectroscopy, set the units in m/s instead of ppm, default True.
  :type spectro: bool

  :param correct_width: param to adjust the width of the Lorentzian if it has been manually modified 
  during the fitting
  :type correct_width: float 

  :param show: automatically show the plot, default False.
  :type show: bool

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str
  """

  if wdw is not None :
    param_wdw = sidelob_param (wdw, dt=1./(2*1.e-6*freq[-1]), do_tf=True)
    model = compute_model (freq, param_pkb, param_wdw=param_wdw, correct_width=correct_width, instr=instr) 
  else :  
    model = compute_model (freq, param_pkb, instr=instr) 

  if back is not None :
    model = model + back

  #Computing residuals, smoothed PSD, etc.
  quot_residuals = psd / model 
  smooth_psd = smooth (psd, smoothing)
  freq_peak = param_pkb [:,2]
  height_peak = np.log (param_pkb [:,4])
  height_error_peak = param_pkb [:,5] #already in log
  width_peak = np.log (param_pkb [:,6])
  width_error_peak = param_pkb [:,7] #already in log
  l_peak = param_pkb [:,1].astype (int)

  # Sub ensembles for with and height representation
  # (one color for each l value)
  i0, = np.where (l_peak == 0)
  i1, = np.where (l_peak == 1)
  i2, = np.where (l_peak == 2)
  i3, = np.where (l_peak == 3)
  f0 = freq_peak[i0]
  f1 = freq_peak[i1]
  f2 = freq_peak[i2]
  f3 = freq_peak[i3]
  h0 = height_peak[i0]
  h1 = height_peak[i1]
  h2 = height_peak[i2]
  h3 = height_peak[i3]
  eh0 = height_error_peak[i0]
  eh1 = height_error_peak[i1]
  eh2 = height_error_peak[i2]
  eh3 = height_error_peak[i3]
  w0 = width_peak[i0]
  w1 = width_peak[i1]
  w2 = width_peak[i2]
  w3 = width_peak[i3]
  ew0 = width_error_peak[i0]
  ew1 = width_error_peak[i1]
  ew2 = width_error_peak[i2]
  ew3 = width_error_peak[i3]

  fig = plt.figure (figsize=(10,10))
  capsize=2.5
  labelpad=0

  #PSD centered on fitted p-mode
  ax1 = fig.add_subplot (321) 
  cond = (freq > np.amin (param_pkb[:,2])-50.)&(freq < np.amax (param_pkb[:,2])+50.)

  ax1.plot (freq[cond], psd[cond], color='grey') 
  ax1.plot (freq[cond], smooth_psd[cond], color='black') 
  ax1.plot (freq[cond], model[cond], color='red') 

  #Global PSD (log-scale)
  ax2 = fig.add_subplot (322) 
  ax2.set_xscale ('log')
  ax2.set_yscale ('log')

  ax2.plot (freq, psd, color='grey') 
  ax2.plot (freq, smooth_psd, color='black') 
  ax2.plot (freq, model, color='red') 

  #Residual / (background+mode)
  ax3 = fig.add_subplot (323, sharex=ax1) 
  ax3.plot (freq[cond], quot_residuals[cond], color='black') 
  ax3.plot (freq[cond], smooth(quot_residuals, 20)[cond], color='green') 
  ax3.plot (freq[cond], smooth(quot_residuals, 50)[cond], color='blue') 
  ax3.plot (freq[cond], smooth(quot_residuals, 100)[cond], color='red') 

  ax3.set_ylim (0., 10)

  #Height
  ax4 = fig.add_subplot (324, sharex=ax1) 
  ax4.errorbar (f0, h0, yerr=eh0, fmt='r ', label='l0', capsize=capsize)
  ax4.errorbar (f1, h1, yerr=eh1, fmt='b ', label='l1', capsize=capsize)
  ax4.errorbar (f2, h2, yerr=eh2, fmt='g ', label='l2', capsize=capsize)
  ax4.errorbar (f3, h3, yerr=eh3, fmt='y ', label='l3', capsize=capsize)
  ax4.legend ()

  #Width
  ax5 = fig.add_subplot (325, sharex=ax1) 
  ax5.errorbar (f0, w0, yerr=ew0, fmt='r ', capsize=capsize)
  ax5.errorbar (f1, w1, yerr=ew1, fmt='b ', capsize=capsize)
  ax5.errorbar (f2, w2, yerr=ew2, fmt='g ', capsize=capsize)
  ax5.errorbar (f3, w3, yerr=ew3, fmt='y ', capsize=capsize)

  #label
  slabel=9

  ax1.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax2.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax3.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax4.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax5.set_xlabel (r'Frequency ($\mu$Hz)', labelpad=labelpad, size=slabel)
  ax5.set_ylabel (r'log Width ($\mu$Hz)', size=slabel)
  if spectro == True :
    ax1.set_ylabel (r'PSD (m$^2$.s$^{-2}$/$\mu$Hz)', size=slabel)
    ax2.set_ylabel (r'PSD (m$^2$.s$^{-2}$/$\mu$Hz)', size=slabel)
    ax3.set_ylabel (r'PSD/(back+model)', size=slabel)
    ax4.set_ylabel (r'log Height (m$^2$.s$^{-2}$/$\mu$Hz)', size=slabel)
  else :
    ax1.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)', size=slabel)
    ax2.set_ylabel (r'PSD (ppm$^2$/$\mu$Hz)', size=slabel)
    ax3.set_ylabel (r'PSD/(back+model)', size=slabel)
    ax4.set_ylabel (r'log Height (ppm$^2$/$\mu$Hz)', size=slabel)

  ax1.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax2.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax3.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax4.tick_params(direction='in', labelsize=8, top=True, right=True)
  ax5.tick_params(direction='in', labelsize=8, top=True, right=True)

  if filename is not None :
    plt.savefig (filename)
  if show==True :
    plt.show()
  return 

