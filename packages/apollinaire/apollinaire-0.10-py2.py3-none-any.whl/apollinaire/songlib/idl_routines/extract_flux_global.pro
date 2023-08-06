PRO EXTRACT_FLUX_GLOBAL, global_dir, dirout

cd, global_dir, CURRENT=src 
list_dir = FILE_SEARCH (/MARK_DIRECTORY)
cd, src
print, list_dir

FOR jj=0, n_elements (list_dir)-1 DO BEGIN
  local_dir = global_dir+list_dir[jj]
  print, 'now extracting from ', local_dir, dirout
  extract_flux, local_dir
ENDFOR


END
