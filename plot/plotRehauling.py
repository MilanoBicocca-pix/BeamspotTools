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
ROOT.gStyle.SetPadGridY(True)
ROOT.gStyle.SetLegendFont(42)

#file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/2016/CMSSW_8_0_11/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/histos.root')
#file = ROOT.TFile.Open('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/atlas_fills/histos_2018A_6638_byLS.root')
#file = ROOT.TFile.Open('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/forMCproduction/histos_2018A_from6688.root')
#file = ROOT.TFile.Open('/afs/cern.ch/work/f/fbrivio/beamSpot/2021/PilotBeam2021/CMSSW_10_6_29/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/BS_result_PiltBeam2021_byRun/histos_Express_PilotBeam2021.root')
#file = ROOT.TFile.Open('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_0_3_patch1/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/histos_PilotBeam2021_ExpressPhysics_FEVT.root')
file = ROOT.TFile.Open('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_0_3_patch1/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/pilotBeams2021_FEVT_LegacyBS_v1/pilotBeams2021_FEVT_LegacyBS_v1.root')

file.cd()

X          = file.Get('X'         )
Y          = file.Get('Y'         )
Z          = file.Get('Z'         )
sigmaZ     = file.Get('sigmaZ'    )
beamWidthX = file.Get('beamWidthX')
beamWidthY = file.Get('beamWidthY')
dxdz       = file.Get('dxdz'      )
dydz       = file.Get('dydz'      )

## Ranges set for 2021 pilot beam test
variables = [
    (X         , 'beam spot x [cm]'         ,  0.15  , 0.19  ),
    (Y         , 'beam spot y [cm]'         , -0.21  ,-0.175 ),
    (Z         , 'beam spot z [cm]'         , -3.    , 3     ),
    (sigmaZ    , 'beam spot #sigma_{z} [cm]',  3.5   , 9.    ),
    (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.00  , 0.025 ),
    (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.00  , 0.025 ),
    (dxdz      , 'beam spot dx/dz [rad]'    , -0.002 , 0.002 ),
    (dydz      , 'beam spot dy/dz [rad]'    , -0.002 , 0.002 ),
]

def drawMyStyle(histo, options = '', title = '', byFill = True, byTime = False):
    
    histo.SetLineColor(ROOT.kGray)
    histo.SetLineWidth(1)

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

    histo3p8T = histo.Clone()    
    histo3p8T = histo.Clone()    
    print ('n entries', histo3p8T.GetEntries())
    histo3p8T .SetMarkerColor(1)
    histo3p8T .SetMarkerStyle(20)
    histo3p8T .SetMarkerSize(1.5)

    cloneHisto3p8T  = histo3p8T .Clone()
    
    byFill = True
    byTime = False

    print ('plotting...')
    for hist in [histo3p8T]:  print (hist.GetEntries()) 
    toplot = [hist for hist in [histo3p8T] if hist.GetEntries() > 0]
#     toplot = [hist for hist in [histo0T, histo3p8T, histo2p8T] if hist.GetEntries() > 0]
        
    for j, hist in enumerate(toplot):
        drawMyStyle(hist, options = 'SAME'*(j!=0), byFill = byFill, byTime = byTime)

#     for hist in [histo0T, histo3p8T, histo2p8T, histoOther]:
    for hist in [histo3p8T]:
        hist.SetTickLength(0, 'X')
    
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

    ROOT.gPad.Print('BSFit_pilotBeams2021_FEVT_LegacyBS_v1/%s.pdf' %histo.GetName())

c1 = ROOT.TCanvas('c1', 'c1', 3000, 1000)
for var in variables:
    saveHisto(var)
