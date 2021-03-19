#!/bin/bash

export PYTHONPATH=$PWD/../:$PYTHONPATH
pytest --cov=userdata_mining --cov-report=xml ../

if [ "$1" = "--coverage" ]; then
    coverage report -m --skip-covered --sort=cover
fi
