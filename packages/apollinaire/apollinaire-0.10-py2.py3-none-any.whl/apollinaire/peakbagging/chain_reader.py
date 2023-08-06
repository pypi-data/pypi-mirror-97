import numpy as np
import pandas as pd
import glob
import emcee
from os import path
import os
from .fit_tools import *
from .a2z_no_pandas import wrapper_cf_to_pkb_extended_nopandas

def read_chain (filename, thin=1, discard=0) :
  '''
  Read chain and return flattened sampled chain with auxiliary informations.

  :param filename: name of the hdf5 file with the stored chain.
  :type filename: str

  :param thin: the returned chain will be thinned according to this factor. Optional, default 1.
  :type thin: int

  :param discard: number of iteration step to discard. Optional, default 0.
  :type discard: int

  :return: tuple with flatchain, labels of param, degrees of param and order of modes.
  :rtype: tuple of ndarrays
  ''' 
  reader = emcee.backends.HDFBackend(filename, read_only=True)

  labels = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=0)
  degrees = np.loadtxt (filename[:len(filename)-3]+'.dat', dtype=str, usecols=2)
  norm = np.loadtxt (filename[:len(filename)-3]+'.dat', usecols=1)

  order = path.basename (filename)[19:21]
  order = int (order)

  flatchain = reader.get_chain(flat=True, thin=thin, discard=discard) * norm

  return flatchain, labels, degrees, order 

def complete_df_with_ampl (df, instr='geometric') :

  a_amp = [['a', '2', 'amp_l', 'global', 0.7, 0.0, 1, 0.0, 0.0],
           ['a', '3', 'amp_l', 'global', 0.2, 0.0, 1, 0.0, 0.0],
           ['a', '1', 'amp_l', 'global', 1.5, 0.0, 1, 0.0, 0.0],
           ['a', '0', 'amp_l', 'global', 1.0, 0.0, 1, 0.0, 0.0]]
  df_amp = pd.DataFrame (data=a_amp) 

  if instr=='golf' :
    df_amp.loc[df[1]=='1', 4] = 1.69
    df_amp.loc[df[1]=='2', 4] = 0.81
    df_amp.loc[df[1]=='3', 4] = 0.17
  if instr=='virgo' :
    df_amp.loc[df[1]=='1', 4] = 1.53
    df_amp.loc[df[1]=='2', 4] = 0.59
    df_amp.loc[df[1]=='3', 4] = 0.09

  df = pd.concat ([df, df_amp])

  return df

def chain_element_to_a2z (param, labels, degrees, order, add_ampl=False, instr='geometric') :
  '''
  Build and a2z DataFrame with any set of parameters taken from a MCMC.

  :return: a2z DataFrame
  :rtype: pandas DataFrame
  '''

  columns = list (range (9))
  aux_index = list (range (labels.size))

  df = pd.DataFrame (index=aux_index, columns=columns)
  df.loc[:,0] = order
  df.loc[:,1] = degrees
  df.loc[:,2] = labels
  df.loc[labels!='a',3] = 'mode'
  df.loc[labels=='a',3] = 'order'
  df.loc[:,4] = param

  #retransforming width and heights
  cond_exp = (df[2]=='height')|(df[2]=='width')
  df.loc[cond_exp,4] = np.exp (df.loc[cond_exp,4])

  df.loc[(df[1]=='2')|(df[1]=='3'), 0] = (df.loc[(df[1]=='2')|(df[1]=='3'), 0].astype (np.int_) - 1).astype (np.str_)
  df.loc[(df[1]=='4')|(df[1]=='5'), 0] = (df.loc[(df[1]=='4')|(df[1]=='5'), 0].astype (np.int_) - 2).astype (np.str_)

  if add_ampl :
    df = complete_df_with_ampl (df, instr='geometric')

  return df

