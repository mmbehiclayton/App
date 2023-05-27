from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)

admin.site.register(Branch)
admin.site.register(ClassCategory)
admin.site.register(CategoryTargetScore)

admin.site.register(Classes)
admin.site.register(Stream)
admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)

admin.site.register(Subject)

admin.site.register(Session)
admin.site.register(SessionTerm)

#Register Exam  on the Admin Site
@admin.register(Exam)
class Exam(admin.ModelAdmin):
    list_display = ['exam_id','session','term','name','target_marks']

#Register Exam Result on the Admin Site
@admin.register(ExamMeanResult)
class ExamMeanResult(admin.ModelAdmin):
    list_display = [ 'result_id','exam','subject','score']


#Register TeacherSubject on the admin Site
@admin.register(TeacherSubject)
class TeacherSubject(admin.ModelAdmin):
    list_display = ['teacher','stream','subject']


#change admin site title
admin.site.site_header = "Alameen Plus"   
