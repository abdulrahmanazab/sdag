# Example 2
Similar to example1, but having the C job exiting with error (replacing ``jobC.sbatch`` with ``jobC_err.sbatch``). This will cause job D to be cancelled from the queue once job C fails. The workflow description file is ``dag_err.sdag``
