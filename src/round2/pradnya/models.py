from __future__ import unicode_literals

from django.db import models
from django import forms

# Create your models here.
	
class user(models.Model):
	user_id=models.CharField(max_length=30,default='',blank=True,null=True,unique=True)
	total_score=models.IntegerField(default=0,blank=True,null=True)
	total_penalty=models.IntegerField(default=0,blank=True,null=True)
	total_time=models.IntegerField(default=0,blank=True,null=True)
	str_total_time=models.CharField(default="0",blank=True,max_length=30,null=True)

	
class Questions(models.Model):
	question_no=models.IntegerField(default=-1,blank=True,null=True)					#we have to create differnt objects of the same question for each user
	questionid=models.CharField(max_length=30,default='def',blank=True,null=True)
	questiontitle=models.CharField(max_length=30,default='def',blank=True,null=True)
	user=models.ForeignKey(user,null=True,blank=True)
	score_obtained=models.IntegerField(default=0,blank=True,null=True)					#highest score obtained
	time_of_submission=models.IntegerField(default=0,blank=True,null=True)				#corresponding time for the highest score submission including penalties
	total_penalty=models.IntegerField(default=0,blank=True,null=True)
	#timelimit

class submissions(models.Model):
	Questions=models.ForeignKey(Questions,null=True,blank=True)
	user_id=models.CharField(max_length=30,default='',blank=True,null=True	)
	timestamp=models.DateTimeField(auto_now_add=True)
	score=models.IntegerField(default=0,blank=True,null=True)							#score of that submission
	penalty=models.IntegerField(default=0,blank=True,null=True)
