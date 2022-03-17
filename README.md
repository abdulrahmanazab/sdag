# SLURM DAG Workflow Submitter
Direct Acyclic Graph (DAG) workflow submitter for [SLURM](http://slurm.schedmd.com/) queueing system

This is workflow manager for SLURM for submitting DAG based workflows. It is a similar but a very simple implementation to [HTCondor DAGMan](http://research.cs.wisc.edu/htcondor/manual/v7.8/2_10DAGMan_Applications.html).

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
Prerequisites
--------------
* Python 2.7+
* [sbatch](https://computing.llnl.gov/linux/slurm/sbatch.html)
* Add ``sdag`` to ``PATH``

Support and Bug Reports
-------------------------------
Report an issue on the [issues](https://github.com/abdulrahmanazab/sdag/issues) section or send an email to azab@usit.uio.no
