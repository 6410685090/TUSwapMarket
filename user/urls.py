from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import sell_item, item_detail

app_name = 'user'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('changepassword/', views.changepassword, name='chpass'),
    path('registered/', views.registered, name='registered'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('sell_item/', sell_item, name='sell_item'),
    path('<str:username>/<str:itemname>/', item_detail, name='item_detail'),
]

