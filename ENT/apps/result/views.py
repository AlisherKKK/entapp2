import json

from django.shortcuts import render

from django.http import Http404, HttpResponseRedirect, HttpResponse

from .models import Person, Result, Subject, Trial, TrialSub, Target, TragetEnt, Admin

from django.urls import reverse

from django.utils import timezone


def index(request):
    return render(request, 'result/login.html', {"word": ""})


def admin(request):
    return render(request, 'result/admin_login.html', {"word": ""})


def add_admin(request):
    req_id = 1000000
    id = request.POST['username']
    fn = request.POST['nameS']
    if len(id) > 0 and len(fn) > 0:
        try:
            el = Admin.objects.order_by('-admin_id')[0].pers_id + 1
        except:
            el = req_id
        req_id = el
        a = Admin(admin_id=el, admin_nick=id, admin_password=request.POST["pass"],
                  admin_fullname=request.POST["nameS"])
        a.save()
        return info(request, req_id)
    else:
        nick = ''
        try:
            id = int(id)
            req_id = id
        except:
            nick = id
            req_id = Admin.objects.get(admin_nick=nick).admin_id
        try:
            if nick == '':
                a = Admin.objects.get(admin_id=id)
            else:
                a = Admin.objects.get(admin_nick=nick)
        except:
            return render(request, 'result/login.html', {"word": "Не правильный id или никнейм"})
        if a.admin_password == request.POST["pass"]:
            return admin_page(request, req_id)
        else:
            return render(request, 'result/admin_login.html', {"word": "Не правильный пороль"})


def admin_page(request, ad_id):
    try:
        admin = Admin.objects.get(admin_id=ad_id)
        students = Person.objects.filter(admin_id=admin.admin_id)
        to_select = Person.objects.all()
    except:
        return add_admin(request)

    context = {
        "admin": admin,
        "name": admin.admin_fullname,
        "student": students,
        "select": to_select
    }

    return render(request, 'result/admin_info.html', context)


def add_std_toadmin(request, ad_id):
    admin = Admin.objects.get(admin_id=ad_id)
    students = request.POST['std']
    stds = students.split(" ")
    for i in stds:
        if len(i) > 1:
            admin.addStudent(int(i))
    return admin_page(request, ad_id)


def remove_std_fromadmin(request, adm_id):
    admin = Admin.objects.get(admin_id=adm_id)
    students = request.POST['std_rem']
    stds = students.split(" ")
    for i in stds:
        if len(i) > 1:
            admin.removeStd(int(i))
    return admin_page(request, adm_id)


def add_person(request):
    req_id = 1000000
    id = request.POST['username']
    fn = request.POST['nameS']
    if len(id) > 0 and len(fn) > 0:
        el = Person.objects.order_by('-pers_id')[0].pers_id + 1
        req_id = el
        a = Person(pers_id=el, pers_nickname=id, pers_password=request.POST["pass"],
                   pers_fullname=request.POST["nameS"],
                   prof_subject_1=int(request.POST["predmet"].split(" ")[0]),
                   prof_subject_2=int(request.POST["predmet"].split(" ")[2]), pers_regdate=timezone.now())
        a.save()
        Target(target_pers_id=el, target_sub_id=int(request.POST["predmet"].split(" ")[0]), person_id=a.id,
               target_date=timezone.now()).save()
        Target(target_pers_id=el, target_sub_id=int(request.POST["predmet"].split(" ")[2]), person_id=a.id,
               target_date=timezone.now()).save()
        Target(target_pers_id=el, target_sub_id=11, person_id=a.id, target_date=timezone.now()).save()
        Target(target_pers_id=el, target_sub_id=12, person_id=a.id, target_date=timezone.now()).save()
        Target(target_pers_id=el, target_sub_id=13, person_id=a.id, target_date=timezone.now()).save()
        return info(request, req_id)
    else:
        nick = ''
        try:
            id = int(id)
            req_id = id
        except:
            nick = id
            req_id = Person.objects.get(pers_nickname=nick).pers_id
        print("b")
        try:
            print("c")
            if nick == '':
                a = Person.objects.get(pers_id=id)
            else:
                a = Person.objects.get(pers_nickname=nick)
        except:
            return render(request, 'result/login.html', {"word": "Не правильный id или никнейм"})
        print("d")

        if a.pers_password == request.POST["pass"]:
            print("q")
            return info(request, req_id)
        else:
            return render(request, 'result/login.html', {"word": "Не правильный пороль"})


