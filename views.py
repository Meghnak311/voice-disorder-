from atexit import register

import matplotlib as matplotlib
from autoscraper import AutoScraper
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from hod.models import batch, scheme, semester_result, subject, \
    subject_to_staff
from staff.models import profile, st_feedback
from student.models import profile_student, parents
from login.models import MyUser
import login
from django.db.models import Q

from django.db.models import Sum, Max

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np


@login_required
def student_profile(request):
    url = 'https://ktu.edu.in/eu/core/announcements.htm'

    try:
        # url = 'https://ktu.edu.in/home.htm'

        wanted_list = ['ANNOUNCEMENTS', 'Dec 24, 2021', 'Exam Registration opened - B.Tech S3 and S5 (supplementary) '
                                                        'Jan 2022']
        scraper = AutoScraper()
        result = scraper.build(url, wanted_list)
        data1 = result[0]
        data2 = result[1]
        data3 = result[2]
        data4 = result[3]
        data5 = result[4]
        data6 = result[5]

        notif = {'data1': data1,
                 'data2': data2,
                 'data3': data3,
                 'data4': data4,
                 'data5': data5,
                 'data6': data6,

                 }
        request.session['notif'] = notif


    except:

        notif = {'data1': "KTU site cannot reach"}
        request.session['notif'] = notif

    # name = request.session['student_name']
    current_user = request.user
    user_id = current_user.username
    student_login_id = current_user.id
    print(student_login_id)
    print(current_user.username)
    student_details_1 = profile_student.objects.get(register_no=user_id)
    name = student_details_1.first_name + " " + student_details_1.last_name
    name = ""
    id = user_id
    student_data = profile_student.objects.filter(register_no=id)

    for i in student_data:
        print('student', i.id)
        student_id = i.id
        batch_id = i.batch

        name_first = i.first_name
        name_last = i.last_name

    # print(student_id)
    name = name_first + " " + name_last
    context = {'name': name}  # display the name

    batch_data = batch.objects.get(id=batch_id)

    tutor_id = batch_data.tutor_id
    tutor_data = profile.objects.filter(id=tutor_id)
    for tutor_data in tutor_data:
        tutor_name = tutor_data.First_name + " " + tutor_data.Last_name

    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)

    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    subject_data = subject.objects.all()

    total_mark_list = []
    attendance_list = []
    sem_result_list = []

    st_id = student_details_1.id

    for i in assign_subject_data:

        st_data = profile_student.objects.get(id=student_id)

        max_chances = semester_result.objects.filter(subject_id=i.subject_id,
                                                     university_no=st_data.university_no).aggregate(
            Max('no_of_chances'))

        sem_result_data = semester_result.objects.filter(subject_id=i.subject_id, university_no=st_data.university_no,
                                                         no_of_chances=max_chances['no_of_chances__max'])

        print(max_chances['no_of_chances__max'])
        for result in sem_result_data:
            print(result)
            sem_result_tuple = (i.subject_id, st_data.register_no, i.semester, result.grade_point, result.no_of_chances)
            sem_result_list.append(sem_result_tuple)
    # print(attendance_list)
    print(total_mark_list)

    '''if 'profile_pic' in request.POST:
        myfile = request.POST.get['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)'''

    if 'submit_feedback' in request.POST:
        rating = request.POST.get('rating')
        expected = request.POST.get('expected')
        revaluation_subject = request.POST.get('subject')
        revaluation = request.POST.get('revaluation')
        semester = request.POST.get('sem')

        if st_feedback.objects.filter(student_id=student_login_id, semester=semester):
            messages.error(request, "Feedback already submitted")
            return redirect(student_profile)
        else:
            st_feedback.objects.create(student_id=student_login_id, semester=semester,
                                       rating=rating, expected=expected,
                                       revaluation=revaluation,
                                       revaluation_subject=revaluation_subject)
            messages.error(request, "Feedback submitted")
            return redirect(student_profile)

    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        # login_data = MyUser.objects.get(username=id)
        user_data = MyUser.objects.get(username=id)
        user_password = user_data.password
        # user_data.set_password(new_password)
        # current_hased = make_password(current_password)
        user_decrypted = check_password(current_password, user_password)

        if new_password != renew_password:
            messages.error(request, "Password mismatch")

        elif user_decrypted is False:
            messages.error(request, "incorrect old password")
        else:
            new_hased = make_password(new_password)
            user_data.password = new_hased
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(student_profile)

    print(student_login_id)
    parents_data = parents.objects.filter(student_id=student_login_id)


    feedback_data = st_feedback.objects.filter(student_id=student_login_id)

    return render(request, 'student_profile.html',
                  {
                      'student_data': student_data,
                      'scheme_data': scheme_data,
                      'batch_data': batch_data,

                      'context': context,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,

                      'sem_result_list': sem_result_list,
                      'parents_data': parents_data,


                      'student_details_1': student_details_1,
                      'tutor_name': tutor_name,
                      'feedback_data': feedback_data,
                      'notif': notif
                  })


@login_required
def feedback(request):
    current_user = request.user
    user_id = current_user.username
    student_login_id = current_user.id
    if 'view_feedback' in request.POST:
        semester = request.POST.get('sem')
        feedback_data = st_feedback.objects.filter(student_id=student_login_id, semester=semester)
        return render(request, 'feedback.html',
                      {
                          'feedback_data': feedback_data,
                          'notif': request.session['notif']
                      })
    return render(request, 'feedback.html', {
        'notif': request.session['notif']
    })


# logout
def log_out(request):
    logout(request)
    return redirect(login.views.login)
