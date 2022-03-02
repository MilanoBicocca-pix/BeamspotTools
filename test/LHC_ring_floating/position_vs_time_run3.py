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
json2021   = readJson(fileName = '/eos/user/c/cmsdqm/www/CAF/certification/scripts/CMSSW_10_0_4/scripts/runregistry_checks/Run_RegistryScripts/Collisions21Special_DcsTrackerPixelJSON.txt')

runs3p8T = sorted([i for i in json2021.keys() ])
bs_by_run = [ibs for ibs in bs_by_run if ibs.Run in runs3p8T]

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

