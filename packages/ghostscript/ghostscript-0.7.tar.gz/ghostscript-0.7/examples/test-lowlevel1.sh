#!/bin/sh

if [ -z "$PYTHON" ] ; then PYTHON=python ; fi

cd $(dirname $0)
PYTHONPATH=$(realpath ..):$PYTHONPATH

$PYTHON ./lowlevel1.py
