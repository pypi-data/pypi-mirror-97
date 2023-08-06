PRO EXTRACT, dir, dirout, parameter, keyword


; ARGUMENTS :
; dir : directory where to read the .siod files
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
; IDL > extract, dir, dirout, "FLUXLEVEL", "flux"


CD, dir, CURRENT=global 
list_siod = FILE_SEARCH ()

id = STRMID (dir, 9, 9, /reverse_offset)

ndata = n_elements (list_siod) 
param = make_array (22, 24, ndata, /double)
stamps = make_array (22, 24, ndata, /double)

RESTORE, list_siod[1]
a = tag_names (datam)
index = where (a EQ parameter)

FOR ii=0, ndata-1 DO BEGIN
  IF ii MOD 100 EQ 0 THEN PRINT, ii, '/', ndata
  RESTORE, list_siod[ii]
  param[*,*,ii] = datam.(index)
  stamps[*,*,ii] = datam.jd_mid
  DELVAR, datam, datas
ENDFOR

stamps = stamps [0,0,*]

CD, global

; save file as HDF5 file
; -------------------------------------------------------------
file = dirout + id + '_out.h5'
print, 'file saved at ', file
fid = H5F_CREATE (file)
datatype_idv = H5T_IDL_CREATE(param)
dataspace_idv = H5S_CREATE_SIMPLE(size(param,/DIMENSIONS))
;; create dataset in the output file
dataset_idv = H5D_CREATE(fid,$
keyword,datatype_idv,dataspace_idv)
;; write data to dataset
H5D_WRITE,dataset_idv,param
;; close all open identifiers
H5D_CLOSE,dataset_idv
H5S_CLOSE,dataspace_idv
H5T_CLOSE,datatype_idv

datatype_ids = H5T_IDL_CREATE(stamps)
dataspace_ids = H5S_CREATE_SIMPLE(size(stamps,/DIMENSIONS))
;; create dataset in the output file
dataset_ids = H5D_CREATE(fid,'stamps',datatype_ids,dataspace_ids)
;; write data to dataset
H5D_WRITE,dataset_ids,stamps
;; close all open identifiers
H5D_CLOSE,dataset_ids
H5S_CLOSE,dataspace_ids
H5T_CLOSE,datatype_ids

H5F_CLOSE,fid
; -------------------------------------------------------------


END
