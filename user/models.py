from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    displayname = models.CharField(max_length=64, blank=True, null=True, default='')
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    userdescription = models.CharField(max_length=300, blank=True, null=True, default='')
    userpicture = models.ImageField(upload_to='user_pictures/')
    coins_balance = models.PositiveIntegerField(default=0)
