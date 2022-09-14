import os
import select
import ROOT
import sys
sys.path.append('..')
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.getFileList   import get_files
ROOT.gROOT.SetBatch(True)

specialRuns = [300019,300029,300043,300050]
XeXeRuns = [304899,304906]

# Past Examples
# ZeroBias
# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v1_es0p9/171114_165107/0000/*' , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v2_es0p9/171113_141403/0000/*' , prependPath=True)

## JetHT
# files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017B_es1p1/171205_220847/0000/*.txt' , prependPath=True)
# files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017C_es1p1/171205_220837/0000/*.txt' , prependPath=True)

## HI
# files += get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/RecoVertex/BeamSpotProducer/test/HI/*.txt' , prependPath=True)

### HighEGJet
#files = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/es0p9/HighEGJet/crab_BS_JetHT_Prompt_Run2017G_es0p9/180220_211350/0000/*.txt' , prependPath=True)

###Run2021 PilotBeam Express
#files = get_files('/afs/cern.ch/work/f/fbrivio/public/BeamSpot/perDavide/BeamFit_LumiBased_NewAlignWorkflow_alcareco_Fill*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_test/211111_155451/0000/BeamFit_LumiBased_NewAlignWorkflow_BeamTest2021*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/test_2021_LHC_BeamTest_ExpressPhysics_FEVT/crab_FEVT_TkAlignment_postCRAFT_noRefit/211115_182853/0000/BeamFit_LumiBased_BeamTest2021_Refit_generalTracks_FEVT_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2021/ExpressPhysics/crab_pilotBeams2021_FEVT_LegacyBS_v1/211124_162035/0000/BeamFit_LumiBased_pilotBeams2021_FEVT_ExpressPhysics_LegacyBS_v1_*.txt' , prependPath=True)
###Run2022 LHC commissioning
files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_3/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_Run2022B*.txt' , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_UpToFill_8076/220801_092708/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_Fill_8078_8128/220829_074537/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_Fill_8132_8151/220829_083733/0000/BeamFit_LumiBased_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)

print ('start loading payloads ...')
myPayload = Payload(files)
print ('... payloads loaded')

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.items():
    if irun in XeXeRuns:
      del allBS[irun]
    n_all_fits = float(len(allBS[irun]))
    allBS[irun] = cleanAndSort(ivalues)
    n_ok_fits = len(allBS[irun])
    if n_ok_fits/n_all_fits < 0.9:
        print ("WARNING: more than 10% of the fits failed for run", irun)

# check if output file exists
fname = 'LHC_Run3Commissioning_13p6TeV_Fills_7920_8151.txt'
# if os.path.isfile(fname):
#     print 'File %s exists. Recreate? (10 sec before defaults to True)' %fname
#     i, o, e = select.select( [sys.stdin], [], [], 10 )
#     if i:
#         answer = sys.stdin.readline().strip()
#         print 'you answered %s' %answer
#         if answer in ('1', 'y', 'yes', 'true', 'True'):
#             os.remove(fname)
#         else:
#             pass        
#     else:
#         os.remove(fname)

# check drifts and create IOV
## filename for txt files containing one IOV
#filename = 'BS_result_PiltBeam2021_byIOV/beamspot_Express_PilotBeam2021_.txt'
count = 0
for irun, ibs in allBS.items():
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True)    
    else:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 1)    
    for p in pairs:
        myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
        bs_list = [ibs[i] for i in sorted(list(myrange))]
        aveBeamSpot = averageBeamSpot(bs_list)
## Create a txt file for each IOV for db object creation
#        fname = filename.replace('_.txt', '_'+str(count)+'.txt')
        aveBeamSpot.Dump(fname, 'a+')
        count = count + 1

merged_payload = Payload(fname)
histos = []

# Plot fit results from txt file
variables = [
  'X'         ,
  'Y'         ,
  'Z'         ,
  'sigmaZ'    ,
  'dxdz'      ,
  'dydz'      ,
  'beamWidthX',
  'beamWidthY'
]

for ivar in variables: 
    histos.append(merged_payload.plot(ivar , -999999, 999999, savePdf = True, dilated = 4, byFill = False, returnHisto = True))

histo_file = ROOT.TFile.Open('LHC_Run3Commissioning_13p6TeV_Fills_7920_8151.root', 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()
