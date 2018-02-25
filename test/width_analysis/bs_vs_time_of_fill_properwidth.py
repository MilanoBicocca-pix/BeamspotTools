import os
import select
import ROOT
import sys
from array               import array
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.getFileList   import get_files
from math import pow, sqrt


from itertools import product
from ROOT import TGraphErrors
ROOT.gROOT.SetBatch(True)

# files   = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/JetHT/crab_BS_Run2017A_JetHT/171013_133647/0000/*'         , prependPath=True)
# files  += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/JetHT/crab_BS_Run2017B_JetHT/171009_113337/0000/*'         , prependPath=True)
# files  += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/JetHT/crab_BS_Run2017C_JetHT/171013_145809/0000/*'         , prependPath=True)

files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017B_es1p1/171205_220847/0000/*.txt'         , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017C_es1p1/171205_220837/0000/*.txt'         , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017D_es1p1/171205_220906/0000/*.txt'         , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017E_es1p1/171205_220856/0000/*.txt'         , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2017/es1p1/JetHT/crab_BS_JetHT_ReRecoNov_Run2017F_es1p1/180112_112626/0000/*.txt'         , prependPath=True)

# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016Bv2/*'         , prependPath=True)
# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016C/*'           , prependPath=True)
# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016D/*'           , prependPath=True)
# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016E/*'           , prependPath=True)
# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016F/*'           , prependPath=True)
# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016G/*'           , prependPath=True)
# files  += get_files('/afs/cern.ch/work/f/fiorendi/public/BeamSpot_Legacy2016/measurementOnJetHT/HLTSelection/Run2016H/*'           , prependPath=True)

outfile = ROOT.TFile('graphs_properWidth_perFill_fromStableBeam_allNovReReco_2017BF_firstPV_JetHT.root', 'recreate')


from utils.fillRunDict import *
fillRunDict  = {k : v.Runs       for k, v in fillDict.items()}
fillTimeDict = {k : v.BeginTime  for k, v in fillDict.items()}

import time, datetime, calendar

print 'start loading payloads ...'
myPayload = Payload(files)
print '... payloads loaded'


# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

# create a dictionary of dictionaries of dictionaries { Fill: {Time from start : BeamSpot Fit Object } }
allBS_byFill_byTime = {}


for irun, ivalues in allBS.iteritems():
    allBS[irun] = cleanAndSort(ivalues)
    
    for k, v in fillRunDict.items():
        if int(irun) in v: 
            theifill = k
            theifilltime =   calendar.timegm(fillTimeDict[theifill].timetuple()) # from UTC to in seconds
            break    

    for ibs in ivalues.items():
        thebstime = ibs[1].IOVBeginTime
        timefromstart = thebstime - theifilltime
      
        try:
          allBS_byFill_byTime[theifill][timefromstart] = ibs
        except:
          toadd = { theifill : {timefromstart : ibs } }
          allBS_byFill_byTime.update( toadd )      


## now test plotting
fills = list(set(v for v in allBS_byFill_byTime.keys()))

vars = ['X', 'Y']

for ifill, var in product( fills, vars):
    
    print 'Fill: ', ifill
    times = list(set(v for v in allBS_byFill_byTime[ifill].keys()))

    lastBin = 0.
    points = []
    bins   = []
    widths = []
    err_b  = []
    err_w  = []

    for itime in sorted(times):

        nowBS = allBS_byFill_byTime[ifill][itime]
        point = (
            float(itime)/3600.                          , #0 x  
            getattr(nowBS[1], 'sigma' + var + 'true')   , #1 y
            1./3600.                                    , #2 xe
            getattr(nowBS[1], 'sigma' + var + 'trueerr'), #3 ye
        )
        
        # fill only if width makes sense
        if point[1]>0.:
            points.append(point)

        points.sort(key=lambda x: x[0])

    for ipoint in points:
        
        bins  .append(ipoint[0])
        widths.append(ipoint[1])
        err_b .append(ipoint[2])
        err_w .append(ipoint[3])

    abins   = array('f', bins  )
    aerr_b  = array('f', err_b )
    awidths = array('f', widths)
    aerr_w  = array('f', err_w )

    if len(abins)==0:
      continue
    graph = TGraphErrors(len(abins), abins, awidths, aerr_w, aerr_w)
    c1 = ROOT.TCanvas('c1%d'%ifill, 'c1%d'%ifill, 1400, 800)
    graph.SetTitle( 'Fill ' + str(ifill) + ' - width' + var + '; hours from start of stable beam for fill; width' + var + ' [cm]')
    graph.SetName('Fill' + str(ifill) + 'width' + var)
    graph.SetMarkerStyle(8)
    graph.Draw('A')
    graph.GetXaxis().SetRangeUser(0, abins[-1]+1000)
    ROOT.gPad.Update()
    outfile.cd()
    graph.Write()  

outfile.Close()

