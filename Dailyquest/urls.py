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

    path('createdailyquestquestions/',views.create_daily_quest_questions,name='createdailyquestquestions'),
    path('submit-questions/',views.submit_questions,name='submit-questions'),
    path('joinquest/<int:quest_id>/',views.join_quest,name="quest-questions"),
    path('<int:quest_id>/',views.quest_questions,name="quest-questions"),
    path('submit-quest-answers/<int:quest_id>/',views.submit_quest_answers,name="submit-quest-answers"),
    path('responses/<int:quest_id>/',views.responses,name="responses"),
    path('check-attendance/',views.check_attendance,name="check-attendance"),
    path('show-attendance',views.show_attendance,name='show-attendance '),
    

    # path('responses/<uuid:quest_id>/',views.responses,name='resposnes'),

]
