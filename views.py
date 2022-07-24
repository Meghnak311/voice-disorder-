from ast import For
import code
from datetime import date, datetime
from itertools import count
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Sum, Max

import login
from hod.models import batch, scheme, semester_result, subject, \
    subject_to_staff
from login.models import MyUser
from staff.models import profile
from student.models import parents, profile_student
from hod.models import batch
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import hod
from django.contrib.auth.decorators import login_required
from autoscraper import AutoScraper


# Create your views here.
# print(make_password('123'))
# print(check_password('1', '1'))


# staff code
@login_required
def add_staff(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username
    # staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = first_name + " " + last_name
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        if password1 != password2:
            messages.error(request, 'Password mismatch')
        else:
            user = MyUser.objects.filter(username=username)
            if user:
                messages.error(request, 'User already exist')
            else:
                # enc_pswrd = make_password(password1)
                # user = super().save(commit=False)
                password = make_password(password1)
                MyUser.objects.create(username=username,
                                      first_name=first_name,
                                      last_name=last_name,
                                      password=password,
                                      is_faculty=True,
                                      is_active=True,
                                      is_student=False,
                                      is_hod=False

                                      )

                profile.objects.create(Faculty_unique_id=username, First_name=first_name, Last_name=last_name)
                messages.error(request, 'Faculty ' + full_name + ' successfully added')

    return render(request, 'add_staff.html', {"context": context, "data_for_self_profile": staff_details_1})


@login_required
def view_faculty(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username
    # print(staff)
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    staff_details = profile.objects.all()
    batch_data = batch.objects.all()

    return render(request, 'view_faculty.html',
                  {"staff_data": staff_details, "context": context, "data_for_self_profile": staff_details_1,
                   'batch_data': batch_data
                   })


# student view
@csrf_exempt
def check_user_exist(request):
    username = request.POST.get('username')
    subject_exist = MyUser.objects.filter(username=username).exists()
    if subject_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required
def add_student(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data_class = batch.objects.all()  # for display the existing batch details
    # batch_data_year = batch.objects.all().distinct()
    scheme_data = scheme.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        batch_id_str = request.POST.get('batch_id')
        batch_id_int = int(batch_id_str)
        u_no = request.POST.get('university_no')

        full_name = first_name + " " + last_name

        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        if batch_id_int == 0:
            messages.error(request, 'Please select Class')
        else:

            batch_data = batch.objects.get(id=batch_id_int)
            class_name = batch_data.class_name
            batch_year = batch_data.date_of_join
            semester = batch_data.semester

            if password1 != password2:
                messages.error(request, 'Password mismatch')
            else:

                user = MyUser.objects.filter(username=username)
                if user:
                    messages.error(request, 'User already exist')
                else:
                    # insert only the year in student profile (column : year_of_join)
                    password = make_password(password1)
                    MyUser.objects.create(username=username,
                                          first_name=first_name,
                                          last_name=last_name,
                                          password=password,
                                          is_faculty=False,
                                          is_active=True,
                                          is_student=True,
                                          is_hod=False

                                          )

                    profile_student.objects.create(
                        register_no=username,
                        first_name=first_name,
                        last_name=last_name,
                        batch=batch_id_int,
                        scheme_id=batch_data.scheme,
                        joined_semester=batch_data.semester,
                        university_no=u_no
                    )
                    student_login = MyUser.objects.get(username=username)
                    student_login_id = student_login.id
                    parents.objects.create(student_id=student_login_id)
                    # local_guardian.objects.create(student_id=student_login_id)
                    # qualification.objects.create(student_id=student_login_id, name_of_exam='SSLC')
                    # qualification.objects.create(student_id=student_login_id, name_of_exam='PLUS TWO')

                    # hostel.objects.create(student_id=student_login_id)
                    # admission_details.objects.create(student_id=student_login_id)
                    # siblings.objects.create(student_id=student_login_id)
                    # s_id = MyUser.objects.latest('id')
                    # print(s_id.id)
                    # admission_details.objects.create(student_id=s_id, joined_semester=batch_data.semester)

                    messages.error(request, 'Student ' + full_name + ' successfully added in ' + batch_data.class_name)

    return render(request, 'add_student.html',
                  {
                      "batch_class": batch_data_class,
                      "context": context,
                      "scheme_data": scheme_data,
                      "data_for_self_profile": staff_details_1
                  }
                  )


@login_required
def view_student(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data = batch.objects.all()
    scheme_data = scheme.objects.all()

    if request.method == 'POST':

        batch_id = request.POST.get('batch_select')
        # print(batch_id)
        batch_id_int = int(batch_id)

        if batch_id == '0':

            messages.error(request, 'Please select Batch')

        else:

            batch_id = batch_id_int

            data = profile_student.objects.filter(batch=batch_id)

            batch_data1 = batch.objects.get(id=batch_id)
            scheme_data1 = scheme.objects.get(id=batch_data1.scheme)

            batch_data = batch.objects.all()
            scheme_data = scheme.objects.all()

            return render(request, 'view_student.html',
                          {"student_data": data, "scheme_data1": scheme_data1, 'batch_data1': batch_data1,
                           "context": context,
                           "scheme_data": scheme_data,
                           'batch': batch_data,
                           "data_for_self_profile": staff_details_1
                           })

    return render(request, 'view_student.html',

                  {
                      "batch": batch_data,
                      "scheme_data": scheme_data,
                      "context": context,
                      "data_for_self_profile": staff_details_1

                  }

                  )


'''def student_list(request):
    name = request.session['name']
    context = {'name': name}

    batch_id = request.session['batch_id']
    
    data = profile_student.objects.filter(batch=batch_id)


    batch_data = batch.objects.get(id=batch_id)
    scheme_data = scheme.objects.get(id=batch_data.scheme)
    return render(request, 'student_list.html', {"student_data": data, "scheme_data":scheme_data, 'batch_data': batch_data, "context": context})
'''


# batch details 

@login_required
def create_batch(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    scheme_data = scheme.objects.all()

    tutor_data = profile.objects.all()

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        date_of_join = request.POST.get('date_of_join')
        semester = request.POST.get('semester')
        scheme_input = request.POST.get('scheme')
        tutor_id = request.POST.get('tutor')
        scheme_input_int = int(scheme_input)
        tutor = int(tutor_id)

        if class_name == '0':
            messages.error(request, 'Please select class')
        elif semester == '0':
            messages.error(request, 'Please select Semester')
        elif scheme_input == '0':
            messages.error(request, 'Please select Scheme')
        elif tutor_id == '0':
            messages.error(request, 'Please select Tutor')
        else:
            data = batch.objects.filter(class_name=class_name, date_of_join=date_of_join, semester=semester,
                                        scheme=scheme_input_int, tutor_id=tutor)

            if data:
                messages.error(request, 'The class already exist')
            else:
                batch.objects.create(class_name=class_name, date_of_join=date_of_join, semester=semester,
                                     scheme=scheme_input_int, tutor_id=tutor)
                messages.error(request, 'Successfully added the class ' + class_name + ' year ' + date_of_join)

    return render(request, 'create_batch.html',
                  {"context": context, "scheme_data": scheme_data, "data_for_self_profile": staff_details_1,
                   "tutor_data": tutor_data})


@login_required
def view_batch(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    data = batch.objects.all()
    scheme_data = scheme.objects.all()
    tutor_data = profile.objects.all()
    return render(request, 'view_batch.html', {"batch_data": data, "scheme_data": scheme_data, "context": context,
                                               "data_for_self_profile": staff_details_1, "tutor_data": tutor_data})


# Manage scheme

@login_required
def create_scheme(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    if request.method == 'POST':
        scheme_input = request.POST.get('scheme')
        scheme_count = scheme.objects.filter(scheme=scheme_input)
        if scheme_count:
            messages.error(request,
                           'Already exist ' + scheme_input)
            return redirect(create_scheme)
        else:
            scheme.objects.create(scheme=scheme_input)
            messages.error(request,
                           'Successfully created ' + scheme_input)
            return redirect(create_scheme)

    return render(request, 'create_scheme.html', {'context': context, "data_for_self_profile": staff_details_1})


@login_required
def view_scheme(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()

    return render(request, 'view_scheme.html',
                  {'context': context, "scheme_data": scheme_data, "data_for_self_profile": staff_details_1})


# Manage Subject

@login_required
def create_subject(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()
    if 'create_subject' in request.POST:
        subject_code_input = request.POST.get('subject_code')
        subject_name_input = request.POST.get('subject_name')
        subject_credit = request.POST.get('subject_credit')
        scheme_id = request.POST.get('scheme')
        scheme_id_int = int(scheme_id)

        subject_code = subject_code_input.upper()
        subject_name = subject_name_input.upper()

        # check the subject already exist
        subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id_int).count()
        if subject_exist == 0:
            subject.objects.create(code=subject_code, subject_name=subject_name, credit=subject_credit,
                                   scheme=scheme_id_int)
            messages.error(request, "The Subject " + subject_name + " successfully added")

            return redirect(create_subject)
            # return redirect(request, 'create_subject.html',
            #             {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:
            messages.error(request, "The Subject code already exist!")
            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

    return render(request, 'create_subject.html',
                  {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})


@csrf_exempt
def check_subject_exist(request):
    subject_code = request.POST.get('subject_code')
    scheme_id = request.POST.get('scheme_id')
    subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id).exists()
    if subject_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required
def view_subject(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()
    view_subject_all = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.all()
    none = "None"
    staff_data = profile.objects.all()
    batch_data = batch.objects.all()

    if 'view_subject' in request.POST:
        scheme_id = request.POST.get('scheme_id')
        scheme_id_int = int(scheme_id)
        print(scheme_id_int)

        if scheme_id_int == 0:
            messages.error(request, "Please select scheme")
            return render(request, 'view_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:

            scheme_details = scheme.objects.filter(id=scheme_id_int)

            # for subject and scheme details
            for i in scheme_details:
                scheme_name = i.scheme
                scheme_input_id = i.id

            view_subject = subject.objects.filter(scheme=scheme_id_int)
            return render(request, 'view_subject.html',
                          {'context': context, 'scheme_data': scheme_data, 'view_subject': view_subject,
                           'scheme_input_id': scheme_input_id,
                           'scheme_name': scheme_name, "data_for_self_profile": staff_details_1,
                           'assign_subject_data': assign_subject_data,
                           'none': none,
                           'staff_data': staff_data,
                           'batch_data': batch_data
                           })

    return render(request, 'view_subject.html',
                  {'context': context,
                   'scheme_data': scheme_data,
                   "data_for_self_profile": staff_details_1,
                   "view_subject": view_subject_all,
                   'assign_subject_data': assign_subject_data,
                   'none': none,
                   'staff_data': staff_data,
                   'batch_data': batch_data
                   })


@login_required
def assign_subject_to_staff(request):
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data_class = batch.objects.all()
    scheme_data = scheme.objects.all()
    subject_data = subject.objects.all()
    faculty = profile.objects.all()

    assign_subject_data = subject_to_staff.objects.all()
    faculty_data = profile.objects.all()

    if request.method == 'POST':
        batch_id = int(request.POST.get('batch_id'))
        subject_id = int(request.POST.get('subject_id'))
        faculty_id = int(request.POST.get('faculty_id'))
        sem = int(request.POST.get('semester'))

        batch_id_data = batch.objects.filter(id=batch_id)
        subject_id_data = subject.objects.filter(id=subject_id)
        valid_scheme = False

        for i in batch_id_data:
            for j in subject_id_data:
                if i.scheme == j.scheme:
                    valid_scheme = True

        if batch_id == 0:
            messages.error(request, "Select Class")
        elif subject_id == 0:
            messages.error(request, "Select Subject")
        elif valid_scheme == False:
            messages.error(request, "Select Subject with same scheme")
        elif sem == 0:
            messages.error(request, "Select Semester")
        elif faculty_id == 0:
            messages.error(request, "Select Faculty")
        else:

            check_exist = subject_to_staff.objects.filter(subject_id=subject_id, batch_id=batch_id)
            if check_exist:
                messages.error(request, "Subject Exist")
            else:
                subject_to_staff.objects.create(subject_id=subject_id, batch_id=batch_id, staff_id=faculty_id,
                                                semester=sem)
                messages.error(request, "Successfully added")

    return render(request, 'assign_subject_to_staff.html',
                  {'context': context, "data_for_self_profile": staff_details_1,
                   'batch_class': batch_data_class,
                   'scheme_data': scheme_data,
                   'subject_data': subject_data,
                   'faculty': faculty,
                   'assign_subject_data': assign_subject_data,
                   'faculty_data': faculty_data
                   })


# logout
def log_out(request):
    logout(request)

    return HttpResponseRedirect('/login/')
