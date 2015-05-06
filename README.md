# SLURM DAG Manager 'sdag'
Direct Acyclic Graph (DAG) Submitter for SLURM queueing system

This is workflow manager for [SLURM](http://slurm.schedmd.com/) for submitting DAG based workflows. It is a similar but a very simple implementation to [HTCondor DAGMan](http://research.cs.wisc.edu/htcondor/manual/v7.8/2_10DAGMan_Applications.html).

To use sdag for submitting your workflow, you need to do the folowing:
* Create a [SLURM script](http://slurm.schedmd.com/sbatch.html#lbAH) for each workflow job.
* Create a DAG description file for your workflow.
* Submit your workflow by: ``sdag`` <i>workflow-description-file</i>

Structure
----------
The workflow description file includes two types of statements:
* <b>Job description</b>: ``JOB``<i>job-name job-script-file-path</i>. This must be provided for each job in the workflow. The keyword ``JOB`` is case sensitive, and is separated from the job script file path using space or tab. 
* <b>Workflow</b>: ``PARENT``<i>parent-jobs-list</i> ``CHILD`` <i>child-jobs-list</i>. Upon the submission, each child job will be submitted with dependency on all parent jobs. A child job won't start before all parent jobs are completed, i.e. ended with exit code 0. If any of the parent jobs fails, all child jobs will be cancelled. This means that there will be no orphan jobs. see [Job dependencies - SLURM](https://www.hpc2n.umu.se/batchsystem/dependencies/abisko). A parent/child job list must be either space or tab separated.

Guidelines
----------
You need to follow these guidelines when using <b>sdag</b>:
* You must provide a valid workflow description file. If not, <b>sdag</b> will return:``Error: You must enter a valid DAG description file`` 
* You must provide a valid job description file path in each job description statement. If not, <b>sdag</b> will return:``Error in line [XX]: XX.sbatch is not a file.`` 
* In case of a wrong syntax in a job description statement, <b>sdag</b> will return: 
```
Error in line [XX]: A job definition statement must be written as:
JOB <job_name> <job_submission_file>
```
* In case of a wrong syntax in a workflow statement, <b>sdag</b> will return: 
```
Error in line [XX]: A workflow Statement must be written as:
PARENT <parent_jobs> CHILD <children_jobs>
```
* In a workflow statement, if one of the child jobs is already defined in a previous workflow statement as a parent for one of the parent jobs, or one of their ancestors, <b>sdag</b> will return: 
```
Error in line [XX]: Job YY Cannot be a parent for job ZZ. Job ZZ is an ancestor of job YY
```
Example1
--------
This example is prepared to run on the [Abel Cluster](http://www.uio.no/english/services/it/research/hpc/abel/) at the [University of Oslo](www.uio.no).

To submit a workflow with four jobs (A, B, C, and D) with the following structure:
```  
           B
          / \
start--> A   D -->end
          \ /
           C
```
Four jobs scripts are included: ``jobA.sbatch``, ``jobB.sbatch``, ``jobC.sbatch``, and ``jobD.sbatch``. The workflow description file is ``dag.sdag`` with the following contents:
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
* * A job name.
An example, when running:
```
python test.py input.txt outA.txt 30 A
```
The output will be:
```
Job[A] Run on machine: compute-10-16.local      Slept for 30 seconds
---------------FILE input.txt STARTED HERE---------------------
This is a test text input file...
---------------FILE input.txt ENDED HERE---------------------
```
To submit the workflow, type:
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
* <b>Job ID</b>: the real job indentifier after submitting the job to SLURM. It can be used to check the status of the job.
* <b>Job parents</b>: a comma separated list of jobs on which the job is dependent.
* <b>Job children</b>: a comma separated list of jobs which are dependent on this job.

Example2
--------
Similar to example1, but having the C job exiting with error (replacing ``jobC.sbatch`` with ``jobC_err.sbatch``). This will cause job D to be cancelled from the queue once job C fails. The workflow description file is ``dag_err.sdag``

Prerequisites
--------------
* Python 2.7+
* [sbatch](https://computing.llnl.gov/linux/slurm/sbatch.html)
* Add ``sdag`` to ``PATH``

Support and Bug Reports
-------------------------------
Report an issue on the [issues](https://github.com/abdulrahmanazab/sdag/issues) section or send an email to azab@usit.uio.no
