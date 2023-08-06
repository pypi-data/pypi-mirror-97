#!/bin/sh

if [ -z "$PYTHON" ] ; then PYTHON=python ; fi

cd $(dirname $0)
PYTHONPATH=$(realpath ..):$PYTHONPATH

$PYTHON ./ps2pdf.py ./test.ps /tmp/out.pdf
