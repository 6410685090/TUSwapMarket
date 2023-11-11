from django.shortcuts import render , redirect
from .models import Item
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return render(request, 'user/homepage.html',{
            'item' : Item.objects.all()
        })  
    return render(request, 'swapmarket/homepage.html',{
        'item' : Item.objects.all()
    })

def about(request):
    if request.user.is_authenticated:
        return render(request,"user/about.html")    
    return render(request,"swapmarket/about.html")
