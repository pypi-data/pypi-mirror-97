Advanced peakbagging
********************

In the **Quickstart** section, I explained how to quickly handle seismic
data and perform peakbagging over it. However, when dealing with
individual mode parameters, you will sometimes need more flexibility on
the fit you want to perform. The goal of this tutorial is to show you
how to fit the background in your data and then perform an advanced fit
on individual parameters thanks to the *a2z* input format.

.. code:: python

    import numpy as np
    import apollinaire as apn
    from apollinaire.peakbagging import (peakbagging, 
                                         perform_mle_background, 
                                         explore_distribution_background)

Dealing with the background
---------------------------

The ``perform_mle_background`` allows you to obtain a first fit of the
background in your data through maximum likelihood estimation:

.. code:: python

    fitted_back, param_mle = perform_mle_background (freq, psd, n_harvey=2, fit_log=True, low_cut=20)

If you need uncertainties over the fitted parameter, you can then refine
this analysis with a bayesian approach, using the ``explore_distribution_background`` function:

.. code:: python

    fitted_back, param_mcmc, sigma = explore_distribution_background (freq, psd, n_harvey=2, guess=param_mle, 
                                                                      fit_log=True, low_cut=20, nsteps=10000,
                                                                      nwalkers=64, coeff_discard=10)

This step is by far longer than the previous one. Be particularly careful with
what you want when setting ``nwalkers``, ``nsteps`` and ``coeff_discard``
arguments.

Note that an important feature of those two functions is controlled by the
``quickfit`` argument. It allows to perform the fit over a smoothed and
logarithmically resampled spectrum, which is way faster than the classical
method of performing the fit over the full spectrum. You can also choose to fit
the parameters or their logarithms with the ``fit_log`` argument. However, this method
may lead to uncorrect/biased uncertainties values and I therefore formally discourage you
to use it for deepened studies of the background parameters. 

Individual mode parameters determination
----------------------------------------

With the determination of the background done, we are ready to begin the
determination of the individual mode parameters. For this purpose, you
need to create a *a2z* file that will be read by the ``peakbagging``
function. The file ``input_golf.a2z`` is given as an example. It
contains guess for solar p-mode from *n*\ =8 to 27 and *l*\ =0 to 3.

.. code:: python

    from apollinaire.peakbagging import read_a2z
    
    df = read_a2z ('input_golf.a2z')
    
    print (df.iloc[247:266].to_string ()) #show just a part of the df


.. parsed-literal::

         0  1       2     3            4    5    6             7            8   
    247  20  3    freq  mode  3082.429700  0.0  0.0  3.080430e+03  3084.429700  
    248  20  3  height  mode     0.004543  0.0  0.0  1.000000e-08     0.022717  
    249  20  3   width  mode     0.886951  0.0  0.0  1.000000e-08     8.000000  
    250  20  3    asym  mode    -0.007878  0.0  0.0 -2.000000e-01     0.200000  
    251  20  3   split  mode     0.400000  0.0  0.0  1.000000e-01     0.800000  
    252  20  2    freq  mode  3024.819500  0.0  0.0  3.022820e+03  3026.819500  
    253  20  2  height  mode     0.020445  0.0  0.0  1.000000e-08     0.102226  
    254  20  2   width  mode     0.886951  0.0  0.0  1.000000e-08     8.000000  
    255  20  2    asym  mode    -0.007878  0.0  0.0 -2.000000e-01     0.200000  
    256  20  2   split  mode     0.400000  0.0  0.0  1.000000e-01     0.800000  
    257  21  1    freq  mode  3098.239400  0.0  0.0  3.096239e+03  3100.239400  
    258  21  1  height  mode     0.040890  0.0  0.0  1.000000e-08     0.204452  
    259  21  1   width  mode     0.886951  0.0  0.0  1.000000e-08     8.000000  
    260  21  1    asym  mode    -0.007878  0.0  0.0 -2.000000e-01     0.200000  
    261  21  1   split  mode     0.400000  0.0  0.0  1.000000e-01     0.800000  
    262  21  0    freq  mode  3033.816200  0.0  0.0  3.031816e+03  3035.816200  
    263  21  0  height  mode     0.022717  0.0  0.0  1.000000e-08     0.113584  
    264  21  0   width  mode     0.886951  0.0  0.0  1.000000e-08     8.000000  
    265  21  0    asym  mode    -0.007878  0.0  0.0 -2.000000e-01     0.200000  


