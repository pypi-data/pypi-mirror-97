pkb and a2z format
******************

a2z DataFrames
##############

The syntax of the a2z files has been designed to specify some pieces of information the
procedure has to be aware of when dealing with individual mode parameters extraction. A
line corresponds to a parameter. The file contains nine columns: order *n*, degree *l*,
*name* of the parameter, *extent*, *value*, *uncertainty*, *fixed* key, *low bound* and
*up bound* of the parameter.

If a parameter has to apply to every order or degrees, the value to specify in the
corresponding column is *a*. The possible parameters *name* are *freq, height, width,
asym, angle, split*. Parameters with name *freq, height* or *width* cannot have *n=a*,
parameters with name *freq* cannot have *l=a*. The *extent* columns reminds the extent of
application of a given parameter: *mode*, *order* or *global*. Only *angle* or *split*
parameters can be set as *global*. For an input a2z file, the *value* column specify the
value around where the sampler will initialise the walkers that will sample the MCMC. The
*uncertainty* column is relevant only for output a2z files. The *fixed* key column values
must be set to 0 or 1 and are managed by the ``peakbagging`` function. Parameters with
*fixed* key 0 at a given step will be fitted while parameters with 1-value will be read as
frozen parameters. In input a2z files, the *low bound* and *up bound* columns specify the
limit values inside which the posterior probability will be sampled. Obviously, the *up
bound* must be greater than the *low bound*, and the *value* term must lay inside the
defined interval.

+---+---+------+--------+-------+-------------+-------+-----------+----------+
| 0 | 1 | 2    | 3      | 4     | 5           | 6     | 7         | 8        |
+---+---+------+--------+-------+-------------+-------+-----------+----------+
| n | l | name | extent | value | value_error | fixed | low_bound | up_bound |
+---+---+------+--------+-------+-------------+-------+-----------+----------+

*l=4* and *l=5* modes can be specified to avoid bias in the fitted frequencies
(see Jiménez-Reyes et al. 2008 for more details). It is important to keep in
mind that whether strategy is chosen (``order`` or ``pair``), those modes will
only be fitted if their guess frequency appears in the frequency window used
for the fit of modes of lower degrees. Note that for *l=4* and *l=5* modes, it
is possible to specify only the frequency in the a2z file, height and width
will be automatically computed considering the height and width of the closest
fitted *l=0* or *l=1* mode. In this case, splittings are fixed to 400 nHz and
no asymmetry is considered for those modes. All m-components of the mode have
the same amplitude ratio. 


pkb arrays
##########

In pkb files, each line correspond to a given mode of order *n* and degree *l*. The file
contains 14 columns: order *n*, degree *l*, mode frequency, uncertainty over frequency,
mode height, uncertainty over height, mode width, uncertainty over width, stellar angle,
uncertainty over stellar angle, mode splitting, uncertainty over mode splitting, mode
asymmetry, uncertainty over mode asymmetry.

.. |nu| replace:: :math:`\nu`
.. |nuerr| replace:: :math:`\sigma` \ :sub:`ν`  
.. |herror| replace:: :math:`\sigma` \ :sub:`height` 
.. |werror| replace:: :math:`\sigma` \ :sub:`width` 
.. |aerror| replace:: :math:`\sigma` \ :sub:`angle` 
.. |serror| replace:: :math:`\sigma` \ :sub:`split` 
.. |asymerror| replace:: :math:`\sigma` \ :sub:`asym` 

+------------+---+---+------+-----------+-----------+-----------+-------+----------+--------+----------+-------+----------+------+-------------+
| index      | 0 | 1 | 2    | 3         | 4         | 5         | 6     | 7        | 8      | 9        | 10    | 11       | 12   | 13          |
+------------+---+---+------+-----------+-----------+-----------+-------+----------+--------+----------+-------+----------+------+-------------+
| parameters | n | l | |nu| | |nuerr|   | height    | |herror|  | width | |werror| | angle  | |aerror| | split | |serror| | asym | |asymerror| |
+------------+---+---+------+-----------+-----------+-----------+-------+----------+--------+----------+-------+----------+------+-------------+
| units      | . | . | µHz  | µHz       | power/µHz | power/µHz | µHz   | µHz      | degree | degree   | µHz   | µHz      | .    | .           |
+------------+---+---+------+-----------+-----------+-----------+-------+----------+--------+----------+-------+----------+------+-------------+

