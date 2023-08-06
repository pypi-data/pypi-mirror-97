import numpy as np
from scipy import signal
import matplotlib
import matplotlib.pyplot as plt

def bdf (f) :
  '''
  Compute backward difference filter (see Garcia & Ballot 2008)
  on a timeseries.
  
  :param f: input timeseries
  :type f: ndarray
 
  :return: filtered timeseries
  :rtype: ndarray
  '''
  f_shiftleft = np.insert (f, 0, [0.])
  f_shiftright = np.append (f, 0.)
  delta_f = f_shiftright - f_shiftleft
  delta_f = np.delete (delta_f, [0])
  delta_f[delta_f.size-1] = delta_f[delta_f.size-2]
  return delta_f

def design_digital_filter (numtaps=1001, 
                           bands=[0, 700e-6, 700e-6, 900e-6, 900e-6, 25e-3], 
                           desired=[0,0,0,1,1,1], 
                           fs=1/20., plot_response=False, return_coeff=True) :

  '''
  Design a digital finit impulse response (FIR) filter using the scipy method 
  scipy.signal.firls. 

  The description of scipy.signal.firls arguments is taken from scipy documentation.

  :param numtaps: The number of taps in the FIR filter. numtaps must be odd.
  :type: int

  :param bands: A monotonic nondecreasing sequence containing the band edges in Hz. 
  All elements must be non-negative and less than or equal to the Nyquist 
  frequency given by nyq.
  :type bands: array-like

  :param desired: A sequence the same size as bands containing the desired gain at 
  the start and end point of each band.
  :type desired: array-like.

  :param fs: The sampling frequency of the signal. Each frequency in bands must be between 
  0 and fs/2 (inclusive). Default is 2.
  :type fs: float

  :param plot_response: Set to True to plot the frequency transfer function of the filter. 
  Default False.
  :type plot_response: bool

  :return: filter that will be used to convolve the signal.
  :rtype: ndarray

  .. note :: By default, the designed filter is a high pass filter with a cut frequency at 800 muHz. 
  The sampling considered is 20 seconds, which corresponds to a Nyquist frequency at 25 mHz.
  If you want to set the cut frequency at, for example, 100 muHz, with another Nyquist frequency value, 
  try passing the following arguments to the function :
  >>> bands = [0, 90e-6, 90e-6, 100e-6, 100e-6, f_nyquist] 
  >>> desired = [0,0,0,1,1,1]
  >>> fs = 2 * f_nyquist 
  '''

  b = signal.firls (numtaps, bands, desired, fs=fs)
  freq, response = signal.freqz (b, fs=fs)
  filt = np.fft.irfft (response)

  if plot_response == True :
      fig = plt.figure ()
      ax = fig.add_subplot (111)
      ax.plot (freq*1e6, np.abs(response))
      ax.set_xscale ('log')
      ax.set_xlabel (r'Frequency ($\mu$Hz)')
      ax.set_ylabel ('Transfer function')

  if return_coeff==True :
      return b
  else :
      return filt

def convolve_filter (series, filt) :
  '''
  Convolve the timeseries by a filter created with design_digital_filter.

  :param series: timeseries to filter.
  :type series: ndarray

  :param filt: filters (created with the design_digital_filter function).
  :type filt: ndarray

  :return: filtered series.
  :rtype: ndarray
  '''
  filtered_series = signal.convolve (series, filt, mode='same')

  return filtered_series

def mirror (series, window_size) :

  '''
  Takes a timeseries with a duty-cycle smaller than 1 (eg for example
  a timeseries corresponing to one day of observation, with no measure
  during the night). The routine replace 0 at the beginning and end of 
  the series by the following (for the beginning) and preceding (for the 
  end of the series) values, taken in reverse order. 
  This routine is useful to avoid losing data when filtering at low 
  frequency. 

  :param series: the timeseries to process.
  :type series: ndarray

  :param window_size: the number of 0 to replace at the beginning and at the end
  of the 'true' measurements.   
  :type window_size: int

  :return: the mirrored series.
  :rtype: ndarrat.
  '''

  mask = (series != 0).astype (int) 

  # Adding mirrored slice at the end of the series
  mask_forward = np.roll (mask, window_size) 
  
  mask_forward[mask.astype(bool)] = 0 
  rerolled_mask = np.roll (mask_forward, -window_size) 

  masked_series = series * rerolled_mask 
  revert_slice = np.extract (masked_series != 0., masked_series) 
  revert_slice = np.flip (revert_slice)

  series[mask_forward.astype(bool)] = revert_slice

  # Adding mirrored slice at the beginning of the series
  mask_backward = np.roll (mask, -window_size)

  mask_backward[mask.astype(bool)] = 0 
  rerolled_mask = np.roll (mask_backward, window_size)

  masked_series = series * rerolled_mask
  revert_slice = np.extract (masked_series != 0., masked_series)
  revert_slice = np.flip (revert_slice)

  series[mask_backward.astype(bool)] = revert_slice

  return series
  
