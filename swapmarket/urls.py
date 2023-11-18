from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name="about"),
    path('sell_item/', views.sell_item, name='sell_item'),
    path('search/<str:tag>/', views.search_by_tag, name='search_by_tag'),
    path('<str:username>/<str:itemname>/', views.item_detail, name='item_detail'),
    path('<str:username>/<str:itemname>/delete/', views.delete_item, name='delete_item'),
]
    