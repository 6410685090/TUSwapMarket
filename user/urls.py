from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about', views.about, name="about"),
    path('profile', views.profile, name="profile"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