Here, each parameter is individual for a given degree. It is also
possible to share a parameter between element of same order *n* and
distinct degrees *l* (note that when I say *same order* I designate
pairs (n,0)/(n-1,2) and (n,1)/(n-1,3)). Here is an example of *a2z*
input for the *Kepler* star Saxo:

.. code:: python

    from apollinaire.peakbagging import read_a2z
    
    df = read_a2z ('input_saxo.a2z')
    
    print (df.to_string ()) 


.. parsed-literal::

         0  1       2       3            4    5    6            7            8
    0   19  1    freq    mode  2198.735167  0.0  0.0  2191.577557  2205.892778
    1   18  2    freq    mode  2251.859534  0.0  0.0  2244.701923  2259.017145
    2   19  0    freq    mode  2256.762699  0.0  0.0  2249.605088  2263.920310
    3   19  a  height   order     7.592848  0.0  0.0     3.796424    30.371392
    4   19  a   width   order     0.949858  0.0  0.0     0.474929     1.899717
    5   20  1    freq    mode  2308.901246  0.0  0.0  2301.743635  2316.058857
    6   19  2    freq    mode  2362.025612  0.0  0.0  2354.868002  2369.183223
    7   20  0    freq    mode  2366.928778  0.0  0.0  2359.771167  2374.086388
    8   20  a  height   order     8.582715  0.0  0.0     4.291358    34.330861
    9   20  a   width   order     0.949858  0.0  0.0     0.474929     1.899717
    10  21  1    freq    mode  2419.239760  0.0  0.0  2412.082149  2426.397370
    11  20  2    freq    mode  2472.364126  0.0  0.0  2465.206516  2479.521737
    12  21  0    freq    mode  2477.267291  0.0  0.0  2470.109681  2484.424902
    13  21  a  height   order     8.082355  0.0  0.0     4.041177    32.329420
    14  21  a   width   order     0.949858  0.0  0.0     0.474929     1.899717
    15  22  1    freq    mode  2529.750709  0.0  0.0  2522.593098  2536.908319
    16  21  2    freq    mode  2582.875075  0.0  0.0  2575.717465  2590.032686
    17  22  0    freq    mode  2587.778241  0.0  0.0  2580.620630  2594.935851
    18  22  a  height   order     6.335368  0.0  0.0     3.167684    25.341473
    19  22  a   width   order     0.949858  0.0  0.0     0.474929     1.899717
    20  23  1    freq    mode  2640.434093  0.0  0.0  2633.276482  2647.591704
    21  22  2    freq    mode  2693.558460  0.0  0.0  2686.400849  2700.716070
    22  23  0    freq    mode  2698.461625  0.0  0.0  2691.304014  2705.619236
    23  23  a  height   order     4.130032  0.0  0.0     2.065016    16.520129
    24  23  a   width   order     0.949858  0.0  0.0     0.474929     1.899717
    25   a  a   split  global     0.000000  0.0  0.0     0.000000     1.000000
    26   a  a   angle  global     0.000000  0.0  0.0     0.000000    90.000000
    27   a  1   amp_l  global     1.500000  0.0  0.0     0.000000     0.000000
    28   a  2   amp_l  global     0.700000  0.0  0.0     0.000000     0.000000
    29   a  0   amp_l  global     1.000000  0.0  0.0     0.000000     0.000000

You can read more about a2z format in the dedicated section.  

.. code:: python

    a2z_file = 'input_saxo.a2z'
    from os import path
    modDir = path.abspath ('..')
    filename = path.join (modDir, 'timeseries/kplr006603624_52_COR_filt_inp.fits')
    hdu = fits.open (filename) [0]
    data = np.array (hdu.data)
    t = data[:,0]
    v = data[:,1]
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq = freq*1e6
    psd = psd*1e-6
    
    df_a2z_fitted = peakbagging (a2z_file, freq, psd, back=fitted_back, spectro=False, 
                                 nsteps_mcmc=1000, progress=True, strategy='order', coeff_discard=10)

The best way to visualise the result is to transform the a2z output of the ``peakbagging`` function into a pkb array and
to feed the ``plot_from_param`` function.  It is also possible to directly save a summary plot with ``peakbagging`` by
specifying the ``filename_summary`` argument. 

.. code:: python

    pkb = a2z_to_pkb (df_a2z_fitted)
    plot_from_param (pkb, freq, psd, spectro=False, show=True)


