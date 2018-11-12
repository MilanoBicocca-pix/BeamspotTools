import sys
sys.path.append('..')
import ROOT
from PlotStyle import PlotStyle
from CMSStyle import CMS_lumi
from utils.fillRunDict import labelByTime, labelByFill, splitByMagneticField
 
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetPadLeftMargin(0.1)
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetMarkerSize(1.5)
ROOT.gStyle.SetHistLineWidth(1)
ROOT.gStyle.SetStatFontSize(0.025)
ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleSize(0.06, 'XYZ')
ROOT.gStyle.SetLabelSize(0.15, 'Y')
ROOT.gStyle.SetLabelSize(0.35, 'X')
ROOT.gStyle.SetNdivisions(510, 'YZ')
ROOT.gStyle.SetNdivisions(10, 'X')
# ROOT.gStyle.SetPadGridX(True)
ROOT.gStyle.SetPadGridY(True)
# ROOT.gStyle.SetGridWidth(1)
ROOT.gStyle.SetLegendFont(42)

# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/2016/CMSSW_8_0_11/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/histos.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/atlas_fills/histos_2018A_6638_byLS.root')
file = ROOT.TFile.Open('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/histos_VdM_319176_merge20.root')

file.cd()

X          = file.Get('X'         )
Y          = file.Get('Y'         )
Z          = file.Get('Z'         )
sigmaZ     = file.Get('sigmaZ'    )
beamWidthX = file.Get('beamWidthX')
beamWidthY = file.Get('beamWidthY')
dxdz       = file.Get('dxdz'      )
dydz       = file.Get('dydz'      )

variables = [
    (X         , 'beam spot x [cm]'         ,  0.09 , 0.104 ),
#     (X         , 'beam spot x [cm]'         ,  0.06 , 0.130  ),
    (Y         , 'beam spot y [cm]'         , -0.095  ,-0.025  ),
#     (Z         , 'beam spot z [cm]'         , -1.5    , 0.5      ),
    (Z         , 'beam spot z [cm]'         , -3.    , 3      ),
    (sigmaZ    , 'beam spot #sigma_{z} [cm]',  3.    , 6.5     ),
    (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.000 , 0.01  ),
    (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.000 , 0.01  ),
    (dxdz      , 'beam spot dx/dz [rad]'    ,  0.000 , 4.e-4  ),
    (dydz      , 'beam spot dy/dz [rad]'    , -2.e-4 , 2.e-4  ),
]

def drawMyStyle(histo, options = '', title = '', byFill = True, byTime = False):
    
    histo.SetLineColor(ROOT.kGray)
    histo.SetLineWidth(1)
#     histo.SetLineStyle(3)

    histo.GetYaxis().SetTitle(var[1])
    histo.GetXaxis().SetTitle('')
    histo.GetYaxis().SetRangeUser(var[2], var[3])

    if byFill:
        labelByFill(histo)
        histo.GetXaxis().SetTitle('Fill')
    
    if byTime:
        labelByFill(histo)
        labelByTime(histo, granularity = 4)

    histo.SetTitle('')
    histo.GetXaxis().SetTickLength(0.03)
    histo.GetYaxis().SetTickLength(0.01)
    histo.GetXaxis().SetTitleOffset(1.25)
    histo.GetYaxis().SetTitleOffset(0.6)
    histo.GetYaxis().SetTitleSize(0.06)
    histo.GetXaxis().SetTitleSize(0.06)
    histo.GetYaxis().SetLabelSize(0.04)
    histo.GetXaxis().SetLabelSize(0.06)
    histo.GetXaxis().SetNdivisions(10, True)

    histo.Draw(options)
  
    ROOT.TGaxis.SetMaxDigits(4)
    ROOT.TGaxis.SetExponentOffset(0.005, -0.05)
    ROOT.gPad.SetTicky()
    ROOT.gPad.Update()

def saveHisto(var):

    histo = var[0]

    histo3p8T, histoVdM, histo90m, histoAli, histoNb, histoOther = splitByMagneticField(
        histo, 
        json    = True, 
        json3p8 = 'json_DCSONLY.txt',
        jsonVdM = 'json_DCSONLY_VdM.txt',
        json90m = 'json_DCSONLY_90m.txt', 
        jsonAli = 'json_DCSONLY_VdmAlice.txt',
        jsonNb  = 'json_DCSONLY_SpecialNBunches.txt',
    )
    
    histoVdM   .SetMarkerColor(ROOT.kRed   + 1)
    histo3p8T .SetMarkerColor(ROOT.kBlack    )
    histo90m .SetMarkerColor(ROOT.kGreen + 1)

    cloneHistoVdM    = histoVdM   .Clone()
    cloneHisto3p8T  = histo3p8T .Clone()
    cloneHisto90m  = histo90m .Clone()

    cloneHistoVdM   .SetMarkerSize(3.)
    cloneHisto3p8T .SetMarkerSize(3.)
    cloneHisto90m .SetMarkerSize(3.)
  
    cloneHistoVdM .SetLineColor(ROOT.kGray + 2)
    cloneHisto3p8T.SetLineColor(ROOT.kGray + 2)
    cloneHisto90m .SetLineColor(ROOT.kGray + 2)
    

    histo3p8T .SetMarkerColor(1)
    histo3p8T .SetMarkerStyle(20)
    histo3p8T .SetMarkerSize(1.5)

    cloneHisto3p8T  = histo3p8T .Clone()
    
    byFill = True
    byTime = False

    print 'plotting...'
#     for hist in [histo3p8T]:  print hist.GetEntries() 
#     toplot = [hist for hist in [histo3p8T] if hist.GetEntries() > 0]
    toplot = [hist for hist in [histoVdM, histo3p8T, histo90m] if hist.GetEntries() > 0]
        
    for j, hist in enumerate(toplot):
        drawMyStyle(hist, options = 'SAME'*(j!=0), byFill = byFill, byTime = byTime)

    for hist in [histoVdM, histo3p8T, histo90m, histoOther]:
#     for hist in [histo3p8T]:
        hist.SetTickLength(0, 'X')
        hist.GetXaxis().SetTitle('LS')
    
    ROOT.gPad.Update()
    
    # SetNdivisions() does not work when bin labels are changed
    # thank you ROOT
    # https://root.cern.ch/phpBB3/viewtopic.php?t=6901
    f1 = ROOT.TF1('f1', 'x', 0, 16)
    labels = ROOT.TGaxis(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), 
                         ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), 
                         'f1', 520)
    labels.SetLabelSize(0)
    labels.Draw()

    
    CMS_lumi(ROOT.gPad, 5, 0)
    ROOT.gPad.Update()
    
    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.75 )
    leg.SetFillColor(10)
    leg.SetLineColor(10)
    if histo3p8T .GetEntries()>0: leg.AddEntry(cloneHisto3p8T , 'B = 3.8 T' , 'EP')


    ROOT.gPad.Print('BS_plot_specials_%s.pdf' %histo.GetName())

c1 = ROOT.TCanvas('c1', 'c1', 3000, 1000)
for var in variables:
    saveHisto(var)


