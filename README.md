# Beamspot Tools

Standalone package to handle beam spot stuff

## Installation under CMSSW 
```shell
  cmsrel CMSSW_X_Y_Z  
  cd CMSSW_X_Y_Z/src
  cmsenv
  git-cms-addpkg RecoVertex/BeamSpotProducer
  cd RecoVertex/BeamSpotProducer/python
  git clone git@github.com:MilanoBicocca-pix/BeamspotTools.git
  cd $CMSSW_BASE/src
  scram b -r -j8
```


## Installation as standalone
```shell
  git clone git@github.com:MilanoBicocca-pix/BeamspotTools.git
  cd BeamspotTools
  source set_environment.[c]sh   # this adds the base BeamspotTools directory to your PYTHONPATH variable 
```




