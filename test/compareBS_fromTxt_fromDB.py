import os
import ROOT
from objects.Payload   import Payload
from objects.BeamSpot  import *
from utils.fillRunDict import labelByTime, labelByFill
from utils.getFileList import get_files
   
ROOT.gROOT.SetBatch(True)

   
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
   
   
#file_TXT = ['/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/IOVforPayloads/2017F/bs_ZB_2017_%d.txt' %i for i in range(1601)]
file_TXT = '/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_0_3_patch1/src/RecoVertex/BeamSpotProducer/python/BeamspotTools/test/pilotBeams2021_FEVT_LegacyBS_v1/pilotBeams2021_FEVT_LegacyBS_v1.txt'

# file obtained by running the CondTools/BeamSpot package:
#file_DB  = '/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/CondTools/BeamSpot/test/2017F_ReRecoNov.txt'
file_DB  = '/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_0_3_patch1/src/CondTools/BeamSpot/test/reference_2021_PilotBeams_LegacyBS_v2.txt'

#variables = [
#    ('X'         , 'beam spot x [cm]'         ,  0.075  , 0.095  ),
#    ('Y'         , 'beam spot y [cm]'         , -0.04   , -0.02  ),
#    ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
#    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5    , 5.    ),
#    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.E-3 , 4E-3 ),
#    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.E-3 , 4E-3 ),
#    ('dxdz'      , 'beam spot dx/dz [rad]'    , -.1e-3 , .8e-3 ),
#    ('dydz'      , 'beam spot dy/dz [rad]'    , -6.e-4 , .8e-3 ),
#]
## Ranges set for 2021 pilot beam test
variables = [
    ('X'         , 'beam spot x [cm]'         ,  0.15  , 0.19  ),
    ('Y'         , 'beam spot y [cm]'         , -0.21  ,-0.175 ),
    ('Z'         , 'beam spot z [cm]'         , -3.    , 3     ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  3.5   , 9.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.00  , 0.025 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.00  , 0.025 ),
    ('dxdz'      , 'beam spot dx/dz [rad]'    , -0.002 , 0.002 ),
    ('dydz'      , 'beam spot dy/dz [rad]'    , -0.002 , 0.002 ),
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
    
    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.7 )
    leg.SetFillColor(ROOT.kWhite)
    leg.SetLineColor(ROOT.kWhite)
    if histo1 .GetEntries()>0: leg.AddEntry(histo1 , 'from txt' , 'pel')
    if histo2 .GetEntries()>0: leg.AddEntry(histo2 , 'from DB'  , 'pel')
    leg.Draw('same')
    
    ROOT.gPad.Update()
    ROOT.gPad.Print('BS_txt_db_comparison/' + histos[0].GetName() + '.pdf')

