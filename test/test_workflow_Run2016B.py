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

# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v1_es0p9/171114_165107/0000/*'         , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v2_es0p9/171113_141403/0000/*'         , prependPath=True)
# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v1_es0p9/171114_174952/0000//*'        , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v2_es0p9/171114_175018/0000//*txt'     , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v3_es0p9/171114_175048/0000//*'        , prependPath=True)
# files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias1/crab_BS_ReRecoNov17_VdM_Run2017C_es0p9/171115_085917/0000/*'        , prependPath=True)
# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017D_es0p9/171114_175116/0000/*'            , prependPath=True)
# files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias8b4e1/crab_BS_ReRecoNov17_HighPU_Run2017D_es0p9/171115_085845/0000/*' , prependPath=True)
# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_es0p9/171114_175143/0000/*'            , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_es0p9/171114_175143/0001/*'            , prependPath=True)

# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017F_es0p9_GTv2/171129_144416/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017F_es0p9_GTv2/171129_144416/0001/*'           , prependPath=True)


# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v1_es1p1/171110_150426/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017B_v2_es1p1/171110_185941/0000/*'           , prependPath=True)

# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v1_es1p1/171110_215538/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v2_es1p1/171110_215641/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017C_v3_es1p1/171110_215747/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017D_v1_es1p1/171110_215814/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_v1_es1p1/171110_215859/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017E_v1_es1p1/171110_215859/0001/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017F_v1_es1p1/171110_215943/0000/*'           , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/ZeroBias/crab_BS_ReRecoNov17_Run2017F_v1_es1p1/171110_215943/0001/*'           , prependPath=True)

## JetHT
# files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017B_es1p1/171205_220847/0000/*.txt'         , prependPath=True)
# files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017C_es1p1/171205_220837/0000/*.txt'         , prependPath=True)
# files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017D_es1p1/171205_220906/0000/*.txt'         , prependPath=True)
# files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017E_es1p1/171205_220856/0000/*.txt'         , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017F_es1p1/180112_112626/0000/*.txt'           , prependPath=True)

## add HI
# files += get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/RecoVertex/BeamSpotProducer/test/HI/*.txt'         , prependPath=True)

###Run2017H  ZeroBias
# files = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2017/CMSSW_9_4_0_pre3/src/RecoVertex/BeamSpotProducer/test/split_2017H_96perc/*.txt'         , prependPath=True)

###Run2017G  HighEGJet
files = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2017/es0p9/HighEGJet/crab_BS_JetHT_Prompt_Run2017G_es0p9/180220_211350/0000/*.txt'         , prependPath=True)

print ('start loading payloads ...')
myPayload = Payload(files)
print ('... payloads loaded')

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.iteritems():
    if irun in XeXeRuns:
      del allBS[irun]
    n_all_fits = float(len(allBS[irun]))
    allBS[irun] = cleanAndSort(ivalues)
    n_ok_fits = len(allBS[irun])
    if n_ok_fits/n_all_fits < 0.9:
        print ("WARNING: more than 10% of the fits failed for run", irun)

# check if output file exists
fname = 'beamspot_2017G_HighEGJet_January.txt'
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
# filename = 'IOVforPayloads/2017G/bs_ZB_2017_.txt'
count = 0
for irun, ibs in allBS.iteritems():
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True)    
    else:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 1)    
    for p in pairs:
        myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
        bs_list = [ibs[i] for i in sorted(list(myrange))]
        aveBeamSpot = averageBeamSpot(bs_list)
#         fname = filename.replace('_.txt', '_'+str(count)+'.txt')
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
    histos.append(merged_payload.plot(ivar , -999999, 999999, savePdf = True, dilated = 8, byFill = False, returnHisto = True))

histo_file = ROOT.TFile.Open('histos_2017G_NovReReco_HighEGJet.root', 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()







