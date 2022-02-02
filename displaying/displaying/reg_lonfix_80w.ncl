begin

  ;************************************************
  ; get data
  ;************************************************

  f1            = addfile ("../data/nc/reg_lonfix_80w.nc", "r")
  f2            = addfile ("../data/nc/reg_lonfix_80w_temp.nc", "r")
  
  u           = f1->u_regress(:,:)
  z           = f1->z_regress(:,:)
  t           = f2->t_regress(:,:)

  lev         = f1->level
  lev@units   = "hPa"
  lat         = f1->lat

  u!0 = "lev"
  u!1 = "lat"
  u&lev = lev 
  u&lat = lat

  ;************************************************
  ; define work station
  ;************************************************

  wtype = "png"
  wks = gsn_open_wks(wtype, "../data/png/reg_lonfix_80w.png")       ; send graphics to PNG file

  ;************************************************
  ; basic resource list for first data array - line contours
  ;************************************************

  res1             = True
  res1@gsnDraw          = False                    ; don't draw yet
  res1@gsnFrame         = False                    ; don't advance frame yet
  ;res1@gsnMaximize = True
  
  ; contour resources
  res1@cnLevelSelectionMode = "ManualLevels"       ; set manual contour levels
  res1@cnMinLevelValF       = -4.8                 ; set min contour level
  res1@cnMaxLevelValF       =  4.8                 ; set max contour level
  res1@cnLevelSpacingF      =  0.3                 ; set contour spacing
  res1@cnLineLabelsOn       = True
  res1@gsnContourZeroLineThicknessF = 0 	       ; eliminates zero contour
  res1@gsnContourNegLineDashPattern = 0 	       ; sets negative contours to dash pattern 1
  
  ; contour display resources
  res1@cnLineThicknessF = 3.5                      ; thicker lines
  res1@cnInfoLabelOn     = False                   ; turn off info label
  res1@cnLineLabelPlacementMode = "Computed"
  res1@cnLineLabelInterval        = 1              ; default = 2
  res1@cnInfoLabelFontHeightF   = 0.03  
  ; res1@cnLineLabelBackgroundColor = -1

  ;************************************************
  ; basic resource list for first data array - shaded contours
  ;************************************************

  res2                  = True
  res2@gsnDraw          = False                    ; don't draw yet
  res2@gsnFrame         = False                    ; don't advance frame yet

  res2@cnLevelSelectionMode = "ExplicitLevels"    ; set explicit contour levels
  res2@cnLevels    = (/ -4.8, 0.0, 4.8/) ; set levels
  res2@cnFillOn    = True                         ; turn on color fill
  res2@cnLinesOn   = False                        ; turn off the contour lines
  res2@cnLineLabelsOn = False                     ; turn the line labels off
  res2@cnInfoLabelOn     = False                 ; turn off info label
  res2@cnFillPalette  = "MPL_Greys"                ; set color map
  res2@cnFillColors = (/ 4, 57, 2, 5/)
  res2@lbLabelBarOn        = False                 ; turn off individual cb's
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

;   res2@tmXMajorGrid      = True
;   res2@tmYMajorGrid      = True
;   res2@tmXMajorGridLineColor = "lightgray"
;   res2@tmYMajorGridLineColor = "lightgray"
;   res2@tmXMajorGridLineDashPattern = 2
;   res2@tmYMajorGridLineDashPattern = 2

  ;************************************************
  ; creating top plot
  ;************************************************

  plot1 = gsn_csm_contour(wks, u, res1)
  plot1 = ColorNegDashZeroPosContour(plot1,"red","magenta","green4") 
  plota = gsn_csm_pres_hgt(wks, u, res2)
  overlay(plota, plot1)
  
  ;************************************************
  ; create panel
  ;************************************************

  plot = new(6,graphic)                          ; create a plot array
  plot(0) = plota
  ;plot(1) = plot2
  ;plot(2) = plot1
  ;plot(3) = plot1
  ;plot(4) = plot1
  ;plot(5) = plot1

  resP                    = True                 ; modify the panel plot
;   resP@gsnPanelLabelBar    = True                ; add common colorbar
;   resP@lbLabelFontHeightF  = 0.007               ; make labels smaller
  resP@gsnPanelYWhiteSpacePercent = 3
  gsn_panel(wks,plot,(/3,2/),resP)             ; now draw as one plot	
  ;delete(wks)

  ;cmd = "convert -trim ../data/png/lg_mba_fldsa.png ../data/png/lg_mba_fldsa.png"
  ;system(cmd)   

  ;draw(plot1)
  ;frame(wks)

end