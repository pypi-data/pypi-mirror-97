import numpy as np

def levels (freq, psd, metric=['mean'], verbose=False) :

  '''
  Evaluate the power in different region of a given
  PSD.

  :param freq: frequency vector. Must be given in Hz.
  :type freq: ndarray

  :param psd: power spectral density vector.
  :type psd: ndarray

  :param metric: which estimator to use to evaluate the noise.
  Possibilities are ['mean'], ['median'], ['mean', 'median'], 
  :type metric: list

  :param verbose: set to True to print the different level
  of power evaluated.
  :type verbose: bool
  '''

  cond_1 = (freq > 1e-3) & (freq < 1.5e-3)
  cond_2 = (freq > 2.5e-3) & (freq < 3.5e-3)
  cond_3 = (freq > 5e-3) & (freq < 6e-3)
  cond_4 = (freq > 8e-3) & (freq < 10e-3)
  cond_5 = (freq > 9e-3) & (freq < 11e-3)
  cond_6 = (freq > 10e-3) & (freq < 12e-3)

  if 'mean' in metric: 
      mean_1 = np.mean (psd[cond_1])
      mean_2 = np.mean (psd[cond_2])
      mean_3 = np.mean (psd[cond_3])
      mean_4 = np.mean (psd[cond_4])
      mean_5 = np.mean (psd[cond_5])
      mean_6 = np.mean (psd[cond_6])

      # signal to noise index
      index_mean_sn = (mean_2 - mean_1) / mean_1

      if verbose==True :
          print ('Mean power [1, 1.5] mHz:', mean_1)
          print ('Mean power [2.5, 3.5] mHz:', mean_2)
          print ('Mean power [5, 6] mHz:', mean_3)
          print ('Mean power [8, 10] mHz:', mean_4)
          print ('Mean power [9, 11] mHz:', mean_5)
          print ('Mean power [10, 12] mHz:', mean_6)
          print ('Signal to noise mean index:', index_mean_sn)
      
      list_mean = [mean_1, mean_2, mean_3, mean_4, mean_5, mean_6, index_mean_sn]

  if 'median' in metric: 
      median_1 = np.median (psd[cond_1])
      max_2 = np.max (psd[cond_2])
      median_3 = np.median (psd[cond_3])
      median_4 = np.median (psd[cond_4])
      median_5 = np.median (psd[cond_5])
      median_6 = np.median (psd[cond_6])

      # signal to noise index
      index_median_sn = (max_2 - median_1) / median_1

      if verbose==True :
          print ('Median power [1, 1.5] mHz:', median_1)
          print ('Max power [2.5, 3.5] mHz:', max_2)
          print ('Median power [5, 6] mHz:', median_3)
          print ('Median power [8, 10] mHz:', median_4)
          print ('Median power [9, 11] mHz:', median_5)
          print ('Median power [10, 12] mHz:', median_6)
          print ('Signal to noise median index:', index_median_sn)

      list_median = [median_1, max_2, median_3, median_4, median_5, median_6, index_median_sn]

  if ('mean' in metric) & ('median' in metric) :
      return list_mean + list_median
  if ('median' in metric) :
      return list_median
  if ('mean' in metric) :
      return list_mean 


  
