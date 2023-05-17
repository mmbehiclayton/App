import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required


from .forms import *
from .models import *
import sweetify


@login_required(redirect_field_name="user_login")
def admin_home(request):
    total_staff = Staff.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    subject_all = Subject.objects.all()
    subject_list = []
    for subject in subject_all:
        subject_list.append(subject.name)
 
   
    context = {
        'page_title': "Administrative Dashboard",
        'total_staff': total_staff,
        'total_subject': total_subject,
        'subject_list': subject_list,
    }
    return render(request, 'hod_template/home_content.html', context)

@login_required(redirect_field_name="user_login")
def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.course = course
                user.save()
                #messages.success(request, "Successfully Added")
                sweetify.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_staff_template.html', context)

@login_required(redirect_field_name="user_login")
def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject()
                subject.name = name
                subject.staff = staff
                subject.course = course
                subject.save()
                sweetify.success(request, "Successfully Added")
                return redirect(reverse('add_subject'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod_template/add_subject_template.html', context)

@login_required(redirect_field_name="user_login")
def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Staff'
    }
    return render(request, "hod_template/manage_staff.html", context)

@login_required(redirect_field_name="user_login")
def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subjects'
    }
    return render(request, "hod_template/manage_subject.html", context)

@login_required(redirect_field_name="user_login")
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Staff'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                staff.course = course
                user.save()
                staff.save()
                sweetify.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                sweetify.error(request, "Could Not Update " + str(e))
        else:
            sweetify.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=staff_id)
        staff = Staff.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)

@login_required(redirect_field_name="user_login")
def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.staff = staff
                subject.course = course
                subject.save()
                sweetify.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                sweetify.error(request, "Could Not Add " + str(e))
        else:
            sweetify.error(request, "Fill Form Properly")
    return render(request, 'hod_template/edit_subject_template.html', context)

@login_required(redirect_field_name="user_login")
def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                sweetify.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                sweetify.error(request, 'Could Not Add ' + str(e))
        else:
            sweetify.error(request, 'Fill Form Properly ')
    return render(request, "hod_template/add_session_template.html", context)

@login_required(redirect_field_name="user_login")
def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "hod_template/manage_session.html", context)
@login_required(redirect_field_name="user_login")


# Terms functionality 

@login_required(redirect_field_name="user_login")
def manage_term(request):
    terms = SessionTerm.objects.all()
    context = {
        'terms': terms
    }
    return render(request, "hod_template/manage_term.html", context)

@login_required(redirect_field_name="user_login")
def add_term(request):
    if request.method == 'POST':
        form = SessionTermForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Term Created")
            return redirect(reverse('manage_term'))
    else:
        form = SessionTermForm()
    context = {
        'form': form
    }

    return render(request, "hod_template/add_term.html", context)
    
@login_required(redirect_field_name="user_login")
def update_term(request, id):

    term_obj = SessionTerm.objects.get(id=id)
    if request.method == 'POST':
        form = SessionTermForm(request.POST, instance=term_obj)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Term updated !')
            return redirect('manage_term')
    else:
        form = SessionTermForm(instance=term_obj)

    context = {
        'form': form
    }
    return render(request, "hod_template/add_term.html", context)

@login_required(redirect_field_name="user_login")
def delete_term(request, id):
    term_obj = SessionTerm.objects.get(id=id)
    try:
        term_obj.delete()
        sweetify.success(request, "Term deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this term.")
    return redirect(reverse('manage_term'))

#  Branches functionalities

@login_required(redirect_field_name="user_login")
def manage_branch(request):
    branch = Branch.objects.all()
    context = {
        'branch': branch
    }
    return render(request, "hod_template/manage_branch.html", context)

@login_required(redirect_field_name="user_login")
def add_branch(request):
    if request.method == 'POST':
        form = BranchesForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Branch Added !')
            return redirect('manage_branch')
    else:
        form = BranchesForm()

    context = {
        'form': form
    }
    return render(request, "hod_template/add_branch.html", context)

