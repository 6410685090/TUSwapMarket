from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    displayname = models.CharField(max_length=64, blank=True, null=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    userdescription = models.CharField(max_length=300, blank=True, null=True, default='')
    userpicture = models.ImageField(upload_to='user_pictures/')
    coins_balance = models.PositiveIntegerField(default=0)

class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chats')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)