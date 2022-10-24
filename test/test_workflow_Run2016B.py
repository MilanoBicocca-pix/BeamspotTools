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
#files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_3/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_Run2022B*.txt' , prependPath=True)
#files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_UpToFill_8076/220801_092708/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
#files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_Fill_8078_8128/220829_074537/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
#files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_Fill_8132_8151/220829_083733/0000/BeamFit_LumiBased_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
## Run2022ABCD runs for ReReco
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_StreamExpressAlignment_TkAlMinBias_ALCARECO_Run356719/220916_091737/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022D_StreamExpressAlignment_TkAlMinBias_ALCARECO_Run357612/220916_093948/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
## Run2022ABCD final fit for ReReco
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022B_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco/220921_132106/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco/220921_135051/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022D_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco/220922_094204/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
## Run2022ABCD runs for FTV MINRES 
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_forTkAlFTV_Run356719_errorScale_1p0/220930_142459/0000/BeamFit_LumiBased_forTkAlFTV_Run2022C_Run356719_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022Dv1_forTkAlFTV_Run357612/220930_143114/0000/BeamFit_LumiBased_forTkAlFTV_Run2022Dv1_Run357612_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022Dv2_forTkAlFTV_Run357815/220930_145232/0000/BeamFit_LumiBased_forTkAlFTV_Run2022Dv2_Run357815_*.txt' , prependPath=True)
## Run2022ABCD final fit for ReReco MINRES
files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE_byRun_1.txt' , prependPath=True)
#files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576.txt' , prependPath=True)
#files = get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE.txt' , prependPath=True)
#files += get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_8/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_forReReco_Run2022A_mp3576_newAPE_1.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/ZeroBias/crab_Run2022B_ZeroBias_TkAlMinBias_ALCARECO_forReReco_mp3576_giusto/221006_134630/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_154527/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
#files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022C_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_154527/0001/BeamFit_LumiBased_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022Dv1_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_121305/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpressAlignment/crab_Run2022Dv2_StreamExpressAlignment_TkAlMinBias_ALCARECO_forReReco_mp3576/221004_082248/0000/BeamFit_LumiBased_*.txt' , prependPath=True)
## Run2022E prompt
#files = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022E_StreamExpress_TkAlMinBias_ALCARECO_promptFit/221017_095826/0000/BeamFit_LumiBased_PromptFit_Run2022E_*.txt' , prependPath=True)
#files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022E_StreamExpress_TkAlMinBias_ALCARECO_promptFit/221017_095826/0001/BeamFit_LumiBased_PromptFit_Run2022E_*.txt' , prependPath=True)
#files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022E_StreamExpress_TkAlMinBias_ALCARECO_promptFit/221017_095826/0002/BeamFit_LumiBased_PromptFit_Run2022E_*.txt' , prependPath=True)

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
#fname = 'Run2022A_forReReco_mp3576_MINRES.txt'
#fname = 'Run2022A_forReReco_mp3576_MINRES_newAPE.txt'
fname = 'Run2022A_forReReco_mp3576_MINRES_newAPE_by10LS.txt'
#fname = 'Run2022B_forReReco_mp3576_MINRES.txt'
#fname = 'Run2022C_forReReco_mp3576_MINRES.txt'
#fname = 'Run2022Dv1_forReReco_mp3576_MINRES.txt'
#fname = 'Run2022Dv2_forReReco_mp3576_MINRES.txt'
#fname = 'Run2022E_PromptFit.txt'
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
#filename = 'Run2022A_forReReco_mp3576_MINRES_.txt'
#filename = 'Run2022A_forReReco_mp3576_MINRES_newAPE_.txt'
filename = 'Run2022A_forReReco_mp3576_MINRES_newAPE_by10LS_.txt'
#filename = 'Run2022B_forReReco_mp3576_MINRES_.txt'
#filename = 'Run2022C_forReReco_mp3576_MINRES_.txt'
#filename = 'Run2022Dv1_forReReco_mp3576_MINRES_.txt'
#filename = 'Run2022Dv2_forReReco_mp3576_MINRES_.txt'
count = 0
for irun, ibs in allBS.items():
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 20)    
    else:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 1)
    for p in pairs:
        myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
        bs_list = [ibs[i] for i in sorted(list(myrange))]
        aveBeamSpot = averageBeamSpot(bs_list)
## Create a txt file for each IOV for db object creation
        #fname = filename.replace('_.txt', '_'+str(count)+'.txt')
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

histo_file = ROOT.TFile.Open('Run2022A_forReReco_mp3576_MINRES_newAPE_by10LS.root', 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()
