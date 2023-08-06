import numpy as np
import pandas as pd
import numba

def split_a2z (df_a2z) :

  inf_a2z = df_a2z[list(range (4))].to_numpy ()
  inf_a2z = inf_a2z.astype (np.str_)
  param_a2z = df_a2z[list(range (4,9))].to_numpy ()
  param_a2z = param_a2z.astype (np.float64)
  n = inf_a2z[inf_a2z[:, 2]=='freq', 0].astype (np.float64)
  l = inf_a2z[inf_a2z[:, 2]=='freq', 1].astype (np.float64)

  return n, l, inf_a2z, param_a2z

def match (n, l, aux, aux_param, inf_amp=None, param_amp=None, name=None) :

 incr = 0
 if l > 1 :
   incr+= 1
 if l > 3 :
   incr+= 1
 
 value = 0
 value_err = 0

 if np.any ((aux[:, 0]==str(n)) & (aux[:, 1]==str(l))) : 
   cond = (aux[:, 0]==str(n)) & (aux[:, 1]==str(l))
   value = aux_param[cond, 0][0]
   value_err = aux_param[cond, 1][0]

 elif (l==4) | (l==5) :

   if name=='split' :
     #l=4 and l=5 are fitted only in solar case : 
     #splitting are fixed to 400 nHz for those modes if not given specifically
     value = 0.4       
     value_err = 0. 
     return value, value_err
 
   if name=='angle' :
     #Set automatically to 90 (solar case)
     value = 90.
     value_err = 0.
     return value, value_err 

   if name=='asym' :
     # No asymmetry fitted for those modes
     value = 0.
     value_err = 0.
     return value, value_err

   elif np.any ( (aux[:,0]==str(n+incr)) & (aux[:,1]=='0') & (aux_param[:,2]==0) ) :
     l_ref = '0'
     ref_ratio = 1.
   else :
     l_ref = '1'
     ref_ratio = 1.8
   value = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref) & (aux_param[:,2]==0), 0][0] 
   value_err = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref) & (aux_param[:,2]==0), 1][0] 
   if inf_amp is not None :
     value = value / ref_ratio
     value_err = value_err / ref_ratio
     if l==4 :
       value = value * 0.0098
       value_err = value_err * 0.0098
     if l==5 :
       value = value * 0.001
       value_err = value_err * 0.001
     
 elif (np.any ( (aux[:, 0]==str(n+incr)) & (aux[:, 1]=='a') ) ) :
   cond2 = (aux[:, 0]==str(n+incr)) & (aux[:, 1]=='a')
   value = aux_param[cond2, 0][0]
   value_err = aux_param[cond2, 1][0]
   if inf_amp is not None :
     value = value * param_amp[inf_amp[:, 1]==str(l), 0][0]

 elif np.any (aux[:,0]=='a') :
   value = aux_param[aux[:,0]=='a', 0][0]   
   value_err = aux_param[aux[:,0]=='a', 1][0]   
   if inf_amp is not None :
     value = value * param_amp[inf_amp[:, 1]==str(l), 0][0]

 return value, value_err

def fill_param (pkb, name, inf_a2z, param_a2z) :
  
  if name=='height' :
    ind = 4
  if name=='width' :
    ind = 6
  if name=='angle' :
    ind = 8
  if name=='split' :
    ind = 10
  if name=='asym' :
    ind = 12

  aux = inf_a2z[inf_a2z[:, 2]==name, :]
  aux_param = param_a2z[inf_a2z[:, 2]==name, :]

  if name =='height' :
    inf_amp = inf_a2z[inf_a2z[:, 2]=='amp_l', :]
    param_amp = param_a2z[inf_a2z[:, 2]=='amp_l', :]
  else :
    inf_amp = None
    param_amp = None

  for ii in range (pkb.shape[0]) :
      v, verr = match (int(pkb[ii, 0]), int (pkb[ii, 1]), aux, aux_param, 
                       inf_amp=inf_amp, param_amp=param_amp, name=name)
      pkb[ii, ind] = v
      pkb[ii, ind+1] = verr

  return

