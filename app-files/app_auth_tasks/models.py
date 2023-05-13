from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=700,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    date_completed=models.DateTimeField(null=True,blank=True)
    important=models.BooleanField(blank=True,default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name + " --by "+self.user.username
class SubTask(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=1200,blank=True)
    created_at=models.DateTimeField(null=False,default=datetime.datetime.now())
    important=models.BooleanField(blank=True,default=False)
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name + " --by "+self.user.username
class Mensaje(models.Model):
    Mensaje=models.CharField(max_length=1000)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.name + " --by "+self.user.username
    
class MensajePrivado(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receptor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receptor')
    mensaje=models.CharField(max_length=1000)
    fecha=models.DateTimeField(null=True,blank=True)