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
Create four SLURM submission scripts, for the four jobs as JOB
```
JOB A jobA.sbatch
JOB B jobB.sbatch
JOB C jobC.sbatch
JOB D jobD.sbatch
PARENT A CHILD B C
PARENT B C CHILD D
```