def info(request, id):
    try:
        name = Person.objects.get(pers_id=id)
        subject1 = Subject.objects.get(sub_id=name.prof_subject_1).sub_name
        subject2 = Subject.objects.get(sub_id=name.prof_subject_2).sub_name
        a = Person.objects.all()
        b = Result.objects.all()

        c1 = Target.objects.filter(target_pers_id=id, target_sub_id=11).order_by('-target_date')
        c2 = Target.objects.filter(target_pers_id=id, target_sub_id=12).order_by('-target_date')
        c3 = Target.objects.filter(target_pers_id=id, target_sub_id=13).order_by('-target_date')
        c4 = Target.objects.filter(target_pers_id=id,
                                   target_sub_id=Person.objects.get(pers_id=id).prof_subject_1).order_by('-target_date')
        c5 = Target.objects.filter(target_pers_id=id,
                                   target_sub_id=Person.objects.get(pers_id=id).prof_subject_2).order_by('-target_date')
        c1 = c1[0] if c1 else ""
        c2 = c2[0] if c2 else ""
        c3 = c3[0] if c3 else ""
        c4 = c4[0] if c4 else ""
        c5 = c5[0] if c5 else ""

        tr = Trial.objects.filter(trial_pers_id=id).order_by('-res_date')
        trial = tr if len(tr) > 0 else ""
        tr = tr[0] if tr else ""

        b1 = TragetEnt.objects.filter(person_id=Person.objects.get(pers_id=id).id, target_sub_id=11).order_by(
            '-target_date')
        b2 = TragetEnt.objects.filter(person_id=Person.objects.get(pers_id=id).id, target_sub_id=12).order_by(
            '-target_date')
        b3 = TragetEnt.objects.filter(person_id=Person.objects.get(pers_id=id).id, target_sub_id=13).order_by(
            '-target_date')
        b4 = TragetEnt.objects.filter(person_id=Person.objects.get(pers_id=id).id,
                                      target_sub_id=Person.objects.get(pers_id=id).prof_subject_1).order_by(
            '-target_date')
        b5 = TragetEnt.objects.filter(person_id=Person.objects.get(pers_id=id).id,
                                      target_sub_id=Person.objects.get(pers_id=id).prof_subject_2).order_by(
            '-target_date')
        trial_sub = TrialSub.objects.filter(person_id=Person.objects.get(pers_id=id).id).order_by('-res_date')
        trial_sub = trial_sub if len(trial_sub) > 0 else ""
        b1 = b1[0] if b1 else ""
        b2 = b2[0] if b2 else ""
        b3 = b3[0] if b3 else ""
        b4 = b4[0] if b4 else ""
        b5 = b5[0] if b5 else ""

        res = Result.objects.filter(res_pers_id=id).order_by('-res_date')
        res = res if len(res) > 0 else ""

        data = zip(trial_sub, trial)
    except:
        add_person(request)

    return render(request, 'result/info_student.html',
                  {"data": data, "trial": trial, "trialS": trial_sub, "resOfPers": res, "tr": tr, "tr1": b1, "tr2": b2,
                   "tr3": b3, "tr4": b4, "tr5": b5, "t1": c1, "t2": c2, "t3": c3, "t4": c4, "t5": c5, "person": a,
                   "result": b, "persnickety": name.pers_nickname, "pers": name.pers_id, "name": name.pers_fullname,
                   "sub1": subject1, "sub2": subject2,
                   "id": name.pers_id})


def add_res(request, per_id):
    f = Person.objects.get(pers_id=per_id).id
    a = Result(res_pers_id=per_id, res_sub_id=11,
               res_target=Target.objects.filter(target_pers_id=per_id, target_sub_id=11).order_by('-target_date')[
                   0].target_targ, res_done=request.POST["done1"], res_date=request.POST["date"], person_id=f)
    b = Result(res_pers_id=per_id, res_sub_id=12,
               res_target=Target.objects.filter(target_pers_id=per_id, target_sub_id=12).order_by('-target_date')[
                   0].target_targ, res_done=request.POST["done2"], res_date=request.POST["date"], person_id=f)
    c = Result(res_pers_id=per_id, res_sub_id=13,
               res_target=Target.objects.filter(target_pers_id=per_id, target_sub_id=13).order_by('-target_date')[
                   0].target_targ, res_done=request.POST["done3"], res_date=request.POST["date"], person_id=f)
    d = Result(res_pers_id=per_id, res_sub_id=Person.objects.get(pers_id=per_id).prof_subject_1, res_target=
    Target.objects.filter(target_pers_id=per_id,
                          target_sub_id=Person.objects.get(pers_id=per_id).prof_subject_1).order_by('-target_date')[
        0].target_targ, res_done=request.POST["done4"], res_date=request.POST["date"], person_id=f)
    e = Result(res_pers_id=per_id, res_sub_id=Person.objects.get(pers_id=per_id).prof_subject_2, res_target=
    Target.objects.filter(target_pers_id=per_id,
                          target_sub_id=Person.objects.get(pers_id=per_id).prof_subject_2).order_by('-target_date')[
        0].target_targ, res_done=request.POST["done5"], res_date=request.POST["date"], person_id=f)
    a.save()
    b.save()
    c.save()
    d.save()
    e.save()
    Target(target_pers_id=per_id, target_sub_id=11, person_id=f, target_targ=request.POST["done11"],
           target_date=timezone.now()).save()
    Target(target_pers_id=per_id, target_sub_id=12, person_id=f, target_targ=request.POST["done22"],
           target_date=timezone.now()).save()
    Target(target_pers_id=per_id, target_sub_id=13, person_id=f, target_targ=request.POST["done33"],
           target_date=timezone.now()).save()
    Target(target_pers_id=per_id, target_sub_id=Person.objects.get(pers_id=per_id).prof_subject_1, person_id=f,
           target_targ=request.POST["done44"], target_date=timezone.now()).save()
    Target(target_pers_id=per_id, target_sub_id=Person.objects.get(pers_id=per_id).prof_subject_2, person_id=f,
           target_targ=request.POST["done55"], target_date=timezone.now()).save()
    return info(request, per_id)


