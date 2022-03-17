#!/bin/bash

# Job name:
#SBATCH --job-name=jD
#
# Project:
#SBATCH --account=ec12
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
cp outB.txt $SCRATCH
cp outC.txt $SCRATCH


## Make sure the results are copied back to the submit directory (see Work Directory below):
savefile outD.txt

## Do some work:
cd $SCRATCH
python test.py outB.txt,outC.txt outD.txt 20 D
