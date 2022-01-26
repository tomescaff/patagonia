load "../displaying/utils.ncl"
begin

  ;************************************************
  ; get data
  ;************************************************

  f1_annual     = addfile ("../data/sstsat_annual.nc", "r")
  f2_annual     = addfile ("../data/mb_largescalecorrs_annual.nc", "r")
  x_annual      = f1_annual->sstsat__corr(:,:)       
  y_annual      = f2_annual->msl__regress(:,:)

  f1_winter     = addfile ("../data/sstsat_annual.nc", "r")
  f2_winter     = addfile ("../data/mb_largescalecorrs_winter.nc", "r")
  x_winter      = f1_winter->sstsat__corr(:,:)       
  y_winter      = f2_winter->msl__regress(:,:)

  f1_summer     = addfile ("../data/sstsat_annual.nc", "r")
  f2_summer     = addfile ("../data/mb_largescalecorrs_summer.nc", "r")
  x_summer      = f1_summer->sstsat__corr(:,:)       
  y_summer      = f2_summer->msl__regress(:,:)

  ;************************************************
  ; define work station and colormap
  ;************************************************

  wks = gsn_open_wks("png","../data/png/three_panels.png")       ; send graphics to PNG file
  gsn_define_colormap(wks,"BlueWhiteOrangeRed")

  ;************************************************
  ; resource list for first data array
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

  res1@mpMinLatF = -90.			                 ; set the minimum latitude = -70.
  res1@mpMaxLatF = 30.			                 ; set the maximum latitude = 30.
  res1@mpCenterLonF = -120
  res1@mpMinLonF = -270.			             ; set the minimum latitude = -70.
  res1@mpMaxLonF = 0.			                 ; set the maximum latitude = 30.

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

  res1@gsnLeftString = "Vector Wind"

  
  ;************************************************
  ; resource list for second data array
  ;************************************************

  res2                      = True
  res2@cnLevelSelectionMode = "ManualLevels"    ; set manual contour levels
  res2@cnMinLevelValF       = -4.8              ; set min contour level
  res2@cnMaxLevelValF       =  4.8              ; set max contour level
  res2@cnLevelSpacingF      =  0.2              ; set contour spacing
  res2@cnLineLabelsOn       = True
  res2@gsnContourZeroLineThicknessF = 0 	    ; eliminates zero contour
  res2@gsnContourNegLineDashPattern = 0 	    ; sets negative contours to dash pattern 1
  res2@gsnDraw          = False                 ; don't draw yet
  res2@gsnFrame         = False                 ; don't advance frame yet
  res2@cnLineThicknessF = 2.8                   ; thicker lines
  res2@cnLineLabelsOn   = False                 ; no line labels
  res2@cnInfoLabelOn     = False                ; turn off info label

  ;************************************************
  ; create top plot
  ;************************************************

  plot1_annual = gsn_csm_contour_map(wks,x_annual,res1)
  plot2_annual = gsn_csm_contour(wks,y_annual,res2)
  plot2_annual = ColorNegDashZeroPosContour(plot2_annual,"blue","magenta","red")
  overlay(plot1_annual,plot2_annual)
  
  ;************************************************
  ; create center plot
  ;************************************************


  plot1_winter = gsn_csm_contour_map(wks,x_winter,res1)
  plot2_winter = gsn_csm_contour(wks,y_winter,res2)
  plot2_winter = ColorNegDashZeroPosContour(plot2_winter,"blue","magenta","red")
  overlay(plot1_winter,plot2_winter)

  ;************************************************
  ; create bottom plot
  ;************************************************

  plot1_summer = gsn_csm_contour_map(wks,x_summer,res1)
  plot2_summer = gsn_csm_contour(wks,y_summer,res2)
  plot2_summer = ColorNegDashZeroPosContour(plot2_summer,"blue","magenta","red")
  overlay(plot1_summer,plot2_summer)

  ;************************************************
  ; create panel
  ;************************************************

  plot = new(3,graphic)                          ; create a plot array
  plot(0) = plot1_annual
  plot(1) = plot1_winter
  plot(2) = plot1_summer

  resP                    = True                 ; modify the panel plot
  resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller
  resP@gsnPanelMainString = "A common title"     ; set main title
  resP@gsnPanelFigureStrings= (/"a)","b)","c)"/) ; add strings to panel
  resP@amJust   = "TopLeft"
  gsn_panel(wks,plot,(/3,1/),resP)               ; now draw as one plot	   
end 