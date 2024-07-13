"""
URL configuration for labxpert project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('registration-validation/',views.registration_validation,name='registration_validation'),
    path('login/',views.login_user ,name='login'),
    path('profile-view/',views.profile_view,name='profile-view'),
    path('login-validation/',views.login_validation,name='login-validation'),
    path('profile-update/',views.profile_update,name='profile-update'),
    path('profile-picture-update/',views.profile_picture_update,name='profile-picture-update'),
    path('profile-update-save/',views.profile_update_save,name='profile-update-save'),
    path('logout/',views.logout_user,name='logout'),
]
