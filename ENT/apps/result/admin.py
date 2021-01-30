from django.contrib import admin
from .models import Person, Result, Subject, Trial, TrialSub, Target, TragetEnt, Admin

admin.site.register(Admin)
admin.site.register(TragetEnt)
admin.site.register(Target)
admin.site.register(Trial)
admin.site.register(TrialSub)
admin.site.register(Person)
admin.site.register(Subject)
admin.site.register(Result)
