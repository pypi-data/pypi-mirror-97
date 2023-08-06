import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import george
import apollinaire.peakbagging.templates as templates
import importlib.resources 

'''
Train and manage random gaussian process for 
epsilon guess.
'''

def gp_predict (value=5770, plot_prediction=True) :

  f = importlib.resources.path (templates, 'kepler_epsilon.csv')
  with f as filename :
    df = pd.read_csv (filename, index_col=0)
  df = df.sort_values ('Teff')
  X = df['Teff'].to_numpy ()
  y = df['epsilon'].to_numpy ()

  k = 100. * george.kernels.ExpSquaredKernel (1.e5)
  kernel = k
  gp = george.GP (kernel=kernel, fit_kernel=True)

  gp.compute (X)
  epsilon, cov_epsilon = gp.predict (y, value) 

  if plot_prediction :
    x_plot = np.linspace (5100, 6600, 100)
    mean, cov = gp.predict (y, x_plot)
    figure, ax = plt.subplots (1, 1)
    ax.scatter (X, y, marker='o', color='black')
    ax.plot (x_plot, mean, color='orange')
    ax.scatter (value, epsilon, marker='*', color='yellow', s=100, zorder=10,
                edgecolor='black')
    ax.set_xlabel (r'$T_\mathrm{eff}$ (K)')
    ax.set_ylabel (r'\epsilon')
    plt.show ()

  return epsilon

def get_min_max_teff () :
  '''
  Get minimum and maximum Teff value for which the epsilon 
  train is performed.
  '''

  f = importlib.resources.path (templates, 'kepler_epsilon.csv')
  with f as filename :
    df = pd.read_csv (filename, index_col=0)
  
  min_t = df['Teff'].min ()
  max_t = df['Teff'].max ()

  return min_t, max_t

if __name__ == '__main__' :

  gp_predict ()
  
