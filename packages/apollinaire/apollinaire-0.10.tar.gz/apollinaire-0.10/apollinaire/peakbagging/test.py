from apollinaire.peakbagging import *
import apollinaire.peakbagging.templates as templates
import importlib.resources
import pandas as pd

def test_a2z (a2z_file) :

  '''
  Test a a2z file to check that it is valid. The function
  checks the bounds set for the parameters, convert the a2z
  DataFrame to pkb

  :param a2z_file: path of the a2z file to test.
  :type a2z_file: str

  :return: state of the file. If the file is valid, the function
    will return ``True``, ``False`` otherwise.    
  :rtype: bool
  '''

  df_a2z = read_a2z (a2z_file)
  check_a2z (df_a2z, verbose=True) 
  pkb = a2z_to_pkb (df_a2z)
  df_pkb = pd.DataFrame (data=pkb)
  
  print (df_a2z)
  print (df_pkb.to_string ())
  print (get_list_order (df_a2z))

  state = True

  if np.any (np.isnan (pkb)) :
    state = False 

  return state

if __name__ == '__main__' :

  f = importlib.resources.path (templates, 'test.a2z')
  with f as filename :
    print (test_a2z (filename))

