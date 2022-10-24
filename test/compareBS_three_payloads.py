import os
import ROOT
from   ROOT     import TH1F, TCanvas, TLegend, gPad, TGaxis
import sys
sys.path.append('..')
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort, splitByDrift, averageBeamSpot
from utils.getFileList   import get_files
from utils.readJson      import readJson
from utils.compareLists  import compareLists
from utils.fillRunDict   import labelByTime, labelByFill, splitByMagneticField

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadLeftMargin(0.1)
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleSize(0.06, 'XYZ')
ROOT.gStyle.SetNdivisions(510, 'YZ')
ROOT.gStyle.SetNdivisions(10, 'X')

ROOT.TGaxis.SetMaxDigits(4)
ROOT.TGaxis.SetExponentOffset(0.005, -0.05)

ROOT.gStyle.SetPadGridY(True)
ROOT.gStyle.SetLegendFont(42)

ROOT.gStyle.SetCanvasDefH(1500) #Height of canvas
ROOT.gStyle.SetCanvasDefW(6000) #Width of canvas

specialRuns = [300019,300029,300043,300050]

verbosePrinting = True
doFromScratch   = True

def _doMerge( bscollection, outfilename ):
  for irun, ibs in bscollection.items():
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 20)    
    else:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 1)    
    for p in pairs:
      myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
      bs_list = [ibs[i] for i in sorted(list(myrange))]
      aveBeamSpot = averageBeamSpot(bs_list)
      aveBeamSpot.Dump(outfilename, 'a+')

def _doSaveHistos( histolist, outfilename ):
  outfile = ROOT.TFile.Open(outfilename, 'recreate')
  outfile.cd()
  for histo in histolist:  
    histo.Write()
  outfile.Close()

## Plot fit results from txt file
## Ranges set for 2022 900 GeV commissioning
variables = [
    ('X'         , 'beam spot x [cm]'         ,  0.15  , 0.19  ),
    ('Y'         , 'beam spot y [cm]'         , -0.21  ,-0.17  ),
    ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  4.    , 10.   ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.    , 0.03  ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.    , 0.03  ),
    ('dxdz'      , 'beam spot dx/dz [rad]'    , -0.002 , 0.002 ),
    ('dydz'      , 'beam spot dy/dz [rad]'    , -0.002 , 0.002 ),
]

## Ranges set for 2022 13 TeV commissioning
#variables = [
#    ('X'         , 'beam spot x [cm]'         ,  0.15  , 0.19  ),
#    ('Y'         , 'beam spot y [cm]'         , -0.21  ,-0.17  ),
#    ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
#    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5   , 4.5   ),
#    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.    , 0.004 ),
#    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.    , 0.004 ),
#    ('dxdz'      , 'beam spot dx/dz [rad]'    , -0.002 , 0.002 ),
#    ('dydz'      , 'beam spot dy/dz [rad]'    , -0.002 , 0.002 ),
#]

variables = list(variables)

runstring = '' 

