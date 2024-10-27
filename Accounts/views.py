from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import re
from django.contrib.auth.decorators import login_required
from .models import Profile
from quiz.models import Quiz
from Dailyquest.models import Quest
from Exam.models import Exam
import Dailyquest
import quiz
from Exam.models import Responses
from django.shortcuts import render
from shapely.geometry import Point, Polygon
from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from shapely.geometry import Polygon, Point
import math
import geocoder

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
            messages.warning(request,'passwords did not match ')
            return redirect('../signup')
        if User.objects.filter(username=pin).exists():
            messages.warning(request, 'Username already exists.')
            return redirect('../signup')
        if User.objects.filter(email=email).exists():
            messages.warning(request,'email already exists')
            return redirect('../signup')
        if len(password)<5:
            messages.warning(request,'password is to short,please enter a valid password.')
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
        user_profile=Profile.objects.create(pin=user)
        if isLecturer is not None:
            user_profile.isLecturer=True
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
        pin = request.POST.get('pin')
        password = request.POST.get('password') 

# Fetch location based on IP address
        check_user_location(request)
        # Authenticate the user
        user = authenticate(username=pin, password=password)
        if user is not None:
            login(request, user)    
            messages.success(request, 'Successfully logged in.')
            return redirect('index')
        else:
            # Authentication failed
            messages.warning(request, 'Invalid username or password')
            return redirect('login')
    
    else:
        # Method Not Allowed for non-POST requests
        return render(request, 'Accounts/login.html')







# Define the central point (longitude, latitude) and radius in meters
REGION_CENTER = (78.452350, 17.402179)  # Choose a central coordinate
ALLOWED_RADIUS_METERS = 100  # Example radius; adjust based on your region

def haversine(lon1, lat1, lon2, lat2):
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371000 *c  # Radius of Earth in meters
    return distance

def check_user_location(request):
    try:
        # Get latitude and longitude from POST request
        # latitude = float(request.POST.get('latitude'))
        # longitude = float(request.POST.get('longitude'))
        latitude=17.402300
        longitude=78.451851
        # Round to six decimal places
        latitude = round(latitude, 6)
        longitude = round(longitude, 6)
     
        # Calculate the distance from the user's location to the central region point
        distance = haversine(longitude, latitude, REGION_CENTER[0], REGION_CENTER[1])
        print(distance)
        # Check if the user is within the allowed radius
        if distance > ALLOWED_RADIUS_METERS:
            messages.warning(request, 'Login denied: Outside region not allowed.')
            return redirect('login')
    except (TypeError, ValueError): 
        messages.warning(request, 'Invalid location data')
        return redirect('login')
    
    # If inside the radius, continue the login process
    # Add any additional login logic here



def logout_user(request):
    messages.success(request,'Sucessfully logged out..')
    logout(request)
    return redirect('index')

@login_required(login_url='/Accounts/login/')
def profile_view(request):
    # print(request.user)
    user_profile = get_object_or_404(Profile, pin=request.user)
    # print(user_profile.isLecturer)
    quizzes=Quiz.objects.filter(host=request.user)
    quests=Quest.objects.filter(host=request.user)
    exams=Exam.objects.filter(host=request.user)
    #quiz responses
    attended_quizes=quiz.models.Responses.objects.filter(pin=request.user)
    #quest responses
    attended_quests=Dailyquest.models.Responses.objects.filter(pin=request.user)
    #exam responses
    attended_exams=Responses.objects.filter(pin=request.user)
    # print(quizzes)
    # users=UserDetails.objects.filter(user=request.user)
    if not user_profile.image:
        user_profile.image="images/avatar7.png"
    # Prepare the details to pass to the template
    details = { 'fullname': user_profile.fullname,'image':user_profile.image,'phone':user_profile.phone,'isLecturer':user_profile.isLecturer,'quizzes':quizzes,'quests':quests,'attended_quizes':attended_quizes,'attended_quests':attended_quests,'exams':exams,'attended_exams':attended_exams}
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
    email=request.POST.get('email')
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
    student=get_object_or_404(User,username=request.user)
    user=get_object_or_404(Profile,pin=request.user)
    user.fullname=fullname
    user.phone=phone
    student.email=email
    student.save()
    # user.phone=phone
    # user.address=address
    user.save()
    messages.success(request,"your profile has been successfully updated..")
    return redirect('profile-view')

@login_required(login_url='/Accounts/login/')
def profile_picture_update(request):
    profile =get_object_or_404(Profile,pin=request.user)
    profile.image = request.FILES.get('image')
    profile.save()
    return redirect('profile-view')  # Redirect to the user's profile page after image update

