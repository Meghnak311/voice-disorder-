from django.urls import path, include


from student.views import student_profile,  feedback, log_out

urlpatterns = [
 

    path('', student_profile, name='student_profile'),
    path('feedback/', feedback, name='feedback'),
    path('log_out/', log_out, name='log_out'),
]