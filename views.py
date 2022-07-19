from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages

from user.models import login
from autoscraper import AutoScraper


def login_page(request):
    user_details = login.objects.all().count()
    print(user_details)

    url = 'https://ktu.edu.in/eu/core/announcements.htm'

    try:
        # url = 'https://ktu.edu.in/home.htm'

        wanted_list = ['ANNOUNCEMENTS', 'Dec 24, 2021', 'Exam Registration opened - B.Tech S3 and S5 (supplementary) '
                                                        'Jan 2022']
        scraper = AutoScraper()
        result = scraper.build(url, wanted_list)
        # print(result)
        data1 = result[0]
        data2 = result[1]
        data3 = result[2]

        notif = {'data1': data1,
                 'data2': data2,
                 'data3': data3
                 }


    except:

        notif = {'data1': "KTU site cannot reach"}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if login.objects.filter(email=username, password=password, category='Student', is_active=True):
            return render(request, 'dash.html', {'notif': notif})
        elif login.objects.filter(email=username, password=password, category='Admin', is_active=True):
            return render(request, 'dashad.html', {'notif': notif})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(login_page)
    return render(request, 'Login.html')




def user_name(request):
    return HttpResponse('<h2>Haii</h2')
