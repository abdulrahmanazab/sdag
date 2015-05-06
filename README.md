# sdag
Direct Acyclic Graph (DAG) Submitter for SLURM queueing system

This is workflow manager for [SLURM](http://slurm.schedmd.com/) for submitting DAG based workflows. It is a similar but a very simple implementation to [HTCondor DAGMan](http://research.cs.wisc.edu/htcondor/manual/v7.8/2_10DAGMan_Applications.html).

To use sdag for submitting your workflow, you need to do the folowing:
* create a [SLURM script](http://slurm.schedmd.com/sbatch.html#lbAH) for each workflow step.
* Create a DAG description file for your workflow.
* Submit your workflow by: ``sdag <workflow-description-file> ``

Example
--------

```  
      B
     / \
--> A   D -->
     \ /
      C
```
