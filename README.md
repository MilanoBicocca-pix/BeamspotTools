# Beamspot Tools

Standalone package to handle beam spot stuff

## Installation under CMSSW 
```shell
  cmsrel CMSSW_X_Y_Z  
  cd CMSSW_X_Y_Z/src
  cmsenv
  git-cms-addpkg RecoVertex/BeamSpotProducer
  cd RecoVertex/BeamSpotProducer/python
  git clone https://github.com/MilanoBicocca-pix/BeamspotTools.git
  cd $CMSSW_BASE/src
  scram b -r -j8
```


## Installation as standalone
```shell
  git clone https://github.com/MilanoBicocca-pix/BeamspotTools.git
  cd BeamspotTools
  source set_environment.[c]sh   # this adds the base BeamspotTools directory to your PYTHONPATH variable 
```

## Installation of python package 'uncertainties'  

This is used in BeamSpot class to correctly propagate the uncertainties when computing the proper beam spot width from projections and tilts.  

For the package information:  
https://pythonhosted.org/uncertainties/

```shell
  # local installation, e.g. on lxplus, by default this points to the python2.6 library
  pip install --user uncertainties
  # but you need to have uncertainties available in python2.7, which is CMSSW's python, so, in a fresh shell do
  scl enable python27 csh
  pip install --user uncertainties
```

