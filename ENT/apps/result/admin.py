from django.contrib import admin
from .models import Person, Result, Subject, Trial, TrialSub

admin.site.register(Trial)
admin.site.register(TrialSub)
admin.site.register(Person)
admin.site.register(Subject)
admin.site.register(Result)