def chain_to_a2z (filename, thin=1, discard=0, add_ampl=False, instr='geometric') :
  '''
  Function to create an a2z dataframe from a sampled chain.

  :param filename: name of the chain. The name format is the following
    ``mcmc_sampler_order_[n_order]_degrees_[n_degrees].h5`` with ``n_degrees`` being ``13`` or ``02``.
  :type filename: str

  :param instr: instrument to consider. Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :return: a2z style dataframe.
  :rtype: pandas DataFrame
  '''

  flatchain, labels, degrees, order = read_chain (filename, thin=thin, discard=discard)

  centiles = np.percentile (flatchain, [16, 50, 84], axis=0) 
  bounds = np.percentile (flatchain, [0,100], axis=0) 

  columns = list (range (9))
  aux_index = list (range (labels.size))

  df = pd.DataFrame (index=aux_index, columns=columns)
  df.loc[:,0] = order
  df.loc[:,1] = degrees
  df.loc[:,2] = labels
  df.loc[labels!='a',3] = 'mode'
  df.loc[labels=='a',3] = 'order'
  df.loc[:,4] = centiles[1,:]

  #retransforming width and heights
  cond_exp = (df[2]=='height')|(df[2]=='width')
  a_cond_exp = cond_exp.to_numpy ()
  for ii in range (centiles.shape[0]) :
    centiles[ii,a_cond_exp] = np.exp (centiles[ii,a_cond_exp])
  df.loc[cond_exp,4] = np.exp (df.loc[cond_exp,4])

  #Computing (symmetric) sigmas
  sigma_1 = centiles[1,:] - centiles[0,:]
  sigma_2 = centiles[2,:] - centiles[1,:]
  sigma = np.maximum (sigma_1, sigma_2)

  df.loc[:,5] = sigma
  df.loc[:,6] = 0.

  #Adding bounds
  df.loc[:,7] = bounds[0,:]
  df.loc[:,8] = bounds[1,:]

  df.loc[(df[1]=='2')|(df[1]=='3'), 0] = (df.loc[(df[1]=='2')|(df[1]=='3'), 0].astype (np.int_) - 1).astype (np.str_)
  df.loc[(df[1]=='4')|(df[1]=='5'), 0] = (df.loc[(df[1]=='4')|(df[1]=='5'), 0].astype (np.int_) - 2).astype (np.str_)

  if add_ampl :
    df = complete_df_with_ampl (df, instr='geometric')

  return df

def complete_df_centile_with_ampl (df, instr='geometric') :

  a_amp = [['a', '2', 'amp_l', 'global', 0.7, 0.0, 0.0],
           ['a', '3', 'amp_l', 'global', 0.2, 0.0, 0.0],
           ['a', '1', 'amp_l', 'global', 1.5, 0.0, 0.0],
           ['a', '0', 'amp_l', 'global', 1.0, 0.0, 0.0]]
  df_amp = pd.DataFrame (data=a_amp)

  if instr=='golf' :
    df_amp.loc[df[1]=='1', 4] = 1.69
    df_amp.loc[df[1]=='2', 4] = 0.81
    df_amp.loc[df[1]=='3', 4] = 0.17
  if instr=='virgo' :
    df_amp.loc[df[1]=='1', 4] = 1.53
    df_amp.loc[df[1]=='2', 4] = 0.59
    df_amp.loc[df[1]=='3', 4] = 0.09

  df = pd.concat ([df, df_amp])

  return df

def chain_to_centile_frame (filename, thin=1, discard=0, add_ampl=False, instr='geometric') :
  '''
  Function to create a centile frame from a sampled chain.

  :param discard: the number of elements to ignore at the beginning of the chain.
  :type discard: int

  :param thin: one element of the chain every ``thin`` elements will be considered.
  :type thin: int

  :param filename: name of the chain. The name format is the following
    'mcmc_sampler_order_[n_order]_degrees_[n_degrees].h5' with n_degrees being '13' or '02'.
  :type filename: str

  :return: centile frame
  :rtype: pandas DataFrame
  '''

  flatchain, labels, degrees, order = read_chain (filename, thin=thin, discard=discard)

  centiles = np.percentile (flatchain, [16, 50, 84], axis=0) 
  bounds = np.percentile (flatchain, [0,100], axis=0) 

  columns = list (range (6))
  aux_index = list (range (labels.size))

  df = pd.DataFrame (index=aux_index, columns=columns)
  df.loc[:,0] = order
  df.loc[:,1] = degrees
  df.loc[:,2] = labels
  df.loc[labels!='a',3] = 'mode'
  df.loc[labels=='a',3] = 'order'
  df.loc[:,4] = centiles[1,:]

  #retransforming width and heights
  cond_exp = (df[2]=='height')|(df[2]=='width')
  a_cond_exp = cond_exp.to_numpy ()
  for ii in range (centiles.shape[0]) :
    centiles[ii,a_cond_exp] = np.exp (centiles[ii,a_cond_exp])
  df.loc[cond_exp,4] = np.exp (df.loc[cond_exp,4])

  #Adding sigmas
  sigma_1 = centiles[1,:] - centiles[0,:]
  sigma_2 = centiles[2,:] - centiles[1,:]

  df.loc[:,5] = sigma_1
  df.loc[:,6] = sigma_2

  df.loc[(df[1]=='2')|(df[1]=='3'), 0] = (df.loc[(df[1]=='2')|(df[1]=='3'), 0].astype (np.int_) - 1).astype (np.str_)
  df.loc[(df[1]=='4')|(df[1]=='5'), 0] = (df.loc[(df[1]=='4')|(df[1]=='5'), 0].astype (np.int_) - 2).astype (np.str_)

  if add_ampl :
    df = complete_df_centile_with_ampl (df, instr='geometric')

  return df

