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
file_DB  = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/CondTools/BeamSpot/test/reference_BeamSpotObjects_PCL_byRun_checkMatrix.txt'             , prependPath=True)
# file_DB  = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/CondTools/BeamSpot/test/reference_BeamSpotObjects_PCL_byLumi_v0_prompt_2018A.txt'  , prependPath=True)
# file_DB += get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_2/src/CondTools/BeamSpot/test/reference_BeamSpotObjects_PCL_byLumi_v0_prompt_2018B.txt'  , prependPath=True)

irun = 315252 ##317080
erun = 999999

variables = [
    ('X'         , 'beam spot x [cm]'         ,  0.09 , 0.104 ),
    ('Y'         , 'beam spot y [cm]'         , -0.07  ,-0.056  ),
    ('Z'         , 'beam spot z [cm]'         , -3.    , 3     ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.    , 5.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.000 , 0.0025 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.000 , 0.0025 ),
    ('dxdz'      , 'beam spot dx/dz [rad]'    , -1.e-4 , 3.e-4 ),
    ('dydz'      , 'beam spot dy/dz [rad]'    , -1.e-4 , 3.e-4 ),
]

myPL_DB  = Payload(file_DB)    

histosDB  = []

for var in variables:
  histosDB .append(myPL_DB .plot(var[0]         , irun, erun, dilated = 8, returnHisto = True))

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
    ROOT.gPad.Print('PCL_2018B/BS_PCL_' + histos[0].GetName() + '_2018AB_June29_checkMatrixChange.pdf')

