import os
import select
import ROOT
import sys
sys.path.append('..')
from datetime import datetime
from itertools import groupby
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.getFileList   import get_files
from utils.readJson      import readJson

files  = get_files('/Users/manzoni/Documents/beamspot/full2015_byIOV/*.txt', prependPath=True)
files += get_files('/Users/manzoni/Documents/beamspot/full2016_byIOV/*.txt', prependPath=True)

print ('start loading payloads ...')
myPayload = Payload(files)
print ('... payloads loaded')

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.items():
    allBS[irun] = cleanAndSort(ivalues)


bs_by_run = []

# check drifts and create IOV
for irun, ibs in allBS.items():
    aveBeamSpot = averageBeamSpot(ibs.values())
    bs_by_run.append(aveBeamSpot)


# keep only 3.8T
json2015 = readJson(fileName = '/Users/manzoni/Desktop/BeamspotTools/data/json2015/json_DCSONLY.txt')
json2016 = readJson(fileName = '/Users/manzoni/Desktop/BeamspotTools/data/json2016/json_DCSONLY.txt')

runs3p8T = sorted([i for i in json2015.keys() + json2016.keys()])
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
        aveBeamSpot.Dump('beamspot_run2_bymonth.txt', 'a+')
        newbs.append(aveBeamSpot)
        tomerge = []
        run = irun
    tomerge.append(ibs)
    month = imonth

outfile = open('run2_bs_xy_vs_month.csv', 'w+')
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



# year 2015, month 7	X = 0.075923 +/- 5.5032E-07 [cm]	Y = 0.093398 +/- 5.4797E-07 [cm]
# year 2015, month 8	X = 0.066654 +/- 5.5848E-07 [cm]	Y = 0.097269 +/- 5.4515E-07 [cm]
# year 2015, month 9	X = 0.000000 +/- 7.0711E-12 [cm]	Y = 0.000000 +/- 7.0711E-12 [cm]
# year 2015, month 10	X = 0.076837 +/- 2.1882E-07 [cm]	Y = 0.092261 +/- 2.1756E-07 [cm]
# year 2015, month 11	X = 0.077149 +/- 1.1199E-06 [cm]	Y = 0.094503 +/- 1.1146E-06 [cm]
# year 2016, month 5	X = 0.064871 +/- 4.0766E-07 [cm]	Y = 0.094045 +/- 4.0545E-07 [cm]
# year 2016, month 6	X = 0.063223 +/- 2.3448E-07 [cm]	Y = 0.098545 +/- 2.3346E-07 [cm]
# year 2016, month 7	X = 0.058485 +/- 2.9540E-07 [cm]	Y = 0.101528 +/- 2.9448E-07 [cm]
# year 2016, month 8	X = 0.058380 +/- 3.1998E-07 [cm]	Y = 0.101729 +/- 3.1790E-07 [cm]
# year 2016, month 9	X = 0.057529 +/- 3.8561E-07 [cm]	Y = 0.105664 +/- 3.8219E-07 [cm]



# flatallbs = []
# 
# for ibs in allBS.values():
#     for iibs in ibs.values():
#         flatallbs.append(iibs)
# 
# grouped = groupby(flatallbs, lambda x: (datetime.utcfromtimestamp(x.IOVBeginTime).year, datetime.utcfromtimestamp(x.IOVBeginTime).month))
# 
# 
# for key, group in grouped:
#     print key, group
#     import pdb ; pdb.setrace()



