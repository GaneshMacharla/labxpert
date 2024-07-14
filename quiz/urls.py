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

    path('create-quiz/',views.create_quiz,name='create-quiz'),
    path('submit-quiz/',views.submit_quiz,name='submit-quiz'),
    path('submit-answers/',views.submit_answers,name='submit-answers'),
    path('<uuid:quiz_id>/',views.quiz_questions,name="quiz-questions"),
    path('responses/<uuid:quiz_id>/',views.responses,name='respones'),
    path('joinquiz/<uuid:quiz_id>/',views.join_quiz,name='join-quiz'),

]
