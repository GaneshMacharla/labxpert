from django.shortcuts import render,redirect
from django.contrib import messages
from .models import FeedBack
# Create your views here.


def feedback(request):
    return render(request,'feedback/feedback.html')


def submit_feedback(request):

    email=request.POST.get('email')
    text=request.POST.get('feedback')
    user=FeedBack.objects.create(email=email,text=text)
    messages.success(request,'your feedback has been submitted sucessfully..')
    return redirect('index')
