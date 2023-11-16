from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name="about"),
    path('sell_item/', views.sell_item, name='sell_item'),
    path('<str:username>/<str:itemname>/', views.item_detail, name='item_detail'),
]
    