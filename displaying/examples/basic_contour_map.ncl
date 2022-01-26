begin

  ;************************************************
  ; get data
  ;************************************************

  f      = addfile ("../data/mb_largescalecorrs_annual.nc", "r")
  x      = f->u850__corr(:,:)      

  ;************************************************
  ; define work station and color map
  ;************************************************

  wks = gsn_open_wks("png","../data/png/u850_corr.png")       ; send graphics to PNG file
  gsn_define_colormap(wks,"BlRe")

  ;************************************************
  ; resource list for data array
  ;************************************************

  res             = True
  res@gsnMaximize = True                        ; maximize plot in frame
  res@mpFillOn    = False                       ; turn map fill off
  res@mpOutlineOn = True                        ; turn the map outline on
  res@cnLevelSelectionMode = "ExplicitLevels"   ; set explicit contour levels
  res@cnLevels    = (/ -0.7, -0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7/)   ; set levels
  res@cnFillOn    = True                        ; turn on color fill
  res@cnLinesOn   = False                       ; turn off the contour lines
  res@cnFillColors = (/ 3,13,23,30,36,41,45,-1,59,63,68,74,81,91,96/)  ; set the colors to be used
  res@cnLineLabelsOn = False                    ; turn the line labels off

  res@mpMinLatF = -90.			                ; set the minimum latitude = -70.
  res@mpMaxLatF = 30.			                ; set the maximum latitude = 30.
  res@mpCenterLonF = -120
  res@mpMinLonF = -270.			                ; set the minimum latitude = -70.
  res@mpMaxLonF = 0.			                ; set the maximum latitude = 30.

  res@mpGridAndLimbOn        = True             ; turn on grid lines
  res@mpGridLineDashPattern  = 5                ; lat/lon lines dashed
  res@mpGridLatSpacingF      = 30
  res@mpGridLonSpacingF      = 30
  
  ;************************************************
  ; creating plot
  ;************************************************

  plot = gsn_csm_contour_map(wks,x,res)    
end 