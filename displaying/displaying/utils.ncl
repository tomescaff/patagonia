undef("ColorNegDashZeroPosContour")
function ColorNegDashZeroPosContour(plot:graphic,cneg:string,czero:string,\
                                    cpos:string) 

local cnlvls, cnlinepat, n, N, cncolor
begin

  cnlvls = get_cnLevels (plot)

  N = dimsizes(cnlvls)
  if (ismissing(N) .or. N.le.0) then
     print ("NegDashLineContour: dimsizes(cnlvls)="+N+" return (non-fatal)")
     return (plot)
  else 
     cnlvls = FixZeroContour (cnlvls, "NegDashLineContour")
  end if

  if (any(cnlvls.lt.0.)) then
     cnlinepat = new (dimsizes(cnlvls), integer) ; create array for line pats
     cnlinepat = 0                               ; default is solid (=0)
     cncolor = new (dimsizes(cnlvls), string)    ; create array for line colors
     cncolor = cpos                              ; default is black	  
     do p=0,dimsizes(cnlvls)-1
        if (cnlvls(p).lt.-1.e-05) then
          cnlinepat(p) = 9                       ; simple dash line pattern
	  cncolor(p)   = cneg
        end if
	if (cnlvls(p).ge.-1.e-05.and.cnlvls(p).le.1.e-05) then
	  cncolor(p) = czero
	end if
     end do
    
     ovrly_plot = GetOverlayPlot (plot, "contourPlotClass", 0)
     setvalues ovrly_plot
        "cnMonoLineDashPattern"  : False
        "cnLineDashPatterns"     : cnlinepat
        "cnMonoLineColor"        : False
        "cnLineColors"           : cncolor
     end setvalues
   end if                                ; any
   return (plot)
end
