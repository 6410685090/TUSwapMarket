from django.shortcuts import render , redirect
from swapmarket.models import Item, Category, Coins
from swapmarket.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from .forms import DepositForm
from user.models import CustomUser
import os

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('deposit/approval/')
        else:
            return render(request, 'user/homepage.html',{
            'item' : Item.objects.all(), 'categories': Category.objects.all()
        })  
    return render(request, 'swapmarket/homepage.html',{
        'item' : Item.objects.all(), 'categories': Category.objects.all()
    })

def about(request):
    if request.user.is_authenticated:
        return render(request,"user/about.html")    
    return render(request,"swapmarket/about.html")

@login_required
def sell_item(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            form.save_m2m()
            
            return redirect('/profile')
    else:
        form = ItemForm()

    return render(request, 'swapmarket/sell_item.html', {'form': form, 'categories': categories})



def sbt(request):
    selected_tags = request.GET.getlist('tags')
    items = Item.objects.filter(itemtag__tag__in=selected_tags).annotate(tag_count=Count('itemtag')).filter(tag_count=len(selected_tags))
    categories = Category.objects.all()
    if request.user.is_authenticated:
        return render(request, 'user/sbt.html', {'item': items, 'categories': categories}) 
    return render(request, 'swapmarket/sbt.html', {'item': items, 'categories': categories})

@login_required
def item_detail(request, username, itemname):
    if Item.objects.filter(seller__username=username, itemname=itemname):
        items = Item.objects.get(seller__username=username, itemname=itemname)
        return render(request, 'swapmarket/item.html' , {
                "item" : items
            })
    else:
        return redirect('home')
    
@login_required
def delete_item(request, username, itemname):
    item = Item.objects.get(seller__username=username, itemname=itemname)

    if request.user == item.seller:
        os.remove(item.itempicture.path)
        item.delete()
        return redirect('/profile')
    else:
        return redirect('home')

@login_required
def deposit_coins(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            deposit = Coins(sender=CustomUser.objects.get(username='admin'), receiver=request.user, amount=amount, is_confirmed=False)
            deposit.save()

            messages.success(request, f'Deposit of {amount} coins successful.')
            return redirect('home') 
    else:
        form = DepositForm()

    return render(request, 'swapmarket/deposit.html', {'form': form})

@login_required
def deposit_approval(request):
    if request.user.is_staff:
        pending_deposits = Coins.objects.filter(is_confirmed=False)
        return render(request, 'swapmarket/deposit_approval.html', {'pending_deposits': pending_deposits})

@login_required
def approve_deposit(request, deposit_id):
    if request.user.is_staff:
        deposit = Coins.objects.get(id=deposit_id)
        if deposit.is_confirmed:
            messages.error(request, 'This deposit has already been confirmed.')
        else:
            deposit.is_confirmed = True
            deposit.receiver.coins_balance += deposit.amount
            deposit.receiver.save()
            deposit.save()
            messages.success(request, f'Deposit of {deposit.amount} coins has been approved.')

        return redirect('deposit_approval')