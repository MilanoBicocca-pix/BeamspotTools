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

specialRuns2017 = [300019,300029,300043,300050]
XeXeRuns        = [304899,304906]
specialRuns     = [319018,319019,318984]

run_string = '2018D'

files = []
if run_string == '2018A':
    files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018A_HP_crab_106X_dataRun2_newTkAl_v18/190812_114423/0000/*.txt'         , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018A_HP_crab_106X_dataRun2_newTkAl_v18/190812_114423/0001/*.txt'         , prependPath=True)

elif run_string == '2018B':
    files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018B_HP_NoFill6768_6778_NoSpecialRuns_crab_106X_dataRun2_newTkAl_v18/190812_114430/0000/*.txt'      , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpress/BS_UL2018B_Fill6768_6778_Legacy_crab_106X_dataRun2_newTkAl_v18//190809_131128/0000/*.txt'                          , prependPath=True)

elif run_string == '2018B_Specials':
    files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018B_SpecialRuns_Legacy_crab_106X_dataRun2_newTkAl_v18/190809_131138/0000/*.txt'         , prependPath=True)

elif run_string == '2018C':
    files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018C_HP_crab_106X_dataRun2_newTkAl_v18/190812_114410/0000/*.txt'                   , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018C_HP_crab_106X_dataRun2_newTkAl_v18/190812_114410/0001/*.txt'                   , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018C_Legacy_LowPU_crab_106X_dataRun2_newTkAl_v18/190812_114437/0000/*.txt'                   , prependPath=True)

elif run_string == '2018D':
  #### 2018D
    files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0000/*.txt'      , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0001/*.txt'      , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0002/*.txt'      , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0003/*.txt'      , prependPath=True)
    files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0004/*.txt'      , prependPath=True)


print 'start loading payloads ...'
myPayload = Payload(files)
print '... payloads loaded'

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.iteritems():
    if irun in XeXeRuns:
      del allBS[irun]
    n_all_fits = float(len(allBS[irun]))
    allBS[irun] = cleanAndSort(ivalues, cleanForSigmaZ = True)
    n_ok_fits = len(allBS[irun])
    if n_ok_fits/n_all_fits < 0.9:
        print "WARNING: more than 10% of the fits failed for run", irun

# check if output file exists
fname = 'beamspot_%s.txt'%run_string
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
# filename = 'IOVforPayloads/%s/bs_2018UL_.txt'%run_string
count = 0
for irun, ibs in allBS.iteritems():
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 20)    
    else:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 1)    
    for p in pairs:
        myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
        bs_list = [ibs[i] for i in sorted(list(myrange))]
        aveBeamSpot = averageBeamSpot(bs_list)
#         fname = filename.replace('_.txt', '_'+str(count)+'.txt')
        aveBeamSpot.Dump(fname, 'a+')
        count = count + 1


# exit()
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
    histos.append(merged_payload.plot(ivar , 322477, 323702, savePdf = True, dilated = 8, byFill = False, returnHisto = True))

histo_file = ROOT.TFile.Open('histos_%s.root'%run_string, 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()







