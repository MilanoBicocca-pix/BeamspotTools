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
import itertools

ROOT.gROOT.SetBatch(True)

specialRuns = [300019,300029,300043,300050]
XeXeRuns = [304899,304906]

fillId = 4954
runId  = 274100
bxId = 2063

#files  = get_files('../../../test/scans_results_from_condor/scan1_X1_bx%s_prompt_ZB1_8_Final/BeamFit_LumiBased_alcareco_*.txt'%bxId     , prependPath=True)
#files += get_files('../../../test/scans_results_from_condor/scan2_Y1_bx%s_prompt_ZB1_8_Final/BeamFit_LumiBased_alcareco_*.txt'%bxId     , prependPath=True)
#files += get_files('../../../test/scans_results_from_condor/scan3_offX1_bx%s_prompt_ZB1_8_Final/BeamFit_LumiBased_alcareco_*.txt'%bxId  , prependPath=True)
#files += get_files('../../../test/scans_results_from_condor/scan4_offY1_bx%s_prompt_ZB1_8_Final/BeamFit_LumiBased_alcareco_*.txt'%bxId  , prependPath=True)
#files += get_files('../../../test/scans_results_from_condor/scan17_X4_bx%s_prompt_ZB1_8_Final/BeamFit_LumiBased_alcareco_*.txt'%bxId    , prependPath=True)
#files += get_files('../../../test/scans_results_from_condor/scan18_Y4_bx%s_prompt_ZB1_8_Final/BeamFit_LumiBased_alcareco_*.txt'%bxId    , prependPath=True)

files = get_files('../../../test/FinalBSfit/BSfit_Fill{FILL}_Run{RUN}_bx{BX}/BeamFit_LumiBased_alcareco_*.txt'.format(FILL=str(fillId),RUN=str(runId),BX=str(bxId)) , prependPath=True)


def DumpCSVTitle(file, mode = 'a'):
    f = open(file, mode)
    title   = 'Runnumber \t'                          \
              'BeginTimeOfFit \t EndTimeOfFit \t'     \
              'Type \t'                               \
              'X0 \t'                                 \
              'X0Err \t'                              \
              'Y0 \t'                                 \
              'Y0Err \t'                              \
              'Z0 \t'                                 \
              'Z0Err \t'                              \
              'sigmaZ0 \t'                            \
              'sigmaZ0Err \t'                         \
              'dxdz \t'                               \
              'dxdzErr \t '                           \
              'dydz \t'                               \
              'dydzErr \t'                            \
              'dxdy \t'                               \
              'dxdyErr \t'                            \
              'BeamWidthX \t'                         \
              'BeamWidthXErr \t'                      \
              'BeamWidthY \t'                         \
              'BeamWidthYErr \t'                      \
              'TrueWidthX \t'                         \
              'TrueWidthXErr \t'                      \
              'TrueWidthY \t'                         \
              'TrueWidthYErr \t'                      \
              '\n'
    f.write(title)

def DumpCSVFromPVFitTitle(file, mode = 'a'):
    f = open(file, mode)
    title   = 'Runnumber \t'                          \
              'BeginTimeOfFit \t EndTimeOfFit \t'     \
              'Type \t'                               \
              'X0 \t'                                 \
              'Y0 \t'                                 \
              'Z0 \t'                                 \
              'sigmaZ0 \t'                            \
              'dxdz \t'                               \
              'dydz \t'                               \
              'dxdy \t'                               \
              'BeamWidthX \t'                         \
              'BeamWidthY \t' 

    for j,k in itertools.product(range(9),range(9)):
        title = title + 'COV{I} \t'.format(I = str(j)+','+str(k))
    title = title + 'nPVs \t FuncValue'
    title = title + '\n'
    f.write(title)


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


# check drifts and create CSV with info from PVs
fname = 'vdm2018_scan1_X_bx%s_PV.txt'%bxId 
DumpCSVFromPVFitTitle(fname,'a+')

for irun, ibs in allBS.iteritems():
    for ival in ibs.values():
        ival.DumpCSVFromPVFit(fname,'a+')


# check drifts and create CSV in the default format
fname_def = 'vdm2018_scan1_X_bx%s_default.txt'%bxId 
DumpCSVTitle(fname_def,'a+')

for irun, ibs in allBS.iteritems():
    for ival in ibs.values():
        ival.DumpCSV(fname_def,'a+')


# check drifts and create file for plotting
fnamePlots = 'vdm2018_scan1_X_bx%s_forPlots.txt'%bxId 
for irun, ibs in allBS.iteritems():
    for ival in ibs.values():
        ival.Dump(fnamePlots,'a+')


merged_payload = Payload(fnamePlots)
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
    histos.append(merged_payload.plotByTime(ivar , 318984, 319018, savePdf = True, dilated = 5, byFill = False, returnHisto = True, additionalString='bx%s_'%bxId ))
#     histos.append(merged_payload.plotByTime(ivar , 319018, 319019, savePdf = True, dilated = 5, byFill = False, returnHisto = True, additionalString='bx%s_'%bxId ))

histo_file = ROOT.TFile.Open('histos_test.root', 'recreate')
histo_file.cd()
for histo in histos:
    histo.Write()

histo_file.Close()



