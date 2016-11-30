import os
import ROOT
from RecoVertex.BeamSpotProducer.BeamspotTools.objects.Payload   import Payload
from RecoVertex.BeamSpotProducer.BeamspotTools.objects.BeamSpot  import *
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.fillRunDict import labelByTime, labelByFill
   
def drawMyStyle(histo, var, options = '', title = '', byFill = True, byTime = False):
    
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

    histo.SetMarkerColor(getattr(ROOT, options.split(' ')[0]))
    histo.SetLineColor  (getattr(ROOT, options.split(' ')[0]))
    histo.SetMarkerSize(0.5)
    histo.SetLineWidth(1)
    
    histo.SetTickLength(0, 'X')

    return histo
   
   
file_TXT = ['/afs/cern.ch/work/m/manzoni/public/september2016rereco/perIoV/2016Bv2/total_bs_2016Bv2_%d.txt' %i for i in range(1279)]
# file obtained by running the CondTools/BeamSpot package:
file_DB  = '/afs/cern.ch/user/f/fiorendi/public/reference_prompt_BeamSpotObjects_2016_LumiBased_v0_offline.txt'

variables = [
    ('X'         , 'beam spot x [cm]'         ,  0.050 , 0.080 ),
    ('Y'         , 'beam spot y [cm]'         ,  0.080 , 0.110 ),
    ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5   , 5.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.000 , 0.008 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.000 , 0.008 ),
    ('dxdz'      , 'beam spot dx/dz [rad]'    ,  0.000 , 4.e-4 ),
    ('dydz'      , 'beam spot dy/dz [rad]'    , -2.e-4 , 2.e-4 ),
]

myPL_TXT = Payload(file_TXT)
myPL_DB  = Payload(file_DB)    

histosTXT = []
histosDB  = []

for var in variables:
  histosTXT.append(myPL_TXT.plot(var[0]         , 0, 999999999999, dilated = 5, returnHisto = True, unitLengthIoV = True))
  histosDB .append(myPL_DB .plot(var[0]         , 0, 999999999999, dilated = 5, returnHisto = True))

ROOT.gROOT.SetBatch(True)
c1 = ROOT.TCanvas('', '', 3000, 1000)

for i, histos in enumerate(zip(histosTXT, histosDB)):
    histo1 = drawMyStyle(histos[0],  variables[i], options = 'kRed '  , byFill = True, byTime = False)
    histo2 = drawMyStyle(histos[1],  variables[i], options = 'kBlack ', byFill = True, byTime = False)
    
    histo1.Draw('')
    histo2.Draw('same')
    
    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.75 )
    leg.SetFillColor(ROOT.kWhite)
    leg.SetLineColor(ROOT.kWhite)
    if histo1 .GetEntries()>0: leg.AddEntry(histo1 , 'from txt' , 'EPL')
    if histo2 .GetEntries()>0: leg.AddEntry(histo2 , 'from DB'  , 'EPL')
    leg.Draw('same')
    
    ROOT.gPad.Update()
    ROOT.gPad.Print('BS_comparison_plot_' + histos[0].GetName() + '.pdf')

