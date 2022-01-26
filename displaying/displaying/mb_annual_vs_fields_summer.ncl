load "utils.ncl"
begin

  ;************************************************
  ; get data
  ;************************************************

  f1            = addfile ("../data/sstsat_summer.nc", "r")
  f             = addfile ("../data/mb_largescalecorrs_summer.nc", "r")
  
  sst           = f1->sstsat__corr(:,:)       
  mslp          = f->msl__regress(:,:)

  u850          = f->u850__corr(:,:)       
  u850_reg      = f->u850__regress(:,:)
  v850_reg      = f->v850__regress(:,:)

  olr           = f->olr__corr(:,:)       
  z300          = f->z300__regress(:,:)

  ;************************************************
  ; define work station and colormap
  ;************************************************

  wtype = "png"
  wks = gsn_open_wks(wtype, "../data/png/mb_annual_vs_fields_summer.png")       ; send graphics to PNG file
  gsn_define_colormap(wks, "BlueWhiteOrangeRed")

  ;************************************************
  ; basic resource list for first data array
  ;************************************************

  res1             = True
  res1@gsnMaximize = True                        ; maximize plot in frame
  res1@mpFillOn    = False                       ; turn map fill off
  res1@mpOutlineOn = True                        ; turn the map outline on
  res1@cnLevelSelectionMode = "ExplicitLevels"   ; set explicit contour levels
  res1@cnLevels    = (/ -0.7, -0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7/) ; set levels
  
  res1@cnFillOn    = True                        ; turn on color fill
  res1@cnLinesOn   = False                       ; turn off the contour lines
  res1@cnLineLabelsOn = False                    ; turn the line labels off

  res1@mpMinLatF = -90.			                     ; set the minimum latitude = -70.
  res1@mpMaxLatF = 30.			                     ; set the maximum latitude = 30.
  res1@mpCenterLonF = -120
  res1@mpMinLonF = -270.			                   ; set the minimum latitude = -70.
  res1@mpMaxLonF = 0.			                       ; set the maximum latitude = 30.

  res1@mpGridAndLimbOn        = True             ; turn on grid lines
  res1@mpGridLineDashPattern  = 12               ; lat/lon lines dashed
  res1@mpGridLatSpacingF      = 30
  res1@mpGridLonSpacingF      = 60
  res1@gsnDraw          = False                  ; don't draw yet
  res1@gsnFrame         = False                  ; don't advance frame yet

  res1@gsnMajorLatSpacing = 30                   ; change maj lat tm spacing
  res1@gsnMajorLonSpacing = 60                   ; change maj lon tm spacing

  res1@lbBoxEndCapStyle = "TriangleBothEnds"
  res1@lbLabelBarOn        = False               ; turn off individual cb's
  
  ;************************************************
  ; basic resource list for second data array
  ;************************************************

  res2                      = True
  res2@cnLevelSelectionMode = "ManualLevels"     ; set manual contour levels
  res2@cnMinLevelValF       = -4.8               ; set min contour level
  res2@cnMaxLevelValF       =  4.8               ; set max contour level
  res2@cnLevelSpacingF      =  0.2               ; set contour spacing
  res2@cnLineLabelsOn       = True
  res2@gsnContourZeroLineThicknessF = 0 	       ; eliminates zero contour
  res2@gsnContourNegLineDashPattern = 0 	       ; sets negative contours to dash pattern 1
  res2@gsnDraw          = False                  ; don't draw yet
  res2@gsnFrame         = False                  ; don't advance frame yet
  res2@cnLineThicknessF = 2.8                    ; thicker lines
  res2@cnInfoLabelOn     = False                 ; turn off info label
  res2@cnLineLabelPlacementMode = "constant"
  res2@cnLineLabelDensityF   = 1.5               ; increase the number of line labels/line
  res2@cnLineLabelInterval        = 1            ; default = 2
  res2@cnLineLabelFontHeightF   = 0.005  
  res2@cnInfoLabelFontHeightF   = 0.02   

  ;************************************************
  ; creating top plot
  ;************************************************

  res1@gsnLeftString = "a) SST/SAT (corr. in colors) & MSLP (reg. in contours)"
  plot1_a = gsn_csm_contour_map(wks, sst, res1)
  plot2_a = gsn_csm_contour(wks, mslp, res2)
  plot2_a = ColorNegDashZeroPosContour(plot2_a,"blue","magenta","red")
  overlay(plot1_a, plot2_a)

  ;************************************************
  ; creating center plot
  ;************************************************

  res1@gsnLeftString = "b) u850 (corr. in colors) & V850 (reg. in vectors)"
  vcres                         = True             ; plot mods desired
  vcres@gsnDraw                 = False            ; don't draw yet
  vcres@gsnFrame                = False            ; so we can draw time stamp
  vcres@vcRefAnnoOrthogonalPosF = -1.0             ; move ref vector up
  vcres@vcRefMagnitudeF         = 0.7              ; define vector ref mag
  vcres@vcRefLengthF            = 0.045            ; define length of vec ref
  vcres@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
  vcres@vcMinDistanceF          = 0.02
  plot1_b = gsn_csm_contour_map(wks, u850, res1)
  vector = gsn_csm_vector(wks, u850_reg, v850_reg, vcres)
  overlay(plot1_b,vector)

  ;************************************************
  ; creating bottom plot
  ;************************************************

  res1@gsnLeftString = "c) OLR (corr. in colors) & Z300 (reg. in contours)"
  res2@cnMinLevelValF       = -30                   ; set min contour level
  res2@cnMaxLevelValF       =  30                   ; set max contour level
  res2@cnLevelSpacingF      =  3                    ; set contour spacing
  plot1_c = gsn_csm_contour_map(wks, olr, res1)
  plot2_c = gsn_csm_contour(wks, z300, res2)
  plot2_c = ColorNegDashZeroPosContour(plot2_c,"blue","magenta","red")
  overlay(plot1_c,plot2_c)

  
  ;************************************************
  ; create panel
  ;************************************************

  plot = new(3,graphic)                          ; create a plot array
  plot(0) = plot1_a
  plot(1) = plot1_b
  plot(2) = plot1_c

  resP                    = True                 ; modify the panel plot
  resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller
  resP@gsnPanelYWhiteSpacePercent = 3
  gsn_panel(wks,plot,(/3,1/),resP)             ; now draw as one plot	
  delete(wks)

  cmd = "convert -trim ../data/png/mb_annual_vs_fields_summer.png ../data/png/mb_annual_vs_fields_summer.png"
  system(cmd)   
end 