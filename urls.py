from django.urls import path, include
from staff.views import add_result, add_sem_result, report, log_out, staff_profile, update_class_of_tutor, \
    update_student_profile, view_classes, university_result

urlpatterns = [
    path('log_out/', log_out, name='log_out'),
    path('staff_profile/', staff_profile, name='staff_profile' ),
    path('', view_classes, name='view_classes'),
    path('update_class_of_tutor/<int:batch_id>/', update_class_of_tutor, name='update_class_of_tutor' ),
    path('university_result/<int:batch_id>/', university_result, name='university_result' ),
    path('update_student_profile/<int:student_id>/', update_student_profile, name='update_student_profile' ),
    path('add_result/<int:batch_id>/', add_result, name='add_result' ),
    path('add_sem_result/<int:batch_id>/<str:month>/<int:year>/<int:semester>/', add_sem_result, name='add_sem_result' ),
    path('report/<int:batch_id>/<int:semester>/', report, name='report'),

]