from django.shortcuts import render,get_object_or_404,redirect
from .models import Quiz,Question,Choice,Answer
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Quiz, Question, Choice, Answer
import uuid


def create_quiz(request):
    return render(request,'quiz/questions.html')


def submit_quiz(request):
    if request.method == 'POST':
        num_questions = int(request.POST.get('numQuestions', 0))
        print(request.POST.get('numQuestions'))
        title = request.POST.get('title')
        quiz = Quiz.objects.create(host=request.user, title=title, unique_id=uuid.uuid4())
        quiz_id = quiz.unique_id
        
        for i in range(num_questions):
            question_text = request.POST.get(f'question{i}')
            print(question_text)
            answer_text = request.POST.get(f'answer{i}')
            question = Question.objects.create(quiz=quiz, question=question_text)
            answer = Answer.objects.create(question=question, answer=answer_text)
            
            for j in range(4):
                choice_text = request.POST.get(f'question{i}choice{j}')
                choice = Choice.objects.create(question=question, choice=choice_text)

        messages.success(request, "Quiz created successfully")
        current_quiz = get_object_or_404(Quiz, unique_id=quiz_id)
        questions = current_quiz.question_set.all()
        print(questions)
        questions_choices = {}
        
        for question in questions:
            choices = question.choice_set.all()
            questions_choices[question] = choices
        
        return render(request, 'quiz/questionslist.html', {'quiz_id': quiz_id, 'questions_choices': questions_choices,'title':title,'total_questions':num_questions})
    
    return render(request, 'quiz/create_quiz.html')



def submit_answers(request):
    
    if request.method=="POST":
        num_questions=int(request.GET.get("total_questions"))
        quiz_id=request.GET.get("quiz_id")

        #fetch the quiz object
        quiz=get_object_or_404(Quiz,unique_id=quiz_id)
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

        return render(request,'quiz/quizresults.html',{'total_correct_answers':total_correct_answers,'total_wrong_answers':total_wrong_answers,'num_questions':num_questions,'correct_answers':correct_answers,'wrong_answers':wrong_answers,'corrected_answers':corrected_answers})
    return redirect('submit-quiz')
        
        

        

        
