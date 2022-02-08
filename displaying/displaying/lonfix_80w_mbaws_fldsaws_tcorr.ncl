begin

  ;************************************************
  ; get data
  ;************************************************

  fa            = addfile ("../../processing/data/nc/lonfix_80w_mba_fldsa.nc", "r")
  fw            = addfile ("../../processing/data/nc/lonfix_80w_mbw_fldsw.nc", "r")
  fs            = addfile ("../../processing/data/nc/lonfix_80w_mbs_fldss.nc", "r")
  fandes        = addfile ("../data/nc/andes_outline.nc", "r")

  ; annual fields
  ua            = fa->u__regress(:,:)
  za            = fa->z__regress(:,:)
  ta            = fa->t__corr(:,:)
  
  ; winter fields
  uw            = fw->u__regress(:,:)
  zw            = fw->z__regress(:,:)
  tw            = fw->t__corr(:,:)
  
  ; summer fields
  us            = fs->u__regress(:,:)
  zs            = fs->z__regress(:,:)
  ts            = fs->t__corr(:,:)

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
  ; define work station
  ;************************************************

  wtype = "png"
  wks = gsn_open_wks(wtype, "../data/png/lonfix_80w_mbaws_fldsaws_tcorr.png")       ; send graphics to PNG file
  
  ;************************************************
  ; basic resource list for first data array - andes & pat icefields
  ;************************************************

  res_andes                  = True
  res_andes@gsnDraw          = False              ; don't draw yet
  res_andes@gsnFrame         = False              ; don't advance frame yet
  res_andes@gsnYRefLine      = 1000               ; create a reference line   
  res_andes@gsnBelowYRefLineColor = "sienna"

  res_pi                      = True
  res_pi@gsnDraw              = False             ; don't draw yet
  res_pi@gsnFrame             = False             ; don't advance frame yet
  res_pi@xyLineColors         = (/"blue"/)
  res_pi@xyLineThicknessF     = 5.0            

  ;***********************************************************
  ; basic resource list for left panels - line contours
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

  ;*************************************************************
  ; basic resource list for left panels - shaded contours
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

  ;************************************************
  ; create left plots
  ;************************************************
  
  ; top plot
  res2@gsnLeftString = "a) Title 1"
  plot11_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes)
  plot11_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi)
  plot11_cont = gsn_csm_contour(wks, ua, res1)
  plot11_cont = ColorNegDashZeroPosContour(plot11_cont,"red","magenta","green4") 
  plot11_latp = gsn_csm_pres_hgt(wks, ua, res2)
  overlay(plot11_latp, plot11_andes)
  overlay(plot11_latp, plot11_pi)
  overlay(plot11_latp, plot11_cont)

  ; center plot
  res2@gsnLeftString = "c) Title 3"
  plot21_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes)
  plot21_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi)
  plot21_cont = gsn_csm_contour(wks, uw, res1)
  plot21_cont = ColorNegDashZeroPosContour(plot21_cont,"red","magenta","green4") 
  plot21_latp = gsn_csm_pres_hgt(wks, uw, res2)
  overlay(plot21_latp, plot21_andes)
  overlay(plot21_latp, plot21_pi)
  overlay(plot21_latp, plot21_cont)

  ; bottom plot
  res2@gsnLeftString = "e) Title 5"
  plot31_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes)
  plot31_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi)
  plot31_cont = gsn_csm_contour(wks, us, res1)
  plot31_cont = ColorNegDashZeroPosContour(plot31_cont,"red","magenta","green4") 
  plot31_latp = gsn_csm_pres_hgt(wks, us, res2)
  overlay(plot31_latp, plot31_andes)
  overlay(plot31_latp, plot31_pi)
  overlay(plot31_latp, plot31_cont)

  ;************************************************
  ; basic resource list for second data array - andes & pat icefields
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
  ; basic resource list for second data array - line contours
  ;***********************************************************

  res3                  = True
  res3@gsnDraw          = False                    ; don't draw yet
  res3@gsnFrame         = False                    ; don't advance frame yet
  
  ; contour resources
  res3@cnLevelSelectionMode = "ManualLevels"       ; set manual contour levels
  res3@cnMinLevelValF       = -60                  ; set min contour level
  res3@cnMaxLevelValF       =  60                  ; set max contour level
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

  ;***********************************************************
  ; basic resource list for second data array - shaded contours
  ;***********************************************************

  res4                  = True
  res4@gsnDraw          = False                    ; don't draw yet
  res4@gsnFrame         = False                    ; don't advance frame yet
  res4@cnLevelSelectionMode = "ExplicitLevels"     ; set explicit contour levels
  res4@cnLevels    = (/ -0.7, -0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7/) ; set levels
  res4@cnFillOn    = True                          ; turn on color fill
  res4@cnLinesOn   = False                         ; turn off the contour lines
  res4@cnLineLabelsOn = False                      ; turn the line labels off
  res4@cnFillOpacityF = 0.6
  res4@cnFillPalette  = "BlueWhiteOrangeRed"                  ; set color map
  res4@lbBoxEndCapStyle = "TriangleBothEnds"
  res4@lbLabelFontHeightF = 0.015
  ;res4@lbLabelAngleF = 90
  res4@lbOrientation =   "vertical"               ; not available when using gsn_csm_pres_hgt
  ;res4@lbLabelBarOn        = False               ; turn off individual cb's
  
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
 
  res4@tiYAxisString = ""
  res4@tiYAxisFontHeightF = 0.020

  ;************************************************
  ; create right plots
  ;************************************************
  
  ; top plot
  res4@gsnLeftString = "b) Title 2"
  plot12_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes2)
  plot12_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi2)
  plot12_cont = gsn_csm_contour(wks, za, res3)
  plot12_latp = gsn_csm_pres_hgt(wks, ta, res4)
  overlay(plot12_latp, plot12_andes)
  overlay(plot12_latp, plot12_pi)
  overlay(plot12_latp, plot12_cont)

  ; center plot
  res4@gsnLeftString = "d) Title 4"
  plot22_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes2)
  plot22_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi2)
  plot22_cont = gsn_csm_contour(wks, zw, res3)
  plot22_latp = gsn_csm_pres_hgt(wks, tw, res4)
  overlay(plot22_latp, plot22_andes)
  overlay(plot22_latp, plot22_pi)
  overlay(plot22_latp, plot22_cont)

  ; top plot
  res4@gsnLeftString = "f) Title 6"
  ;res4@lbLabelBarOn        = True               ; turn on individual cb's
  plot32_andes = gsn_csm_xy(wks, andes_lat, andes_pres, res_andes2)
  plot32_pi = gsn_csm_xy(wks, pi_lat, pi_pres, res_pi2)
  plot32_cont = gsn_csm_contour(wks, zs, res3)
  plot32_latp = gsn_csm_pres_hgt(wks, ts, res4)
  overlay(plot32_latp, plot32_andes)
  overlay(plot32_latp, plot32_pi)
  overlay(plot32_latp, plot32_cont)


  ;************************************************
  ; create panel
  ;************************************************

  plot = new(6,graphic)                            ; create a plot array
  plot(0) = plot11_latp
  plot(2) = plot21_latp
  plot(4) = plot31_latp
  plot(1) = plot12_latp
  plot(3) = plot22_latp
  plot(5) = plot32_latp

  resP                    = True                   ; modify the panel plot
  gsn_panel(wks,plot,(/3,2/),resP)                 ; now draw as one plot	
  ;delete(wks)

  ;cmd = "convert -trim ../data/png/lonfix_80w_mba_fldsaws.png ../data/png/lonfix_80w_mba_fldsaws.png"
  ;system(cmd)   

end