def add_res_ent(request, tr_id):
    f = Person.objects.get(pers_id=tr_id).id
    res = list()
    res.append(request.POST["ent1"])
    res.append(request.POST["ent2"])
    res.append(request.POST["ent3"])
    res.append(request.POST["ent4"])
    res.append(request.POST["ent5"])

    res2 = list()
    res2.append(request.POST["ent11"])
    res2.append(request.POST["ent22"])
    res2.append(request.POST["ent33"])
    res2.append(request.POST["ent44"])
    res2.append(request.POST["ent55"])

    entTar = TragetEnt.objects.filter(target_pers_id=tr_id).order_by('-target_date')
    a = TrialSub(trsub_subid=11,
                 trsub_target=entTar.filter(target_sub_id=11).order_by('-target_date')[0].target_targ if entTar.filter(
                     target_sub_id=11).order_by('-target_date') else 0, trsub_res=res[0],
                 res_date=request.POST["dateT"], person_id=Person.objects.get(pers_id=tr_id).id)
    b = TrialSub(trsub_subid=12,
                 trsub_target=entTar.filter(target_sub_id=12).order_by('-target_date')[0].target_targ if entTar.filter(
                     target_sub_id=12).order_by('-target_date') else 0, trsub_res=res[1],
                 res_date=request.POST["dateT"], person_id=Person.objects.get(pers_id=tr_id).id)
    c = TrialSub(trsub_subid=13,
                 trsub_target=entTar.filter(target_sub_id=13).order_by('-target_date')[0].target_targ if entTar.filter(
                     target_sub_id=13).order_by('-target_date') else 0, trsub_res=res[2],
                 res_date=request.POST["dateT"], person_id=Person.objects.get(pers_id=tr_id).id)
    d = TrialSub(trsub_subid=Person.objects.get(pers_id=tr_id).prof_subject_1, trsub_target=
    entTar.filter(target_sub_id=Person.objects.get(pers_id=tr_id).prof_subject_1).order_by('-target_date')[
        0].target_targ if entTar.filter(target_sub_id=Person.objects.get(pers_id=tr_id).prof_subject_1).order_by(
        '-target_date') else 0, trsub_res=res[3], res_date=request.POST["dateT"],
                 person_id=Person.objects.get(pers_id=tr_id).id)
    e = TrialSub(trsub_subid=Person.objects.get(pers_id=tr_id).prof_subject_2, trsub_target=
    entTar.filter(target_sub_id=Person.objects.get(pers_id=tr_id).prof_subject_2).order_by('-target_date')[
        0].target_targ if entTar.filter(target_sub_id=Person.objects.get(pers_id=tr_id).prof_subject_2).order_by(
        '-target_date') else 0, trsub_res=res[4], res_date=request.POST["dateT"],
                 person_id=Person.objects.get(pers_id=tr_id).id)
    a.save()
    b.save()
    c.save()
    d.save()
    e.save()
    total = 0
    for i in res:
        total += int(i)
    total2 = 0
    for i in res2:
        total2 += int(i)
    Trial(trial_pers_id=tr_id, tr_type=request.POST["typ"], tr_target=total2, trial_res=total,
          res_date=request.POST["dateT"], person_id=Person.objects.get(pers_id=tr_id).id).save()
    TragetEnt(target_pers_id=tr_id, target_sub_id=11, person_id=f, target_targ=int(res2[0]),
              target_date=timezone.now()).save()
    TragetEnt(target_pers_id=tr_id, target_sub_id=12, person_id=f, target_targ=int(res2[1]),
              target_date=timezone.now()).save()
    TragetEnt(target_pers_id=tr_id, target_sub_id=13, person_id=f, target_targ=int(res2[2]),
              target_date=timezone.now()).save()
    TragetEnt(target_pers_id=tr_id, target_sub_id=Person.objects.get(pers_id=tr_id).prof_subject_1, person_id=f,
              target_targ=int(res2[3]), target_date=timezone.now()).save()
    TragetEnt(target_pers_id=tr_id, target_sub_id=Person.objects.get(pers_id=tr_id).prof_subject_2, person_id=f,
              target_targ=int(res2[4]), target_date=timezone.now()).save()

    return info(request, tr_id)
