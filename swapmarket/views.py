from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import CustomUser 
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
# Create your views here.

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('user:home'))
        else:
            message = "Invalid username or password. Please try again."
    else:
        message = None

    return render(request, "swapmarket/signin.html", {"message": message})

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

            return redirect('registered')

    return render(request, 'swapmarket/signup.html')

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
            return redirect('registered')

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
        return redirect(reverse('user:home'))

    return render(request, 'swapmarket/registered.html')

def changepass(request):
    return render(request,"user/chpass.html")