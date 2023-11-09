from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import CustomUser 
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import CustomUserEditForm

def profile(request):
    return render(request,"user/profile.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            message = "Invalid username or password. Please try again."
    else:
        message = None

    return render(request, "user/signin.html", {"message": message})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        elif password != cpassword:
            messages.error(request, 'Passwords do not match')
        else:
            request.session['signup_username'] = username
            request.session['signup_email'] = email
            request.session['signup_password'] = password

            return redirect('/registered')

    return render(request, 'user/signup.html')

def registered(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        userdescription = request.POST['userdescription']
        userpicture = request.FILES['userpicture']  

        username = request.session.get('signup_username')
        email = request.session.get('signup_email')
        password = request.session.get('signup_password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('/registered')

            
        fs = FileSystemStorage()
        filename = fs.save('user_pictures/' + userpicture.name, userpicture)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            firstname=firstname,
            lastname=lastname,
            userdescription=userdescription,
            userpicture=filename  
        )

        del request.session['signup_username']
        del request.session['signup_email']
        del request.session['signup_password']

        login(request, user)
        return redirect(reverse('home'))

    return render(request, 'user/registered.html')

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile') 
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'user/editprofile.html', {'form': form})

def changepass(request):
    
    return render(request,"user/chpass.html")