# sdag
Direct Acyclic Graph (DAG) Submitter for SLURM queueing system

This is workflow manager for SLURM for submitting DAG based workflows. It is a similar but a very simple implementation to [HTCondor DAGMan](http://research.cs.wisc.edu/htcondor/manual/v7.8/2_10DAGMan_Applications.html).
  
      B
     / \
--> A   D -->
     \ /
      C

