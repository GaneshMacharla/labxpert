from django.shortcuts import render,get_object_or_404
from Accounts.models import Profile
# Create your views here.


def index(request):
    print(request.user)
    if request.user.is_authenticated:
        profile=get_object_or_404(Profile,pin=request.user)
    else:
        profile=None
    # print(profile.isLecturer)
    return render(request,'Home/index.html',{'profile':profile})

 
