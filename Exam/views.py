from django.shortcuts import render,redirect,get_object_or_404
import uuid
from .models import Exam,Question,Answer
from django.utils import timezone
from Accounts.models import Profile
from .models import Responses
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


def submit_exam_answers(request,quest_id):
    quest=get_object_or_404(Exam,quest_id=quest_id)
    response=Responses.objects.create(quest=quest,pin=request.user)
    response.submitted_date=timezone.now()
    questions=quest.question_set.all()
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





def check_code(api_key,code,question,max_points):
    # Set the API key as an environment variable
    os.environ['API_KEY'] = api_key
    
    # Configure the API key
    genai.configure(api_key=os.environ['API_KEY'])
    
    # Choose a model that's appropriate for your use case
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Define the prompt
    prompt =f"""
    question:{question},
    code:{code},
    max_points:{max_points},
    I have given question,code and max_points You should evaluate the code based on the question and you have to allot points for that code.
    Main points:you have to see is the user written correct code and following the syntaxes.
    conditions:You should give to me only points and you must not exceed the max_points range while alloting the points to the code. 
"""
    
    # Generate content based on the prompt
    response = model.generate_content(prompt)
    print(response.text)
    # Return the generated content
    return response.text


