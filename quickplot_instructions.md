# Instruction to produce a new beamspot payload 

These instruction explains how to fit a new beamspot in a given run, alignment and release, and how to create a new payload from the fit results for a new global tag. An example is described at the end.

## work space setup

Download your favourite CMSSW release, e.g. *13_2_0_pre3*

```bash
cmsrel CMSSW_13_2_0_pre3
cd CMSSW_13_2_0_pre3/src
cmsenv
```

Fetch the beamspot tools and compile

```bash
git-cms-addpkg RecoVertex/BeamSpotProducer
cd RecoVertex/BeamSpotProducer/python
git clone https://github.com/MilanoBicocca-pix/BeamspotTools.git
cd $CMSSW_BASE/src
scram b -r -j8
```

The *uncertainty* python module is used in some scripts. It should be included in recent CMSSW releases, if not:

```bash
pip install --user uncertainties
```

## beamspot fit

The beamspot fit is configured by the [BeamFit_custom_workflow.py](python/BeamspotTools/test/BeamFit_custom_workflow.py) file, which is an extension  of the standard *BeamFit_\*_Workflow.py* configuration files. To run the fit:

```bash
cmsRun BeamFit_custom_workflow.py     \
  jobName="name"                        \
  globalTag="tag"                       \
  refit=bool                            \
  runs="run:ls-run:ls"                  \
  dataset="/dataset/period/tier"        \
  storage="root://service"              \
  highPurity=bool                       \
  tracks="collection_name"              \
  alignment="record1:tag1,record2:tag2" \
  saveRootFiles=bool
```

where:
- **jobName** is the string used to create the output file names (default: beamspotFit).
- **globalTag**<sup>(\*)</sup> is the global tag (default: '').
- **refit** decides whether to re-run the track refit and consequently the vertex finding (default: false). Remember to set true when changing the tracker alignment and whatnot.
- **runs** is the run range in the form "run:ls-run:ls,run:ls[...]" (default: 0:min-999999:max - all runs).
- **dataset**<sup>(\*\*)</sup> is the input dataset. The code will fetch the input files from DAS. If the *inputFiles* argument is passed, it will be used instead (default: ''). The */StreamExpress/Run\*/ALCARECO* and */ZeroBias/Run*\*/RAW* datasets can be used.
- **storePrepend** in case files should be fetched from a specific store (default: '' - auto)
- **highPurity** decides whether to use a high purity track selection (default: false)
- **tracks** is the input track collection, which depends on the type of input dataset (default: generalTracks)
- **updateGT** is used to update records, tags and labels in the global tag. Defined in the form "record1:tag1:label1,record2:tag2:label2,[...]".
- **saveRootFile** decides whether to save the fit results to a *.root* file. Usually needed only for debugging.

*<sup>(\*)</sup>&nbsp;&nbsp;&nbsp;the argument is mandatory*  
*<sup>(\*\*)</sup>&nbsp;the argument or --inputFiles is mandatory*  

The result of the fit will be a *.txt* file containing the list of runs and the fit results in some format **not** compatible with the CMS database (see below how to convert this file to a *.db* file).  
If the *saveRootFile* argument is set to *true*, a *.root* file will be created containing the fit results. Both the *.txt* and *.root* file name are set by the *jobName* argument.   
A file with the "_filelist.txt" prefix is also creted. It contains the list of files used in the fit (**NOTE**: if specific lumisections are analyzed by setting the *runs* argument, the fitter might consume more files than needed as there is no way to fetch single lumisections from DAS. These files will also appear in this list but their content will be skipped).  
(NOT YET) A file with the "_cfg.py" prefix will be written and will contain the full configuration of the job.
  
**NOTE** the track collection from *ALCARECO* is *ALCARECOTkAlMinBias*, for *RAW* the label is *generalTracks*.  
**NOTE** Other parameters of the fitter are present in the configuration file and usually there is no need to modify them.  
**NOTE** by default, the fit is run on five lumisections. This can be changed by editing the parameters (note: set them equal).  
**NOTE** if a track refit is done and the alignment is not changed, the beamspot result will still be different. This is because, in such case, the configuration introduces additional cuts on the PVs.
**NOTE** the fitter appends the results of the fit to the *.txt* file live, thread safety is **NOT** guaranteed.

## beamspot plot

**NOTE** the plotting script is a work in progress. At the moment it can plot a single file in a format good for check-ups (bs parameter vs. time). For instructions on how to produce complete BS plots, see [here]().
**NOTE** this script does not work with any CMSSW release. Python 3 is required. All the modules used should be available in the default python3 distribution, except [ROOT](https://root.cern/).
**NOTE** [auth-get-sso-cookie](https://gitlab.cern.ch/authzsvc/tools/auth-get-sso-cookie) is required. This is available by default on lxplus or can be installed user-side following the instructions of the repo.
**NOTE** a valid kerberos ticket is required to download data from OMS.

To plot the results, run [plotFromTxt.py](BeamspotTools/python/plot/plotFromTxt.py):

```bash
python3 plotFromTxt.py --input input_file_list --output output_dir --streams 5
```

where 
- *--input* is the list of input *.txt* files produced by the BeamSpotProducer (*NOTE* currently works with a single file)
- *--output* is the output directory
- *--streams* is the number of parallel requests made to OMS (default: 1)
- *--canfail* is a boolean which allows to select failed BS fits (type!=2 in the *.txt* file) (default: false)

The script will communicate with OMS to fetch date information for each lumisection and other paramters of the fill. This may take some time, depending on the number of lumisections selected.  
The script will create the output directory and plot the beam spot parameters as a function of time (run / lumisection) in epoch format.

## payload creation

WIP
To convert the fit results in the payload format, ready for the new GT, run:

```bash
```

## example

We want to fit the beamspot on ALCARECO files for run 370772 of 2023D, updating the tracker alignemtn tag to *TrackerAlignment_collisions23_forHLT_v5*. We will use a single local file from the */StreamExpress/Run2023D-TkAlMinBias-Express-v2/ALCARECO* dataset (to run on the full run, use *--dataset=dataset_name* instead of *--inputFiles*)

```bash
xrdcp root://cms-xrd-global.cern.ch//store/express/Run2023D/StreamExpress/ALCARECO/TkAlMinBias-Express-v2/000/370/772/00001/63cbf285-ce54-4ad2-bc9b-833799330067.root AlcaFile_2023D.root
cmsRun BeamFit_flexible_workflow.py         \
  jobName="localTest_refit_alignmentUpdate" \
  inputFiles="file:AlcaFile_2023D.root"     \
  runs="370772:min-370772:max"              \
  globalTag="130X_dataRun3_Express_v3"      \
  tracks=ALCARECOTkAlMinBias                \
  refit=True                                \
  updateGT="TrackerAlignmentRcd:TrackerAlignment_collisions23_forHLT_v5"
```
The result can be compared to running without the *--updateGT* argument to see the effect of the new alignment.  
  
To plot and check the result:

```bash
python3 plotFromTxt.py --input --output Run2023_370772
```
