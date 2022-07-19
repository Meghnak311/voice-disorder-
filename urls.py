from django.urls import path, include

from user.views import user_page

urlpatterns = {
    path('user/', user_page, name=user_page),
}
