PRO EXTRACT_FLUX, dir, dirout

CD, dir, CURRENT=global 
list_siod = FILE_SEARCH ()

;print, list_siod
;print, n_elements (list_siod)
id = STRMID (dir, 9, 9, /reverse_offset)

ndata = n_elements (list_siod) 
flux = make_array (22, 24, ndata, /double)
stamps = make_array (22, 24, ndata, /double)

FOR ii=0, ndata-1 DO BEGIN
  IF ii MOD 100 EQ 0 THEN PRINT, ii, '/', ndata
  RESTORE, list_siod[ii]
  flux[*,*,ii] = datam.fluxlevel
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
datatype_idv = H5T_IDL_CREATE(flux)
dataspace_idv = H5S_CREATE_SIMPLE(size(flux,/DIMENSIONS))
;; create dataset in the output file
dataset_idv = H5D_CREATE(fid,$
'fluxlevel',datatype_idv,dataspace_idv)
;; write data to dataset
H5D_WRITE,dataset_idv,flux
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
