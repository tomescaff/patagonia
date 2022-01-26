load "utils.ncl"
begin

  ;************************************************
  ; get data
  ;************************************************

  f1     = addfile ("../data/sstsat_annual.nc", "r")
  f2     = addfile ("../data/mb_largescalecorrs_annual.nc", "r")
  x      = f1->sstsat__corr(:,:)       
  y      = f2->msl__regress(:,:) 

  ;************************************************
  ; define work station and colormap
  ;************************************************

  wks = gsn_open_wks("png","../data/png/annual_t2m_corr_mslp_reg.png")       ; send graphics to PNG file
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

  ; No margins around labelbar.
  res1@lbBottomMarginF      = 0.0
  res1@lbLeftMarginF        = 0.0
  res1@lbRightMarginF       = 0.0
  res1@lbTopMarginF         = 0.0

  ; Labelbar width
  res1@lbBoxMinorExtentF    = 0.2
  
  ;************************************************
  ; resource list for second data array
  ;************************************************

  res2                      = True
  res2@cnLevelSelectionMode = "ManualLevels"     ; set manual contour levels
  res2@cnMinLevelValF       = -4.8              ; set min contour level
  res2@cnMaxLevelValF       =  4.8              ; set max contour level
  res2@cnLevelSpacingF      =  0.2              ; set contour spacing
  res2@cnLineLabelsOn       = True
  res2@gsnContourZeroLineThicknessF = 0 	; eliminates zero contour
  res2@gsnContourNegLineDashPattern = 0 	; sets negative contours to dash pattern 1
  res2@gsnDraw          = False   ; don't draw yet
  res2@gsnFrame         = False   ; don't advance frame yet
  res2@cnLineThicknessF = 2.8                      ; thicker lines
  res2@cnLineLabelsOn   = False                    ; no line labels
  res2@cnInfoLabelOn     = False                ; turn off info label

  ;************************************************
  ; creating plot
  ;************************************************

  plot_1 = gsn_csm_contour_map(wks,x,res1)
  plot_2 = gsn_csm_contour(wks,y,res2)
  plot_2 = ColorNegDashZeroPosContour(plot_2,"blue","magenta","red")
  overlay(plot_1,plot_2)
  draw(plot_1)
  frame(wks)	   
end 