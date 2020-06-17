import os
import sys

def get_result(l, q, t, s):
	LANG_ID			= str(l)
	QUES_NO			= str(q)
	TEAM			= str(t)
	SUB_ID			= str(s)
	CPU_SET 		= "0-3"
	MEMORY_HARD		= "100M"
	MEMORY_SOFT		= "50M"
	MEMORY_SWAP		= "100M"
	MEMORY_KERNAL	= "50M" 
	SRC1			= "/pradnya/pradnya/input/q" + QUES_NO
	DEST1			= "/tmp/input"
	SRC2			= "/pradnya/pradnya/submissions/" + TEAM + "/q" + QUES_NO + "/s" + SUB_ID
	DEST2			= "/tmp/submissions"
	SRC3			= "/pradnya/pradnya/script"
	DEST3			= "/tmp/script"
	SRC4			= "/pradnya/pradnya/files"
	DEST4			= "/tmp/files/"

	TIMEOUT			= str(15)
	COMMAND			= "python3 script/script.py"
	ARGS = LANG_ID + " " + QUES_NO + " " + TEAM + " " + SUB_ID 
	
	#INSERTING INTO QUEUE
	path_host		= "/pradnya"
	queue_path		= path_host + "/queue"
	

	index_f = open(queue_path + "/index","r")
	index = index_f.readline()
	if(index==""): index=0; 	
	index = int(index)+1
	
	index_f.close()

	queue_f = open(queue_path + "/queue" + str(index),"w+");
	os.system("chown " + str(index) + " " + SRC2)
	os.system("chmod -R 777 " +  SRC2)
	
	cmd = (	"docker run  --rm " + 
				" --user " + str(index) + " " +
				" --cpuset-cpus " + CPU_SET + 
				" -m " + MEMORY_HARD +
				" --memory-reservation " + MEMORY_SOFT +
				#" --kernel-memory " + MEMORY_KERNAL +
				#" --memory-swap " + MEMORY_SWAP +
				" --ulimit nproc=100 " +
				" -v " + SRC1 + ":" + DEST1 + ":ro " +
				" -v " + SRC2 + ":" + DEST2 + 
				" -v " + SRC3 + ":" + DEST3 + ":ro " +
				" -v " + SRC4 + ":" + DEST4 + ":ro " +

				"-t ubuntu " + 
				"timeout " + TIMEOUT + " " + 
				COMMAND +" " +  ARGS)

	queue_f.write(cmd);
	queue_f.close();
	index_f = open(queue_path + "/index","w+")
	index_f.write(str(index))
	index_f.close();

	'''
	path_sub1			= path_host + "/submissions"
	path_sub2			= path_sub1 + "/" + str(TEAM)
	path_sub3			= path_sub2 + "/" + "q" + str(QUES_NO)
	path_sub4			= path_sub3 + "/" + str(SUB_ID)


	comp_f = open(path_sub4 + "/result.txt", "r")
	arr = []
	for x in comp_f:
		arr.append(int(x[0]))
	return arr
	'''


get_result(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


