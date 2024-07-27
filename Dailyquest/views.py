from django.shortcuts import render,redirect,get_object_or_404
from .models import Quest,Question,Answer,Responses
import uuid
from django.utils import timezone
from Accounts.models import Profile
# Create your views here.

def create_daily_quest_questions(request):
    return render(request,'Dailyquest/createdailyquestquestions.html')

def submit_questions(request):

    if request.method=='POST':
        num_quesetions=int(request.POST.get('numQuestions',0))
        subject=request.POST.get('subject')
        title=request.POST.get('title')
        quest=Quest.objects.create(host=request.user,subject=subject,title=title,quest_id=uuid.uuid4(),created_date=timezone.now())
        for i in range(num_quesetions):
            question_text=request.POST.get(f'question{i}')
            question=Question.objects.create(quest=quest,question_text=question_text)
        
        return redirect('profile-view')

def quest_questions(request,quest_id):
    quest=get_object_or_404(Quest,quest_id=quest_id)
    questions=quest.question_set.all()
    # print(questions)
    profile=get_object_or_404(Profile,pin=request.user)

    return render(request,'Dailyquest/questquestionslists.html',{'questions':questions,'isLecturer':profile.isLecturer,'quest_id':quest.quest_id})


def join_quest(request,quest_id):
    return quest_questions(request,quest_id)

def submit_quest_answers(request,quest_id):
    quest=get_object_or_404(Quest,quest_id=quest_id)
    response=Responses.objects.create(quest=quest,pin=request.user)
    questions=quest.question_set.all()
    counter=1
    for question in questions:
        code=request.POST.get(f"code{counter}")
        answer=Answer()
        answer.output=request.FILES.get(f"image{counter}")
        if answer.output==None or answer.output=="":
            answer.output="/quest/outputs/nocode.jpeg"
        answer.code=code
        answer.question=question
        answer.save()
        # answer=Answer.objects.create(question=question,code=code,output=output)
        counter+=1
        
    
    

    # print("Ganesh")
    

