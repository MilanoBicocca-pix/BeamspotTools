import os
import ROOT
from   ROOT     import TH1F, TCanvas, TLegend, gPad, TGaxis
from RecoVertex.BeamSpotProducer.BeamspotTools.objects.Payload     import Payload
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.beamSpotMerge import cleanAndSort, splitByDrift, averageBeamSpot
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.getFileList   import get_files
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.readJson      import readJson
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.compareLists  import compareLists
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.fillRunDict   import labelByTime, labelByFill, splitByMagneticField

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


verbosePrinting = True
doFromScratch   = True


def _doMerge( bscollection, outfilename ):
  for irun, ibs in bscollection.iteritems():
    pairs = splitByDrift(ibs, slopes = True)    
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
    ('X'         , 'beam spot x [cm]'         ,  0.08  , 0.092  ),
    ('Y'         , 'beam spot y [cm]'         , -0.04   , -0.031  ),
    ('Z'         , 'beam spot z [cm]'         , -6.    , 6.    ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  2.5    , 5.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.2E-3 , 4E-3 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.2E-3 , 4E-3 ),
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

runstring = '2017B' 
if doFromScratch:
  r_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v1/*'           , prependPath=True)
  r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v1_missingLumis/*'           , prependPath=True)
  r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2/*'           , prependPath=True)
  r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_missingLumis/*'           , prependPath=True)
  r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_SpecialRuns/*'           , prependPath=True)

#   r_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v1/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v1_missingLumis/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_missingLumis/*'           , prependPath=True)
#   r_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_SpecialRuns/*'           , prependPath=True)
  
  p_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v1_Prompt/*'        , prependPath=True)
  p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_Prompt/*'        , prependPath=True)
  p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017B_v2_Prompt_SpecialRuns/*'        , prependPath=True)
#   p_files  = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v1_Prompt/*'        , prependPath=True)
#   p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_Prompt/*'        , prependPath=True)
#   p_files += get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/SeptRepro2017/crab_BS_ReproSept2017_Run2017C_v2_Prompt_SpecialRuns/*'        , prependPath=True)
 
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
#     import pdb; pdb.set_trace()
    for ls in LSinRecoNotInPrompt:
      try:
        if recoBS[irun][ls]:
          del recoBS[irun][ls]
      except:
        print irun, ls    
  
  # remove from prompt collection the LSs not in reco file 
    for ls in LSinPromptNotInReco:
      if promptBS[irun][ls]:
        del promptBS[irun][ls]
  
  
  newPromptBS = {k:v for k, v in promptBS.iteritems() if k in runsCommon}
  newRecoBS   = {k:v for k, v in recoBS.iteritems()   if k in runsCommon}
  
  # remove not-converged fits and sort
  for irun, ivalues in newPromptBS.iteritems():
      newPromptBS[irun] = cleanAndSort(ivalues)
  for irun, ivalues in newRecoBS.iteritems():
      newRecoBS[irun] = cleanAndSort(ivalues)
      
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
      p_histos.append(merged_payload_p.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 5, byFill = True, returnHisto = True))
      r_histos.append(merged_payload_r.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 5, byFill = True, returnHisto = True))
  
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

  h_r = histo_file_r.Get(ivar[0])
  h_r.SetMarkerSize(0.2)
  h_r.SetMarkerColor(2)
  h_r.SetLineColor(2)
  h_r.Draw('SAME')

  leg = ROOT.TLegend( 0.902, 0.6, 1.0, 0.75 )
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.AddEntry(h_p   , 'Prompt'   , 'pel')
  leg.AddEntry(h_r   , 'ReReco Sept2017'    , 'pel')
  leg.SetTextSize(0.03)
  leg.Draw('SAME')
  
  can.Update()
  can.Modified()
  can.SaveAs('comparePromptReco_September2017/' + runstring + '/'+ivar[0] + '_Prompt_vs_SeptReco_' + runstring + '.pdf')