def a2z_to_pkb_nopandas (n, l, inf_a2z, param_a2z) :

  freq = param_a2z[inf_a2z[:, 2]=='freq', 0]
  freq_err = param_a2z[inf_a2z[:, 2]=='freq', 1]
  pkb = np.zeros ((n.size, 14)) 
  pkb[:, 0] = n
  pkb[:, 1] = l
  pkb[:, 2] = freq
  pkb[:, 3] = freq_err

  fill_param (pkb, 'height', inf_a2z, param_a2z) 
  fill_param (pkb, 'width', inf_a2z, param_a2z) 
  if np.any (inf_a2z[:, 2]=='split') :
    fill_param (pkb, 'split', inf_a2z, param_a2z) 
    pkb[pkb[:,1]==0, 10] = 0. #fixing splitting for l=0 modes 
    pkb[pkb[:,1]==0, 11] = 0. 
  if np.any (inf_a2z[:, 2]=='asym') :
    fill_param (pkb, 'asym', inf_a2z, param_a2z) 
  if np.any (inf_a2z[:, 2]=='angle') :
    fill_param (pkb, 'angle', inf_a2z, param_a2z) 
  else :
    pkb[:, 8] = 90

  return pkb

def wrapper_a2z_to_pkb_nopandas (df_a2z) :

  n, l, inf_a2z, param_a2z = split_a2z (df_a2z)
  pkb = a2z_to_pkb_nopandas (n, l, inf_a2z, param_a2z)

  return pkb


###
# Same functions but for centile frame and pkb_extended
###

def split_cf (cf) :

  inf_a2z = cf[list(range (4))].to_numpy ()
  inf_a2z = inf_a2z.astype (np.str_)
  param_a2z = cf[list(range (4,7))].to_numpy ()
  param_a2z = param_a2z.astype (np.float64)
  n = inf_a2z[inf_a2z[:, 2]=='freq', 0].astype (np.float64)
  l = inf_a2z[inf_a2z[:, 2]=='freq', 1].astype (np.float64)

  return n, l, inf_a2z, param_a2z

def match_cf (n, l, aux, aux_param, inf_amp=None, param_amp=None, name=None) :

 incr = 0
 if l > 1 :
   incr+= 1
 if l > 3 :
   incr+= 1
 
 value = 0
 verr1 = 0
 verr2 = 0

 if np.any ((aux[:, 0]==str(n)) & (aux[:, 1]==str(l))) : 
   cond = (aux[:, 0]==str(n)) & (aux[:, 1]==str(l))
   value = aux_param[cond, 0][0]
   verr1 = aux_param[cond, 1][0]
   verr2 = aux_param[cond, 2][0]

 elif (l==4) | (l==5) :

   if name=='split' :
     value = 0.4       #splitting are fixed to 400 nHz for those modes if not given specifically
     verr1 = 0. 
     verr2 = 0. 
     return value, verr1, verr2

   if name=='angle' :
     #Set automatically to 90 (solar case)
     value = 90.
     verr1 = 0.
     verr2 = 0.
     return value, verr1, verr2 

   if name=='asym' :
     # No asymmetry fitted for those modes
     value = 0.
     verr1 = 0.
     verr2 = 0.
     return value, verr1, verr2 

   elif np.any ( (aux[:,0]==str(n+incr)) & (aux[:,1]=='0') ) :
     l_ref = '0'
     ref_ratio = 1.
   else :
     l_ref = '1'
     ref_ratio = 1.8
   value = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref), 0][0] 
   verr1 = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref), 1][0] 
   verr2 = aux_param[(aux[:,0]==str(n+incr)) & (aux[:,1]==l_ref), 2][0] 
   if inf_amp is not None :
     value = value / ref_ratio
     verr1 = verr1 / ref_ratio
     verr2 = verr2 / ref_ratio
     if l==4 :
       value = value * 0.0098
       verr1 = verr1 * 0.0098
       verr2 = verr2 * 0.0098
     if l==5 :
       value = value * 0.001
       verr1 = verr1 * 0.001
       verr2 = verr2 * 0.001
     
 elif (np.any ( (aux[:, 0]==str(n+incr)) & (aux[:, 1]=='a') ) ) :
   cond2 = (aux[:, 0]==str(n+incr)) & (aux[:, 1]=='a')
   value = aux_param[cond2, 0][0]
   verr1 = aux_param[cond2, 1][0]
   verr2 = aux_param[cond2, 2][0]
   if inf_amp is not None :
     value = value * param_amp[inf_amp[:, 1]==str(l), 0][0]

 elif np.any (aux[:,0]=='a') :
   value = aux_param[aux[:,0]=='a', 0][0]   
   verr1 = aux_param[aux[:,0]=='a', 1][0]   
   verr2 = aux_param[aux[:,0]=='a', 2][0]   
   if inf_amp is not None :
     value = value * param_amp[inf_amp[:, 1]==str(l), 0][0]

 return value, verr1, verr2

