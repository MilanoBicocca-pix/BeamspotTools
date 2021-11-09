import os
import ROOT
import sys
sys.path.append('..')
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
  for irun, ibs in bscollection.items():
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
    ('X'         , 'beam spot x [cm]'         ,  0.15  , 0.19  ),
    ('Y'         , 'beam spot y [cm]'         , -0.21  ,-0.175 ),
    ('Z'         , 'beam spot z [cm]'         , -3.    , 3     ),
    ('sigmaZ'    , 'beam spot #sigma_{z} [cm]',  3.5   , 9.    ),
    ('beamWidthX', 'beam spot #sigma_{x} [cm]',  0.00  , 0.025 ),
    ('beamWidthY', 'beam spot #sigma_{y} [cm]',  0.00  , 0.025 ),
#   ('dxdz'      , 'beam spot dx/dz [rad]'    , -0.002 , 0.002 ),
#   ('dydz'      , 'beam spot dy/dz [rad]'    , -0.002 , 0.002 ),
]
variables = list(variables)


# PCL workflow name
#  HPBS_byLumi     : reference_PCL_HPBS_byLumi.txt      ----> Prompt GT
#  HPBS_byRun      : reference_PCL_HPBS_byRun.txt       ----> Express and HLT GT
#  LegacyBS_byLumi : reference_PCL_LegacyBS_byLumi.txt  ----> Legacy
#  LegacyBS_byRun  : reference_PCL_LegacyBS_byRun.txt   ----> Legacy
nameWF = 'HPBS_byLumi'

if doFromScratch:

  # Reco files
  r_files = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/perDavide/BeamFit_LumiBased_NewAlignWorkflow_alcareco_Fill*.txt', prependPath=True)

  # PCL files
  p_files = get_files('/afs/cern.ch/work/f/fbrivio/public/per_Davide/PilotBeamBStxt/reference_PCL_'+nameWF+'.txt', prependPath=True)
 
  print ('start loading payloads ...')
  pclPayload  = Payload(p_files)
  recoPayload = Payload(r_files)
  print ('... payloads loaded')

  # convert results into a dictionary { Run : {Lumi Range: BeamSpot Fit Object} }
  pclBS  = pclPayload .fromTextToBS() 
  recoBS = recoPayload.fromTextToBS() 

  # this returns a dictionary of runs and LS in the txt file, like {195660 : [1,2,3,...]}
  runsLumisPcl  = pclPayload.getProcessedLumiSections() 
  runsLumisReco = recoPayload.getProcessedLumiSections() 
  runsPcl       = runsLumisPcl.keys()
  runsReco      = runsLumisReco.keys()

  # filter for common runs 
  runsCommon = set(runsPcl) & set(runsReco)
  inPclNotInReco = set(runsPcl)  - set(runsReco)
  inRecoNotInPcl = set(runsReco) - set(runsPcl)

  for irun in runsCommon:
    LSinPclNotInReco, LSinRecoNotInPcl = compareLists(runsLumisReco[irun], runsLumisPcl[irun], 0, 'pcl', 'reco' )
    if verbosePrinting and len(LSinRecoNotInPcl) > 0:
      s = ''
      for ls in LSinRecoNotInPcl:
        s += str(ls) + ', '
      print ('Run ' + str(irun) + ': ' + s)

  # remove from reco collection the LSs not in pcl file 
    for ls in LSinRecoNotInPcl:
      try:
        if recoBS[irun][ls]:
          del recoBS[irun][ls]
      except:
        print (irun, ls)

  # remove from pcl collection the LSs not in reco file 
    if len(LSinPclNotInReco) > 0: print ('missing in Rereco:')
    for ls in LSinPclNotInReco:
      if pclBS[irun][ls]:
        print (irun, ls)
        del pclBS[irun][ls]

  newPclBS  = {k:v for k, v in pclBS.items()  if k in runsCommon}
  newRecoBS = {k:v for k, v in recoBS.items() if k in runsCommon}

  n_all_fits_pcl = len(newPclBS)

  # remove not-converged fits and sort
  print ('--- Job Report ---')
  for irun, ivalues in newPclBS.items():
    n_all_fits_pcl = len(newPclBS[irun])
    newPclBS[irun] = cleanAndSort(ivalues)
    n_ok_fits_pcl = float (len(newPclBS[irun]))
    print ('fit failures in pcl for run', irun, ':', 1. - n_ok_fits_pcl/n_all_fits_pcl)

  for irun, ivalues in newRecoBS.items():
    n_all_fits_reco = len(newRecoBS[irun])
    newRecoBS[irun] = cleanAndSort(ivalues)
    n_ok_fits_reco  = float (len(newRecoBS[irun]))
    print ('fit failures in reco for run', irun, ':',   1. - n_ok_fits_reco/n_all_fits_reco)

  #print '--- Job Report ---'
  #print 'fit failures in pcl :', 1. - n_ok_fits_pcl/n_all_fits_pcl
  #print 'fit failures in reco:', 1. - n_ok_fits_reco/n_all_fits_reco

  # now check if the remaining BSs are there in both collections and delete sinlgetons
  runsLumisPclCleaned  = []
  runsLumisRecoCleaned = []

  for i, irun in enumerate(runsCommon):
    runsLumisPclCleaned .append(newPclBS[irun].keys())
    runsLumisRecoCleaned.append(newRecoBS[irun].keys())

    for ilumi in list(runsLumisRecoCleaned[i]):
      if ilumi not in runsLumisPclCleaned[i]:  del newRecoBS[irun][ilumi]
    for ilumi in list(runsLumisPclCleaned[i]):
      if ilumi not in runsLumisRecoCleaned[i]:  del newPclBS[irun][ilumi]

  # dump the list into a txt file, and save histos into root files
  pclname  = 'BS_comparison_PCL/pcl_payloads_'  + nameWF + '.txt'
  reconame = 'BS_comparison_PCL/reco_payloads_' + nameWF + '.txt'

  _doMerge(newPclBS , pclname)
  _doMerge(newRecoBS, reconame)

  merged_payload_p = Payload(pclname)
  merged_payload_r = Payload(reconame)

  p_histos = []
  r_histos = []

  for ivar in variables: 
    p_histos.append(merged_payload_p.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 5, byFill = False, returnHisto = True))
    r_histos.append(merged_payload_r.plot(ivar[0] , -999999, 999999, savePdf = False, dilated = 5, byFill = False, returnHisto = True))
  
  _doSaveHistos( p_histos, 'BS_comparison_PCL/histos_pcl_' + nameWF + '.root' )
  _doSaveHistos( r_histos, 'BS_comparison_PCL/histos_reco_' + nameWF + '.root'   )


histo_file_p = ROOT.TFile.Open('BS_comparison_PCL/histos_pcl_'  + nameWF + '.root', 'read')
histo_file_r = ROOT.TFile.Open('BS_comparison_PCL/histos_reco_' + nameWF + '.root', 'read')

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

  h_r = histo_file_r.Get(ivar[0])
  h_r.SetMarkerSize(0.2)
  h_r.SetMarkerColor(2)
  h_r.SetLineColor(2)
  h_r.Draw('SAME')

  leg = ROOT.TLegend( 0.902, 0.6, 1.0, 0.75 )
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.AddEntry(h_p, 'PCL '+nameWF    , 'pel')
  leg.AddEntry(h_r, 'Offline Re-Reco', 'pel')
  leg.SetTextSize(0.03)
  leg.Draw('SAME')
  
  can.Update()
  can.Modified()
  can.SaveAs('BS_comparison_PCL/'+nameWF + '_BS_' + ivar[0] + '.pdf')