def cf_to_pkb_extended (df_centile, nopandas=True) :
  '''
  Take centile frame and return pkb extended array. Frequency units are given in µHz and not Hz. pkb format is the following: 

  +------------+---+---+-----+---------------+-----------+-----------+-----------+-------+------+------+--------+--------+--------+-------+------+------+----------------+---------+
  | parameters | n | l | nu  | nu_e- | nu_e+ | height    | height_e- | height_e+ | width | w_e- | w_e+ | angle  | a_e-   | a_e+   | split | s_e- | s_e+ | asym | asym_e- | asym_e+ |
  +------------+---+---+-----+---------------+-----------+-----------+-----------+-------+------+------+--------+--------+--------+-------+--------------------+---------+---------+
  | units      | . | . | µHz | µHz   | µHz   | power/µHz | power/µHz | power/µHz | µHz   | µHz  | µHz  | degree | degree | degree | µHz   | µHz  | µHz  | .    | .       | .       |
  +------------+---+---+-----+---------------+-----------+-----------+-----------+-------+------+------+--------+--------+--------+-------+------+------+------+---------+---------+

  :param df_centile: input parameters as a centile frame.
  :type df_centile: pandas DataFrame

  :return: array extended pkb. 
  :rtype: ndarray
  '''

  if nopandas :
    return wrapper_cf_to_pkb_extended_nopandas (df_centile)
  
  modes = df_centile.loc[df_centile[2]=='freq'].copy ()
  height = df_centile.loc[df_centile[2]=='height'].copy ()
  width = df_centile.loc[df_centile[2]=='width'].copy ()
  amp_l = df_centile.loc[df_centile[2]=='amp_l'].copy ()
  asym = df_centile.loc[df_centile[2]=='asym'].copy ()
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
    aux_height = aux_height.set_index(aux_height[0]).join (height[[4,5,6]].set_index(height[0]))
    aux_height = aux_height.set_index (aux_height[1]).join (amp_l[['ratio']].set_index(amp_l[1]))
    aux_height.loc[:,4] = aux_height[4].to_numpy() * aux_height['ratio'].to_numpy ()
    aux_height.loc[:,5] = aux_height[5].to_numpy() * aux_height['ratio'].to_numpy ()
    aux_height.loc[:,6] = aux_height[5].to_numpy() * aux_height['ratio'].to_numpy ()
    aux_height = aux_height.reset_index (drop=True)
    aux_height.loc[aux_height[1]>1, 0] = aux_height.loc[aux_height[1]>1, 0] - 1
    aux_height = aux_height.rename (columns={4:'height', 5:'height_error-', 6:'height_error+'})
  else : #case where heights are fitted degree to degree
    height.loc[:,1] = height.loc[:,1].map (np.int_)
    height = height.set_index([0,1])
    aux_height = aux_height.set_index([0,1]).join (height[[4,5,6]])
    aux_height = aux_height.reset_index ()
    aux_height = aux_height.rename (columns={4:'height', 5:'height_error-', 6:'height_error+'})
  if (width[1]=='a').any () : #width are fitted order to order
    # 'correcting' order in order to have the right height and width value when performing the
    # join step.
    aux_width.loc[aux_width[1]>1, 0] = aux_width.loc[aux_width[1]>1, 0] + 1
    aux_width = aux_width.set_index(aux_width[0]).join (width[[4,5,6]].set_index(width[0]))
    aux_width = aux_width.reset_index (drop=True)
    aux_width.loc[aux_width[1]>1, 0] = aux_width.loc[aux_width[1]>1, 0] - 1
    aux_width = aux_width.rename (columns={4:'width', 5:'width_error-', 6:'width_error+'})
  else : #case where widths are fitted degree to degree
    width.loc[:,1] = width.loc[:,1].map (np.int_)
    width = width.set_index([0,1])
    aux_width = aux_width.set_index([0,1]).join (width[[4,5,6]])
    aux_width = aux_width.reset_index ()
    aux_width = aux_width.rename (columns={4:'width', 5:'width_error-', 6:'width_error+'})

  # extracting angle, angle_error, split and split_error
  cond_split = (df_centile.loc[df_centile[2]=='split'].index.size > 1) 
  if cond_split :
    split = df_centile.loc[df_centile[2]=='split'].copy ()
    split.loc[:,0] = split.loc[:,0].map (np.int_)
    aux_split = modes[[0,1]].copy ()
    if (split[1]=='a').any () : #splitting are fitted order to order
      aux_split.loc[aux_split[1]>1, 0] = aux_split[aux_split[1]>1, 0] + 1
      aux_split = aux_split.set_index(aux_split[0]).join (split[[4,5,6]].set_index(split[0]))
      aux_split = aux_split.reset_index (drop=True)
      aux_split.loc[aux_split[1]>1, 0] = aux_split.loc[aux_split[1]>1, 0] - 1
      aux_split = aux_split.rename (columns={4:'split', 5:'split_error-', 6:'split_error+'})
    else : #splitting are fitted degree to degree
      split.loc[:,1] = split.loc[:,1].map (np.int_)
      split = split.set_index([0, 1])
      aux_split = aux_split.set_index([0, 1]).join (split[[4,5,6]])
      aux_split = aux_split.reset_index ()
      aux_split.loc[aux_split[1]==0, 4] = 0   #set splitting for l=0 to 0 instead of NaN
      aux_split.loc[aux_split[1]==0, 5] = 0
      aux_split.loc[aux_split[1]==0, 6] = 0
      aux_split = aux_split.rename (columns={4:'split', 5:'split_error-', 6:'split_error+'})
  elif (df_centile.loc[df_centile[2]=='split'].index.size == 1) :
    split = df_centile.loc[df_centile[2]=='split', 4].values[0]
    split_error_minus = df_centile.loc[df_centile[2]=='split', 5].values[0]
    split_error_plus = df_centile.loc[df_centile[2]=='split', 6].values[0]
  else :
    split = 0.
    split_error_minus = 0.
    split_error_plus = 0.

  #asymetry extraction
  if not asym.empty : 
    if (asym[1]=='a').any () : #asym are fitted order to order
      aux_asym = modes[[0,1]].copy ()
      aux_asym.loc[aux_asym[1]>1, 0] = aux_asym[0] + 1
      aux_asym = aux_asym.set_index(aux_asym[0]).join (asym[[4,5,6]].set_index(asym[0]))
      aux_asym = aux_asym.reset_index (drop=True)
      aux_asym.loc[aux_asym[1]>1, 0] = aux_asym[0].loc[aux_asym[1]>1] - 1
      aux_asym = aux_asym.rename (columns={4:'asym', 5:'asym_error-', 6:'asym_error+'})
    else : #asym are fitted degree to degree
      asym.loc[:,1] = asym.loc[:,1].map (np.int_)
      aux_asym = modes[[0,1]].copy ()
      asym  = asym.set_index([0,1])
      aux_asym = aux_asym.set_index([0, 1]).join (asym[[4,5,6]])
      aux_asym = aux_asym.reset_index ()
      aux_asym = aux_asym.rename (columns={4:'asym', 5:'asym_error-', 6:'asym_error+'})

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

  try :
    angle = df_centile.loc[df_centile[2]=='angle', 4].values[0]
    angle_error_minus = df_centile.loc[df_centile[2]=='angle', 5].values[0]
    angle_error_plus = df_centile.loc[df_centile[2]=='angle', 6].values[0]
  except IndexError :
    angle = 90.
    angle_error_minus = 0.
    angle_error_plus = 0.
  # ------------------------------------------------------------------------

  # Filling pkb_extended array 
  pkb_extended = np.zeros ((n_elt, 20))
  pkb_extended[:,0] = modes[0].to_numpy () #n - order
  pkb_extended[:,1] = modes[1].to_numpy () #l - degree
  pkb_extended[:,2] = modes[4].to_numpy () #nu - freq
  pkb_extended[:,3] = modes[5].to_numpy () #nu_error - freq
  pkb_extended[:,4] = modes[6].to_numpy () #nu_error - freq
  # height are given in ***^2/muHz
  pkb_extended[:,5] = modes['height'].to_numpy ()  
  pkb_extended[:,6] = modes['height_error-'].to_numpy () 
  pkb_extended[:,7] = modes['height_error+'].to_numpy () 
  #
  pkb_extended[:,8] = modes['width'].to_numpy () 
  pkb_extended[:,9] = modes['width_error-'].to_numpy () 
  pkb_extended[:,10] = modes['width_error+'].to_numpy () 
  pkb_extended[:,11] = angle
  pkb_extended[:,12] = angle_error_minus
  pkb_extended[:,13] = angle_error_plus
  if cond_split :
    pkb_extended[:,14] = modes['split'].to_numpy ()  
    pkb_extended[:,15] = modes['split_error-'].to_numpy () 
    pkb_extended[:,16] = modes['split_error+'].to_numpy () 
    pkb_extended[:,14] = np.nan_to_num (pkb_extended[:,14]) #allow to not specify every split value
    pkb_extended[:,15] = np.nan_to_num (pkb_extended[:,15]) #in the a2z input 
    pkb_extended[:,16] = np.nan_to_num (pkb_extended[:,16])  
  else :
    pkb_extended[:,14] = split
    pkb_extended[:,15] = split_error_minus
    pkb_extended[:,16] = split_error_plus
  if not asym.empty :
    pkb_extended[:,17] = modes['asym'].to_numpy ()
    pkb_extended[:,18] = modes['asym_error-'].to_numpy ()
    pkb_extended[:,19] = modes['asym_error+'].to_numpy ()
    pkb_extended[:,17] = np.nan_to_num (pkb_extended[:,12]) #allow not to specify every asym value in
    pkb_extended[:,18] = np.nan_to_num (pkb_extended[:,13]) #the a2z input
    pkb_extended[:,19] = np.nan_to_num (pkb_extended[:,13]) 

  return pkb_extended


