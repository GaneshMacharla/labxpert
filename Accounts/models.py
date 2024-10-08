from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    pin=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=100)
    # address=models.CharField(max_length=100)
    fullname=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/',default='images/avatar7.png')
    isLecturer=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.pin} profile" 

            