from django.db import models

# Create your models here.


class FeedBack(models.Model):
    email=models.EmailField(max_length=254)
    text=models.TextField()



    
    