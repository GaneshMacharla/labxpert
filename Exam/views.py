import io
from django.shortcuts import render,redirect,get_object_or_404
import uuid
from .models import Exam,Question,Answer
from django.utils import timezone
from Accounts.models import Profile
from .models import Responses,Exam
import os
# import google.generativeai as genai
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Dailyquest.views import check_code
# Create your views here.
api_key = 'AIzaSyBiwzkDo3NW1vau6UaNlMlppIhdBGQzF7o'

def create_exam(request):
    return render(request,'Exam/createexamquestions.html')


def submit_questions(request):
    if request.method=='POST':
        num_quesetions=int(request.POST.get('numQuestions',0))
        subject=request.POST.get('subject')
        title=request.POST.get('title')
        exam=Exam.objects.create(host=request.user,subject=subject,title=title,exam_id=uuid.uuid4(),created_date=timezone.now())
        for i in range(num_quesetions):
            question_text=request.POST.get(f'question{i}')
            question=Question.objects.create(quest=exam,question_text=question_text)
        
        return redirect('profile-view')
    

def exam_questions(request,exam_id):
    exam=get_object_or_404(Exam,exam_id=exam_id)
    questions=exam.question_set.all()
    profile=get_object_or_404(Profile,pin=request.user)
    return render(request,'Exam/examquestionslist.html',{'questions':questions,'isLecturer':profile.isLecturer,'exam_id':exam.exam_id})





def join_exam(request,exam_id):
    return exam_questions(request,exam_id)


def submit_exam_answers(request,exam_id):
    exam=get_object_or_404(Exam,exam_id=exam_id)
    response=Responses.objects.create(exam=exam,pin=request.user)
    response.submitted_date=timezone.now()
    questions=exam.question_set.all()
    counter=1
    total_points=0
    for question in questions:
        code=request.POST.get(f"code{counter}")
        answer=Answer()
        answer.output=request.FILES.get(f"image{counter}")
        if answer.output==None or answer.output=="":
            answer.output="/quest/outputs/nocode.jpeg"
        answer.code=code
        answer.question=question
        answer.save()
        print(question)
        total_points+=int(check_code(api_key,code,question.question_text,10))
        # answer=Answer.objects.create(question=question,code=code,output=output)
        counter+=1
    response.total_points=total_points
    return redirect('profile-view')


def generate_pdf(exam):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    # Title and quiz information
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.darkblue)
    p.drawString(100, height - 50, f"Quiz ID: {exam.exam_id}")
    p.drawString(100, height - 80, f"Title: {exam.title}")

    # Table headers
    headers = ["S.No", "PIN", "Correct Answers"]

    # Fetch and prepare response data
    responses = exam.responses_set.all()
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
    table.drawOn(p, 70, height - 200)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def responses(request, exam_id):
    quest = get_object_or_404(Exam,exam_id=exam_id)
    # print(quiz)
    pdf_buffer = generate_pdf(quest)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}-responses.pdf"'.format(quest.title)
    return response

