import os
import sys
import select
import ROOT
from RecoVertex.BeamSpotProducer.BeamspotTools.objects.Payload     import Payload
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.beamSpotMerge import cleanAndSort
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.beamSpotMerge import splitByDrift
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.beamSpotMerge import averageBeamSpot
from RecoVertex.BeamSpotProducer.BeamspotTools.utils.getFileList   import get_files

files  = get_files('/afs/cern.ch/work/m/manzoni/public/bs_2016B/PromptReco-v1/*'           , prependPath=True)
files += get_files('/afs/cern.ch/work/m/manzoni/public/bs_2016B/PromptReco-v2-upTo274443/*', prependPath=True)

print 'start loading payloads ...'
myPayload = Payload(files)
print '... payloads loaded'

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.iteritems():
    allBS[irun] = cleanAndSort(ivalues)

# check if output file exists
fname = 'total_bs.txt'
if os.path.isfile(fname):
    print 'File %s exists. Recreate? (10 sec before defaults to True)' %fname
    i, o, e = select.select( [sys.stdin], [], [], 10 )
    if i:
        answer = sys.stdin.readline().strip()
        print 'you answered %s' %answer
        if answer in ('1', 'y', 'yes', 'true', 'True'):
            os.remove(fname)
        else:
            pass        
    else:
        os.remove(fname)

# check drifts and create IOV
for irun, ibs in allBS.iteritems():
    pairs = splitByDrift(ibs)
    for p in pairs:
        myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
        bs_list = [ibs[i] for i in sorted(list(myrange))]
        aveBeamSpot = averageBeamSpot(bs_list)
        aveBeamSpot.Dump(fname, 'a+')


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
    histos.append(myPayload.plot(ivar , -999999, 999999, savePdf = True, dilated = 5, byFill = True, returnHisto = True))

histo_file = ROOT.TFile.Open('histos.root', 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()







