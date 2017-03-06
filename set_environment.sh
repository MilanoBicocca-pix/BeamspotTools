#!/bin/bash

# set path to look python bits for
echo "adding base Beamspot directory to PYTHONPATH"
echo $PWD
export PYTHONPATH=$PWD:$PYTHONPATH
export BSBASE=$PWD
