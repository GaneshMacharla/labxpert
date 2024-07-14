from django.shortcuts import render,get_object_or_404,redirect
from .models import Quiz,Question,Choice,Answer
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Quiz, Question, Choice, Answer,Responses
from Accounts.models import Profile
import uuid
import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_quiz(request):
    return render(request,'quiz/questions.html')

def quiz_questions(request,quiz_id):
    current_quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    profile=get_object_or_404(Profile,pin=request.user)
    questions = current_quiz.question_set.all()
    # print(questions)
    questions_choices = {}
        
    for question in questions:
        choices = question.choice_set.all()
        questions_choices[question] = choices
        
    return render(request, 'quiz/questionslist.html', {'quiz_id': quiz_id, 'questions_choices': questions_choices,'title':current_quiz.title,'total_questions':len(questions),'profile':profile})


def submit_quiz(request):
    if request.method == 'POST':
        num_questions = int(request.POST.get('numQuestions', 0))
        # print(request.POST.get('numQuestions'))
        title = request.POST.get('title')
        profile=get_object_or_404(Profile,pin=request.user)
        quiz = Quiz.objects.create(host=request.user, title=title, quiz_id=uuid.uuid4())
        quiz_id = quiz.quiz_id
        
        for i in range(num_questions):
            question_text = request.POST.get(f'question{i}')
            # print(question_text)
            answer_text = request.POST.get(f'answer{i}')
            question = Question.objects.create(quiz=quiz, question=question_text)
            answer = Answer.objects.create(question=question, answer=answer_text)
            
            for j in range(4):
                choice_text = request.POST.get(f'question{i}choice{j}')
                choice = Choice.objects.create(question=question, choice=choice_text)

        messages.success(request, "Quiz created successfully")
        return redirect('profile-view')
    return render(request, 'quiz/create_quiz.html')


#student can submit answers

def submit_answers(request):
    
    if request.method=="POST":
        num_questions=int(request.GET.get("total_questions"))
        quiz_id=request.GET.get("quiz_id")

        #fetch the quiz object
        quiz=get_object_or_404(Quiz,quiz_id=quiz_id)
        questions=quiz.question_set.all()

        #processing the answers or checking the answers
        # results={}
        # answers={}
        correct_answers={}
        wrong_answers={}
        corrected_answers={}
        i=1
        for question in questions:
            choice_id=request.POST.get(f"question{i}")
            if choice_id:
                # answers[question]=question.answer
                choice=get_object_or_404(Choice,id=choice_id)
                answer=get_object_or_404(Answer,question=question)
                # results[question]=choice
                if choice.choice==answer.answer:
                    correct_answers[question]=choice.choice
                else:
                    wrong_answers[question]=choice.choice
                    corrected_answers[question]=answer.answer
            i=i+1
        total_correct_answers=len(correct_answers)
        total_wrong_answers=num_questions-total_correct_answers
        student=Responses.objects.create(quiz=quiz,pin=request.user,correct_answers=total_correct_answers)
        return render(request,'quiz/quizresults.html',{'total_correct_answers':total_correct_answers,'total_wrong_answers':total_wrong_answers,'num_questions':num_questions,'correct_answers':correct_answers,'wrong_answers':wrong_answers,'corrected_answers':corrected_answers})
    return redirect('submit-quiz')
        

# def responses(request,quiz_id):
#     quiz=get_object_or_404(Quiz,quiz_id=quiz_id)
#     usernames=quiz.responses_set.all()
#     print(usernames)
#     # print("Ganesh")

def generate_pdf(quiz):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Quiz ID: {quiz.quiz_id}")
    p.drawString(100, height - 70, f"Title: {quiz.title}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 120, "S.No")
    p.drawString(300, height - 120, "PIN")
    p.drawString(450, height - 120, "Correct Answers")

    responses = quiz.responses_set.all()
    if responses.exists():
        p.setFont("Helvetica", 12)
        y_position = height - 140
        for i, response in enumerate(responses, start=1):
            p.drawString(100, y_position, str(i))
            # p.drawString(150, y_position, response.)
            p.drawString(300, y_position, response.pin)
            p.drawString(450, y_position, str(response.correct_answers))


            # Draw lines for the columns
            p.line(90, y_position + 10, 550, y_position + 10)
            y_position -= 20
    else:
        p.setFont("Helvetica", 12)
        p.drawString(200, height -200, "No responses have been submitted yet.")

    # Draw the horizontal line after the headers
    p.line(90, height - 130, 550, height - 130)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

        
def responses(request, quiz_id):
    quiz = get_object_or_404(Quiz,quiz_id=quiz_id)
    pdf_buffer = generate_pdf(quiz)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}-responses.pdf"'.format(quiz.title)
    return response

def join_quiz(request,quiz_id):
    return quiz_questions(request,quiz_id)


def download_pdf(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    pdf_buffer = generate_pdf(quiz)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}-responses.pdf"'.format(quiz.title)
    return response
