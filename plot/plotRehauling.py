import ROOT
from PlotStyle import PlotStyle
from CMSStyle import CMS_lumi
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.fillRunDict import labelByTime, labelByFill, splitByMagneticField
 
ROOT.gROOT.SetBatch(False)
ROOT.gROOT.Reset()
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


#era_name = 'BC'
#INdir = '/afs/cern.ch/work/f/fbrivio/beamSpot/ReproSept2017/CMSSW_9_2_10/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/final_results/BS_plots/byIOV/'
#INdir = '/afs/cern.ch/work/f/fbrivio/beamSpot/ReproSept2017/CMSSW_9_2_10/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/final_results/BS_plots/byLS/'
#file = ROOT.TFile.Open(INdir+era_name+'/histos_BS_byIOV_Run2017'+era_name+'.root')
#file = ROOT.TFile.Open(INdir+era_name+'/histos_BS_byLS_Run2017'+era_name+'.root')

file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/2016/CMSSW_8_0_11/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/histos.root')

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
    (X         , 'beam spot x [cm]'         ,  0.075 , 0.095 ),
    #(Y         , 'beam spot y [cm]'         ,  0.050 , 0.120 ),
    (Y         , 'beam spot y [cm]'         ,  -0.040 , -0.028 ),
    (Z         , 'beam spot z [cm]'         , -6.    , 6.    ),
    (sigmaZ    , 'beam spot #sigma_{z} [cm]',  2.0   , 5.    ),
    (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.000 , 0.008 ),
    (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.000 , 0.008 ),
    (dxdz      , 'beam spot dx/dz [rad]'    , -4.e-4 , 4.e-4 ),
    (dydz      , 'beam spot dy/dz [rad]'    , -4.e-4 , 4.e-4 ),
]

def drawMyStyle(histo, options = '', title = '', byFill = True, byTime = False):
    
    #histo.SetLineColor(ROOT.kGray)
    histo.SetLineColor(920)
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
        labelByTime(histo)

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

    histo.SetMarkerSize(1.3)

    ROOT.TGaxis.SetMaxDigits(4)
    ROOT.TGaxis.SetExponentOffset(0.005, -0.05)
    ROOT.gPad.SetTicky()
    ROOT.gPad.Update()

def saveHisto(var):

    histo = var[0]

    histo0T, histo3p8T, histo2p8T, histoOther = splitByMagneticField(
        histo, 
        json    = True, 
        json3p8 = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY.txt',
        #json2p8 = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY_SpecialRun.txt',
        json2p8 = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY_2.8T.txt', # dummy
        json0 = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY_noBField.txt',
    )
    
    #histo0T   .SetMarkerColor(ROOT.kRed   + 1)
    #histo3p8T .SetMarkerColor(ROOT.kBlack    )
    #histo2p8T .SetMarkerColor(ROOT.kGreen + 1)
    histo0T   .SetMarkerColor(633)
    histo3p8T .SetMarkerColor(1  )
    histo2p8T .SetMarkerColor(417)
    
    cloneHisto0T    = histo0T   .Clone()
    cloneHisto3p8T  = histo3p8T .Clone()
    cloneHisto2p8T  = histo2p8T .Clone()

    cloneHisto0T   .SetMarkerSize(3.)
    cloneHisto3p8T .SetMarkerSize(3.)
    cloneHisto2p8T .SetMarkerSize(3.)
  
    #cloneHisto0T   .SetLineColor(ROOT.kGray + 2)
    #cloneHisto3p8T .SetLineColor(ROOT.kGray + 2)
    #cloneHisto2p8T .SetLineColor(ROOT.kGray + 2)
    cloneHisto0T   .SetLineColor(922)
    cloneHisto3p8T .SetLineColor(922)
    cloneHisto2p8T .SetLineColor(922)

    byFill = True
    byTime = False

    toplot = [hist for hist in [histo0T, histo3p8T, histo2p8T] if hist.GetEntries() > 0]
        
    for j, hist in enumerate(toplot):
        drawMyStyle(hist, options = 'SAME'*(j!=0), byFill = byFill, byTime = byTime)

    for hist in [histo0T, histo3p8T, histo2p8T, histoOther]:
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
    
    CMS_lumi(ROOT.gPad, 4, 0)
    ROOT.gPad.Update()
    
    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.75 )
    #leg.SetFillColor(ROOT.kWhite)
    #leg.SetLineColor(ROOT.kWhite)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    if histo3p8T .GetEntries()>0: leg.AddEntry(cloneHisto3p8T , 'B = 3.8 T' , 'EP')
    if histo0T   .GetEntries()>0: leg.AddEntry(cloneHisto0T   , 'B = 0 T'   , 'EP')
    if histo2p8T .GetEntries()>0: leg.AddEntry(cloneHisto2p8T , 'B = 2.8 T' , 'EP')
    #if histo2p8T .GetEntries()>0: leg.AddEntry(cloneHisto2p8T , 'SpecialRuns' , 'EP')
    if histoOther.GetEntries()>0: leg.AddEntry(histoOther     , 'magnet ramping', 'F')
    leg.Draw('SAME')

    ROOT.gPad.Print('BS_plot_full_by_fill_run2016B_%s.pdf' %histo.GetName())
    #ROOT.gPad.Print(INdir+era_name+'/NEW_BS_plot_byFill_byIOV_run2017'+era_name+'_%s.pdf' %histo.GetName())
    #ROOT.gPad.Print(INdir+era_name+'/BS_plot_byFill_byLS_run2017'+era_name+'_%s.pdf' %histo.GetName())

c1 = ROOT.TCanvas('', '', 3000, 1000)
for var in variables:
    saveHisto(var)


