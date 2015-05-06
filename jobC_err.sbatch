#!/bin/bash

# Job name:
#SBATCH --job-name=j1
#
# Project:
#SBATCH --account=staff
#
# Wall clock limit:
#SBATCH --time=00:01:00
#
# Max memory usage:
#SBATCH --mem-per-cpu=4000

## Set up job environment
source /cluster/bin/jobsetup

## Copy input files to the work directory:
cp test.py $SCRATCH
cp outA.txt $SCRATCH


## Make sure the results are copied back to the submit directory (see Work Directory below):
chkfile outC.txt

## Do some work:
cd $SCRATCH
python test_err.py outA.txt outC.txt 20 C
