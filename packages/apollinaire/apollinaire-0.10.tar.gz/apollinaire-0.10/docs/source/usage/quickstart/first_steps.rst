Quickstart
**********

Let’s assume that you want to use *apollinaire* to fit p-mode parameters
for a given star. First we need to import the package :

.. code:: python

    import apollinaire as apn

The name of the star we are going to work with is KIC6603624, also
known as Saxo. The package includes a version of the lightcurves
calibrated following the KEPSEISMIC method (see García et al. 2014).

.. code:: python

    from astropy.io import fits
    from os import path
    import numpy as np
    import matplotlib.pyplot as plt
    
    modDir = path.abspath ('..')
    filename = path.join (modDir, 'timeseries/kplr006603624_52_COR_filt_inp.fits')
    hdu = fits.open (filename) [0]
    data = np.array (hdu.data)
    t = data[:,0]
    v = data[:,1]
    
    fig, ax = plt.subplots ()
    ax.plot (t-t[0], v, color='black')
    
    ax.set_xlabel ('Time (days)')
    ax.set_ylabel ('Luminosity variation (ppm)')


.. image:: output_3_1.png


Let’s compute the psd of this lightcurve with the dedicated function:

.. code:: python

    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq = freq*1e6
    psd = psd*1e-6
    
    fig, ax = plt.subplots ()
    ax.plot (freq, psd, color='black')
    ax.set_xlabel (r'Frequency ($\mu$Hz)')
    ax.set_ylabel (r'PSD (ppm$^2$ / $\mu$Hz)')
    ax.set_yscale ('log')
    ax.set_xscale ('log')



.. image:: output_5_0.png


Here are the p-modes we want to fit :

.. code:: python

    fig, ax = plt.subplots ()
    cond = (freq>1500.)&(freq<3000.)
    ax.plot (freq[cond], psd[cond], color='black')
    ax.set_xlabel (r'Frequency ($\mu$Hz)')
    ax.set_ylabel (r'PSD (ppm$^2$ / $\mu$Hz)')


.. image:: output_7_1.png


We can also take a look at the echelle diagram of the modes. For this
purpose, we have to compute :math:`\Delta\nu`, the large separation,
through the scaling law, knowing mass and radius of the star. Mass and
radius values are taken from the DR25 *Kepler* catalog (see Mathur et
al. 2017).

.. code:: python

    r = 1.162
    m = 1.027
    dnu_sun = 135.
    dnu = dnu_sun * np.power (m, 0.5) * np.power (r, -1.5)
    apn.psd.echelle_diagram (freq[cond]*1e-6, psd[cond], dnu)


.. image:: output_9_0.png


The main peakbagging tool provided by *apollinaire* is the
``stellar_framework`` function. It will successively fit the background
of the star, the global pattern of the p-modes, and finally the
individual parameters of the modes. Radius, mass and effective
temperature are needed as input.

.. code:: python

    
    teff = 5671
    apn.peakbagging.stellar_framework (freq, psd, r, m, teff, n_harvey=2, low_cut=50., filename_back='background',
                           filemcmc_back=None, nsteps_mcmc_back=2000, n_order=3, n_order_peakbagging=5,  
                           filename_pattern='pattern', filemcmc_pattern=None, nsteps_mcmc_pattern=2000, 
                           parallelise=True, spectro=False, quickfit=True, num=500,
                           progress=True, a2z_file='modes_param.a2z', nsteps_mcmc_peakbagging=2000, 
                           filename_peakbagging='summary_peakbagging.pdf')

In the first step of analysis, the stellar background activity is fitted in order to be removed from the spectrum:

.. image:: background_saxo.png


From now on, the real spectrum is divided by the fitted background spectrum.
The second step of the automated analysis is to adjust a global pattern on the
p-mode bump using a limited set of parameters: 

.. |eps| replace:: ε
.. |alpha| replace:: α
.. |numax| replace:: ν \ :sub:`max` 
.. |deltanu| replace:: Δν 
.. |Hmax| replace:: H \ :sub:`max`
.. |Wenv| replace:: W \ :sub:`env`
.. |d02| replace:: :math:`\delta` \ :sub:`02`
.. |d01| replace:: :math:`\delta` \ :sub:`01`
.. |d13| replace:: :math:`\delta` \ :sub:`13`
.. |b02| replace:: :math:`\beta` \ :sub:`02`
.. |b01| replace:: :math:`\beta` \ :sub:`01`
.. |b03| replace:: :math:`\beta` \ :sub:`03`

+-------+---------+-----------+---------+--------+--------+---+-------+-------+-------+-------+-------+-------+
| |eps| | |alpha| | |deltanu| | |numax| | |Hmax| | |Wenv| | w | |d02| | |b02| | |d01| | |b01| | |d13| | |b03| |
+-------+---------+-----------+---------+--------+--------+---+-------+-------+-------+-------+-------+-------+

Note that it is possible to fit only the pairs 02 by setting the argument
``fit_l1`` and ``fit_l3`` to ``False``. The parameters |d01|, |b01|, |d13| and |b03| will not be fitted in
this case. In the current version of the code, it is not possible to fit l=3 modes without fitting l=1.

This is what the fitted global pattern looks like:

.. image:: pattern_saxo.png

The individual mode parameters are extracted thanks to a final series of MCMC
explorations, performed on each radial order. ``n_order`` around |numax| were
used to fit the global pattern, but it is possible to fit more modes: the
argument ``n_order_peakbagging`` allows you to choose the number of orders you
want to fit at this step. This parameter is set to 5 for this example. Here is
for example what we get when fitting order *n=21*:

.. image:: mcmc_sampler_order_21.png 

The global profile fitted (including the background) can finally be visualised thanks to 
the summary plot:

.. image:: summary_saxo.png

A word about uncertainties
##########################

When you want to fit interest parameters, it is always good to be aware of
the way uncertainties are computed.  In *apollinaire*, output values and their
uncertainties are computed the following way: once the posterior probability
distribution has been sampled, the output value is selected as the median of
the distribution. The 16th and 84th centiles are also selected. If the
distribution has been sampled over the natural logarithm of the given
parameter, median and both centiles are transformed back. Differences between,
first, the median and the 16th centile and, secondly, the 84th centile and the
median are then computed.  The returned uncertainty corresponds then to largest
of those two values.  

You may also want to keep an eye both on uncertainties from the 16th and 84th
centiles (especially for parameter for which it is the natural logarithm that
has been fitted). It is possible by generating an extended summary file through
the ``hdf5_to_pkb`` function. 