@login_required(redirect_field_name="user_login")
def update_branch(request,id):
    branch_obj = Branch.objects.get(branch_id=id)
    if request.method == 'POST':
        form = BranchesForm(request.POST, instance=branch_obj)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Branch updated !')
            return redirect('manage_branch')
    else:
        form = BranchesForm(instance=branch_obj)
    context = {
        'form': form
    }
    return render(request, "hod_template/add_branch.html", context)

@login_required(redirect_field_name="user_login")
def delete_branch(request, id):
    branch_obj = Branch.objects.get(branch_id=id)
    branch_obj.delete()
    sweetify.success(request, "Branch deleted successfully!")            
    return redirect(reverse('manage_branch'))

# classes Functionalities
@login_required(redirect_field_name="user_login")
def manage_classes(request):
    classes = Classes.objects.all()
    context = {
        'classes': classes
    }
    return render(request, "hod_template/manage_classes.html", context)

@login_required(redirect_field_name="user_login")
def add_classes(request):
    if request.method == 'POST':
        form = ClassesForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Class Added !')
            return redirect('manage_classes')
    else:
        form = ClassesForm()

    context = {
        'form': form
    }
    return render(request, "hod_template/add_class.html", context)

@login_required(redirect_field_name="user_login")
def update_classes(request,id):
    class_obj = Classes.objects.get(class_id=id)
    if request.method == 'POST':
        form = ClassesForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Class updated !')
            return redirect('manage_classes')
    else:
        form = ClassesForm(instance=class_obj)
    context = {
        'form': form
    }
    return render(request, "hod_template/add_branch.html", context)

@login_required(redirect_field_name="user_login")
def delete_class(request, id):
    class_obj =Classes.objects.get(class_id=id)
    class_obj.delete()
    sweetify.success(request, "Class deleted successfully!")            
    return redirect(reverse('manage_classes'))


# stream Functionalities

@login_required(redirect_field_name="user_login")
def manage_stream(request):
    stream = Stream.objects.all()
    context = {
        'stream': stream
    }
    return render(request, "hod_template/manage_stream.html", context)

@login_required(redirect_field_name="user_login")
def add_stream(request):
    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Stream Added !')
            return redirect('manage_stream')
    else:
        form = StreamForm()

    context = {
        'form': form
    }
    return render(request, "hod_template/add_stream.html", context)

@login_required(redirect_field_name="user_login")
def update_stream(request,id):
    stream = StreamForm.objects.get(class_id=id)
    if request.method == 'POST':
        form = ClassesForm(request.POST, instance=stream)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Stream updated !')
            return redirect('manage_classes')
    else:
        form = ClassesForm(instance=stream)
    context = {
        'form': form
    }
    return render(request, "hod_template/add_stream.html", context)

@login_required(redirect_field_name="user_login")
def delete_stream(request, id):
    stream_obj =Stream.objects.get(stream_id=id)
    stream_obj.delete()
    sweetify.success(request, "Class deleted successfully!")            
    return redirect(reverse('manage_classes'))


@login_required(redirect_field_name="user_login")
def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                sweetify.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_session_template.html", context)
        else:
            sweetify.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_session_template.html", context)

    else:
        return render(request, "hod_template/edit_session_template.html", context)



@login_required(redirect_field_name="user_login")
@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)

@login_required(redirect_field_name="user_login")
@csrf_exempt
def staff_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'hod_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)

@login_required(redirect_field_name="user_login")
def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                sweetify.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                sweetify.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)

@login_required(redirect_field_name="user_login")
def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


@login_required(redirect_field_name="user_login")
@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

@login_required(redirect_field_name="user_login")
def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    sweetify.success(request, "Staff deleted successfully!")
    return redirect(reverse('manage_staff'))

@login_required(redirect_field_name="user_login")
def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    sweetify.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))

@login_required(redirect_field_name="user_login")
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    sweetify.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))

@login_required(redirect_field_name="user_login")
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        sweetify.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))
