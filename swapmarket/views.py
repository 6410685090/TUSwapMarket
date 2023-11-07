from django.shortcuts import render , redirect

# Create your views here.


def about(request):
    return render(request,"swapmarket/about.html")

def home(request):
    return render(request,"swapmarket/homepage.html")

def signin(request):
    return render(request,"user/signin.html")

def signup(request):
    return render(request,"user/signup.html")

def changepass(request):
    return render(request,"user/chpass.html")