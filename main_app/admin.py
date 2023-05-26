from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)

admin.site.register(Branch)
admin.site.register(Classes)
admin.site.register(Stream)
admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)

admin.site.register(Subject)
admin.site.register(Session)

admin.site.register(Exam)
admin.site.register(ExamMeanResult)
admin.site.register(SessionTerm)

admin.site.register(TeacherSubject)
admin.site.register(TeacherPerformance)
admin.site.register(StreamPerformance)
admin.site.register(SchoolPerformance)
admin.site.register(ClassCategory)
admin.site.register(CategoryTargetScore)


#change admin site title
admin.site.site_header = "Alameen Plus"
