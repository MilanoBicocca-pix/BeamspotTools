import os
from collections import OrderedDict
import sys
sys.path.append('..')
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.readJson      import readJson
from utils.compareLists  import compareLists
from utils.getFileList   import get_files

# input parameters
runNumber = 247324
initlumi  = 1  
endlumi   = 100000  

dict_runs = {}
dict_runs['2018A'] = 	[315252,316995]
dict_runs['2018C'] = 	[319337,320065]
dict_runs['2018D'] = 	[320673,325175]
dict_runs['2018B'] = 	[317080,319310]

		
# B		317080	318621
# B legacy	317591	317696
# B special	318622	319310

# copy result files from eos to local area
# for file in get_files('/store/group/phys_tracking/beamspot/ZeroBias/crab_Run2015D-v3_6Oct15_74X_dataRun2_Candidate_2015_10_06_09_25_21/151006_162657/0000','.txt'):
#   os.system('cmsStage ' + file + ' copy_of_crab_Run2015D_6Oct15_74X_dataRun2_Candidate_2015_10_06_09_25_21/')
# exit()

# files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/crab_BS_SeptReReco_ExpressAlignment_2018B_fix/180912_140800/0000/*.txt' , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/crab_BS_SeptReReco_ExpressAlignment_2018B_fix/180912_140800/0001/*.txt' , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/crab_BS_SeptReReco_ExpressAlignment_2018B_Specials/180913_091416/0000/*.txt'               , prependPath=True)
# files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpress/crab_BS_SeptReReco_ExpressAlignment_2018B_Fill6768_6778_fix2/180912_151520/0000/*.txt'                      , prependPath=True)

files  = get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/_106X_dataRun2_newTkAl_v18_BS_UL2018B_HP_NoFill6768_6778_NoSpecialRuns/190806_092559/0000/*.txt' , prependPath=True)
files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/_106X_dataRun2_newTkAl_v18_BS_UL2018B_SpecialRuns_Legacy/190806_092608/0000/*.txt'               , prependPath=True)
files += get_files('/eos/cms//store/group/phys_tracking/beamspot/13TeV/2018/StreamExpress/_106X_dataRun2_newTkAl_v18_BS_UL2018B_Fill6768_6778_Legacy/190806_092534/0000/*.txt'                      , prependPath=True)

print 'start loading payloads ...'
myPayload = Payload(files)


# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
# allBS            = myPayload.fromTextToBS() 
# for irun,ivalues in allBS.items():
#   allBS[irun] = cleanAndSort(allBS[irun],cleanBadFits = False)

# check if any run is missing
theJson   = "../../../test/merged_json_2018UL.json"
# theJson   = "../../../test/json_2018b_existingLSInDatasetAndJson.json"

# this returns a dictionary of runs and LS in the txt file, like {195660 : [1,2,3,...]}
runsLumisCrab = myPayload.getProcessedLumiSections() 
runsCrab      = runsLumisCrab.keys()

# this returns a dictionary of runs and LS in the json file
runsLumisJson = readJson(dict_runs['2018B'][0], dict_runs['2018B'][1], theJson, False)
runsJson      = runsLumisJson.keys()

# filter for json file 
runsCommon      = set(runsCrab) & set(runsJson)
inCrabNotInJson = set(runsCrab) - set(runsJson)
inJsonNotInCrab = set(runsJson) - set(runsCrab)
print 'completely missing runs:'
print inJsonNotInCrab

print 'missing LSs from runs:'
for irun in runsCommon:
  inJsonNotCrab, inCrabNotJson = compareLists(runsLumisCrab[irun], runsLumisJson[irun], 100, 'crab', 'json' )
  if len(inJsonNotCrab) > 0:
    print 'run ' + str(irun) 
    for ls in inJsonNotCrab:
      print str(ls) 

# remove LS not in json file 
#   for ls in inCrabNotJson:
#     del allBS[irun][ls]



# check drifts and create IOV
#   pairs = splitByDrift(allBS[irun])
#   for p in pairs:
#     myrange = set(range(p[0], p[1] + 1)) & set(allBS[irun].keys())
#     bs_list = [allBS[irun][i] for i in sorted(list(myrange))]
#     aveBeamSpot = averageBeamSpot(bs_list)
#     aveBeamSpot.Dump('2015D/bs_weighted_results_' + str(irun) + '_' + str(p[0]) +'_LumiIOV.txt', 'a+')
    # nb: the LumiIOV file is opened in "append mode"



# now evaluate average BS for the entire run
# pairs = [(initlumi, endlumi)]
# for p in pairs:
#     myrange = set(range(p[0], p[1] + 1)) & set(allBS[runNumber].keys())
#     bs_list = [allBS[runNumber][i] for i in sorted(list(myrange))]
#     aveBeamSpot = averageBeamSpot(bs_list)
#     aveBeamSpot.Dump('bs_weighted_results_' + str(runNumber) + '_AllRun.txt', 'w+')


