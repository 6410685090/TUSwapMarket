from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return render(request, 'user/homepage.html')        
    return render(request, 'swapmarket/homepage.html')

def about(request):
    if request.user.is_authenticated:
        return render(request,"user/about.html")    
    return render(request,"swapmarket/about.html")

def profile(request):
    return render(request,"user/profile.html")

