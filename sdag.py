import sys,getopt,os,subprocess

class SLURM_DAGMan(object):
    
    def __init__(self, dagFile):
        self.dagFile = dagFile
        self.jobs = []
    
    def parse(self):
        with open(self.dagFile) as f:
            lines = f.readlines()
            for i,line in enumerate(lines):
                if line.startswith('#') or line.strip() == '':
                    continue
                elif line.strip().startswith('JOB'):
                    try:
                        lineItems = line.split()
                        job = {}
                        job['name'] = lineItems[1]
                        scriptFile = lineItems[2]
                        if not os.path.isfile(scriptFile):
                            self._Error(i,10,scriptFile+' is not a file.')
                    except:
                        self._Error(i,2)
                    job['script'] = scriptFile
                    job['parents'] = set()
                    job['children'] = set()
                    job['ID'] = None
                    self.jobs.append(job)
                
                elif line.strip().startswith('PARENT'):
                    try:
                        jobs =  line.strip().lstrip('PARENT').split('CHILD')
                        if len(jobs) != 2:
                            self._Error(i,1)
                    except:
                        self._Error(i,1)
                    parents_names = jobs[0].split()
                    children_names = jobs[1].split()
                    parents = [self._getJob(i,name) for name in parents_names]
                    children = [self._getJob(i,name) for name in children_names]
                    for job in parents:
                        ancestors = self._getJobAncestors(job['name'])
                        if ancestors is not None:
                            for child in children_names:
                                if child in ancestors:
                                    self._Error(i,10,'Job '+job['name']+\
                                                ' Cannot be a parent for job '+child+\
                                                '. Job '+child+\
                                                ' is an ancestor of job '+job['name'])
                        job['children'].update(children_names)
                    for job in children:
                        job['parents'].update(parents_names)
                else:
                    self._Error(i,0)
    
    def _getJobAncestors(self,jobName):
        job = self._getJob('#',jobName)
        aList = set()
        parents = list(job['parents'])
        if len(parents) == 0:
            return
        for parent in parents:
            aList.add(parent)
            gParents = self._getJobAncestors(parent)
            if not gParents is None:
                aList.update(gParents)
        return list(aList)
    
    def run(self):
        for job in self.jobs:
            if len(job['children']) == 0:
                self._submit(job['name'])
        
    
    def _submit(self,jobName):
        job = self._getJob('#',jobName)
        commandList = ['sbatch']
        if len(job['parents']) > 0:
            parents = [self._getJob('#',name) for name in list(job['parents'])]
            dependencies = '--dependency=afterok:'
            parentIDs = []
            for parent in parents:
                if parent['ID'] is None:
                    parent['ID'] = self._submit(parent['name']).decode('utf-8')
                parentIDs.append(parent['ID'])
            dependencies += ':'.join(parentIDs)
            commandList.append(dependencies)
        
        commandList.append(job['script'])
        
        p = subprocess.Popen(commandList, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
        out, err = p.communicate()
        
        #out = subprocess.check_output(' '.join(commandList), stderr=subprocess.STDOUT)
        
        if out.strip()==b'':
            self._Error('#','#','Error submitting job '+jobName+'\n'+str(err))
        else:
            job['ID'] = out.strip(b'\n').split()[-1]
            #print 'submitted:\n' + ' '.join(commandList)
            #print out
            return job['ID']
        
    def _getJob(self,lineNo,jobName):
        for job in self.jobs:
            if job['name'] == jobName:
                return job
        self._Error(lineNo,10,'Job '+jobName+' is not defined')
        
    def _Error(self,lineNo,errorNo, message = ''):
        if lineNo == '#':
            msg = message
            print(msg, file=sys.stderr)
            os._exit(0)
        elif errorNo == 0:
            msg = 'Invalid syntax'
        elif errorNo == 1:
            msg = 'A workflow Statement must be written as:\n'+\
            'PARENT <parent_jobs> CHILD <children_jobs>'
        elif errorNo == 2:
            msg = 'A job definition Statement must be written as:\n'+\
            'JOB <job_name> <job_submission_file>'
        elif errorNo == 10:
            msg = message
            
        print('Error in line ['+str(lineNo)+']: '+ msg, file=sys.stderr)
        os._exit(0)
        
    def _getJobString(self,job):
        string = ''
        if isinstance(job['ID'], bytes):
            string+='Job '+job['name']+'\t'+'ID: '+str(job['ID'], "utf-8")+'\n'
        elif isinstance(job['ID'], str):
            string+='Job '+job['name']+'\t'+'ID: '+job['ID']+'\n'
        else:
            os._exit(0)
        string+='Parents: '+','.join(list(job['parents']))+'\n'
        string+='Children: '+','.join(list(job['children']))+2*'\n'
        return string
        
    def __str__(self):
        string = ''
        if len(self.jobs) > 0:
            for job in self.jobs:
                string+= self._getJobString(job)
        return string
        
######################################################################
def main(argv):
    if len(argv) != 1:
        print('Missing argument: DAG description file')
        sys.exit()
    arg = argv[0]
    if arg in ['-h','--help']:
        print('A simple DAG manager for SLURM.')
        sys.exit()
    else:
        dagFile = arg
        if not os.path.isfile(dagFile):
            print('Error: You must enter a valid DAG description file')
            sys.exit(1)
        dagman = SLURM_DAGMan(dagFile)
        dagman.parse()
        dagman.run()
        print(dagman)

if __name__ == "__main__":
    main(sys.argv[1:])



