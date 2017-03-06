#!/bin/tcsh

# set path to look python bits for
echo "adding base Beamspot directory to PYTHONPATH"
echo $PWD
setenv PYTHONPATH $PWD:$PYTHONPATH
setenv BSBASE $PWD

