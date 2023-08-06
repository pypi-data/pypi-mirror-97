#!/bin/sh

if [ -z "$PYTHON" ] ; then PYTHON=python ; fi

cd $(dirname $0)
PYTHONPATH=$(realpath ..):$PYTHONPATH

$PYTHON ./dxmain.py -dBATCH -sDEVICE=display \
    -sDEFAULTPAPERSIZE=a5 -dFitPage ./test.ps
