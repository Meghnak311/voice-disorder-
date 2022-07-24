from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import AuthenticationBackend, MyUser
from django.contrib import messages
import student
from django.contrib.auth import login


# Create your views here.
from django.shortcuts import render

from django.shortcuts import render


def error_404(request, exception):
    return render(request, '404.html')


def error_500(request, *args, **argv):
    data = {}
    return render(request, '500.html', data)


def error_403(request, exception):
    return render(request, '403.html')


def error_400(request, exception):
    data = {}
    return render(request, '400.html', data)

def login_page(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        # bug in login
        # user = AuthenticationBackend.authenticate(self=None,request=request, username=username1, password=password1, is_hod = True ,  is_faculty=False, is_student=False)
        # print(user)
        if AuthenticationBackend.authenticate(self=None, request=request, username=username1, password=password1,
                                              is_hod=True, is_faculty=False, is_student=False) is not None:
            user = AuthenticationBackend.authenticate(self=None, request=request, username=username1,
                                                      password=password1, is_hod=True, is_faculty=False,
                                                      is_student=False)

            login(request, user)
            # Redirect to a success page.
            return redirect('add_staff')
        elif AuthenticationBackend.authenticate(self=None, request=request, username=username1, password=password1,
                                                is_hod=False, is_faculty=True, is_student=False) is not None:
            user = AuthenticationBackend.authenticate(self=None, request=request, username=username1,
                                                      password=password1, is_hod=False, is_faculty=True,
                                                      is_student=False)
            login(request, user)
            # Redirect to a success page.
            return redirect('view_classes')

        elif AuthenticationBackend.authenticate(self=None, request=request, username=username1, password=password1,
                                                is_hod=False, is_faculty=False, is_student=True) is not None:
            user = AuthenticationBackend.authenticate(self=None, request=request, username=username1,
                                                      password=password1, is_hod=False, is_faculty=False,
                                                      is_student=True)

            login(request, user)
            # Redirect to a success page.
            return redirect('student_profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_page')


    return render(request, 'login.html')
