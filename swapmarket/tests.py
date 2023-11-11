from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from .models import Category, Item, Coins
from .views import home, about
from user.models import CustomUser

# Create your tests here.

