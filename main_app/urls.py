"""college_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

# from main_app.EditResultView import EditResultView

from . import hod_views, staff_views, student_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
   
   
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
  
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
 
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),


    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         hod_views.delete_student, name='delete_student'),
    
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),


    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
  
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
  
    
    
  

   



     #  TERMS 
     path('manage/terms/', hod_views.manage_term, name='manage_term'),
     path('add/term/', hod_views.add_term, name='add_term'),
     path('update/term/<int:id>/', hod_views.update_term, name='update_term'),
     path('delete/term/<int:id>/', hod_views.delete_term, name='delete_term'),
     
     # BRANCH 
     path('manage/branch/', hod_views.manage_branch, name='manage_branch'),
     path('add/branch/', hod_views.add_branch, name='add_branch'),
     path('update/branch/<int:id>/', hod_views.update_branch, name='update_branch'),
     path('delete/term/<int:id>/', hod_views.delete_branch, name='delete_branch'),

     # CLASSES
     path('manage/class/', hod_views.manage_classes, name='manage_classes'),
     path('add/class/', hod_views.add_classes, name='add_classes'),
     path('update/class/<int:id>/', hod_views.update_classes, name='update_classes'),
     path('delete/class/<int:id>/', hod_views.delete_class, name='delete_class'),

     # STREAM 
     path('manage/stream/', hod_views.manage_stream, name='manage_stream'),
     path('add/stream/', hod_views.add_stream, name='add_stream'),
     path('update/stream/<int:id>/', hod_views.update_stream, name='update_stream'),
     path('delete/stream/<int:id>/', hod_views.delete_stream, name='delete_stream'),

     # EXAMS
     path('manage/exam/', hod_views.manage_exam, name='manage_exam'),
     path('add/exam/', hod_views.add_exam, name='add_exam'),
     path('update/exam/<int:id>/', hod_views.update_exam, name='update_exam'),
     path('delete/exam/<int:id>/', hod_views.delete_exam, name='delete_exam'),

     # EXAMS RESULTS
     path('manage/exam_result/', hod_views.manage_exam_result, name='manage_exam_result'),
     path('add/exam_result/', hod_views.add_exam_result, name='add_exam_result'),
     path('update/exam_result/<int:id>/', hod_views.update_exam_result, name='update_exam_result'),
     path('delete/exam_result/<int:id>/', hod_views.delete_exam_result, name='delete_exam_result'),


     
     

]
