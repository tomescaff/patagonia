begin

  ;************************************************
  ; get data
  ;************************************************

  f      = addfile ("../data/regional_latlon_reg_mb_annual.nc", "r")
  x      = f->tas_corrmap(:,:)    

  fglacier_npi = "../data/shapes/glims/NPI_shape.shp"
  fglacier_spi = "../data/shapes/glims/SPI_shape.shp"

  ;************************************************
  ; define work station and color map
  ;************************************************

  wks = gsn_open_wks("png","../data/png/regional_tas_corr.png")       ; send graphics to PNG file
  gsn_define_colormap(wks,"BlRe")

  ;************************************************
  ; resource list for data array
  ;************************************************

  res             = True

  res@gsnDraw     = False
  res@gsnFrame    = False

  res@gsnMaximize = True                        ; maximize plot in frame
  res@mpOutlineOn = True                        ; turn the map outline on
  res@cnLevelSelectionMode = "ExplicitLevels"   ; set explicit contour levels
  res@cnLevels    = (/ -0.7, -0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7/)   ; set levels
  res@cnFillOn    = True                        ; turn on color fill
  res@cnFillMode  = "AreaFill"   ; for faster draw
  res@cnLinesOn   = False                       ; turn off the contour lines
  res@cnFillColors = (/ 3,13,23,30,36,41,45,-1,59,63,68,74,81,91,96/)  ; set the colors to be used
  res@cnLineLabelsOn = False                    ; turn the line labels off

  res@mpProjection = "Mercator"
  res@mpLimitMode  = True
  res@mpMinLatF = -57.			                ; set the minimum latitude = -70.
  res@mpMaxLatF = -40.			                ; set the maximum latitude = 30.
  res@mpMinLonF = -90.			                ; set the minimum latitude = -70.
  res@mpMaxLonF = -60.			                ; set the maximum latitude = 30.
  res@mpCenterLonF = (res@mpMinLonF + res@mpMaxLonF) / 2.
  

  res@mpGridAndLimbOn        = True             ; turn on grid lines
  res@mpGridLineDashPattern  = 5                ; lat/lon lines dashed
  res@mpGridLatSpacingF      = 5.
  res@mpGridLonSpacingF      = 10.
  
  res@mpOutlineOn = True
  res@mpDataBaseVersion    = "HighRes"
  res@mpDataResolution = "Finest"
  
  res@gsnAddCyclic = False
  ;************************************************
  ; creating plot
  ;************************************************
  
  plot = gsn_csm_contour_map(wks, x, res)
  
  pres             = True
  pres@gsLineColor = "black"
  ;pres@gsFillIndex        = 4 
  pres@gsLineThicknessF = 6.0
  poly_npi = gsn_add_shapefile_polylines(wks, plot, fglacier_npi, pres)
  poly_spi = gsn_add_shapefile_polylines(wks, plot, fglacier_spi, pres)
  draw(plot)
  frame(wks)
end 