from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', views.userhome, name='userhome'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]