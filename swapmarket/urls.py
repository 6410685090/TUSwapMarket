from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name="about"),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('changepassword', views.changepass, name='chpass'),
    path('registered/', views.registered, name='registered'),
]