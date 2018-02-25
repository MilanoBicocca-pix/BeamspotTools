import os
import ROOT
from   ROOT     import TH1F, TCanvas, TLegend, gPad, TGaxis
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort, splitByDrift, averageBeamSpot
from utils.getFileList   import get_files
from utils.readJson      import readJson
from utils.compareLists  import compareLists
from utils.fillRunDict   import labelByTime, labelByFill, splitByMagneticField

ROOT.gROOT.SetBatch(True)
# ROOT.gROOT.Reset()
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
  for irun, ibs in bscollection.iteritems():
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True)    
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


# # Plot fit results from txt file
variables = [
    ('X'         , 'beam spot x [cm]'         ,  0.076  , 0.088  ),
    ('Y'         , 'beam spot y [cm]'         , -0.036  , -0.024  ),
    ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5    , 5.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.E-3 , 4E-3 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.E-3 , 4E-3 ),
    ('dxdz'      , 'beam spot dx/dz [rad]'    , -.1e-3 , .8e-3 ),
    ('dydz'      , 'beam spot dy/dz [rad]'    , -6.e-4 , .8e-3 ),
### for 2017C
#     ('X'         , 'beam spot x [cm]'         ,  0.05  , 0.12  ),
#     ('Y'         , 'beam spot y [cm]'         , -0.065 ,-0.005  ),
#     ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
#     ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5    , 5.5    ),
#     ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.2E-3 , 9E-3 ),
#     ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.2E-3 , 9E-3 ),
#     ('dxdz'      , 'beam spot dx/dz [rad]'    , -.1e-3 , .8e-3 ),
#     ('dydz'      , 'beam spot dy/dz [rad]'    , -6.e-4 , .8e-3 ),
]

variables = list(variables)


# variables = [
#   'X'         ,
#   'Y'         ,
#   'Z'         ,
#   'sigmaZ'    ,
#   'dxdz'      ,
#   'dydz'      ,
#   'beamWidthX',
#   'beamWidthY'
# ]

runstring = '2017H' 


if doFromScratch:

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v1_es0p9/171114_165107/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v2_es0p9/171113_141403/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v1_es0p9/171114_174952/0000//*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v2_es0p9/171114_175018/0000//*txt'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v3_es0p9/171114_175048/0000//*'           , prependPath=True)
#   r_files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias1/crab_BS_ReRecoNov17_VdM_Run2017C_es0p9/171115_085917/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017D_es0p9/171114_175116/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias8b4e1/crab_BS_ReRecoNov17_HighPU_Run2017D_es0p9/171115_085845/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_es0p9/171114_175143/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_es0p9/171114_175143/0001/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017F_es0p9_GTv2/171129_144416/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017F_es0p9_GTv2/171129_144416/0001/*'           , prependPath=True)

#   r_files = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017F_es1p1/180112_112626/0000/*.txt'           , prependPath=True)
#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017D_es0p9/171114_175116/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v1_es1p1/171110_150426/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v2_es1p1/171110_185941/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v1_es1p1/171110_215538/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v2_es1p1/171110_215641/0000/*.txt'       , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v3_es1p1/171110_215747/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017D_v1_es1p1/171110_215814/0000/*'           , prependPath=True)

#   r_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_v1_es1p1/171110_215859/0000/*'           , prependPath=True)
#   r_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_v1_es1p1/171110_215859/0001/*'           , prependPath=True)

#   r_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v1/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v1_missingLumis/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_missingLumis/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_SpecialRuns/*'           , prependPath=True)

