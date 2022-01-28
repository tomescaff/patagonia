load "utils.ncl"
begin

  ;************************************************
  ; get data
  ;************************************************

  f      = addfile ("../data/nc/reg_mba_fldss.nc", "r")
  tas    = f->tas_corrmap(:,:) 
  uas    = f->uas_regmap(:,:)
  vas    = f->vas_regmap(:,:)
  pr     = f->pr_corrmap(:,:) 
  u700   = f->ua700_regmap(:,:)
  v700   = f->va700_regmap(:,:)

  fglacier_npi = "../data/shapes/glims/NPI_shape.shp"
  fglacier_spi = "../data/shapes/glims/SPI_shape.shp"

  ;************************************************
  ; define work station and colormap
  ;************************************************

  wtype = "png"
  wks = gsn_open_wks(wtype, "../data/png/reg_mba_fldss.png")       ; send graphics to PNG file
  
  ;************************************************
  ; basic resource list for first data array
  ;************************************************

  res1             = True
  res1@gsnMaximize = True                         ; maximize plot in frame
  res1@mpOutlineOn = True                         ; turn the map outline on
  res1@cnLevelSelectionMode = "ExplicitLevels"    ; set explicit contour levels
  res1@cnLevels    = (/ -0.7, -0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7/) ; set levels
 
  res1@cnFillOn    = True                         ; turn on color fill
  res1@cnLinesOn   = False                        ; turn off the contour lines
  res1@cnLineLabelsOn = False                     ; turn the line labels off
  res1@cnFillPalette  = "MPL_BrBG"                ; set color map
  res1@mpProjection = "Mercator"
  res1@mpLimitMode  = True
  res1@mpMinLatF = -57.			                      ; set the minimum latitude = -70.
  res1@mpMaxLatF = -40.			                      ; set the maximum latitude = 30.
  res1@mpMinLonF = -90.			                      ; set the minimum latitude = -70.
  res1@mpMaxLonF = -60.			                      ; set the maximum latitude = 30.
  res1@mpCenterLonF = (res1@mpMinLonF + res1@mpMaxLonF) / 2.
  
  res1@pmTickMarkDisplayMode = "Always" 
  res1@mpGridAndLimbOn        = True              ; turn on grid lines
  res1@mpGridLineDashPattern  = 12                ; lat/lon lines dashed
  res1@mpGridLatSpacingF      = 4
  res1@mpGridLonSpacingF      = 5
 
  res1@gsnDraw          = False                   ; don't draw yet
  res1@gsnFrame         = False                   ; don't advance frame yet
  
  res1@mpOutlineOn = True
  res1@mpDataBaseVersion    = "HighRes"
  res1@mpDataResolution = "Finest"
  res1@gsnAddCyclic = False
 
  res1@lbBoxEndCapStyle = "TriangleBothEnds"
  res1@lbLabelBarOn        = True                 ; turn off individual cb's
  res1@lbOrientation =   "vertical"               ; vertical label bar

  ;************************************************
  ; basic resource list for vector map
  ;************************************************

  vcres                         = True             ; plot mods desired
  vcres@gsnDraw                 = False            ; don't draw yet
  vcres@gsnFrame                = False            ; so we can draw time stamp
  vcres@vcRefAnnoOrthogonalPosF = -1.084           ; move ref vector up
  vcres@vcRefMagnitudeF         = .8               ; define vector ref mag
  vcres@vcRefLengthF            = 0.03             ; define length of vec ref
  vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
  vcres@vcMinDistanceF          = 0.025

  ;************************************************
  ; basic resource list for icefields' shapes
  ;************************************************

  pres             = True
  pres@gsLineColor = "black"
  pres@gsLineThicknessF = 6.0

  ;************************************************
  ; creating top plot
  ;************************************************

  res1@gsnLeftString = "a) PRECIP (corr. in colors) & V700 (reg. in vectors)"
  plot1_a = gsn_csm_contour_map(wks, pr, res1)
  poly_npi_a = gsn_add_shapefile_polylines(wks, plot1_a, fglacier_npi, pres)
  poly_spi_a = gsn_add_shapefile_polylines(wks, plot1_a, fglacier_spi, pres)

  plot2_a = gsn_csm_vector(wks, u700, v700, vcres)
  overlay(plot1_a, plot2_a)

  ;************************************************
  ; creating bottom plot
  ;************************************************
  
  res1@cnFillPalette  = "BlueWhiteOrangeRed"          ; set color map
  res1@gsnLeftString = "b) SAT (corr. in colors) & V2m (reg. in vectors)"
  vcres@vcRefMagnitudeF         = 0.5
  plot1_b = gsn_csm_contour_map(wks, tas, res1)
  poly_npi_b = gsn_add_shapefile_polylines(wks, plot1_b, fglacier_npi, pres)
  poly_spi_b = gsn_add_shapefile_polylines(wks, plot1_b, fglacier_spi, pres)

  plot2_b = gsn_csm_vector(wks, uas, vas, vcres)
  overlay(plot1_b, plot2_b)

  ;************************************************
  ; create panel
  ;************************************************

  plot = new(2,graphic)                          ; create a plot array
  plot(0) = plot1_a
  plot(1) = plot1_b
  
  resP                    = True                 ; modify the panel plot
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller
  resP@gsnPanelYWhiteSpacePercent = 3
  gsn_panel(wks,plot,(/2,1/),resP)               ; now draw as one plot	
  delete(wks)

  cmd = "convert -trim ../data/png/reg_mba_fldss.png ../data/png/reg_mba_fldss.png"
  system(cmd)   
end 