def hdf5_to_a2z (workDir='.', a2zname='summary_fit.a2z', discard=0, thin=10, instr='geometric', centile=False) :

  '''
  Create a a2z file with the hdf5 files stored in a given folder.

  :param workDir: the directory where the hdf5 file will be read.
  :type workDir: str

  :param a2zname: the name of the output file. Set to ``None`` if you do not want to save any file.
  :type pkbname: str

  :param discard: the number of elements to ignore at the beginning of the chain.
  :type discard: int

  :param thin: one element of the chain every ``thin`` elements will be considered.
  :type thin: int

  :param centile: if set to True, change the structure of the output to write a centile frame.
    Optional, default ``False``.
  :type centile: bool

  :param instr: instrument to consider. Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :return: a2z DataFrame
  :rtype: pandas DataFrame
  '''

  listHDF5 = glob.glob (path.join (workDir, 'mcmc_sampler_order_*.h5'))
  listHDF5.sort ()
  df = pd.DataFrame ()
  add_ampl = False
  for ii, filename in enumerate (listHDF5) :
    print (filename)
    if ii==len (listHDF5) - 1 :
      add_ampl=True
    if not centile :
      aux = chain_to_a2z (filename, thin=thin, discard=discard, add_ampl=add_ampl, instr=instr)
    else :
      aux = chain_to_centile_frame (filename, thin=thin, discard=discard, add_ampl=add_ampl, instr=instr)
    df = pd.concat ([df, aux])

  if a2zname is not None :
    save_a2z (path.join (workDir, a2zname), df)

  return df

