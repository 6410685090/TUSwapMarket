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

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',  
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        error_messages={
            'add': 'This user has the permission already.',
        },
    )