#   r_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v1/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v1_missingLumis/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_missingLumis/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_SpecialRuns/*'           , prependPath=True)
  
  r_files = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/RecoVertex/BeamSpotProducer/test/split_2017H_96perc/*.txt'         , prependPath=True)
  
  
#   p_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v1_Prompt/*'        , prependPath=True)
#   p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_Prompt/*'        , prependPath=True)
#   p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_Prompt_SpecialRuns/*'        , prependPath=True)

#   p_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v1_Prompt/*'        , prependPath=True)
#   p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_Prompt/*'        , prependPath=True)
#   p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_Prompt_SpecialRuns/*'        , prependPath=True)
#   p_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_PromptNov17_Run2017C_v3/171112_165810/0000/*'        , prependPath=True)

#   p_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_PromptNov17_Run2017D/171112_165728/0000/*'        , prependPath=True)
#   p_files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias8b4e1/crab_BS_PromptNov17_HighPU_Run2017D_es1p1/171112_165429/0000/*'        , prependPath=True)

#   p_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_PromptNov17_Run2017E/171112_165645/0000/*'        , prependPath=True)
#   p_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_PromptNov17_Run2017E/171112_165645/0001/*'        , prependPath=True)

#   p_files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_Prompt_Run2017F/171129_224109/0000/*'        , prependPath=True)
#   p_files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_Prompt_Run2017F/171129_224109/0001/*'        , prependPath=True)

#   p_files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_Prompt_Run2017F_es1p1/171205_220828/0000/*.txt'         , prependPath=True)
  p_files = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/RecoVertex/BeamSpotProducer/test/split_2017H_prompt_96perc/*.txt'         , prependPath=True)

 
  print 'start loading payloads ...'
  promptPayload = Payload(p_files)
  recoPayload   = Payload(r_files)
  print '... payloads loaded'
  
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
      print 'Run ' + str(irun) + ': ' + s
  
  # remove from reco collection the LSs not in prompt file 
    for ls in LSinRecoNotInPrompt:
      try:
        if recoBS[irun][ls]:
          del recoBS[irun][ls]
      except:
        print irun, ls    
  
  # remove from prompt collection the LSs not in reco file 
    if len(LSinPromptNotInReco) > 0:  print 'missing in Rereco:'
    for ls in LSinPromptNotInReco:
      if promptBS[irun][ls]:
        print irun, ls        
        del promptBS[irun][ls]
  
  
  newPromptBS = {k:v for k, v in promptBS.iteritems() if k in runsCommon}
  newRecoBS   = {k:v for k, v in recoBS.iteritems()   if k in runsCommon}
  
  n_all_fits_prompt = len(newPromptBS)
  
  # remove not-converged fits and sort
  print '--- Job Report ---'
  for irun, ivalues in newPromptBS.iteritems():
      n_all_fits_prompt = len(newPromptBS[irun])
      newPromptBS[irun] = cleanAndSort(ivalues)
      n_ok_fits_prompt = float (len(newPromptBS[irun]))
      print 'fit failures in prompt for run', irun, ':',  1. - n_ok_fits_prompt/n_all_fits_prompt  
      
  for irun, ivalues in newRecoBS.iteritems():
      n_all_fits_reco   = len(newRecoBS[irun])
      newRecoBS[irun] = cleanAndSort(ivalues)
      n_ok_fits_reco   = float (len(newRecoBS[irun]))
      print 'fit failures in reco for run', irun, ':',   1. - n_ok_fits_reco/n_all_fits_reco  

#   print '--- Job Report ---'
#   print 'fit failures in prompt:', 1. - n_ok_fits_prompt/n_all_fits_prompt  
#   print 'fit failures in reco:',   1. - n_ok_fits_reco/n_all_fits_reco  
      
  # now check if the remaining BSs are there in both collections and delete sinlgetons
  runsLumisPromptCleaned = []
  runsLumisRecoCleaned   = []
  
  for i, irun in enumerate(runsCommon):
    runsLumisPromptCleaned.append( newPromptBS[irun].keys())
    runsLumisRecoCleaned  .append( newRecoBS[irun].keys())
    
    for ilumi in runsLumisRecoCleaned[i]:
      if ilumi not in runsLumisPromptCleaned[i]:  del newRecoBS[irun][ilumi]
    for ilumi in runsLumisPromptCleaned[i]:
      if ilumi not in runsLumisRecoCleaned[i]:  del newPromptBS[irun][ilumi]
  
  
  # dump the list into a txt file, and save histos into root files
  promptname = 'prompt_payloads' + runstring + '.txt'
  reconame   = 'reco_payloads' + runstring + '.txt'
  
  _doMerge(newPromptBS, promptname)
  _doMerge(newRecoBS  , reconame  )
  
 
  
  merged_payload_p = Payload(promptname)
  merged_payload_r = Payload(reconame)
  
  p_histos = []
  r_histos = []
  
  for ivar in variables: 
      p_histos.append(merged_payload_p.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 5, byFill = False, returnHisto = True))
      r_histos.append(merged_payload_r.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 5, byFill = False, returnHisto = True))
  
  _doSaveHistos( p_histos, 'histos_prompt' + runstring + '.root' )
  _doSaveHistos( r_histos, 'histos_reco' + runstring + '.root'   )
  
  

histo_file_p = ROOT.TFile.Open('histos_prompt' + runstring + '.root', 'read')
histo_file_r = ROOT.TFile.Open('histos_reco' + runstring + '.root'  , 'read')


for ivar in variables: 
  print ivar

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
  leg.AddEntry(h_p   , 'Prompt'   , 'pel')
  leg.AddEntry(h_r   , 'ReReco'    , 'pel')
  leg.SetTextSize(0.03)
  leg.Draw('SAME')
  
  can.Update()
  can.Modified()
  can.SaveAs('comparePromptReco_ZB_RunH/' + runstring + '/'+ivar[0] + '_Prompt_vs_NovReco_' + runstring + '.pdf')

