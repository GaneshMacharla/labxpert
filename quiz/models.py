from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    quiz_id=models.IntegerField(null=True,default=0)
    created_date=models.DateTimeField(null=True,blank=True)
    time_limit=models.TimeField(null=True,blank=True)
    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=200) 

class Responses(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    pin=models.CharField(max_length=200)
    submitted_date=models.DateTimeField(null=True,blank=True)
    correct_answers=models.IntegerField(null=True,default=0) 
       


class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    answer=models.CharField(max_length=200)
    def __str__(self):
        return self.answer

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice=models.CharField(max_length=200)



    


