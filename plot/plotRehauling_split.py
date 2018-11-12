import sys
sys.path.append('..')
import ROOT
from PlotStyle import PlotStyle
from CMSStyle import CMS_lumi
from utils.fillRunDict import labelByTime, labelByFill, splitByMagneticField, splitByJson
 
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
file = ROOT.TFile.Open('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_2_0/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/results_SeptReReco_final/histos_2018B_SeptReReco_Specials.root')

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
    (X         , 'beam spot x [cm]'         ,  0.078 , 0.110  ),
    (Y         , 'beam spot y [cm]'         , -0.075  ,0.15 ),
#     (Y         , 'beam spot y [cm]'         , -0.075  ,-0.055 ),
#     (X         , 'beam spot x [cm]'         ,  0.06 , 0.130  ),
#     (Z         , 'beam spot z [cm]'         , -1.5    , 0.5      ),
    (Z         , 'beam spot z [cm]'         , -3.    , 3      ),
    (sigmaZ    , 'beam spot #sigma_{z} [cm]',  2.    , 7     ),
    (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.000 , 0.018  ),
    (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.000 , 0.018 ),
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

    histoList = splitByJson(
        histo, 
        ['json_DCSONLY.txt',
         'json_DCSONLY_VdM.txt',
         'json_DCSONLY_90m.txt', 
         'json_DCSONLY_VdmAlice.txt',
         'json_DCSONLY_SpecialNBunches.txt'
        ]
    )

    histo3p8T = histoList[0]
    histoVdM  = histoList[1]
    histo90m  = histoList[2]
    histoAli  = histoList[3]
    histoNb   = histoList[4]

    histoVdM   .SetMarkerColor(ROOT.kRed   + 1)
    histo3p8T  .SetMarkerColor(ROOT.kBlack    )
    histo90m   .SetMarkerColor(ROOT.kGreen + 1)
    histoAli   .SetMarkerColor(ROOT.kBlue  + 1)
    histoNb    .SetMarkerColor(ROOT.kOrange+ 1)

    cloneHistoVdM   = histoVdM  .Clone()
    cloneHisto3p8T  = histo3p8T .Clone()
    cloneHisto90m   = histo90m  .Clone()
    cloneHistoAli   = histoAli  .Clone()
    cloneHistoNb    = histoNb   .Clone()

    cloneHistoVdM  .SetMarkerSize(0.7) ; cloneHistoVdM  .SetMarkerStyle(20)
    cloneHisto3p8T .SetMarkerSize(0.7) ; cloneHisto3p8T .SetMarkerStyle(20)
    cloneHisto90m  .SetMarkerSize(0.7) ; cloneHisto90m  .SetMarkerStyle(20)
    cloneHistoAli  .SetMarkerSize(0.7) ; cloneHistoAli  .SetMarkerStyle(20)
    cloneHistoNb   .SetMarkerSize(0.7) ; cloneHistoNb   .SetMarkerStyle(20)
  
    cloneHistoVdM .SetLineColor(ROOT.kGray + 2)
    cloneHisto3p8T.SetLineColor(ROOT.kGray + 2)
    cloneHisto90m .SetLineColor(ROOT.kGray + 2)
    cloneHistoAli .SetLineColor(ROOT.kGray + 2)
    cloneHistoNb  .SetLineColor(ROOT.kGray + 2)

    
    byFill = True
    byTime = False

    print 'plotting...'
#     toplot = [hist for hist in [cloneHistoVdM, cloneHisto3p8T] if hist.GetEntries() > 0]
    toplot = [hist for hist in [cloneHistoVdM, cloneHisto3p8T, cloneHisto90m, cloneHistoAli, cloneHistoNb] if hist.GetEntries() > 0]
        
    for j, hist in enumerate(toplot):
        drawMyStyle(hist, options = 'SAME'*(j!=0), byFill = byFill, byTime = byTime)

#     for hist in [cloneHistoVdM, cloneHisto3p8T]:
    for hist in [cloneHistoVdM, cloneHisto3p8T, cloneHisto90m, cloneHistoAli, cloneHistoNb]:
        hist.SetTickLength(0, 'X')
        hist.GetXaxis().SetTitle('Fill')
    
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
    leg.SetTextSize(0.027)

    if cloneHisto3p8T .GetEntries()>0: leg.AddEntry(cloneHisto3p8T , 'Standard'               , 'EP')
#     if cloneHistoVdM  .GetEntries()>0: leg.AddEntry(cloneHistoVdM  , 'ZeroBias'               , 'EP')
    if cloneHistoVdM  .GetEntries()>0: leg.AddEntry(cloneHistoVdM  , 'VdM scan CMS'           , 'EP')
    if cloneHisto90m  .GetEntries()>0: leg.AddEntry(cloneHisto90m  , '90m #beta*'             , 'EP')
    if cloneHistoAli  .GetEntries()>0: leg.AddEntry(cloneHistoAli  , 'VdM ALICE/LHCb'         , 'EP')
    if cloneHistoNb   .GetEntries()>0: leg.AddEntry(cloneHistoNb   , 'Special # bunches'      , 'EP')
    leg.Draw()

    ROOT.gPad.Print('BS_Run2018B_SeptReReco_Specials_%s.pdf' %histo.GetName())

c1 = ROOT.TCanvas('c1', 'c1', 3000, 1000)
for var in variables:
    saveHisto(var)

