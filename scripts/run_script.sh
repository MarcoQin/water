#!/bin/bash

argc=$#
BASEDIR=$(dirname "$0")

if [ $argc -eq 0 ]
then
    echo "Usage: $0 script_name"
else
    echo ""
    echo "Time: $(date +%Y-%m-%d--%H:%M:%S)"
    echo "Script: $1"
    cd $BASEDIR
    /usr/local/bin/python2.7 $1
    echo "--> finish now leaving $BASEDIR <--"
    echo ""
fi
