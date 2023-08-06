#!/bin/sh

if [ -z "$PYTHON" ] ; then PYTHON=python ; fi

cd $(dirname $0)
PYTHONPATH=$(realpath ..):$PYTHONPATH

$PYTHON ./lowlevel2.py \
    -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -sOutputFile=/tmp/out.pdf \
    -c .setpdfwrite -f ./test.ps
