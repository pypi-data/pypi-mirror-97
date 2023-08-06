import numpy as np

def flux_nan (s, v) :
    '''
    List here the date where velocity should be set to NaN due to
    flux problems. By calling flux_nan, the function will return
    input velocity vector with predetermined interval set to NaN 

    :param s: Julian day timestamps of the series.
    :type s: ndarray
  
    :param v: 1d velocity vector.
    :type v: ndarray

    :return: velocity vector with intervals with flux issues replaced by NaN.
    :rtype: ndarray
    '''

    d0=2458272.5

    # 30 days "gold series" (03062018 to 02072018)
    v[(s>2458272.5)&(s<2458272.8057)] = np.nan
    v[(s>2458274.262)&(s<2458274.28)] = np.nan
    v[(s>2458274.775)&(s<2458274.805)] = np.nan 
    v[(s>2458285.9535)&(s<2458285.9539)] = np.nan
    v[(s>2458286.009)&(s<2458286.0385)] = np.nan
    v[(s>2458286.05525)&(s<2458286.05600)] = np.nan
    v[(s>2458286.05589)&(s<2458286.0592)] = np.nan
    v[(s>2458286.063)&(s<2458286.0665)] = np.nan
    v[(s>2458286.0695)&(s<2458286.0715)] = np.nan
    v[(s>2458286.073)&(s<2458286.082)] = np.nan
    v[(s>2458298.92)&(s<2458299.35)] = np.nan

    # additionall corrections over the 57 days
    v[(s>d0-6.63681)&(s<d0-6.63418)] = np.nan
    v[(s>d0-6.6427)&(s<d0-6.64076)] = np.nan
    v[(s>d0-6.6398)&(s<d0-6.6389)] = np.nan
    v[(s>d0-3.74)&(s<d0-3.67473)] = np.nan
    v[(s>d0-3.)&(s<d0-3.)] = np.nan
    v[(s>d0-2.74)&(s<d0-2.72396)] = np.nan
    v[(s>d0-1.74)&(s<d0-1.67859)] = np.nan
    v[(s>d0-1.64615)&(s<d0-1.61702)] = np.nan
    v[(s>d0-1.61298)&(s<d0-1.60954)] = np.nan
    v[(s>d0-1.59002)&(s<d0-1.58233)] = np.nan
    v[(s>d0-1.22206)&(s<d0-1.205)] = np.nan
    v[(s>d0-0.648669)&(s<d0-0.2)] = np.nan

    v[(s>d0+30.7935)&(s<d0+30.7983)] = np.nan
    v[(s>d0+31.35)&(s<d0+31.4254)] = np.nan
    v[(s>d0+31.4699)&(s<d0+31.4902)] = np.nan
    v[(s>d0+32.7915)&(s<d0+32.8)] = np.nan
    v[(s>d0+35.5633)&(s<d0+35.5749)] = np.nan
    v[(s>d0+35.5894)&(s<d0+35.5934)] = np.nan
    v[(s>d0+35.7908)&(s<d0+35.8)] = np.nan
    v[(s>d0+37.3)&(s<d0+37.4433)] = np.nan
    v[(s>d0+37.4752)&(s<d0+37.5232)] = np.nan
    v[(s>d0+37.5336)&(s<d0+37.5429)] = np.nan
    v[(s>d0+37.5556)&(s<d0+38.5683)] = np.nan
    v[(s>d0+37.6742)&(s<d0+38.7031)] = np.nan
    v[(s>d0+38.3)&(s<d0+38.4426)] = np.nan
    v[(s>d0+38.4594)&(s<d0+38.4687)] = np.nan
    v[(s>d0+38.5346)&(s<d0+38.6081)] = np.nan
    v[(s>d0+38.62)&(s<d0+38.6209)] = np.nan
    v[(s>d0+39.3459)&(s<d0+39.3754)] = np.nan

    return v

def manual_nan (s, v) : 
    '''
    List here the date where velocity should be set to NaN due to
    visible problems. By calling manual_nan, the function will return
    input velocity vector with predetermined interval set to NaN.

    :param s: Julian day timestamps of the series.
    :type s: ndarray
  
    :param v: 1d velocity vector.
    :type v: ndarray

    :return: velocity vector with predetermined intervals replaced by NaN.
    :rtype: ndarray
    '''

    d0=2458272.5

    v[(s>d0+2.25)&(s<d0+2.33084)] = np.nan
    v[(s>d0+14.25)&(s<d0+14.318)] = np.nan
    v[(s>d0+24.25)&(s<d0+24.3265)] = np.nan
    v[(s>d0+26.25)&(s<d0+26.3529)] = np.nan
    v[(s>d0+27.25)&(s<d0+27.3688)] = np.nan
    v[(s>d0+28.25)&(s<d0+28.3754)] = np.nan
    v[(s>d0+29.25)&(s<d0+29.384)] = np.nan

    v[(s>d0+31.4455)&(s<d0+31.4464)] = np.nan
    v[(s>d0+31.4521)&(s<d0+31.453)] = np.nan
    v[(s>d0+31.464)&(s<d0+31.4651)] = np.nan
    v[(s>d0+35.5584)&(s<d0+35.5637)] = np.nan
    v[(s>d0+38.7883)&(s<d0+38.7971)] = np.nan
    v[(s>d0+45.7645)&(s<d0+45.7883)] = np.nan

    return v

