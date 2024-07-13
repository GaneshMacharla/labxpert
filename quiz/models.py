from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    quiz_id=models.UUIDField(default=uuid.uuid4,unique=True)
    created_date=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=200) 

class Responses(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    pin=models.CharField(max_length=200)
    correct_answers=models.IntegerField
    

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    answer=models.CharField(max_length=200)
    def __str__(self):
        return self.answer

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice=models.CharField(max_length=200)



    