if doFromScratch:

  files_1 = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE.txt' , prependPath=True)
  files_1 += get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE_1.txt' , prependPath=True)
  
  files_2 = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576.txt' , prependPath=True)

  files_3 = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576.txt' , prependPath=True)

  print ('start loading payloads ...')
  payload_1 = Payload(files_1)
  payload_2 = Payload(files_2)
  payload_3 = Payload(files_3)
  print ('... payloads loaded')
  
  # convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
  bs_1 = payload_1.fromTextToBS() 
  bs_2 = payload_2.fromTextToBS() 
  bs_3 = payload_3.fromTextToBS() 
  
  # this returns a dictionary of runs and LS in the txt file, like {195660 : [1,2,3,...]}
  runsLumis1 = payload_1.getProcessedLumiSections() 
  runsLumis2 = payload_2.getProcessedLumiSections() 
  runsLumis3 = payload_3.getProcessedLumiSections() 
  runs1      = runsLumis1.keys()
  runs2      = runsLumis2.keys()
  runs3      = runsLumis3.keys()
  
  # filter for common runs 
  runsCommon = set(runs1) & set(runs2) & set(runs3)

  newBS1 = {k:v for k, v in bs_1.items() if k in runsCommon}
  newBS2 = {k:v for k, v in bs_2.items() if k in runsCommon}
  newBS3 = {k:v for k, v in bs_3.items() if k in runsCommon}

  # remove not-converged fits and sort
  print ('--- Job Report ---')
  for irun, ivalues in newBS1.items():
      n_all_fits_payload1 = len(newBS1[irun])
      newBS1[irun] = cleanAndSort(ivalues)
      n_ok_fits_payload1 = float (len(newBS1[irun]))
      if(n_all_fits_payload1 != 0): print ('fit failures in payload1 for run', irun, ':',  1. - n_ok_fits_payload1/n_all_fits_payload1)  

  for irun, ivalues in newBS2.items():
      n_all_fits_payload2 = len(newBS2[irun])
      newBS2[irun] = cleanAndSort(ivalues)
      n_ok_fits_payload2 = float (len(newBS2[irun]))
      if(n_all_fits_payload2 != 0): print ('fit failures in payload2 for run', irun, ':',  1. - n_ok_fits_payload2/n_all_fits_payload2)  

  for irun, ivalues in newBS3.items():
      n_all_fits_payload3 = len(newBS3[irun])
      newBS3[irun] = cleanAndSort(ivalues)
      n_ok_fits_payload3 = float (len(newBS3[irun]))
      if(n_all_fits_payload3 != 0): print ('fit failures in payload3 for run', irun, ':',  1. - n_ok_fits_payload3/n_all_fits_payload3)  

  # now check if the remaining BSs are there in both collections and delete sinlgetons
  runsLumisPayload1Cleaned = []
  runsLumisPayload2Cleaned = []
  runsLumisPayload3Cleaned = []
  
  for i, irun in enumerate(runsCommon):
    runsLumisPayload1Cleaned.append(newBS1[irun].keys())
    runsLumisPayload2Cleaned.append(newBS2[irun].keys())
    runsLumisPayload3Cleaned.append(newBS3[irun].keys())
    
    for ilumi in list(runsLumisPayload1Cleaned[i]):
      if (ilumi not in runsLumisPayload2Cleaned[i]) or (ilumi not in runsLumisPayload3Cleaned[i]):  del newBS1[irun][ilumi]
    for ilumi in list(runsLumisPayload2Cleaned[i]):
      if (ilumi not in runsLumisPayload1Cleaned[i]) or (ilumi not in runsLumisPayload3Cleaned[i]):  del newBS2[irun][ilumi]
    for ilumi in list(runsLumisPayload3Cleaned[i]):
      if (ilumi not in runsLumisPayload1Cleaned[i]) or (ilumi not in runsLumisPayload2Cleaned[i]):  del newBS3[irun][ilumi]
  
  # dump the list into a txt file, and save histos into root files
  BS1Name = 'BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/prompt_payloads' + runstring + '.txt'
  BS2Name = 'BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/ReRecoZB0_payloads' + runstring + '.txt'
  BS3Name = 'BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/ReRecoZB0-10_payloads' + runstring + '.txt'
  
  _doMerge(newBS1, BS1Name)
  _doMerge(newBS2, BS2Name)
  _doMerge(newBS3, BS3Name)
  
  merged_payload_1 = Payload(BS1Name)
  merged_payload_2 = Payload(BS2Name)
  merged_payload_3 = Payload(BS3Name)
  
  payload1_histos = []
  payload2_histos = []
  payload3_histos = []
  
  for ivar in variables: 
      payload1_histos.append(merged_payload_1.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 4, byFill = False, returnHisto = True))
      payload2_histos.append(merged_payload_2.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 4, byFill = False, returnHisto = True))
      payload3_histos.append(merged_payload_3.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 4, byFill = False, returnHisto = True))
  
  _doSaveHistos( payload1_histos, 'BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/histos_prompt' + runstring + '.root' )
  _doSaveHistos( payload2_histos, 'BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/histos_ReRecoZB0' + runstring + '.root')
  _doSaveHistos( payload3_histos, 'BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/histos_ReRecoZB0-10' + runstring + '.root')

histo_file_1 = ROOT.TFile.Open('BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/histos_prompt' + runstring + '.root', 'read')
histo_file_2 = ROOT.TFile.Open('BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/histos_ReRecoZB0' + runstring + '.root' , 'read')
histo_file_3 = ROOT.TFile.Open('BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/histos_ReRecoZB0-10' + runstring + '.root', 'read')

for ivar in variables: 
  print (ivar)

  can = ROOT.TCanvas('can','can')
  can.cd()

  h_p = histo_file_1.Get(ivar[0])

  h_p.SetMarkerSize(0.2)
  h_p.SetMarkerColor(1)
  h_p.SetLineColor(1)

  h_p.SetTitle('')
  h_p.SetTitleFont(42, 'XY')
  h_p.SetLabelFont(42, 'XY')
  h_p.GetXaxis().SetTickLength(0.03)
  h_p.GetYaxis().SetTickLength(0.01)
  h_p.GetXaxis().SetTitleOffset(1.25)
  h_p.GetYaxis().SetTitleOffset(0.7)
  h_p.GetYaxis().SetLabelSize(0.03)
  h_p.GetXaxis().SetLabelSize(0.04)
  h_p.GetXaxis().SetNdivisions(10, True)

  h_p.Draw('')

  h_p.GetYaxis().SetRangeUser(ivar[2], ivar[3])
  
  if runstring == '2017C' and 'Width' in ivar[0]:
    h_p.GetYaxis().SetRangeUser(ivar[2], 9E-3)

  h_r = histo_file_2.Get(ivar[0])
  h_r.SetMarkerSize(0.2)
  h_r.SetMarkerColor(2)
  h_r.SetLineColor(2)
  h_r.Draw('SAME')

  h_s = histo_file_3.Get(ivar[0])
  h_s.SetMarkerSize(0.2)
  h_s.SetMarkerColor(4)
  h_s.SetLineColor(4)
  h_s.Draw('SAME')

  leg = ROOT.TLegend( 0.902, 0.6, 1.0, 0.75 )
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.AddEntry(h_p, 'Prompt Fit', 'pel')
  leg.AddEntry(h_r, 'Fit ZB0', 'pel')
  leg.AddEntry(h_s, 'Fit ZB0-10', 'pel')
  leg.SetTextSize(0.03)
  leg.Draw('SAME')
  
  can.Update()
  can.Modified()
  can.SaveAs('BS_comparison_Prompt_ReRecoZB0_ReRecoZB0-10_2022A_mp3576/' + runstring + 'BS_' + ivar[0] + '_Prompt_ReReco_2022A' + '.pdf')

