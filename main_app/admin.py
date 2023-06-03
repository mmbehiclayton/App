from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(Branch)
admin.site.register(ClassCategory)

@admin.register(CategoryTargetScore)
class CategoryTargetScore(admin.ModelAdmin):
    list_display = ('class_category','term','target_score')
    list_filter = ('class_category','term')

# Custom ModelAdmin for Classes
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'branch', 'created_at', 'updated_at')
    list_filter = ('category', 'branch', 'created_at', 'updated_at')

admin.site.register(Classes, ClassesAdmin)

# Custom ModelAdmin for Stream
class StreamAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'name', 'created_at', 'updated_at')
    list_filter = ('class_id', 'created_at', 'updated_at')

admin.site.register(Stream, StreamAdmin)

#register custom user
@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('email', 'user_type', 'gender', 'created_at', 'updated_at')
    list_filter = ('user_type', 'gender', 'created_at', 'updated_at')

#Register Staff on Admin Site
admin.site.register(Staff)

# Custom ModelAdmin for Subject
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name','created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

admin.site.register(Subject, SubjectAdmin)

@admin.register(Session)
class Session(admin.ModelAdmin):
    list_display = ('name', 'start_year', 'end_year')
    list_filter = ('name', 'start_year', 'end_year')

@admin.register(SessionTerm)
class SessionTerm(admin.ModelAdmin):
    list_display = ('term', 'session', 'name')
    list_filter = ('term', 'session')

# Custom ModelAdmin for Exam
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_date', 'target_marks', 'session', 'term')
    list_filter = ('session', 'term')

admin.site.register(Exam, ExamAdmin)

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
