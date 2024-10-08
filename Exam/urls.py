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

    path('create-exam/',views.create_exam,name="create-exam"),
    # path('responses/<uuid:quest_id>/',views.responses,name='resposnes'),
    path('submit-questions/',views.submit_questions,name="submit-questions"),
    path('<int:exam_id>/',views.exam_questions,name='exam-questions'),
    path('joinexam/<int:exam_id>/',views.join_exam,name='join-exam'),
    path('responses/<int:exam_id>/',views.responses,name='responses'),
    path('submit-exam-answers/<int:exam_id>/',views.submit_exam_answers,name='submit-exam-answers'),
    # path('responses/<uuid:quest_id>/',views.responses,name='resposnes'),

]
