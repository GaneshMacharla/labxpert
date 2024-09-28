import io
from django.shortcuts import render,redirect,get_object_or_404
from .models import Quest,Question,Answer,Responses
import uuid
from django.utils import timezone
from Accounts.models import Profile
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import google.generativeai as genai
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from labxpert.generateid import generate_id
from django.contrib import messages
from django.conf import settings
# Create your views here.

api_key = 'AIzaSyBiwzkDo3NW1vau6UaNlMlppIhdBGQzF7o'


def create_daily_quest_questions(request):
    return render(request,'Dailyquest/createdailyquestquestions.html')

def submit_questions(request):
    if request.method=='POST':
        num_quesetions=int(request.POST.get('numQuestions',0))
        shift=request.POST.get('shift')
        semester=request.POST.get('semester')
        subject=request.POST.get('subject')
        title=request.POST.get('title')
        starting_time=request.POST.get('starttime')
        ending_time=request.POST.get('endtime')
        quest=Quest.objects.create(host=request.user,subject=subject,title=title,quest_id=generate_id(),created_date=timezone.now(),start_time=starting_time,end_time=ending_time,shift=shift,semester=semester)
        for i in range(num_quesetions):
            question_text=request.POST.get(f'question{i}')
            question=Question.objects.create(quest=quest,question_text=question_text)
        
        messages.success(request,'Dailyquest has been created Sucessfully..')
        return redirect('profile-view')

@login_required(login_url='/Accounts/login/')
def quest_questions(request,quest_id):
    quest=get_object_or_404(Quest,quest_id=quest_id)
    questions=quest.question_set.all()
    # now=timezone.now()
    # remaining_time=quest.end_time-now
    # print(remaining_time)
    # print(questions)
    profile=get_object_or_404(Profile,pin=request.user)
    return render(request,'Dailyquest/questquestionslists.html',
                  {'questions':questions,'isLecturer':profile.isLecturer,'quest_id':quest.quest_id,'title':quest.title,'subject':quest.subject,'quest':quest})

@login_required(login_url='/Accounts/login/')
def join_quest(request,quest_id):
    return quest_questions(request,quest_id)

def submit_quest_answers(request,quest_id):
    
    user=User.objects.get(username=request.user)
    quest=get_object_or_404(Quest,quest_id=quest_id)

    if Responses.objects.filter(pin=request.user,quest=quest).exists():
        messages.warning(request,"sorry,you have already submitted the answers..")
        return redirect('index')

    # response.submitted_date=timezone.now()
    questions=quest.question_set.all()
    min_points=(len(questions)*10)//4
    print(min_points)
    counter=1
    total_points=0
    for question in questions:
        code=request.POST.get(f"code{counter}")
        if len(code)==0:
            code="0"
        answer=Answer()
        answer.output=request.FILES.get(f"image{counter}")
        if answer.output==None or answer.output=="":
            answer.output="/quest/outputs/nocode.jpeg"
        answer.code=code
        answer.question=question
        answer.save()
        # print(question)
        total_points+=int(check_code(api_key,code,question.question_text,10))
        # answer=Answer.objects.create(question=question,code=code,output=output)
        counter+=1
    response=Responses.objects.create(quest=quest,pin=user.username,submitted_date=timezone.now())
    response.total_points=total_points
    response.subject=quest.subject
    response.shift=quest.shift
    response.semester=quest.semester    
    print(total_points)
    if total_points>min_points:
        response.attendance_status=True
        send_attendance_email(user.email,request.user,quest.subject,total_points,isPresent=True)
    else:
        send_attendance_email(user.email,request.user,quest.subject,total_points,isPresent=False)



    response.save()

    # print(min_points)
    # print("Ganesh")
    messages.success(request,'your answers has been saved Sucessfully..')
    return redirect('profile-view')




def check_code(api_key,code,question,max_points):
    # Set the API key as an environment variable
    os.environ['API_KEY'] = api_key
    
    # Configure the API key
    genai.configure(api_key=os.environ['API_KEY'])
    
    # Choose a model that's appropriate for your use case
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print(code)
    # Define the prompt
    prompt =f"""
    question:{question},
    code:{code},
    max_points:{max_points},
    if the code is empty give 0 points for the code.
    I have given question,code and max_points You should evaluate the code based on the question and you have to allot points for that code.
    Main points:you have to see, is the user written correct code and following the syntaxes  based on langauge.if the code allot zero marks.
    conditions:You should give to me only points and you must not exceed the max_points range while alloting the points to the code. Don't give any extra information.
"""
    
    # Generate content based on the prompt
    response = model.generate_content(prompt)
    print(response.text)
    # Return the generated content
    return response.text




def generate_pdf(quest):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    # Title and quiz information
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.darkblue)
    p.drawString(100, height - 50, f"Quiz ID: {quest.quest_id}")
    p.drawString(100, height - 80, f"Title: {quest.title}")

    # Table headers
    headers = ["S.No", "PIN", "Correct Answers"]

    # Fetch and prepare response data
    responses = quest.responses_set.all()
    data = [headers]  # Add headers as the first row
    if responses.exists():
        for i, response in enumerate(responses, start=1):
            data.append([str(i), response.pin, str(response.total_points)])
    else:
        data.append(["-", "-", "No responses have been submitted yet."])

    # Create table
    table = Table(data, colWidths=[50, 200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Calculate position to draw the table
    table.wrapOn(p, width, height)
    table.drawOn(p, 70, height - 150)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer



def responses(request, quest_id):
    quest = get_object_or_404(Quest,quest_id=quest_id)
    # print(quiz)
    pdf_buffer = generate_pdf(quest)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}-responses.pdf"'.format(quest.title)
    return response

@login_required(login_url='/Accounts/login/')
def check_attendance(request):
    return render(request,'Dailyquest/checkattendance.html')


def show_attendance(request):
    if request.method=="POST":
        branch=request.POST.get('branch')
        shift=request.POST.get('shift')
        semester=request.POST.get('semester')
        subject=request.POST.get('subject')
        profile=get_object_or_404(Profile,pin=request.user)
        attended_students_attendance=None
        semester_attendance=None
        print(semester)
        print(shift)
        if profile.isLecturer:
            attended_students_attendance=Responses.objects.filter(subject=subject,shift=shift,semester=semester,attendance_status=True)
            # print("HELLO WORLD")
        else:
            semester_attendance=Responses.objects.filter(pin=request.user,subject=subject,shift=shift,semester=semester)
        
        messages.success(request,'Attendance has been fetched Sucessfully..')
        return  render(request,'Dailyquest/showattendance.html',{'attended_students_attendance':attended_students_attendance,'semester_attendance':semester_attendance,'isLecturer':profile.isLecturer})
    




#email
from django.core.mail import send_mail
from django.conf import settings

def send_attendance_email(student_email, student_name,s,marks,isPresent):
    subject = 'Quest Attendance Status'
    if isPresent:
        message = f'Hi 👋 {student_name},\n\nYour attendance for the today {s} quest has been successfully recorded.\n\n your marks: {marks}\n\n Attendance status:Present \n\nThank you!  keep going.. 🙌🙌\n\n--labxpert TeamMembers'
    else:
        message = f'Hi 👋 {student_name},\n\nYour attendance for the today {s} quest has not been recorded.Because you got less marks for the today daily quest.\n\n your marks: {marks}\n\n Attendance status:Present\n\n\n\nAttend well for the upcoming quests\n\n--labxpert TeamMembers'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student_email]
    send_mail(subject, message, email_from, recipient_list)