Extended pkb arrays
###################

.. |sigma-| replace:: :math:`\sigma` \ :sub:`-`  
.. |sigma+| replace:: :math:`\sigma` \ :sub:`+`  
.. |nuerr-| replace:: :math:`\sigma` \ :sub:`ν,-`  
.. |nuerr+| replace:: :math:`\sigma` \ :sub:`ν,+`  
.. |herror-| replace:: :math:`\sigma` \ :sub:`height,-` 
.. |herror+| replace:: :math:`\sigma` \ :sub:`height,+` 
.. |werror-| replace:: :math:`\sigma` \ :sub:`width,-` 
.. |werror+| replace:: :math:`\sigma` \ :sub:`width,+` 
.. |aerror-| replace:: :math:`\sigma` \ :sub:`angle,-` 
.. |aerror+| replace:: :math:`\sigma` \ :sub:`angle,+` 
.. |serror-| replace:: :math:`\sigma` \ :sub:`split,-` 
.. |serror+| replace:: :math:`\sigma` \ :sub:`split,+` 
.. |asymerror-| replace:: :math:`\sigma` \ :sub:`asym,-` 
.. |asymerror+| replace:: :math:`\sigma` \ :sub:`asym,+` 

The format of the extended pkb array is close to the classical pkb array,
except that, for each parameters, it contains two uncertainty value: |sigma+|,
corresponding to the difference between the 16th centiles and the median of the
distribution, and |sigma-|, corresponding to the difference between the median
and the 84th centile of the distribution. 

+------------+---+---+------+-----------+-----------+-----------+-----------+-----------+-------+-----------+-----------+--------+-----------+-----------+-------+-----------+-----------+------+--------------+--------------+
| index      | 0 | 1 | 2    | 3         | 4         | 5         | 6         | 7         | 8     | 9         | 10        | 11     | 12        | 13        | 14    | 15        | 16        | 17   | 18           | 19           |
+------------+---+---+------+-----------+-----------+-----------+-----------+-----------+-------+-----------+-----------+--------+-----------+-----------+-------+-----------+-----------+------+--------------+--------------+
| parameters | n | l | |nu| | |nuerr-|  | |nuerr+|  | height    | |herror-| | |herror+| | width | |werror-| | |werror+| | angle  | |aerror-| | |aerror+| | split | |serror-| | |serror+| | asym | |asymerror-| | |asymerror+| |
+------------+---+---+------+-----------+-----------+-----------+-----------+-----------+-------+-----------+-----------+--------+-----------+-----------+-------+-----------+-----------+------+--------------+--------------+
| units      | . | . | µHz  | µHz       | µHz       | power/µHz | power/µHz | power/µHz | µHz   | µHz       | µHz       | degree | degree    | degree    | µHz   | µHz       | µHz       | .    | .            | .            |
+------------+---+---+------+-----------+-----------+-----------+-----------+-----------+-------+-----------+-----------+--------+-----------+-----------+-------+-----------+-----------+------+--------------+--------------+

Examples
########

Here is an example of an a2z DataFrame :

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

And here is the corresponding pkb array :

.. parsed-literal::

    [[  19.       1.    2198.735    0.      11.389    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  18.       2.    2251.86     0.       5.315    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  19.       0.    2256.763    0.       7.593    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  20.       1.    2308.901    0.      12.874    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  19.       2.    2362.026    0.       6.008    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  20.       0.    2366.929    0.       8.583    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  21.       1.    2419.24     0.      12.124    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  20.       2.    2472.364    0.       5.658    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  21.       0.    2477.267    0.       8.082    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  22.       1.    2529.751    0.       9.503    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  21.       2.    2582.875    0.       4.435    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  22.       0.    2587.778    0.       6.335    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  23.       1.    2640.434    0.       6.195    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  22.       2.    2693.558    0.       2.891    0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]
     [  23.       0.    2698.462    0.       4.13     0.       0.95     0.       0.       0.       0.       0.       0.       0.   ]]
