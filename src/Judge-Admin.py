import os
import sys
from datetime import datetime
import time

#GETTING DOCKERS FROM QUEUE AND ANALYSING
path_host		= "/pradnya"
queue_path		= path_host + "/queue"

#INITIATING JUDGE...
os.system("clear")
print ("Welcome...")
print ("Press Enter to start the judgements...")
raw_input()

try:
	dock_index_f = open(queue_path + "/done", "r+")
except Exception, e:
	dock_index_f = open(queue_path + "/done", "w+")
	dock_index_f.write("0")
	dock_index_f.close()
	dock_index_f = open(queue_path + "/done", "r+")

docker_index_done = dock_index_f.readline()
dock_index_f.close()
if(docker_index_done=="" ): docker_index_done=0
docker_index_done = int(docker_index_done)

tmp=0;
while 1:
	try:
		index_f = open(queue_path + "/index", "r+")
	except Exception, e:
		index_f = open(queue_path + "/index", "w+")
		index_f.write("0")
		index_f.close()
		index_f = open(queue_path + "/index", "r+")	

	index = index_f.readline()
	index_f.close()

	if(index==""): index=0;
	index = int(index)
	if(docker_index_done < index):
		os.system("clear")
		docker_index_done +=1
		queue_f = open(queue_path + "/queue" + str(docker_index_done),"r+");
		print "Analysis Started ===> "  + str(docker_index_done) + "/" + str(index)
		com = queue_f.readline() 
		os.system(com);
		
		queue_f.close()
		dock_index_f = open(queue_path + "/done", "w+")
		dock_index_f.write(str(docker_index_done))
		dock_index_f.close()
		com = com.split()
		print "Submission Analysed ===> [ " + str(com[len(com)-2]) + " ] " + str(docker_index_done) + "/" + str(index) 
		if(not os.path.isfile("/pradnya/pradnya/submissions/" + str(com[len(com)-2])+ "/q" + str(com[len(com)-3]) + "/s" + str(com[len(com)-1]) + "/result.txt")):
			path_to_testcase 	= "/pradnya/pradnya/input/q" + str(com[len(com)-3]) + "/test"
			tcount = 6
			result = open("/pradnya/pradnya/submissions/" + str(com[len(com)-2])+ "/q" + str(com[len(com)-3]) + "/s" + str(com[len(com)-1]) + "/result.txt", "w+")
			for x in range(tcount):
				result.write("-1\n")
			result.close()
	
	time.sleep(.2)

