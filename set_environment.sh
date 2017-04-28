#!/bin/bash

# set path to look python bits for
echo "adding base Beamspot directory to PYTHONPATH"
echo $PWD
export PYTHONPATH=$PWD:$PYTHONPATH
export BSBASE=$PWD

# also touch __init__.py files, just in case
touch data/__init__.py
touch objects/__init__.py
touch plot/__init__.py
touch utils/__init__.py
touch test/__init__.py

