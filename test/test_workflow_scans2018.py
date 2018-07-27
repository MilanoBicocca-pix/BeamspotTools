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

files  = get_files('/afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_7/src/RecoVertex/BeamSpotProducer/test/run318984_scan1_x/BeamFit_LumiBased_alcareco*.txt' , prependPath=True)


print 'start loading payloads ...'
myPayload = Payload(files)
print '... payloads loaded'

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 


for irun, ivalues in allBS.iteritems():
    n_all_fits = float(len(allBS[irun]))
    allBS[irun] = cleanAndSort(ivalues)
    n_ok_fits = len(allBS[irun])

print n_ok_fits


# check drifts and create IOV
fname = 'vdm2018_scan_x1_test_nomerge.txt'
for irun, ibs in allBS.iteritems():
    for ival in ibs.values():
        ival.Dump(fname,'a+')

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
    histos.append(merged_payload.plotByTime(ivar , 0, 99999999999, savePdf = True, dilated = 5, byFill = False, returnHisto = True))

histo_file = ROOT.TFile.Open('histos_test.root', 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()