def fill_param_extended (pkb, name, inf_a2z, param_a2z) :
  
  if name=='height' :
    ind = 5
  if name=='width' :
    ind = 8
  if name=='angle' :
    ind = 11
  if name=='split' :
    ind = 14
  if name=='asym' :
    ind = 17

  aux = inf_a2z[inf_a2z[:, 2]==name, :]
  aux_param = param_a2z[inf_a2z[:, 2]==name, :]

  if name =='height' :
    inf_amp = inf_a2z[inf_a2z[:, 2]=='amp_l', :]
    param_amp = param_a2z[inf_a2z[:, 2]=='amp_l', :]
  else :
    inf_amp = None
    param_amp = None

  for ii in range (pkb.shape[0]) :
      v, verr1, verr2 = match_cf (int(pkb[ii, 0]), int (pkb[ii, 1]), aux, aux_param, 
                                  inf_amp=inf_amp, param_amp=param_amp, name=name)
      pkb[ii, ind] = v
      pkb[ii, ind+1] = verr1
      pkb[ii, ind+2] = verr2

  return

def cf_to_pkb_extended_nopandas (n, l, inf_a2z, param_a2z) :

  freq = param_a2z[inf_a2z[:, 2]=='freq', 0]
  freq_err1 = param_a2z[inf_a2z[:, 2]=='freq', 1]
  freq_err2 = param_a2z[inf_a2z[:, 2]=='freq', 2]
  pkb = np.zeros ((n.size, 20)) 
  pkb[:, 0] = n
  pkb[:, 1] = l
  pkb[:, 2] = freq
  pkb[:, 3] = freq_err1
  pkb[:, 4] = freq_err2

  fill_param_extended (pkb, 'height', inf_a2z, param_a2z) 
  fill_param_extended (pkb, 'width', inf_a2z, param_a2z) 
  if np.any (inf_a2z[:, 2]=='split') :
    fill_param_extended (pkb, 'split', inf_a2z, param_a2z) 
    pkb[pkb[:,1]==0, 14] = 0. #fixing splitting for l=0 modes 
    pkb[pkb[:,1]==0, 15] = 0. 
    pkb[pkb[:,1]==0, 16] = 0. 
  if np.any (inf_a2z[:, 2]=='asym') :
    fill_param_extended (pkb, 'asym', inf_a2z, param_a2z) 

  if np.any (inf_a2z[:, 2]=='angle') :
    fill_param_extended (pkb, 'angle', inf_a2z, param_a2z) 
  else :
    pkb[:, 11] = 90

  return pkb

def wrapper_cf_to_pkb_extended_nopandas (cf) :

  n, l, inf_a2z, param_a2z = split_cf (cf)
  pkb = cf_to_pkb_extended_nopandas (n, l, inf_a2z, param_a2z)

  return pkb
