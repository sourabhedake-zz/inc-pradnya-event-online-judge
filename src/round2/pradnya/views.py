from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required	
from django.shortcuts import render,redirect,render_to_response
from django.template import loader, Context
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext 
from django.core.mail import EmailMessage
import datetime,json
from django.core.exceptions import ValidationError
from pradnya.models import *
import os
from django.utils import timezone
import datetime,time,threading

global temp_score
CONTEST_RUNTIME = 2*60*60 + 30*60
ourtime=((17*60))*60
import time

def timecal():
      now=timezone.now()
      minutes=now.minute*60
      hr=now.hour*3600								#function sets the IST by adding seconds in GMT
      sec=(hr+minutes+now.second)
      ist=sec+19800
      return ist  


@csrf_exempt
def get_timer(request):
      sec1=ourtime-timecal()	
      						#7200 offset
      return HttpResponse(str(sec1))

# Create your views here.

@csrf_exempt
def firstpage(request):
		return render(request,'register.html')

@csrf_exempt
def signup(request):													#here question objects will be created along with users

	if request.POST.get("permit"):
		name1=request.POST.get("name1")
		name2=request.POST.get("name2")
		teamid=request.POST.get("username")									
		password=request.POST.get("password")
		email=request.POST.get("email")		
						#creating django users


		if name1  and teamid and password and email : 

			u2 =user.objects.filter(user_id  = teamid)
			if(len(u2)>0):
				return render(request,'register.html',{'log': 'failed'})
			else:


				user1=User.objects.create_user(teamid)
				user1.set_password(password)
				user1.first_name=name1
				user1.last_name=name2
				user1.email=email
				user1.save()

				u=user(user_id=teamid)											#creating our user
				u.save()

				new_question=u.questions_set.create(question_no=1,questionid="SNR1", questiontitle="Alternating",score_obtained=0,time_of_submission=0,total_penalty=0)		#creating question objects
				new_question=u.questions_set.create(question_no=2,questionid="SNR2", questiontitle="Birthday",score_obtained=0,time_of_submission=0,total_penalty=0)		#creating question objects
				new_question=u.questions_set.create(question_no=3,questionid="SNR3", questiontitle="Computer and Queues",score_obtained=0,time_of_submission=0,total_penalty=0)		#creating question objects
				new_question=u.questions_set.create(question_no=4,questionid="SNR4", questiontitle="Exclusive OR",score_obtained=0,time_of_submission=0,total_penalty=0)		#creating question objects
				new_question=u.questions_set.create(question_no=5,questionid="SNR5", questiontitle="Minimum cost",score_obtained=0,time_of_submission=0,total_penalty=0)		#creating question objects
				new_question=u.questions_set.create(question_no=6,questionid="SNR6", questiontitle="Triangles And Circles",score_obtained=0,time_of_submission=0,total_penalty=0)		#creating question objects

				new_question.save()
										
				return render(request,"login.html")
		else:
			u="****ALL FIELDS REQUIRED****"
			return render(request,"register.html",{'message':u})


	else:
		return render(request,"login.html")

	
@csrf_exempt
def userlogin(request):
	if timecal()>ourtime:
		print timecal(), ourtime
		return HttpResponseRedirect('/leaderboard/')
	else:
		if request.method=='POST':
			username=request.POST.get("username")
			passwd=request.POST.get("password")
			res=authenticate(username=username,password=passwd)

			if res is not None:
				print username , "logged in with passwd ", passwd
				login(request,res)
				return render(request,"home.html")
			else :
			
				return HttpResponse("failed")	
		else:
			return render(request,"login.html")

@csrf_exempt
def homepage(request):
	if timecal()>ourtime:
		return HttpResponseRedirect('/leaderboard/')
	else:
		return render(request,"home.html")



