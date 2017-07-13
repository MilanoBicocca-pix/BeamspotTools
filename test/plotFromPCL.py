import os
import ROOT
from RecoVertex.BeamSpotProducer.BeamspotTools.objects.Payload   import Payload
from RecoVertex.BeamSpotProducer.BeamspotTools.objects.BeamSpot  import *
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.fillRunDict import labelByTime, labelByFill
from utils.getFileList   import get_files
   
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetPadGridY(True)

   
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
    histo.SetMarkerSize(0.8)
    histo.SetLineWidth(1)
    
    histo.SetTickLength(0, 'X')

    return histo
   
# file obtained by running the CondTools/BeamSpot package:
# file_DB  = '/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_2_0/src/CondTools/BeamSpot/test/reference_prompt_BeamSpotObjects_PCL_byLumi_v0_prompt_2017B.txt'
file_DB  = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_2_0/src/CondTools/BeamSpot/test/reference_prompt_BeamSpotObjects_PCL_byLumi_v0_prompt_2017B.txt'             , prependPath=True)
file_DB += get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_2_0/src/CondTools/BeamSpot/test/reference_prompt_BeamSpotObjects_PCL_byLumi_v0_prompt_2017B_from298653.txt'  , prependPath=True)


variables = [
    ('X'         , 'beam spot x [cm]'         ,  0.078 , 0.094 ),
    ('Y'         , 'beam spot y [cm]'         , -0.046 ,-0.030 ),
    ('Z'         , 'beam spot z [cm]'         , -3.    , 2.5    ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5   , 5.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.000 , 0.007 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.000 , 0.007 ),
    ('dxdz'      , 'beam spot dx/dz [rad]'    ,  0.000 , 4.e-4 ),
    ('dydz'      , 'beam spot dy/dz [rad]'    , -2.e-4 , 2.e-4 ),
]

myPL_DB  = Payload(file_DB)    

histosDB  = []

for var in variables:
  histosDB .append(myPL_DB .plot(var[0]         , 297620, 999999, dilated = 5, returnHisto = True))

ROOT.gROOT.SetBatch(True)
c1 = ROOT.TCanvas('', '', 3000, 1000)

for i, histos in enumerate(zip(histosDB)):
    histo1 = drawMyStyle(histos[0],  variables[i], options = 'kBlack '  , byFill = True, byTime = False)
#     histo2 = drawMyStyle(histos[1],  variables[i], options = 'kBlack ', byFill = True, byTime = False)
    
    histo1.Draw('')
#     histo2.Draw('same')
    
    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.75 )
    leg.SetFillColor(ROOT.kWhite)
    leg.SetLineColor(ROOT.kWhite)
    if histo1 .GetEntries()>0: leg.AddEntry(histo1 , 'PCL' , 'EPL')
#     if histo2 .GetEntries()>0: leg.AddEntry(histo2 , 'from DB'  , 'EPL')
#     leg.Draw('same')
    
    ROOT.gPad.Update()
    ROOT.gPad.Print('PCL_2017B/afterTS/BS_PCL_' + histos[0].GetName() + '.pdf')

