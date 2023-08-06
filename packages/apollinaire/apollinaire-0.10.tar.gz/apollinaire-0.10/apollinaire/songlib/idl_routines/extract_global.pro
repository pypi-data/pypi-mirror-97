PRO EXTRACT_GLOBAL, global_dir, dirout, parameter, keyword

; ARGUMENTS :
; global_dir : directory containing the directories with
; the .siod files (one directory per file).
; dirout : directory where to write the hdf5 files
; parameter : parameter to extract, see Solar-SONG
; .siod files documentation or do  
; IDL > tag_names (datam)  
; CAUTION : case-sensitive
; keyword : keyword to use in filenames that will be 
; written.
; EXAMPLE :
; IDL > dir = ***
; IDL > dirout = ***
; IDL > extract_global, global_dir, dirout, "FLUXLEVEL", "flux" 

cd, global_dir, CURRENT=src 
list_dir = FILE_SEARCH (/MARK_DIRECTORY)
cd, src
print, list_dir

FOR jj=0, n_elements (list_dir)-1 DO BEGIN
  local_dir = global_dir+list_dir[jj]
  print, 'now extracting from ', local_dir
  extract, local_dir, dirout, parameter, keyword
ENDFOR


END
