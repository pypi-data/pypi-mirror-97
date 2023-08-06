#!/bin/bash

export RESCOV=${PWD}/coverage_results.txt
tulist="tuPaveList.py tuPlaneCut.py tuWaveGeom.py tuPoserMeshed.py tuFigure.py tuPoserFile.py tuQSlim.py tuWFBasic.py"

# Compute Current version
pp3dv=`(export PYTHONPATH=${PYTHONPATH}:${PWD}/src ; python3 -c "import pypos3d; print(pypos3d.__version__)" )`

echo "Unit Tests of pypos3d version" $pp3dv "on" `date` 
echo "Unit Tests of pypos3d version" $pp3dv "on" `date` > $RESCOV

# To be executed before SVN commit

# Launch all Unitests

cd src/pypos3dtu 
PYTHONPATH=${PWD}/..
export PYTHONPATH

# Check results dirs (for distributed packages)
[[ -d tures ]] || mkdir tures
[[ -d tulog ]] || mkdir tulog

for tumod in $tulist
  do
  python3 -m unittest ${tumod} > tulog/${tumod}.log 2>&1 && echo `date --rfc-3339=s` $tumod "Success" >> $RESCOV  &
  done
wait $(jobs -p)

# Clean Coverage DB
rm -f .coverage*
for tumod in $tulist
  do
  # coverage run --append --source=../src/pypos3d -m unittest ${tumod} > tures/${tumod}.log 2>&1 && echo `date --rfc-3339=s` $tumod "Cov Success" 2>&1 $RESCOV
  coverage run --parallel-mode --source=../pypos3d -m unittest ${tumod} > tures/${tumod}.log 2>&1 && echo `date --rfc-3339=s` $tumod "Cov Success" 2>&1 $RESCOV &
  done
wait $(jobs -p) 

# Combine the various .coverage* files into one .coverage
coverage combine --append

# Generate Coverage Report
# cd ../.metadata/.plugins/org.python.pydev.debug/coverage/
coverage report  >> ${RESCOV}
cd -

# Clean tures
rm -f src/pypos3dtu/tures/*
