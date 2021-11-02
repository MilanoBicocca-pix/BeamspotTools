import os
import select
import ROOT
import sys
sys.path.append('..')
import time
from datetime import datetime
from itertools import groupby, product
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.getFileList   import get_files
from utils.readJson      import readJson
from utils.fillRunDict   import _createFillList

files = get_files('/Users/manzoni/Documents/beamspot/Run1/fromDB_BeamSpotObjects_allRun1.txt', prependPath=True)

print ('start loading payloads ...')
myPayload = Payload(files)
print ('... payloads loaded')

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.iteritems():
    allBS[irun] = cleanAndSort(ivalues)

bs_by_run = []

# check drifts and create IOV
for irun, ibs in allBS.iteritems():
    aveBeamSpot = averageBeamSpot(ibs.values())
    bs_by_run.append(aveBeamSpot)

# keep only 3.8T
json2010 = readJson(fileName = '/Users/manzoni/Desktop/BeamspotTools/data/json2010/json_DCSONLY.txt')
json2011 = readJson(fileName = '/Users/manzoni/Desktop/BeamspotTools/data/json2011/json_DCSONLY.txt')
json2012 = readJson(fileName = '/Users/manzoni/Desktop/BeamspotTools/data/json2012/json_DCSONLY.txt')

runs3p8T = sorted([i for i in json2010.keys() + json2011.keys() + json2012.keys()])
bs_by_run = [ibs for ibs in bs_by_run if ibs.Run in runs3p8T]

# since these BS are from the database, they don't carry a timestamp.
# Do the matching by hand through the Fill thingy
# An approximation is assumed for simplicity sake: the time stamp of 
# the begin of stable beams is assigned to all runs in the fill.
# Good enough for now

fillrun = _createFillList()

for ibs, ifill in product(bs_by_run, fillrun.values()):
    if ibs.Run in ifill.Runs:
        ibs.IOVBeginTime = time.mktime(ifill.BeginTime.timetuple())

# prune from runs which weren't in any stable fill (there are some in 2010)
bs_by_run = [ibs for ibs in bs_by_run if ibs.IOVBeginTime > 0.]


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
        aveBeamSpot.Dump('beamspot_run1_bymonth.txt', 'a+')
        newbs.append(aveBeamSpot)
        tomerge = []
        run = irun
    tomerge.append(ibs)
    month = imonth

outfile = open('run1_bs_xy_vs_month.csv', 'w+')
print >> outfile, 'year,month,x,xerr,y,yerr'

for ibs in newbs:
    date_start = datetime.utcfromtimestamp(ibs.IOVBeginTime)
    print ('year {}, month {}\t'\
          'X = {:3.6f} +/- {:3.4E} [cm]\t' \
          'Y = {:3.6f} +/- {:3.4E} [cm]' \
          .format(date_start.year, date_start.month,
                  ibs.X          , ibs.Xerr        ,
                  ibs.Y          , ibs.Yerr        ,))
    print >> outfile, ','.join([str(date_start.year), 
                                str(date_start.month), 
                                str(ibs.X), 
                                str(ibs.Xerr), 
                                str(ibs.Y), 
                                str(ibs.Yerr)])     
 
outfile.close()


# year 2011, month 3	X = 0.077839 +/- 9.7902E-07 [cm]	Y = 0.028113 +/- 9.7715E-07 [cm]
# year 2011, month 4	X = 0.073770 +/- 7.4586E-07 [cm]	Y = 0.031826 +/- 7.4746E-07 [cm]
# year 2011, month 5	X = 0.073375 +/- 6.7365E-07 [cm]	Y = 0.033227 +/- 6.7243E-07 [cm]
# year 2011, month 6	X = 0.073288 +/- 4.6439E-07 [cm]	Y = 0.035653 +/- 4.6361E-07 [cm]
# year 2011, month 7	X = 0.070141 +/- 8.5694E-07 [cm]	Y = 0.041313 +/- 8.5277E-07 [cm]
# year 2011, month 8	X = 0.069972 +/- 1.1458E-06 [cm]	Y = 0.042607 +/- 1.1408E-06 [cm]
# year 2011, month 9	X = 0.075704 +/- 4.5109E-07 [cm]	Y = 0.041030 +/- 4.4913E-07 [cm]
# year 2011, month 10	X = 0.075489 +/- 4.4468E-07 [cm]	Y = 0.041007 +/- 4.4240E-07 [cm]
# year 2012, month 4	X = 0.073277 +/- 4.1297E-07 [cm]	Y = 0.056441 +/- 4.1600E-07 [cm]
# year 2012, month 5	X = 0.072273 +/- 4.4371E-07 [cm]	Y = 0.061710 +/- 4.4601E-07 [cm]
# year 2012, month 6	X = 0.071984 +/- 4.7545E-07 [cm]	Y = 0.063612 +/- 4.7791E-07 [cm]
# year 2012, month 7	X = 0.071005 +/- 4.5817E-07 [cm]	Y = 0.060969 +/- 4.6010E-07 [cm]
# year 2012, month 8	X = 0.070873 +/- 4.4563E-07 [cm]	Y = 0.063639 +/- 4.4742E-07 [cm]
# year 2012, month 9	X = 0.069778 +/- 5.6908E-07 [cm]	Y = 0.063423 +/- 5.7218E-07 [cm]
# year 2012, month 10	X = 0.069772 +/- 4.1637E-07 [cm]	Y = 0.062735 +/- 4.1755E-07 [cm]
# year 2012, month 11	X = 0.069930 +/- 4.2480E-07 [cm]	Y = 0.062511 +/- 4.2626E-07 [cm]
# year 2012, month 12	X = 0.069043 +/- 9.4942E-07 [cm]	Y = 0.062314 +/- 9.5232E-07 [cm]


