# Example 1
--------
This example is prepared to run on the [Fox Cluster](https://www.uio.no/english/services/it/research/platforms/edu-research/help/hpc/docs/fox/index.md) at the [University of Oslo](www.uio.no).

To submit a workflow with four jobs (A, B, C, and D) with the following structure:
```  
           B
          / \
start--> A   D -->end
          \ /
           C
```
Four jobs scripts are included: ``jobA.sbatch``, ``jobB.sbatch``, ``jobC.sbatch``, and ``jobD.sbatch``. The workflow description file is ``example1.sdag`` with the following contents:
```
JOB A jobA.sbatch
JOB B jobB.sbatch
JOB C jobC.sbatch
JOB D jobD.sbatch
PARENT A CHILD B C
PARENT B C CHILD D
```
Each job is calling a python script ``test.py``, which takes the following arguments:
* A comma separated list of input files.
* An output file name.
* An integer indicating the runtime in seconds.
* A job name.

An example, having an input file ``input.txt`` with the following contents:
```
This is a test text input file...
```
Then running:
```
python test.py input.txt outA.txt 30 A
```
The output ``outA.txt`` will contain the following:
```
Job[A] Run on machine: compute-10-16.local      Slept for 30 seconds
---------------FILE input.txt STARTED HERE---------------------
This is a test text input file...
---------------FILE input.txt ENDED HERE---------------------

```
**To submit the workflow, type:**
```
module load Python/2.7.15-GCCcore-8.2.0
cd sdag/example1
python ../sdag example1.sdag
```
**You will get an output like the following:**
```
Job A   ID: 11008698
Parents:
Children: C,B

Job B   ID: 11008700
Parents: A
Children: D

Job C   ID: 11008699
Parents: A
Children: D

Job D   ID: 11008701
Parents: C,B
Children:
```
For each job, four values are displayed:
* <b>Job name</b>: given in the workflow description.
* <b>Job ID</b>: the real job indentifier after submitting the job to SLURM. It can be used to check the status of the job.
* <b>Job parents</b>: a comma separated list of jobs on which the job is dependent.
* <b>Job children</b>: a comma separated list of jobs which are dependent on this job.

