from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Quest(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    quest_id=models.UUIDField(default=uuid.uuid4,unique=True)
    created_date=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.title
    
class Question(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200) 

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    code=models.TextField()
    output=models.ImageField(upload_to="quest/outputs/",default="/quest/outputs/nocode.jpeg")

class Responses(models.Model):
    quest=models.ForeignKey(Quest,on_delete=models.CASCADE)
    pin=models.CharField(max_length=200)
    submitted_date=models.DateTimeField(null=True,blank=True)
    total_points=models.IntegerField(null=True,default=0) 
    


    
# class Answer(models.Model):
# question=models.ForeignKey(Question,on_delete=models.CASCADE)

