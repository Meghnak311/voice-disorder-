from django.urls import path, include
from hod.views import assign_subject_to_staff, add_staff, view_student, create_batch, add_student, \
    view_faculty, add_staff, log_out,view_faculty, add_student, create_batch, view_student

from hod.views import view_batch,  create_scheme
from hod.views import view_scheme, create_subject, view_subject
from hod.views import check_subject_exist, check_user_exist

urlpatterns = [

    #path('', hod_index, name='hod_index'),
    path('', add_staff, name='add_staff'),
    path('log_out/', log_out, name='log_out'),
    path('view_faculty/', view_faculty, name='view_faculty'),
    path('add_student/', add_student, name='add_student'),
    path('create_batch/', create_batch, name='create_batch'),
    path('view_student/', view_student, name='view_student'),
    path('view_batch/', view_batch, name='view_batch'),
    path('create_scheme/', create_scheme, name='create_scheme'),
    path('view_scheme/', view_scheme, name='view_scheme'),
    path('create_subject/', create_subject, name='create_subject'),
    path('view_subject/', view_subject, name='view_subject'),
    path('assign_subject/', assign_subject_to_staff, name='assign_subject_to_staff'),
    path('check_subject_exist', check_subject_exist, name='check_subject_exist'),
    path('check_user_exist', check_user_exist, name='check_user_exist'),

]
