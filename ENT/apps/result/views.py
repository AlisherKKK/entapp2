from django.shortcuts import render

from django.http import Http404, HttpResponseRedirect

from .models import Person, Result, Subject, Trial

from django.urls import reverse

from django.utils import timezone

def index(request):
	return render(request, 'result/index.html', {"word": ""})

def add_person(request):
	req_id=1000000
	id = request.POST['username']
	if (len(id)<2):
		el = Person.objects.order_by('-pers_id')[0].pers_id+1
		req_id=el
		a = Person(pers_id=el, pers_fullname=request.POST["nameS"], prof_subject_1=int(request.POST["predmet"].split(" ")[0]), prof_subject_2=int(request.POST["predmet"].split(" ")[2]), pers_regdate=timezone.now())
		a.save()
	else:
		id=int(id)
		req_id=id
		a = Person.objects.get(pers_id=id)
		print(a.pers_password,request.POST["pass"])
		if (a.pers_password==request.POST["pass"]):
			return info(request, req_id)
		else:
			return render(request, 'result/index.html', {"word" : "Не правильный пороль"})
	return info(request, req_id)


def info(request, id):
	name = Person.objects.get(pers_id=id)
	subject1 = Subject.objects.get(sub_id=name.prof_subject_1).sub_name
	subject2 = Subject.objects.get(sub_id=name.prof_subject_2).sub_name
	a = Person.objects.all()
	b = Result.objects.all()
	return render(request, 'result/info.html', {"person":a, "result":b,"pers": name.pers_id, "name": name.pers_fullname, "sub1": subject1, "sub2": subject2, "id": name.pers_id})
	

def add_res(request, per_id):
	f = Person.objects.get(pers_id=per_id).id
	a = Result(res_pers_id=per_id, res_sub_id=11, res_target=request.POST["target1"], res_done=request.POST["done1"],res_date=request.POST["date"], person_id=f)
	b = Result(res_pers_id=per_id, res_sub_id=12, res_target=request.POST["target2"], res_done=request.POST["done2"],res_date=request.POST["date"], person_id=f)
	c = Result(res_pers_id=per_id, res_sub_id=13, res_target=request.POST["target3"], res_done=request.POST["done3"],res_date=request.POST["date"], person_id=f)
	d = Result(res_pers_id=per_id, res_sub_id=Person.objects.get(pers_id=per_id).prof_subject_1, res_target=request.POST["target4"], res_done=request.POST["done4"],res_date=request.POST["date"], person_id=f)
	e = Result(res_pers_id=per_id, res_sub_id=Person.objects.get(pers_id=per_id).prof_subject_2, res_target=request.POST["target5"], res_done=request.POST["done5"],res_date=request.POST["date"], person_id=f)
	a.save()
	b.save()
	c.save()
	d.save()
	e.save()
	print("QQ")

	return info(request, per_id)

def add_res_ent(request, tr_id):

	Trial(trial_pers_id=tr_id, tr_type=request.POST["typ"], trial_res=request.POST["ent1"], res_date=request.POST["dateT"],person_id=Person.objects.get(pers_id=tr_id).id).save()
	return info(request, tr_id)

