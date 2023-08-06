import numpy as np
import sys
"""
"""

def ampl_mode (l, m, i_deg, sini, cosi, instr='geometric') :
  '''
  Compute geometrical ratio of amplitude between the mode
  according to the inclination of the star.

  :param l: degree of the mode
  :type l: int
  :param m: azimuthal order 
  :type m: int
  :param i: inclination (in degrees)
  :type i: float
  :param sini: sin (i)
  :type sini: float
  :param cosi: cos (i)
  :type cosi: float

  :param instr: instrument to consider (amplitude ratio inside degrees depend on geometry 
  AND instrument and should be adaptated). Possible argument : 'kepler', 'golf'
  :type instr: str

  :return: R
  :rtype: float
  '''
  R=-1
  i = i_deg / 360. * 2. * np.pi

  if (l == 0) & (m == 0) : 
     R = 1.0
  
  if instr=='kepler' or instr=='geometric' :

    if (l == 1) & (abs(m) == 0) : 
       R = cosi*cosi
    if (l == 1) & (abs(m) == 1) : 
       R = 0.5 * sini * sini
    if (l == 2) & (abs(m) == 0) : 
       R = 0.25 * ((3.0 * cosi * cosi) - 1.0)**2
    if (l == 2) & (abs(m) == 1) : 
       sinti = np.sin(2.0*i)
       R = (3.0/8.0) * sinti * sinti
    if (l == 2) & (abs(m) == 2) : 
       R = (3.0/8.0)*sini*sini*sini*sini
    if (l == 3) & (abs(m) == 0) : 
       R = (1.0/64.0) * ((5.0*np.cos(3.0*i)) + (3.0*cosi))**2
    if (l == 3) & (abs(m) == 1) : 
       R = (3.0/64.0)*((5.0*np.cos(2.0*i))+3)**2*sini*sini
    if (l == 3) & (abs(m) == 2) : 
       R = (15.0/8.0)*cosi*cosi*sini*sini*sini*sini
    if (l == 3) & (abs(m) == 3) : 
       R = (5.0/16.0)*sini*sini*sini*sini*sini*sini
    if (l == 4) & (abs(m) == 0) : 
       R = (1.0/64.0)*((35.0*cosi*cosi*cosi*cosi)-(30.0*cosi*cosi)+3)**2
    if (l == 4) & (abs(m) == 1) : 
       R = (5.0/256.0)*(((7.0/2.0)*np.sin(4.0*i))+(np.sin(2.0*i)))**2
    if (l == 4) & (abs(m) == 2) : 
       R = (5.0/128.0)*((7.0*np.cos(2.0*i))+5)^2*sini*sini*sini*sini
    if (l == 4) & (abs(m) == 3) : 
       R = (35.0/16.0)*cosi*cosi*sini*sini*sini*sini*sini*sini
    if (l == 4) & (abs(m) == 4) : 
       R = (35.0/128.0)*sini*sini*sini*sini*sini*sini*sini*sini

  if instr=='golf' :
    if (l == 1) & (m == 0) :
      R = 0.
    if (l == 1) & (abs(m) == 1) :
      R = 0.5
    if (l == 2) & (abs(m) == 0) :
      R = 0.65 / 2.65
    if (l == 2) & (abs(m) == 1) :
      R = 0.
    if (l == 2) & (abs(m) == 2) :
      R = 1. / 2.65
    if (l == 3) & (abs(m) == 0) :
      R = 0.
    if (l == 3) & (abs(m) == 1) :
      R = 0.41 / 2.82
    if (l == 3) & (abs(m) == 2) :
      R = 0.
    if (l == 3) & (abs(m) == 3) :
      R = 1. / 2.82

  if instr=='virgo' :
    if (l == 1) & (m == 0) :
      R = 0.
    if (l == 1) & (abs(m) == 1) :
      R = 0.5
    if (l == 2) & (abs(m) == 0) :
      R = 0.75 / 2.75
    if (l == 2) & (abs(m) == 1) :
      R = 0.
    if (l == 2) & (abs(m) == 2) :
      R = 1. / 2.75
    if (l == 3) & (abs(m) == 0) :
      R = 0.
    if (l == 3) & (abs(m) == 1) :
      R = 0.63 / 3.26
    if (l == 3) & (abs(m) == 2) :
      R = 0.
    if (l == 3) & (abs(m) == 3) :
      R = 1. / 3.26

  if R==-1 :
    print (l)
    print (m)
    raise Exception ('Issue with order and degrees values, ratio returned -1')
   
  return R
