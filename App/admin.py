from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
admin.site.register(Students)
admin.site.register(Questions)
admin.site.register(College)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Answer)
admin.site.register(Exam)
admin.site.register(Proctor)
admin.site.register(Semester)
admin.site.unregister(Group)