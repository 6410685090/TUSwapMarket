from django.shortcuts import render , redirect

# Create your views here.


def about(request):
    return render(request,"swapmarket/about.html")

def home(request):
    return render(request,"swapmarket/homepage.html")