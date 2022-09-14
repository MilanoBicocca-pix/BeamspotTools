import os
import select
import ROOT
from datetime import datetime
from itertools import groupby

import sys
sys.path.append('../..')
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.getFileList   import get_files
from utils.readJson      import readJson

## 2021
files = get_files('/afs/cern.ch/work/f/fbrivio/public/per_Davide/BS_result_PiltBeam2021_byFill/*.txt', prependPath=True)
###Run2022 LHC commissioning
files += get_files('/afs/cern.ch/work/d/dzuolo/private/BeamSpot/CMSSW_12_4_3/src/RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_Run2022B*.txt' , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_UpToFill_8076/220801_092708/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_Fill_8078_8128/220829_074537/0000/BeamFit_LumiBased_Run2022C_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/StreamExpress/crab_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_Fill_8132_8151/220829_083733/0000/BeamFit_LumiBased_Run2022D_StreamExpress_TkAlMinBias_ALCARECO_*.txt' , prependPath=True)

print ('start loading payloads ...')
myPayload = Payload(files)
print ('... payloads loaded')

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.items():
    allBS[irun] = cleanAndSort(ivalues, cleanBadFits = True, iov = True)

bs_by_run = []

# check drifts and create IOV
for irun, ibs in allBS.items():
    aveBeamSpot = averageBeamSpot(ibs.values())
    bs_by_run.append(aveBeamSpot)

# keep only DCS JSON
json2021   = readJson(fileName = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions21/collisions21Special_346235_346512_DcsTrackerPixelJSON.txt')
json2022   = readJson(fileName = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Cert_Collisions2022_355100_357900_13p6TeV_DCSOnly_TkPx.json')

runs3p8T = sorted([i for i in list(json2021.keys()) + list(json2022.keys()) ])
bs_by_run = [ibs for ibs in bs_by_run if ibs and ibs.Run in runs3p8T]

# create container for by run bs
newbs = []

# create a container for runs to merge
tomerge =[]

month = -1

for ibs in bs_by_run:
    #print 'processing run', ibs.Run
    date   = datetime.utcfromtimestamp(ibs.IOVBeginTime) 
    imonth = date.month
    if (imonth != month and month > 0) or ibs == bs_by_run[-1]:
        print ('processing run %d year %d month %d' %(ibs.Run, date.year, imonth))
        aveBeamSpot = averageBeamSpot(tomerge, doNotCheck=['Run'])
        aveBeamSpot.Dump('beamspot_run3_bymonth_redo.txt', 'a+')
        newbs.append(aveBeamSpot)
        tomerge = []
        run = irun
    tomerge.append(ibs)
    month = imonth

outfile = open('run3_bs_xy_vs_month_redo.csv', 'w+')
print ('year,month,x,xerr,y,yerr', file=outfile)

for ibs in newbs:
    date_start = datetime.utcfromtimestamp(ibs.IOVBeginTime)
    print ('year {}, month {}\t'\
          'X = {:3.6f} +/- {:3.4E} [cm]\t' \
          'Y = {:3.6f} +/- {:3.4E} [cm]' \
          .format(date_start.year, date_start.month,
                  ibs.X          , ibs.Xerr        ,
                  ibs.Y          , ibs.Yerr        ,))
    print (','.join([str(date_start.year), str(date_start.month), str(ibs.X), str(ibs.Xerr), str(ibs.Y), str(ibs.Yerr)]),file=outfile)
 
outfile.close()
