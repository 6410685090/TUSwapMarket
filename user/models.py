from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    displayname = models.CharField(max_length=64, blank=True, null=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    userdescription = models.CharField(max_length=300, blank=True, null=True)
    userpicture = models.ImageField(upload_to='user_pictures/')
    coins_balance = models.PositiveIntegerField(default=0)

class Room(models.Model):
    name = models.CharField(max_length=1000,null=True)

class Message(models.Model):
    value = models.CharField(max_length=1000000,null=True)
    date= models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000,null=True)
    room = models.CharField(max_length=1000000,null=True)

