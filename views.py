from datetime import date, datetime
from autoscraper import AutoScraper
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum, Max

import login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

from hod.models import scheme, semester_result, subject, subject_to_staff, batch
from staff.models import profile, st_feedback, ktu_notification
from login.models import MyUser
from staff.send_sms import send_sms
from student.models import profile_student, parents
from django.core.mail import send_mail

# Staff profile

@login_required
def staff_profile(request):

    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name

    context = {'name': fullname}



    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = MyUser.objects.get(username=user_id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")

        elif check_password(current_password, user_password) is False:
            messages.error(request, "incorrect old password")

        else:
            new_hashed = make_password(new_password)
            user_data.password = new_hashed
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(staff_profile)
    return render(request, 'staff_profile.html',
                  {
                      'context': context,
                      'staff_details': staff_details,
                      'date': date,
                      'notif': request.session['notif']

                  })








# View the classes if tutor
@login_required
def view_classes(request):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    notif_list = []
    notif_data = ktu_notification.objects.all().order_by('-id')[:6]
    for i in notif_data:
        notif_list.append(i.content)

    notif = {
        'data1': notif_list[0],
        'data2': notif_list[1],
        'data3': notif_list[2],
        'data4': notif_list[3],
        'data5': notif_list[4],
        'data6': notif_list[5]
    }
    request.session['notif'] = notif

    staff_id = staff_details.id
    batch_data = batch.objects.filter(tutor_id=staff_id)
    scheme_data = scheme.objects.all()

    return render(request, 'view_classes.html',

                  {

                      'context': context,
                      'batch_data': batch_data,
                      'scheme_data': scheme_data,
                      'staff_details': staff_details,
                      'notif': notif

                  })


# Class details if tutor
@login_required
def update_class_of_tutor(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    batch_data = batch.objects.get(id=batch_id)
    staff_data = profile.objects.all()
    scheme_data = scheme.objects.all()
    join_date = str(batch_data.date_of_join)
    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    sem_result = semester_result.objects.filter(batch_id=batch_id)

    subject_in_sem = subject_to_staff.objects.filter(batch_id=batch_id)
    # all_subject = subject.objects.all()

    if 'update_semester' in request.POST:
        sem = request.POST.get('semester')
        batch_data_update = batch.objects.get(id=batch_id)
        sem = int(sem)
        batch_data_update.semester = sem
        batch_data_update.save()
        messages.error(request, 'Successfully Updated the semester')
        return redirect(update_class_of_tutor, batch_id)

    return render(request, 'update_class_of_tutor.html',
                  {

                      'context': context,
                      'staff_data': staff_data,
                      'batch_data': batch_data,
                      'scheme_data': scheme_data,
                      'date': join_date,
                      'student_data': student_data,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,
                      'semester_result': sem_result,

                      'subject_in_sem': subject_in_sem,
                      'staff_details': staff_details,
                      'notif': request.session['notif']

                  })


# University Result
@login_required
def university_result(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id)

    if 'semester' in request.POST:
        sem = request.POST.get('semester')
        print(sem, type(sem))
        sem = int(sem)
        subject_data = subject.objects.all()

        subject_this_sem = subject_to_staff.objects.filter(semester=sem, batch_id=batch_id)

        return render(request, 'university_result.html',
                      {
                          'context': context,
                          'student_data': student_data,
                          'subject_data': subject_data,
                          'subject_this_sem': subject_this_sem,
                          'staff_details': staff_details,
                      })

    return render(request, 'university_result.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'staff_details': staff_details,
                      'notif': request.session['notif']
                  })


# View and update Student Profile
@login_required
def update_student_profile(request, student_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    print(student_id)
    id = int(student_id)
    student_data = profile_student.objects.filter(id=id)

    for i in student_data:
        batch_id = i.batch
        name_first = i.first_name
        name_last = i.last_name

    batch_data = batch.objects.get(id=batch_id)
    tutor_id = batch_data.tutor_id
    tutor_data = profile.objects.filter(id=tutor_id)
    for tutor_data in tutor_data:
        tutor_name = tutor_data.First_name + " " + tutor_data.Last_name

    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    subject_data = subject.objects.all()


    sem_result_list = []

    for i in assign_subject_data:

        st_data = profile_student.objects.get(id=id)
        # x print(mark_tupple)




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
    # print(total_mark_list)

    if 'edit_profile' in request.POST:

        university_no = request.POST.get('university_no')
        roll_no = request.POST.get('roll_no')

        # parents details

        # Father
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_address = request.POST.get('father_address')
        father_phn = request.POST.get('father_phn')
        father_email = request.POST.get('father_email')

        # Mother
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_address = request.POST.get('mother_address')
        mother_phn = request.POST.get('mother_phn')
        mother_email = request.POST.get('mother_email')

        '''# Guardian
        guardian_name = request.POST.get('guardian_name')
        guardian_relationship = request.POST.get('guardian_relationship')
        guardian_occupation = request.POST.get('guardian_occupation')
        guardian_address = request.POST.get('guardian_address')
        guardian_phn = request.POST.get('guardian_phn')
        guardian_email = request.POST.get('guardian_email')'''

        student_data1 = profile_student.objects.get(id=id)
        username = student_data1.register_no
        student_login = MyUser.objects.get(username=username)
        student_login_id = student_login.id
        student_data1.university_no = university_no
        student_data1.roll_no = roll_no

        student_data1.save()

        if parents.objects.filter(student_id=student_login_id):
            update_parent = parents.objects.get(student_id=student_login_id)
            update_parent.fathers_name = father_name
            update_parent.fathers_occupation = father_occupation
            update_parent.fathers_number = father_phn
            update_parent.fathers_email_id = father_email
            update_parent.fathers_address = father_address

            update_parent.mothers_name = mother_name
            update_parent.mothers_occupation = mother_occupation
            update_parent.mothers_number = mother_phn
            update_parent.mothers_email_id = mother_email
            update_parent.mothers_address = mother_address
            update_parent.save()

        messages.error(request, "Successfully updated")
        return redirect(update_student_profile, student_id)

    if 'change_password' in request.POST:
        # current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')
        student_data1 = profile_student.objects.get(id=id)

        user_data = MyUser.objects.get(username=student_data1.register_no)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")
            return redirect(update_student_profile, student_id)
        # elif current_password != user_password:
        #    messages.error(request, "incorrect old password")
        else:
            new_hashed = make_password(new_password)
            user_data.password = new_hashed
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(update_student_profile, student_id)

    std_profile_data_login = profile_student.objects.get(id=id)
    login_details = MyUser.objects.get(username=std_profile_data_login.register_no)

    student_login_id = login_details.id

    parents_data = parents.objects.filter(student_id=student_login_id)


    feedback_data = st_feedback.objects.all().order_by('semester')
    return render(request, 'update_student_profile.html',
                  {
                      'student_data': student_data,
                      'scheme_data': scheme_data,
                      'batch_data': batch_data,

                      'context': context,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,

                      'sem_result_list': sem_result_list,
                      'parents_data': parents_data,


                      'tutor_name': tutor_name,
                      'staff_details': staff_details,
                      'feedback_data': feedback_data,
                      'notif': request.session['notif']
                  })


# Selecting the sem, month and year for add sem result
@login_required
def add_result(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    batch_id = int(batch_id)
    sem_result = semester_result.objects.filter(batch_id=batch_id).order_by('semester').distinct('semester')

    if 'select_sem_and_year' in request.POST:
        month_year = request.POST.get('month_and_year')
        semester = request.POST.get('sem')
        month_year = month_year.split('-')

        print(month_year, type(month_year))
        print(semester, type(semester))
        month = int(month_year[1])
        year = int(month_year[0])
        print(month, year)
        return redirect(add_sem_result, batch_id, int(month), year, semester)
    return render(request, 'add_result.html', {
        'context': context,
        'sem_result': sem_result,
        'staff_details': staff_details,
        'notif': request.session['notif']
    })


# Adding the sem result
@login_required
def add_sem_result(request, batch_id, month, year, semester):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id)
    subject_in_sem = subject_to_staff.objects.filter(batch_id=batch_id, semester=semester)
    all_subject = subject.objects.all()
    sem_result = semester_result.objects.filter(semester=semester, batch_id=batch_id)

    batch_data = batch.objects.get(id=batch_id)
    batch_scheme_id = batch_data.scheme
    batch_scheme_data = scheme.objects.get(id=batch_scheme_id)
    batch_scheme = batch_scheme_data.scheme
    print(batch_scheme)

    if request.method == 'POST':
        mark_list = []
        for j in student_data:
            for i in subject_in_sem:
                name_of_tag = str(j.university_no) + '-' + str(i.subject_id)
                print(name_of_tag)
                x = request.POST.getlist(name_of_tag)
                print(x)

                mark_tuple = (j.university_no, i.subject_id, float(x[0]))
                mark_list.append(mark_tuple)
                # print(type(int(month)))
                print(month)
                month_int = month
                year_int = year
                already_exist = semester_result.objects.filter(university_no=j.university_no, subject_id=i.subject_id,
                                                               grade_point=float(x[0]))
                if already_exist:
                    pass
                else:
                    chance_count = semester_result.objects.filter(university_no=j.university_no,
                                                                  subject_id=i.subject_id).count()
                    if chance_count == 0:
                        semester_result.objects.create(university_no=j.university_no, subject_id=i.subject_id,
                                                       grade_point=float(x[0]), semester=semester, month=month_int,
                                                       year=year_int, batch_id=batch_id, no_of_chances=1)
                    else:
                        chance_count += 1
                        semester_result.objects.create(university_no=j.university_no, subject_id=i.subject_id,
                                                       grade_point=float(x[0]), semester=semester, month=month_int,
                                                       year=year_int, batch_id=batch_id, no_of_chances=chance_count)

                # print(x)
        print(mark_list)

        return redirect(report, batch_id, semester)
        # return redirect(update_class_of_tutor, batch_id=batch_id)
    return render(request, 'add_sem_result.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_in_sem': subject_in_sem,
                      'all_subject': all_subject,
                      'semester_result': sem_result,
                      'batch_scheme': batch_scheme,
                      'staff_details': staff_details,
                      'notif': request.session['notif']
                  })


# Generate report
@login_required
def report(request, batch_id, semester):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    batch_data = batch.objects.filter(id=batch_id)
    student_data = profile_student.objects.filter(batch=batch_id)
    result_data = semester_result.objects.filter(batch_id=batch_id, semester=semester)
    subject_data = subject.objects.all()
    subject_in_sem_id = subject_to_staff.objects.filter(semester=semester, batch_id=batch_id)

    previous_sem = range(1, semester)
    print(previous_sem)

    mark_report = []

    total_credit = 0
    for j in subject_in_sem_id:
        for subj in subject_data:
            if subj.id == j.subject_id:
                total_credit += subj.credit

    print('credit', total_credit)
    for i in student_data:
        arrears_in_current_sem = 0
        absent = 0
        sgpa = 0
        for j in subject_in_sem_id:
            for subj in subject_data:
                if subj.id == j.subject_id:
                    for result in result_data:
                        if i.university_no == result.university_no:
                            if result.subject_id == subj.id:
                                if result.no_of_chances == 1:
                                    if result.grade_point == 0:
                                        arrears_in_current_sem += 1
                                    if result.grade_point == -1:
                                        absent += 1
                                    gpi = result.grade_point
                                    if result.grade_point == -1:
                                        gpi = 0
                                    sgpa = sgpa + (subj.credit * gpi)
        print(i.first_name, sgpa)
        tuple_data = (i.university_no, arrears_in_current_sem, absent, round(sgpa / total_credit, 2))
        mark_report.append(tuple_data)
    print(mark_report)

    prev_sem_arrears = []
    for i in range(1, semester + 1):
        for j in student_data:
            count = 0
            subject_in_sem = subject_to_staff.objects.filter(semester=i)
            for subject_in_sem in subject_in_sem:
                if semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                  university_no=j.university_no).count() > 1:
                    chance = semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                            university_no=j.university_no).count()
                    supply = semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                            university_no=j.university_no, no_of_chances=chance,
                                                            grade_point__lte=0)
                    if supply:
                        count += 1
                else:
                    # chance = semester_result.objects.filter(subject_id = subject_in_sem.subject_id, semester=i,
                    # university_no=j.university_no).count()
                    supply = semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                            university_no=j.university_no, no_of_chances=1,
                                                            grade_point__lte=0)
                    if supply:
                        count += 1
            arrear_tuple = (j.university_no, i, count)
            prev_sem_arrears.append(arrear_tuple)

    print(prev_sem_arrears)

    absent_in_each_subject = []
    no_of_students_passed = []
    no_of_students_failed = []
    no_of_o_grade = []
    failed_only_this_subj = []
    students_appeared = []
    total_students = profile_student.objects.filter(batch=batch_id).count()
    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_absent = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point=-1).count()
                absent_subject_tuple = (j.code, no_of_absent)
                absent_in_each_subject.append(absent_subject_tuple)

    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_passed = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point__gte=5.5).count()
                passed = (j.code, no_of_passed)
                no_of_students_passed.append(passed)

    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_failed = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point__lte=0).count()
                failed = (j.code, no_of_failed)
                no_of_students_failed.append(failed)
    print('subj', no_of_students_failed)
    for i in no_of_students_failed:
        print(i)

    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_o_gr = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                            grade_point=10).count()
                no_o_grade = (j.code, no_of_o_gr)
                no_of_o_grade.append(no_o_grade)

    print('grade', no_of_o_grade)
    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_absent = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point=-1).count()
                appeared_subject_tuple = (j.code, total_students - no_of_absent)
                students_appeared.append(appeared_subject_tuple)

    pass_per_by_total = []
    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_passed = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point__gte=5).count()
                passed_perc = (j.code, round((no_of_passed / total_students * 100), 2))
                pass_per_by_total.append(passed_perc)

    appeared_perc = []
    for i in students_appeared:
        for j in no_of_students_passed:
            if i[0] == j[0]:
                pass_perc_by_appear = round((j[1] / i[1]) * 100, 2)
                tple = (i[0], pass_perc_by_appear)
                appeared_perc.append(tple)
    print(appeared_perc)

    return render(request, 'report.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'result_data': result_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'semester': semester,
                      'subject_in_sem_id': subject_in_sem_id,
                      'previous_sem': previous_sem,
                      'mark_report': mark_report,
                      'prev_sem_arrears': prev_sem_arrears,
                      'absent_in_each_subject': absent_in_each_subject,
                      'no_of_students_passed': no_of_students_passed,
                      'no_of_students_failed': no_of_students_failed,
                      'no_of_o_grade': no_of_o_grade,
                      'failed_only_this_subj': failed_only_this_subj,
                      'total_students': total_students,
                      'students_appeared': students_appeared,
                      'pass_per_by_total': pass_per_by_total,
                      'appeared_perc': appeared_perc,
                      'staff_details': staff_details,
                      'notif': request.session['notif']

                  })


# logout

def log_out(request):
    logout(request)
    return redirect(login.views.login)
