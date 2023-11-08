from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def userhome(request):
    if request.user.is_staff:
        return redirect('/admin/')
    else:
        return render(request, 'user/homepage.html')
