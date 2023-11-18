from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import CustomUser, Message
from swapmarket.models import  Item
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import CustomUserEditForm, MessageForm
from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
import os

def profile(request):
    return render(request,"user/profile.html",{
        "myitem" : Item.objects.filter(seller=request.user)
    })

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
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
            return render(request, 'user/signup.html',{
                'message' : 'Username already exists.'
            })
        elif CustomUser.objects.filter(email=email).exists():
            return render(request, 'user/signup.html',{
                'message' : 'Email already exists'
            })
        elif password != cpassword:
            return render(request, 'user/signup.html',{
                'message' : 'Passwords do not match'
            })
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
        
        

        username = request.session.get('signup_username')
        email = request.session.get('signup_email')
        password = request.session.get('signup_password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('/registered')

       
        try :
            userpicture = request.FILES['userpicture']   
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
        except:
            return render(request, 'user/registered.html',{
                        'message' : "Please upload you picture"
                    })
        
        del request.session['signup_username']
        del request.session['signup_email']
        del request.session['signup_password']

        login(request, user)
        return redirect(reverse('home'))

    return render(request, 'user/registered.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        old_picture = request.user.userpicture.path if request.user.userpicture else None
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():

            print(old_picture)
            form.save()

            if old_picture and os.path.exists(old_picture):
                os.remove(old_picture)

            return redirect('/profile') 
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'user/editprofile.html', {'form': form})

@login_required
def changepassword(request):
    if request.method == "POST":
        if request.POST["newpass"] == request.POST["cnewpass"]:
            user = CustomUser.objects.get(username = request.user)
            user.set_password(request.POST["newpass"])
            user.save()
            return redirect('/logout')
        else:
            return render(request, 'user/chpass.html',{
                'message' : 'Password not match.'
            })
    return render(request, 'user/chpass.html')

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('user:inbox')
    else:
        form = MessageForm()
    return render(request, 'user/send_message.html', {'form': form})

@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    all_messages = list(chain(received_messages, sent_messages))
    all_messages.sort(key=attrgetter('timestamp'))

    return render(request, 'user/inbox.html', {'all_messages': all_messages})