@csrf_exempt
@login_required
def question_handler(request):
	if timecal()>ourtime:
		return HttpResponseRedirect('/leaderboard/')
	else:
		q=Questions.objects.all()
		q1=list(q)
		q1.sort(key=lambda x: x.question_no)			#sorts a list of objects by its attributes
		us=request.user 						#currently logged in user
		user_id=us.username	
		q2 = Questions.objects.filter(user__user_id = user_id)
		if request.GET.get('x'):
			quest=request.GET.get('x')
			questno =0;
			for i in q:
				questno+=1
				if i.questionid==quest:
					question_obj=i
					break

			buff1=""
			buff2=""
			buff3=""
			buff4=""

			os.system("mkdir /pradnya/pradnya/submissions/"+str(user_id))
			os.system("mkdir /pradnya/pradnya/submissions/"+str(user_id) + "/q" + str(questno))
			os.system("mkdir /pradnya/pradnya/submissions/"+str(user_id) + "/q" + str(questno) + "/Buffer/")

			try:
				bf1=open("/pradnya/pradnya/submissions/" + str(user_id) + "/q" + str(questno) + "/Buffer/1","r")
				buff1 = bf1.read()
				bf1.close()
			except:
				print "Error in Buffer"
				buff1="#include <stdio.h>\nint main()\n{\n\tprintf(\"Hello World\");\n\treturn 0;\n}";

			try:
				bf2=open("/pradnya/pradnya/submissions/" + str(user_id) + "/q" + str(questno) + "/Buffer/2","r")
				buff2 = bf2.read()
				bf2.close()
			except:
				buff2="#include <bits/stdc++.h>\nusing namespace std;\nint main()\n{\n\tcout<<\"Hello World\"<<endl;\n\treturn 0;\n}";

			try:
				bf3=open("/pradnya/pradnya/submissions/" + str(user_id) + "/q" + str(questno) + "/Buffer/3","r")
				buff3 = bf3.read()
				bf3.close()
			except:
				buff3="class Pradnya{\n\tpublic static void main(String args[]){\n\t\tSystem.out.println(\"Hello World\");\n\t}\n}"

			try:
				bf4=open("/pradnya/pradnya/submissions/" + str(user_id) + "/q" + str(questno) + "/Buffer/4","r")
				buff4 = bf4.read()
				bf4.close()
			except:
				buff4="print \"Hello World\"";



			return render(request,"question"+str(question_obj.question_no)+".html",{'question':question_obj, 'buf1':buff1, 'buf2': buff2, 'buf3':buff3, 'buf4':buff4})

		else:
			return render(request,"all_questions.html",{'questions':q2})

