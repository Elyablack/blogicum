from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        '',
        views.CreateProfileView.as_view(),
        name='registration'
    ),
    path(
        'profile/edit/',
        views.EditProfileView.as_view(),
        name='edit_profile'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='registration/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='registration/login.html'),
        name='login'),
]
