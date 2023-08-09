import FWCore.ParameterSet.Config       as cms
import FWCore.ParameterSet.VarParsing   as VarParsing
import os

def get_run_ranges(run_string):
    ''' get a list of tuples from the luminosity range string format "run1:ls1-run2:ls2,[...]"
    '''
    ranges = [( int(run.split('-')[0                ].split(':')[0]),
                int(run.split('-')[int('-' in run)  ].split(':')[0])
    ) for run in run_string.split(',')]
    assert all(r2>=r1 for (r1,r2) in ranges), "ERROR: run ranges are ill defined"
    return ranges

# input arguments
options = VarParsing.VarParsing('analysis')
options.inputFiles = ''
options.maxEvents  = -1
options.register('jobName', 'beamspotFit',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "determines the output files names"         ,
)
options.register('globalTag', '',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "global tag to be used"                     ,
)
options.register('refit', False,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.bool          ,
    "whether to refit the tracks or not"        ,
)
options.register('runs', '0:min-9999999:max'    ,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "lumirange in the format 'run:ls-run:ls,run:ls[...]'",
)
options.register('dataset', ''                  ,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "input dataset"                             ,
)
options.register('storePrepend', '',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "explicitly set the xroot store path used to read the dataset (root://server.somewhere/)",
)
options.register('highPurity', False,
    VarParsing.VarParsing.multiplicity.singleton  ,
    VarParsing.VarParsing.varType.bool            ,
    "additional selections on tracks and vertices",
)
options.register('tracks', 'generalTracks',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "track collection to be used"               ,
)
options.register('updateGT', ''             ,
    VarParsing.VarParsing.multiplicity.list ,
    VarParsing.VarParsing.varType.string    ,
    "records, tags and labels to update in the form record1:tag1:label1,record2:tag2:label2,[...]",
)
options.register('saveRootFile', False              ,
    VarParsing.VarParsing.multiplicity.singleton    ,
    VarParsing.VarParsing.varType.bool              ,
    "save the fit result also in root file (debug)" ,
)
options.parseArguments()

# fetch the file list from the dataset using dasgoclient or from an input
if options.inputFiles==['']:
    runranges = get_run_ranges(options.runs)
    dasquery  = 'dasgoclient --query="file dataset={D} run in [{L},{H}]"'
    filelist_ = [os.popen(dasquery.format(
        D=options.dataset, L=rrange[0], H=rrange[1]
        )).readlines() for rrange in runranges
    ]
    filelist = [f.strip('\n') for rfiles in filelist_ for f in rfiles]
    filelist = [options.storePrepend+f for f in filelist]
else:
    filelist = options.inputFiles

with open(options.jobName+'_filelist.txt', 'w') as filefile:
    filefile.write('\n'.join(filelist))

process = cms.Process("BSworkflow")

# source files
process.source      = cms.Source("PoolSource", 
    fileNames       = cms.untracked.vstring(*filelist),
    lumisToProcess  = cms.untracked.VLuminosityBlockRange(options.runs) 
)

process.maxEvents   = cms.untracked.PSet(input=cms.untracked.int32(-1))
process.options     = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

# message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.debugModules   = ['BeamSpotAnalyzer']
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(reportEvery = cms.untracked.int32(1000))

# global tag for the Express, to be consistent with the file above
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff") 
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff") 
process.GlobalTag.globaltag = options.globalTag
if options.updateGT!=['']:
    align_psets = [
        cms.PSet(record=cms.string(r), tag=cms.string(t), label=cms.untracked.string(l)) 
        for r,t,l in [o.split(':') for o in options.updateGT]
    ]
    process.GlobalTag.toGet = cms.VPSet(*align_psets)

# Track and PV refit
INPUT_TRACKS = 'TrackRefitter'                          if options.refit else options.tracks
INPUT_PVS    = 'offlinePrimaryVerticesFromRefittedTrks' if options.refit else 'offlinePrimaryVertices'
if bool(options.refit):
    process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
    process.TrackRefitter.src = options.tracks
    process.TrackRefitter.NavigationSchool = ''
    
    process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
    from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
    process.offlinePrimaryVerticesFromRefittedTrks  = offlinePrimaryVertices.clone()
    process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                   = cms.InputTag(INPUT_TRACKS) 
    process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam          = 1
    process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2         = 20
    process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits  = 5
    process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance         = 5.0 
    process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits    = 2   

# beamspot fitter
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = options.jobName+'.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = False
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers        = 6
process.d0_phi_analyzer.BeamFitter.OutputFileName            = options.jobName+'.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = INPUT_TRACKS
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = options.saveRootFile
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = options.saveRootFile
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = options.saveRootFile
   
process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10 
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = INPUT_PVS 
   
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1

if options.highPurity:
    d0_phi_analyzer_cff.PVFitter.useOnlyFirstPV     = True
    d0_phi_analyzer_cff.PVFitter.minSumPt           = 50.0
    d0_phi_analyzer_cff.PVFitter.minVertexNTracks   = 30

process.p = cms.Path(   
    process.offlineBeamSpot                        + 
    process.TrackRefitter                          + 
    process.offlinePrimaryVerticesFromRefittedTrks +
    process.d0_phi_analyzer                        
) if options.refit else cms.Path(
    process.offlineBeamSpot + 
    process.d0_phi_analyzer                        
)
