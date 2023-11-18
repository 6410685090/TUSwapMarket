from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'user'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('changepassword/', views.changepassword, name='chpass'),
    path('registered/', views.registered, name='registered'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('send/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
]