@csrf_exempt
def submission_handler(request):											#here the judge is called
	if timecal()>ourtime:
		return HttpResponseRedirect('/leaderboard/')
	else:
		if request.GET.get('x'):	
			us=request.user 						#currently logged in user
			user_id=us.username
			
			q=Questions.objects.all()
			quest=request.GET.get('x')				#questionid
			lang=request.POST.get('language')
			if lang=="C":
				lang_id=1
				extension=".c"
			elif lang=="C++":
				lang_id=2
				extension=".cpp"
			elif lang=="Java":
				lang_id=3
				extension=".java"
			elif lang=="Python":
				lang_id=4
				extension=".py"
			
			if request.FILES:													#if user uploadds file
				for filename,file in request.FILES.iteritems():
					 name=request.FILES[filename].name							#getting data and name of the uploaded file
					 data=request.FILES[filename].read()

			else:																#else we ll see the textarea 
				data=request.POST.get('my_textarea')
			q1=Questions.objects.filter(user__user_id=user_id)								#a list of questions which have the same user as logged in user	
			qtemp=Questions.objects.filter(questionid=quest)
			qtemp=list(qtemp)
			question_no=qtemp[0].question_no

			questionid_for_judge=str(question_no)

			subcount=1;
			while (os.path.isfile("/pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/" + str(subcount))):
				subcount+=1
				pass

	 		os.system("touch /pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/" + str(subcount))
			latest_submission_id= str(subcount)
			
			os.system("mkdir /pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id))
			try:
				buff = open("/pradnya/pradnya/submissions/" + str(user_id)+"/q" +str(questionid_for_judge) +"/Buffer/" + str(lang_id), "w+")
				buff.write(data)
				buff.close
			except:
				print "Buffer not created.."
						
													#file format should be  "userid$question$submissionid"  and for java pradnya.java	
			main_string_for_judge=str(user_id)+"_"+str(questionid_for_judge)+"_"+str(latest_submission_id)	#main string for passing to judge


			if lang_id is not 3:
				os.system("touch /pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id)+"/1"+extension)
				our_file=open("/pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id)+"/1"+extension,"r+")									#creates our own file at our required destination
				our_file.write(data)
				our_file.close()
			else:
				os.system("touch /pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id)+"/Pradnya"+extension)
				our_file=open("/pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id)+"/Pradnya"+extension,"r+")									#creates our own file at our required destination
				our_file.write(data)
				our_file.close()

			os.system("touch /pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id)+"/time")
			our_file=open("/pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(questionid_for_judge)+"/s"+str(latest_submission_id)+"/time","w+")									#creates our own file at our required destination
			our_file.write(str(timecal() - (ourtime - CONTEST_RUNTIME) ))
			our_file.close()

			os.system("python /home/sourabh/testCode.py " + str(lang_id) + " " + str(questionid_for_judge) + " " + str(user_id) + " " + str(latest_submission_id))
			path_to_testcase 	= "/pradnya/pradnya/input/q" + str(questionid_for_judge) + "/test"
			tcount = 1
			
			while( os.path.isfile( path_to_testcase + str(tcount+1) )):
				tcount+=1;
			return render(request,"submission.html",{'ques' : quest ,'subid': main_string_for_judge,'tcount':range(tcount)})							#users submission page

		elif request.GET.get('result'):
			str1=request.GET.get('result')
			str2 = str1.split('_')

			path_to_testcase 	= "/pradnya/pradnya/input/q" + str(str2[1]) + "/test"
			tcount=6
			
			subpath = "/pradnya/pradnya/submissions/" + str2[0] + "/q" + str2[1] + "/s" + str2[2];
			while(not os.path.isfile( subpath + "/result.txt")):
				print "Waiting...",( subpath + "/result.txt")
				time.sleep(0.5)
				pass

			time.sleep(0.5)

			result = open( subpath + "/result.txt", "r")
			res =[]
			for x in result:
				res.append(int(x))

			result.close()
			for x in range(len(res),tcount):
				res.append(int(-1))
			print res

			str1 =""
			error=0;
			cnt1 = [0,0,0,0]
			maxscr = 0
			scrarr = [0,0,0,0,0,0]
			colarr = ["#EEE","#EEE","#EEE","#EEE","#EEE","#EEE"]

			for x in range(len(res)):
				if res[x] ==3 :
					colarr[x] = "#EBFAEB"
					if x<=3:
						maxscr+=10
						scrarr[x] = 10
					else:
						maxscr+=30
						scrarr[x] = 30
				if res[x] == 0:
					error=1;
					break;
				elif res[x]==-1:
					cnt1[0] +=1
				else:
					cnt1[res[x]-1] +=1

			strimg = ""
			total_penalty=600	
			if ( error==1):
				str1="Compile Time Error"
				strimg = "ctr.gif"
			elif(cnt1[3-1] > 0):
				total_penalty=0
				str1="Solution Accepted (AC)"
				strimg = "ac.gif"
			elif (cnt1[4-1] >0):
				str1="Wrong Answer (WA)"
				strimg = "wrong.png"
			elif (cnt1[1-1] >0):
				str1="Time Limit Exceed (TLE)"
				strimg = "tle.gif"
			else:
				str1="Run Time Error (RTE)"
				strimg = "rte.gif"


			score_for_submission=maxscr											#judge will be called here	#score and penalty will be calculated here 

			us=request.user 						#currently logged in user
			user_id=us.username
			
			q=Questions.objects.all()
			quest=request.POST.get('questionn')				#questionid

			#q1=Questions.objects.filter(user__user_id=user_id,uestionid=quest)								#a list of questions which have the same user as logged in user	
			qtemp=Questions.objects.filter(user__user_id=user_id,questionid=quest)

			qtemp=list(qtemp)
			question_no=qtemp[0].question_no
			
			u=user.objects.filter(user_id=us.username)
			u=list(u)
	
			if qtemp[0].score_obtained<score_for_submission :							#if it is a better submission then changing the score
				qtemp[0].score_obtained=score_for_submission				
				u[0].total_score+=score_for_submission							#total_score updated
				qtemp[0].time_of_submission=(ourtime-timecal())	#time added in seconds

			
			qtemp[0].total_penalty=qtemp[0].total_penalty+total_penalty 				#penalty added in seconds to question
			tmp_time = qtemp[0].time_of_submission
			qtemp[0].save()	
			u[0].total_penalty=u[0].total_penalty+total_penalty								#penalty added to user objectS
			our_file=open("/pradnya/pradnya/submissions/"+str(user_id)+"/q"+str(str2[1])+"/s"+str(str2[2])+"/time","r")	

			u[0].total_time = int(our_file.readline()) +u[0].total_penalty
			u[0].str_total_time = str(int(u[0].total_time/60/60)) + " H : " + str(int((u[0].total_time/60)%60)) + " M : " + str(int(u[0].total_time%60)) + " S"
			u[0].save()


			
			return render(request,"submission.html",{'ques':quest, 'colarr': colarr, 'str1':str1, 'maxscr':maxscr, 'scrarr': scrarr, 'strimg':strimg, 'res':res,'subid': str1,'tcount':range(tcount)})							#users submission page

		else:
			return HttpResponse("Error")

@csrf_exempt
@login_required
def leaderboard_handler(request):
	u=user.objects.order_by('-total_score','total_time')

	return render(request,"leaderboard.html",{"leaders":u})
