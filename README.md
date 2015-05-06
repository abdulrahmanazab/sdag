# sdag
Direct Acyclic Graph (DAG) Submitter for SLURM queueing system

This is workflow manager for [SLURM](http://slurm.schedmd.com/) for submitting DAG based workflows. It is a similar but a very simple implementation to [HTCondor DAGMan](http://research.cs.wisc.edu/htcondor/manual/v7.8/2_10DAGMan_Applications.html).

To use sdag for submitting your workflow, you need to do the folowing:
* Create a [SLURM script](http://slurm.schedmd.com/sbatch.html#lbAH) for each workflow job.
* Create a DAG description file for your workflow.
* Submit your workflow by: ``sdag <workflow-description-file> ``

Example
--------
To submit a workflow with four jobs (A, B, C, and D) with the following structure:
```  
           B
          / \
start--> A   D -->end
          \ /
           C
```
Create four SLURM submission scripts, for the four jobs as: ``jobA.sbatch``, ``jobB.sbatch``, ``jobC.sbatch``, and ``jobD.sbatch``. Then create the workflow description file, ``dagtest.sdag`` with the following contents:
```
JOB A jobA.sbatch
JOB B jobB.sbatch
JOB C jobC.sbatch
JOB D jobD.sbatch
PARENT A CHILD B C
PARENT B C CHILD D
```
Finally, submit your workflow by:
```
sdag dagtest.sdag
```
You will get an output like the following:
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
* Job ID: the real job indentifier after submitting the job to SLURM. It can be used to check the status of the job.
* Job parents: a comma separated list of jobs on which the job is dependent, i.e. the job won't start before these jobs end with exit code 0.
* Job children: a comma separated list of jobs which are dependent on this job.
