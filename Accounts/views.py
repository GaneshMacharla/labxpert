from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpRequest
from django.http import JsonResponse
import re
from django.contrib.auth.decorators import login_required
from .models import Profile
from quiz.models import Quiz,Responses
from Dailyquest.models import Quest
from Dailyquest import models
# Create your views heref.


def is_valid_email(email):
    # Regular expression for basic email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def is_valid_phone(phone):
    phone_regex=r'^[7896]\d{9}$'
    return re.match(phone_regex,phone)

def signup(request):
    return render(request,'Accounts/signup.html')

def login_user(request):
    return render(request,'Accounts/login.html')

def registration_validation(request):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        fullname=request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        isLecturer=request.POST.get('isLecturer')
        # phone=request.POST.get('phone')
        # address=request.POST.get('address')
        # Generate fingerprint and store
        #fingerprint = generate_fingerprint(request)
        
        #check edge cases for user details
        if password!=confirm_password:
            messages.error(request,'passwords did not match ')
            return redirect('../signup')
        if User.objects.filter(username=pin).exists():
            messages.error(request, 'Username already exists.')
            return redirect('../signup')
        if User.objects.filter(email=email).exists():
            messages.error(request,'email already exists')
            return redirect('../signup')
        if len(password)<5:
            messages.error(request,'password is to short,please enter a valid password.')
            return redirect('../signup')
        if not is_valid_email(email):
            messages.error(request,'email is invalid')
            return redirect('../signup')
        # if not is_valid_phone(phone):
        #     messages.error(request,'phone number is invalid')
        #     return redirect('../signup')
        user=User.objects.create_user(pin,email,password)
        user.save()
        #store some more information about the user into the database
        user_profile=Profile()
        if isLecturer is not None:
            user_profile.isLecturer=True
        user_profile.pin=user
        user_profile.phone="0000-0000-00"
        # user_profile.address=address
        user_profile.fullname=fullname
        user_profile.save()
        

        messages.success(request, 'Successfully registered.')
        return redirect('../login')
    else:
        return render(request,'Accounts/signup.html')
    

def login_validation(request):
    if request.method == 'POST':
        pin= request.POST.get('pin')
        password = request.POST.get('password') 
        #fingerprint = generate_fingerprint(request) 1
        # Authenticate the user
        user = authenticate(username=pin, password=password)
        # print(user)
        if user is not None:
            login(request,user)
            messages.success(request,'sucessfully logged in')
            return redirect('index')
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password')
            return redirect('login')
        
    else:
        # Method Not Allowed for non-POST requests
        return render(request, 'Accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/Accounts/login/')
def profile_view(request):
    # print(request.user)
    user_profile = get_object_or_404(Profile, pin=request.user)
    print(user_profile.isLecturer)

    quizzes=Quiz.objects.filter(host=request.user)
    # print(f"Quizzes: {quizzes}")

    quests=Quest.objects.filter(host=request.user)
    #quiz responses
    attended_quizes=Responses.objects.filter(pin=request.user)
    attended_quests=models.Responses.objects.filter(pin=request.user)
    # print(quizzes)
    # users=UserDetails.objects.filter(user=request.user)
    if not user_profile.image:
        user_profile.image="images/avatar7.png"
    # Prepare the details to pass to the template
    details = { 'fullname': user_profile.fullname,'image':user_profile.image,'phone':user_profile.phone,'isLecturer':user_profile.isLecturer,'quizzes':quizzes,'quests':quests,'attended_quizes':attended_quizes,'attended_quests':attended_quests}
    # Render the profile template with the details
    return render(request, 'Accounts/profile.html', details)  
    

@login_required(login_url='/Accounts/login/')
def profile_update(request):
    user=get_object_or_404(Profile,pin=request.user)
    if not user.image:
        user.image="images/avatar7.png"
    details={'fullname':user.fullname,'image':user.image,'phone':user.phone}
    return render(request,'Accounts/profileupdate.html',details)

@login_required(login_url='/Accounts/login/')
def profile_update_save(request):
    fullname=request.POST.get('fullname')
    phone=request.POST.get('phone')
    # phone=request.POST.get('phone')
    # address=request.POST.get('address')
    # if not is_valid_phone(phone):
    #     messages.error(request,'phone number is invalid')
    #     return redirect('profile-update-save')
    if len(fullname)==0:
        messages.error(request,'name cannot be empty')
        return redirect('profile-update-save')
    # if len(address)==0:
    #     messages.error(request,'address cannot be empty')
    #     return redirect('profile-update-save')
    
    user=get_object_or_404(Profile,pin=request.user)
    user.fullname=fullname
    user.phone=phone
    # user.phone=phone
    # user.address=address
    user.save()
    return redirect('profile-view')

@login_required(login_url='/Accounts/login/')
def profile_picture_update(request):
    profile =get_object_or_404(Profile,pin=request.user)
    profile.image = request.FILES.get('image')
    profile.save()
    return redirect('profile-view')  # Redirect to the user's profile page after image update

