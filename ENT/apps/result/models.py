from django.db import models

import datetime

from django.utils import timezone 
# Create your models here.

class Person(models.Model):
	pers_id = models.IntegerField(unique=True)
	pers_password=models.CharField("passwd", max_length=100)
	pers_fullname = models.CharField("fullname", max_length = 50);

	prof_subject_1 = models.IntegerField(null=True,unique=False, editable=True, max_length=2)
	prof_subject_2 = models.IntegerField(null=True,unique=False, editable=True, max_length=2)
	pers_regdate = models.DateTimeField("date")

	def __str__(self):
		return str(self.pers_id)+" "+self.pers_fullname

	def get_all_target(self):
		a = self.get_res_last_7days()
		b=str(a[0])
		return b

	def get_all_result(self):
		a = self.get_res_last_7days()
		b=str(a[1])
		return b

	def get_res_last_7days(self):
		b = list()
		for i in Result.objects.raw('SELECT * FROM result_result WHERE res_pers_id='+str(self.pers_id)):
			b.append(i)
		res=list()
		s1,s2=0,0
		for i in b:
			s1+=i.res_target
			s2+=i.res_done 
		res.append(s1)
		res.append(s2)
		return res

	def get_last_submit(self):
		b = Result.objects.filter(res_pers_id=self.pers_id).order_by('-res_date')
		if b:
			return b[0].res_date
		return ""

	def get_last_trials_res(self):
		b = Trial.objects.filter(trial_pers_id=self.pers_id).order_by('-res_date')
		if b:
			return b[0].trial_res
		return ""

	def get_last_trials_date(self):
		b = Trial.objects.filter(trial_pers_id=self.pers_id).order_by('-res_date')
		if b:
			return b[0].res_date
		return ""



class Trial(models.Model):
	person = models.ForeignKey(Person, on_delete=models.DO_NOTHING) 
	trial_pers_id = models.IntegerField(unique=False)
	tr_type = models.CharField(max_length=50)
	trial_res = models.IntegerField(unique=False) 
	res_date = models.DateTimeField("date of pass", null=True)


class Subject(models.Model):
	sub_id = models.IntegerField(unique=True, max_length=2)
	sub_name = models.CharField("subject", max_length=50) 

	def __str__(self):
		return self.sub_name

class Result(models.Model): 
	person = models.ForeignKey(Person, on_delete=models.DO_NOTHING) 
	res_pers_id = models.IntegerField(unique=False) 
	res_sub_id = models.IntegerField(unique=False, max_length=2) 
	res_target = models.IntegerField(unique=False) 
	res_done = models.IntegerField(unique=False) 
	res_date = models.DateTimeField("date of pass") 

	def __str__(self):
		a = Person.objects.get(pers_id = self.res_pers_id)
		x=' '
		return str(a.pers_id)+" "+a.pers_fullname+'\t'+str(self.res_date)





class TrialSub(models.Model):
	trial = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
	trsub_subid = models.IntegerField(unique=False)
	trsub_res = models.IntegerField(unique=False)
	res_date = models.DateTimeField("date of pass", null=True)