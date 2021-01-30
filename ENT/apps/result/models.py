from django.db import models

import datetime

from django.utils import timezone


# Create your models here.


class Admin(models.Model):
    admin_id = models.IntegerField(unique=True)
    admin_nick = models.CharField("nick", unique=True, null=False, max_length=50)
    admin_password = models.CharField("pass", max_length=50)
    admin_fullname = models.CharField("name", max_length=100)

    def __str__(self):
        return "{} {} {}".format(self.admin_id, self.admin_nick, self.admin_fullname)

    def addStudent(self, st_id):
        std = Person.objects.get(pers_id=st_id)
        std.admin_id = self.admin_id
        std.save()

    def removeStd(self, st_id):
        std = Person.objects.get(pers_id=st_id)
        std.admin_id = 0
        std.save()


class Person(models.Model):
    pers_id = models.IntegerField(unique=True)
    pers_nickname = models.CharField("nick", unique=True, null=True, max_length=50)
    pers_password = models.CharField("passwd", max_length=100)
    pers_fullname = models.CharField("fullname", max_length=50);
    admin_id = models.IntegerField(unique=False, null=False, default=0)
    prof_subject_1 = models.IntegerField(null=True, unique=False, editable=True)
    prof_subject_2 = models.IntegerField(null=True, unique=False, editable=True)
    pers_regdate = models.DateTimeField("date")

    def __str__(self):
        return str(self.pers_id) + " " + self.pers_fullname

    def get_last_ent(self):
        try:
            ent = Trial.objects.filter(trial_pers_id=self.pers_id).order_by('-res_date')[0].trial_res
        except:
            ent="No result"
        return ent

    def get_all_target(self):
        a = self.get_res_last_7days()
        b = str(a[0])
        return b

    def get_all_result(self):
        a = self.get_res_last_7days()
        b = str(a[1])
        return b

    def get_res_last_7days(self):
        b = list()
        for i in Result.objects.filter(res_pers_id=self.pers_id):
            if i.last_7_day():
                b.append(i)
        res = list()
        s1, s2 = 0, 0
        for i in b:
            s1 += i.res_target
            s2 += i.res_done
        res.append(s1)
        res.append(s2)
        return res

    def get_res_last_7days_target(self):
        b = list()
        for i in Result.objects.filter(res_pers_id=self.pers_id):
            if i.last_7_day():
                b.append(i)
        s1 = 0
        for i in b:
            s1 += i.res_target
        return s1

    def get_res_last_7days_done(self):
        b = list()
        for i in Result.objects.filter(res_pers_id = self.pers_id):
            if i.last_7_day():
                b.append(i)
        s1 = 0
        for i in b:
            s1 += i.res_done
        return s1

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

    def update(self):
        t = Target.objects.filter(target_pers_id=self.pers_id)
        for i in t:
            if int(i.target_targ) < 30:
                i.target_targ += 3
                i.save()


class Trial(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    trial_pers_id = models.IntegerField(unique=False)
    tr_type = models.CharField(max_length=50)
    tr_target = models.IntegerField(unique=False, default=75)
    trial_res = models.IntegerField(unique=False)
    res_date = models.DateTimeField("date of pass", null=True)

    def get_date(self):
        return '{}'.format(self.res_date.strftime('%d.%m.%Y'))


class Subject(models.Model):
    sub_id = models.IntegerField(unique=True)
    sub_name = models.CharField("subject", max_length=50)

    def __str__(self):
        return self.sub_name


class Result(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    res_pers_id = models.IntegerField(unique=False)
    res_sub_id = models.IntegerField(unique=False)
    res_target = models.IntegerField(unique=False)
    res_done = models.IntegerField(unique=False, null=True)
    res_date = models.DateTimeField("date of pass")

    def __str__(self):
        a = Person.objects.get(pers_id=self.res_pers_id)
        x = ' '
        return str(a.pers_id) + " " + a.pers_fullname + '\t' + str(self.res_date)

    def last_7_day(self):
        return self.res_date >= (timezone.now() - datetime.timedelta(days=7))

    def get_subject_name(self):
        return Subject.objects.get(sub_id=self.res_sub_id).sub_name

    def get_date(self):
        return '{}'.format(self.res_date.strftime('%d.%m.%Y'))




class TrialSub(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    trsub_target = models.IntegerField(unique=False, default=15)
    trsub_subid = models.IntegerField(unique=False)
    trsub_res = models.IntegerField(unique=False)
    res_date = models.DateTimeField("date of pass", null=True)

    def get_date(self):
        return '{}'.format(self.res_date.strftime('%d.%m.%Y'))

    def get_subject_name(self):
        return Subject.objects.get(sub_id=self.trsub_subid).sub_name

    def __str__(self):
        return Person.objects.get(id=self.person_id).pers_fullname


class Target(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    target_pers_id = models.IntegerField(unique=False)
    target_sub_id = models.IntegerField(unique=False)
    target_targ = models.IntegerField(unique=False, default=15)
    target_date = models.DateTimeField(null=True)


class TragetEnt(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    target_pers_id = models.IntegerField(unique=False)
    target_sub_id = models.IntegerField(unique=False)
    target_targ = models.IntegerField(unique=False, default=15)
    target_date = models.DateTimeField(null=True)
