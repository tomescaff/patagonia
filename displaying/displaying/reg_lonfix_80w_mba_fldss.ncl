begin

  ;************************************************
  ; define work station
  ;************************************************

  wtype = "png"
  wks = gsn_open_wks(wtype, "../data/png/reg_lonfix_80w_mba_fldss.png")       ; send graphics to PNG file
  cmd = "convert -trim ../data/png/reg_lonfix_80w_mba_fldss.png ../data/png/reg_lonfix_80w_mba_fldss.png"
  ;************************************************
  ; get data
  ;************************************************

  f             = addfile ("../../processing/data/nc/lonfix_80w_mba_fldss.nc", "r")
  g             = addfile ("../data/nc/reg_mba_fldss.nc", "r")
  fandes        = addfile ("../data/nc/andes_outline.nc", "r")
  fglacier_npi  = "../data/shapes/glims/NPI_shape.shp"
  fglacier_spi  = "../data/shapes/glims/SPI_shape.shp"


  u            = f->u__regress(:,:)
  z            = f->z__regress(:,:)
  t            = f->t__regress(:,:)

  tas    = g->tas_corrmap(:,:) 
  uas    = g->uas_regmap(:,:)
  vas    = g->vas_regmap(:,:)
  pr     = g->pr_corrmap(:,:) 
  u700   = g->ua700_regmap(:,:)
  v700   = g->va700_regmap(:,:)

  ; topography - pressure conversion
  topo_hgt    = fandes->topo
  topo_pres   = 1000*exp(-topo_hgt/8000)
  topo_lat    = fandes->lat

  ; remove nans explicitly
  andes_lat   = topo_lat(3:478)
  andes_pres  = topo_pres(3:478)

  ; patagonian icefields outline [-51.5, -46.4]
  pi_lat  = topo_lat(52:110)
  pi_pres = topo_pres(52:110)


  ;************************************************
  ; lonfitude fixed 80w maps
  ;************************************************
  
  ;************************************************
  ; basic resource list for top right panel - andes & pat icefields
  ;************************************************

  res_andes                  = True
  res_andes@gsnDraw          = False               ; don't draw yet
  res_andes@gsnFrame         = False               ; don't advance frame yet
  res_andes@gsnYRefLine      = 1000                ; create a reference line   
  res_andes@gsnBelowYRefLineColor = "sienna"

  res_andes@vpWidthF = 0.71
  res_andes@vpHeightF = 0.61

  res_pi                      = True
  res_pi@gsnDraw              = False              ; don't draw yet
  res_pi@gsnFrame             = False              ; don't advance frame yet
  res_pi@xyLineColors         = (/"blue"/)
  res_pi@xyLineThicknessF     = 5.0 

  res_pi@vpWidthF = 0.71
  res_pi@vpHeightF = 0.61           

  ;***********************************************************
  ; basic resource list for top right panel - line contours
  ;***********************************************************

  res1                  = True
  res1@gsnDraw          = False                    ; don't draw yet
  res1@gsnFrame         = False                    ; don't advance frame yet
  
  ; contour resources
  res1@cnLevelSelectionMode = "ManualLevels"       ; set manual contour levels
  res1@cnMinLevelValF       = -4.8                 ; set min contour level
  res1@cnMaxLevelValF       =  4.8                 ; set max contour level
  res1@cnLevelSpacingF      =  0.3                 ; set contour spacing
  res1@cnLineLabelsOn       = True
  res1@gsnContourZeroLineThicknessF = 0 	       ; eliminates zero contour
  res1@gsnContourNegLineDashPattern = 0 	       ; sets negative contours to dash pattern 1
  
  ; contour display resources
  res1@cnLineThicknessF = 2.5                      ; thicker lines
  res1@cnInfoLabelOn     = False                   ; turn off info label
  res1@cnLineLabelPlacementMode = "randomized"
  res1@cnLineLabelInterval        = 1              ; default = 2
  res1@cnLineLabelFontHeightF   = 0.009  
  res1@cnLineLabelDensityF = 1.0

  res1@vpWidthF = 0.71
  res1@vpHeightF = 0.61

  ;*************************************************************
  ; basic resource list for top right panel - shaded contours
  ;*************************************************************

  res2                  = True
  res2@gsnDraw          = False                    ; don't draw yet
  res2@gsnFrame         = False                    ; don't advance frame yet

  res2@cnLevelSelectionMode = "ExplicitLevels"     ; set explicit contour levels
  res2@cnLevels    = (/ -4.8, 0.0, 4.8/)           ; set levels
  res2@cnFillOn    = True                          ; turn on color fill
  res2@cnLinesOn   = False                         ; turn off the contour lines
  res2@cnLineLabelsOn = False                      ; turn the line labels off
  res2@cnInfoLabelOn = False                       ; turn off info label
  res2@cnFillPalette  = "MPL_Greys"                ; set color map
  res2@cnFillColors = (/ 4, 70, 2, 5/)
  res2@lbLabelBarOn = False                        ; turn off individual cb's
  res2@cnFillOpacityF = 0.35

  ; axis resources
  res2@trXReverse = True                           ; reverse axis
  res2@trXMinF = -80                               ; set min lat
  res2@trXMaxF = -15                               ; set max lat

  res2@tmXBTickStartF = -80                        ; bottom X tick start
  res2@tmXBTickEndF = -15                          ; bottom X tick end
  res2@tmXBTickSpacingF = 10                       ; bottom X tick spacing

  res2@tmYROn = False                              ; turn off right Y tickmarks
  res2@tmXTOn = False                              ; turn off top X tickmarks
  res2@tmYRMode = "Automatic"                      ; turn off special labels on right axis
  res2@tmYLMode = "Explicit"                       ; explicit Y tickmarks
  res2@tmYLValues = ispan(100, 1000, 100)          ; tickmark values
  res2@tmYLLabels = "" + res2@tmYLValues           ; tickmark labels
 
  res2@tiYAxisString = "Pressure level (hPa)"
  res2@tiYAxisFontHeightF = 0.020
  res2@vpWidthF = 0.71
  res2@vpHeightF = 0.61

  ;************************************************
  ; create top right plot
  ;************************************************
  
  res2@gsnLeftString = "b) Zonal wind (reg. in contours) @ 80W"
  res2@gsnLeftStringFontHeightF = 0.022
  plot12_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes)
  plot12_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi)
  plot12_cont = gsn_csm_contour(wks, u, res1)
  plot12_cont = ColorNegDashZeroPosContour(plot12_cont,"black","black","black") 
  plot12_latp = gsn_csm_pres_hgt(wks, u, res2)
  overlay(plot12_latp, plot12_andes)
  overlay(plot12_latp, plot12_pi)
  overlay(plot12_latp, plot12_cont)

  ;************************************************
  ; basic resource list for bottom right panel - andes & pat icefields
  ;************************************************

  res_andes2                  = True
  res_andes2@gsnDraw          = False              ; don't draw yet
  res_andes2@gsnFrame         = False              ; don't advance frame yet
  res_andes2@gsnYRefLine           = 1000          ; create a reference line   
  res_andes2@gsnBelowYRefLineColor = "sienna"

  res_pi2                      = True
  res_pi2@gsnDraw              = False             ; don't draw yet
  res_pi2@gsnFrame             = False             ; don't advance frame yet
  res_pi2@xyLineColors         = (/"blue"/)
  res_pi2@xyLineThicknessF     = 5.0      

  ;***********************************************************
  ; basic resource list for bottom right panel - line contours
  ;***********************************************************

  res3                  = True
  res3@gsnDraw          = False                    ; don't draw yet
  res3@gsnFrame         = False                    ; don't advance frame yet
  
  ; contour resources
  res3@cnLevelSelectionMode = "ManualLevels"       ; set manual contour levels
  res3@cnMinLevelValF       = -20                  ; set min contour level
  res3@cnMaxLevelValF       =  20                  ; set max contour level
  res3@cnLevelSpacingF      =  2                   ; set contour spacing
  res3@cnLineLabelsOn       = True
  res3@gsnContourZeroLineThicknessF = 0 	       ; eliminates zero contour
  res3@gsnContourNegLineDashPattern = 1 	       ; sets negative contours to dash pattern 1

  ; contour display resources
  res3@cnLineThicknessF = 2.5                      ; thicker lines
  res3@cnInfoLabelOn     = False                   ; turn off info label
  res3@cnLineLabelPlacementMode = "randomized"
  res3@cnLineLabelInterval        = 1              ; default = 2
  res3@cnLineLabelFontHeightF   = 0.009  
  res3@cnLineLabelDensityF = 0.9 
  res3@vpWidthF = 0.71
  res3@vpHeightF = 0.61   

  ;***********************************************************
  ; basic resource list for bottom right panel - shaded contours
  ;***********************************************************

  res4                  = True
  res4@gsnDraw          = False                    ; don't draw yet
  res4@gsnFrame         = False                    ; don't advance frame yet
  res4@cnLevelSelectionMode = "ExplicitLevels"     ; set explicit contour levels
  res4@cnLevels    = (/ -0.42, -0.36,-0.30,-0.24,-0.18,-0.12,-0.06,0.06,0.12,0.18,0.24,0.30,0.36,0.42/) ; set levels
  res4@cnFillOn    = True                          ; turn on color fill
  res4@cnLinesOn   = False                         ; turn off the contour lines
  res4@cnLineLabelsOn = False                      ; turn the line labels off
  res4@cnFillOpacityF = 0.6
  res4@cnFillPalette  = "MPL_bwr"                  ; set color map
  res4@lbBoxEndCapStyle = "TriangleBothEnds"
  res4@lbLabelFontHeightF = 0.015
  res4@lbOrientation =   "vertical"                ; not available when using gsn_csm_pres_hgt
  res4@pmLabelBarWidthF      = 0.11                ; default is shorter
  
  ; axis resources
  res4@trXReverse = True                           ; reverse axis
  res4@trXMinF = -80                               ; set min lat
  res4@trXMaxF = -15                               ; set max lat

  res4@tmXBTickStartF = -80                        ; bottom X tick start
  res4@tmXBTickEndF = -15                          ; bottom X tick end
  res4@tmXBTickSpacingF = 10                       ; bottom X tick spacing

  res4@tmYROn = False                              ; turn off right Y tickmarks
  res4@tmXTOn = False                              ; turn off top X tickmarks
  res4@tmYRMode = "Automatic"                      ; turn off special labels on right axis
  res4@tmYLMode = "Explicit"                       ; explicit Y tickmarks
  res4@tmYLValues = ispan(100, 1000, 100)          ; tickmark values
  res4@tmYLLabels = "" + res4@tmYLValues           ; tickmark labels
 
  res4@tiYAxisString = "Pressure level (hPa)"
  res4@tiYAxisFontHeightF = 0.020
  res4@vpWidthF = 0.71
  res4@vpHeightF = 0.61

  ;************************************************
  ; create bottom right plot
  ;************************************************
  
  ; top plot
  res4@gsnLeftString = "d) T (reg. in colors) & Z (reg. in contours) @ 80W"
  res4@gsnLeftStringFontHeightF = 0.022
  plot22_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes2)
  plot22_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi2)
  plot22_cont = gsn_csm_contour(wks, z, res3)
  plot22_latp = gsn_csm_pres_hgt(wks, t, res4)
  overlay(plot22_latp, plot22_andes)
  overlay(plot22_latp, plot22_pi)
  overlay(plot22_latp, plot22_cont)

  ;************************************************
  ; regional lat lon maps
  ;************************************************
  
  ;************************************************
  ; basic resource list for left plots
  ;************************************************

  res5             = True
  res5@gsnMaximize = True                          ; maximize plot in frame
  res5@mpOutlineOn = True                          ; turn the map outline on
  res5@cnLevelSelectionMode = "ExplicitLevels"     ; set explicit contour levels
  res5@cnLevels    = (/ -0.7, -0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7/) ; set levels
 
  res5@cnFillOn    = True                          ; turn on color fill
  res5@cnLinesOn   = False                         ; turn off the contour lines
  res5@cnLineLabelsOn = False                      ; turn the line labels off
  res5@cnFillPalette  = "MPL_BrBG"                 ; set color map
  res5@mpProjection = "Mercator"
  res5@mpLimitMode  = True
  res5@mpMinLatF = -57.			                   ; set the minimum latitude = -70.
  res5@mpMaxLatF = -40.			                   ; set the maximum latitude = 30.
  res5@mpMinLonF = -90.			                   ; set the minimum latitude = -70.
  res5@mpMaxLonF = -60.			                   ; set the maximum latitude = 30.
  res5@mpCenterLonF = (res5@mpMinLonF + res5@mpMaxLonF) / 2.
  
  res5@pmTickMarkDisplayMode = "Always" 
  res5@mpGridAndLimbOn        = True               ; turn on grid lines
  res5@mpGridLineDashPattern  = 12                 ; lat/lon lines dashed
  res5@mpGridLatSpacingF      = 4
  res5@mpGridLonSpacingF      = 5
 
  res5@gsnDraw          = False                    ; don't draw yet
  res5@gsnFrame         = False                    ; don't advance frame yet
  
  res5@mpOutlineOn = True
  res5@mpDataBaseVersion    = "HighRes"
  res5@mpDataResolution = "Finest"
  res5@gsnAddCyclic = False
 
  res5@lbBoxEndCapStyle = "TriangleBothEnds"
  res5@lbLabelBarOn        = True                  ; turn off individual cb's
  res5@lbOrientation =   "vertical"                ; vertical label bar
  res5@pmLabelBarWidthF      = 0.1                 ; default is shorter
  res5@vpWidthF = 0.6
  res5@vpHeightF = 0.6

  ;************************************************
  ; basic resource list for vector map
  ;************************************************

  vcres                         = True             ; plot mods desired
  vcres@gsnDraw                 = False            ; don't draw yet
  vcres@gsnFrame                = False            ; so we can draw time stamp
  vcres@vcRefAnnoOrthogonalPosF = -1.084           ; move ref vector up
  vcres@vcRefMagnitudeF         = 0.8              ; define vector ref mag
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
  ; creating left top plot
  ;************************************************
  
  res5@gsnLeftString = "a) Precip (corr. in colors) & V700 (reg. in vectors)"
  res5@gsnLeftStringFontHeightF = 0.0185
  plot11 = gsn_csm_contour_map(wks, pr, res5)
  poly_npi_11 = gsn_add_shapefile_polylines(wks, plot11, fglacier_npi, pres)
  poly_spi_11 = gsn_add_shapefile_polylines(wks, plot11, fglacier_spi, pres)
  
  plot11_vec = gsn_csm_vector(wks, u700, v700, vcres)
  overlay(plot11, plot11_vec)
  
  ;************************************************
  ; creating left bottom plot
  ;************************************************
  
  res5@cnFillPalette  = "BlueWhiteOrangeRed"       ; set color map
  res5@gsnLeftString = "c) SAT (corr. in colors) & V10m (reg. in vectors)"
  res5@gsnLeftStringFontHeightF = 0.0185
  vcres@vcRefMagnitudeF         = 0.5
  plot21 = gsn_csm_contour_map(wks, tas, res5)
  poly_npi_21 = gsn_add_shapefile_polylines(wks, plot21, fglacier_npi, pres)
  poly_spi_21 = gsn_add_shapefile_polylines(wks, plot21, fglacier_spi, pres)

  plot21_vec = gsn_csm_vector(wks, uas, vas, vcres)
  overlay(plot21, plot21_vec)


  ;************************************************
  ; create panel
  ;************************************************

  plot = new(4,graphic)                            ; create a plot array
  plot(0) = plot11
  plot(1) = plot12_latp
  plot(2) = plot21
  plot(3) = plot22_latp
  
  resP = True                                      ; modify the panel plot
  resP@gsnPanelYWhiteSpacePercent = 5	
  resP@gsnPanelXWhiteSpacePercent = 7.5
  gsn_panel(wks,plot,(/2,2/),resP)                 ; now draw as one plot
  
  delete(wks)
  system(cmd)   

end