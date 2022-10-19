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

  r_files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE_by10LS.txt' , prependPath=True)
  #r_files += get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE_byLS_specialRuns.txt' , prependPath=True)
  #r_files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE.txt' , prependPath=True)
  #r_files += get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE_1.txt' , prependPath=True)
  #r_files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/ZeroBias/crab_Run2022B_ZeroBias_TkAlMinBias_ALCARECO_forReReco_mp3576_giusto/221006_134630/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
  #r_files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_154527/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
  #r_files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_154527/0001/BeamFit_LumiBased_*.txt' , prependPath=True)
  #r_files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022Dv1_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_121305/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
  #r_files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022Dv2_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_082248/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
  
  p_files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576.txt' , prependPath=True)
  #p_files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_Run*.txt' , prependPath=True)
  #p_files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_UpToFill_8076/220801_092708/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
  #p_files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_Fill_8078_8128/220829_074537/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
  #p_files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_Fill_8132_8151/220829_083733/0000/BeamFit_LumiBased_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)

  print ('start loading payloads ...')
  promptPayload = Payload(p_files)
  recoPayload   = Payload(r_files)
  print ('... payloads loaded')
  
  # convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
  promptBS = promptPayload.fromTextToBS() 
  recoBS   = recoPayload  .fromTextToBS() 
  
  # this returns a dictionary of runs and LS in the txt file, like {195660 : [1,2,3,...]}
  runsLumisPrompt = promptPayload.getProcessedLumiSections() 
  runsLumisReco   = recoPayload.getProcessedLumiSections() 
  runsPrompt      = runsLumisPrompt.keys()
  runsReco        = runsLumisReco.keys()
  
  # filter for common runs 
  runsCommon        = set(runsPrompt) & set(runsReco)
  inPromptNotInReco = set(runsPrompt) - set(runsReco)
  inRecoNotInPrompt = set(runsReco)   - set(runsPrompt)
  
  for irun in runsCommon:
    LSinPromptNotInReco, LSinRecoNotInPrompt = compareLists(runsLumisReco[irun], runsLumisPrompt[irun], 0, 'prompt', 'reco' )
    if verbosePrinting and len(LSinRecoNotInPrompt) > 0:
      s = ''
      for ls in LSinRecoNotInPrompt:
        s += str(ls) + ', '
      print ('Run ' + str(irun) + ': ' + s)
  
  # remove from reco collection the LSs not in prompt file 
    for ls in LSinRecoNotInPrompt:
      try:
        if recoBS[irun][ls]:
          del recoBS[irun][ls]
      except:
        print (irun, ls)    
  
  # remove from prompt collection the LSs not in reco file 
    if len(LSinPromptNotInReco) > 0:  print ('missing in Rereco:')
    for ls in LSinPromptNotInReco:
      if promptBS[irun][ls]:
        print (irun, ls)        
        del promptBS[irun][ls]
  
  
  newPromptBS = {k:v for k, v in promptBS.items() if k in runsCommon}
  newRecoBS   = {k:v for k, v in recoBS.items()   if k in runsCommon}
    
  # remove not-converged fits and sort
  print ('--- Job Report ---')
  for irun, ivalues in newPromptBS.items():
      n_all_fits_prompt = len(newPromptBS[irun])
      newPromptBS[irun] = cleanAndSort(ivalues)
      n_ok_fits_prompt = float (len(newPromptBS[irun]))
      if(n_all_fits_prompt != 0): print ('fit failures in prompt for run', irun, ':',  1. - n_ok_fits_prompt/n_all_fits_prompt)  
      
  for irun, ivalues in newRecoBS.items():
      n_all_fits_reco   = len(newRecoBS[irun])
      newRecoBS[irun] = cleanAndSort(ivalues)
      n_ok_fits_reco   = float (len(newRecoBS[irun]))
      if(n_all_fits_reco != 0): print ('fit failures in reco for run', irun, ':',   1. - n_ok_fits_reco/n_all_fits_reco)  

  # now check if the remaining BSs are there in both collections and delete sinlgetons
  runsLumisPromptCleaned = []
  runsLumisRecoCleaned   = []
  
  for i, irun in enumerate(runsCommon):
    runsLumisPromptCleaned.append( newPromptBS[irun].keys())
    runsLumisRecoCleaned  .append( newRecoBS[irun].keys())
    
    for ilumi in list(runsLumisRecoCleaned[i]):
      if ilumi not in runsLumisPromptCleaned[i]:  del newRecoBS[irun][ilumi]
    for ilumi in list(runsLumisPromptCleaned[i]):
      if ilumi not in runsLumisRecoCleaned[i]:  del newPromptBS[irun][ilumi]
  
  # dump the list into a txt file, and save histos into root files
  promptname = 'BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/prompt_payloads' + runstring + '.txt'
  reconame   = 'BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/reco_payloads' + runstring + '.txt'
  
  _doMerge(newPromptBS, promptname)
  _doMerge(newRecoBS  , reconame  )
  
  merged_payload_p = Payload(promptname)
  merged_payload_r = Payload(reconame)
  
  
  p_histos = []
  r_histos = []
  
  for ivar in variables: 
      p_histos.append(merged_payload_p.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 4, byFill = False, returnHisto = True))
      r_histos.append(merged_payload_r.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 4, byFill = False, returnHisto = True))
  
  _doSaveHistos( p_histos, 'BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/histos_prompt' + runstring + '.root' )
  _doSaveHistos( r_histos, 'BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/histos_reco' + runstring + '.root'   )

histo_file_p = ROOT.TFile.Open('BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/histos_prompt' + runstring + '.root', 'read')
histo_file_r = ROOT.TFile.Open('BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/histos_reco' + runstring + '.root'  , 'read')

for ivar in variables: 
  print (ivar)

  can = ROOT.TCanvas('can','can')
  can.cd()

  h_p = histo_file_p.Get(ivar[0])

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

  h_r = histo_file_r.Get(ivar[0])
  h_r.SetMarkerSize(0.2)
  h_r.SetMarkerColor(2)
  h_r.SetLineColor(2)
  h_r.Draw('SAME')

  leg = ROOT.TLegend( 0.902, 0.6, 1.0, 0.75 )
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.AddEntry(h_p, 'Prompt Fit', 'pel')
  leg.AddEntry(h_r, 'Fit For ReReco', 'pel')
  leg.SetTextSize(0.03)
  leg.Draw('SAME')
  
  can.Update()
  can.Modified()
  can.SaveAs('BS_comparison_Prompt_ReReco_2022A_mp3576_by10LS/' + runstring + 'BS_' + ivar[0] + '_Prompt_ReReco_2022A' + '.pdf')

