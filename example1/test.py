#!/software/VERSIONS/python2-2.7.6/bin/python
import sys,platform,time
inputFiles = sys.argv[1]
inputFilesList = inputFiles.split(',')
output = sys.argv[2]
sleep = int(sys.argv[3])
jobName = sys.argv[4]
#if len(sys.argv) > 3:
#   sleep = int(sys.argv[3])
#else:
#   sleep = 1
time.sleep(sleep)
outputLines = []
for iFile in inputFilesList:
    f = open(iFile,'r')
    lines = f.readlines()
    f.close()
    lines.insert(0,'Job['+jobName+'] Run on machine: '+str(platform.node())+'\tSlept for '+str(sleep)+' seconds\n')
    lines.insert(1,'---------------FILE '+iFile+' STARTED HERE---------------------\n')
    lines.append('---------------FILE '+iFile+' ENDED HERE---------------------\n\n')
    outputLines.extend(lines)
f = open(output,'w')
f.writelines(outputLines)
f.close()