def hdf5_to_pkb (workDir='.', pkbname='summary_fit.pkb', discard=0, thin=10, instr='geometric', extended=False) :

  '''
  Create a pkb file with the hdf5 files stored in a given folder.

  :param workDir: the directory where the hdf5 file will be read.
  :type workDir: str

  :param pkbname: the name of the output pkb. Set to ``None`` if you do not want to save a file.
  :type pkbname: str

  :param discard: the number of elements to ignore at the beginning of the chain.
  :type discard: int

  :param thin: one element of the chain every ``thin`` elements will be considered.
  :type thin: int

  :param extended: if set to True, change the structure of the output to write a pkb extended.
    Optional, default ``False``.
  :type extended: bool

  :param instr: instrument to consider. Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :return: pkb array
  :rtype: ndarray
  '''

  centile = False
  if extended :
    centile = True

  df = hdf5_to_a2z (workDir=workDir, a2zname=None, discard=discard, thin=thin, instr=instr, centile=centile)

  df = df.loc[(df[1]!='4')&(df[1]!='5')]
  if extended :
    pkb = cf_to_pkb_extended (df)
  else :
    pkb = a2z_to_pkb (df)
  if pkbname is not None :
    np.savetxt (path.join (workDir, pkbname), pkb, fmt='%-s')

  return pkb
