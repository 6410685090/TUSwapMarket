from django.shortcuts import render , redirect
from swapmarket.models import Item, Category, Coins
from swapmarket.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from .forms import DepositForm , WithdrawForm
from user.models import CustomUser
import os

# Create your views here.

def home(request):
    return render(request, 'swapmarket/homepage.html',{
        'item' : Item.objects.all(), 'categories': Category.objects.all()
    })

def about(request):
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
    return render(request, 'swapmarket/sbt.html', {'item': items, 'categories': categories})

@login_required
def item_detail(request, username, itemname):
    try:
        item = Item.objects.get(seller__username=username, itemname=itemname)
    except Item.DoesNotExist:
        messages.error(request, 'Item not found.')
        return redirect('home')

    if request.method == 'POST':
        nitem_buyers = request.POST.get('nitem_buyers', 0)

        if request.user == item.seller:
            messages.error(request, 'You cannot buy your own item.')
            return redirect('item_detail', username=username, itemname=itemname)
        
        if not nitem_buyers.isdigit() or int(nitem_buyers) <= 0:
            messages.error(request, 'Invalid nitem.')
            return redirect('item_detail', username=username, itemname=itemname)

        nitem_buyers = int(nitem_buyers)

        if nitem_buyers > item.nItem:
            messages.error(request, 'Item exceeds available stock.')
            return redirect('item_detail', username=username, itemname=itemname)

        total_cost = nitem_buyers * item.price
        if request.user.coins_balance < total_cost:
            messages.error(request, 'Insufficient funds.')
            return redirect('item_detail', username=username, itemname=itemname)

        coins_transfer = Coins(sender=request.user, receiver=item.seller, amount=total_cost, is_confirmed=False)
        coins_transfer.sender.coins_balance -= coins_transfer.amount
        coins_transfer.sender.save()
        admin_user = CustomUser.objects.get(username='admin')
        admin_user.coins_balance += coins_transfer.amount
        admin_user.save()
        coins_transfer.save()

        item.nItem -= nitem_buyers
        item.save()

        messages.success(request, f'Successfully purchased {nitem_buyers} {item.itemname}(s).')
        return redirect('home')

    return render(request, 'swapmarket/item.html', {'item': item})
    
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
def deposit_admin(request):
    if request.user.is_staff:
        pending_deposits = Coins.objects.filter(sender=CustomUser.objects.get(username='admin'),is_confirmed=False)
        return render(request, 'swapmarket/deposit_admin.html', {'pending_deposits': pending_deposits})
    else:
        return redirect('home')

@login_required
def approve_deposit(request, deposit_id):
    if request.user.is_staff:
        deposit = Coins.objects.get(id=deposit_id)
        if deposit.is_confirmed:
            messages.error(request, 'This deposit has already been confirmed.')
        elif deposit.sender.coins_balance >= deposit.amount:
            deposit.is_confirmed = True
            deposit.sender.coins_balance -= deposit.amount
            deposit.sender.save()
            deposit.receiver.coins_balance += deposit.amount
            deposit.receiver.save()
            deposit.save()
            messages.success(request, f'Deposit of {deposit.amount} coins has been approved.')

        return redirect('deposit_admin')
    
@login_required
def withdraw_coins(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            withdraw = Coins(sender=request.user, receiver=CustomUser.objects.get(username='admin'), amount=amount, is_confirmed=False)
            withdraw.save()

            messages.success(request, f'Withdraw of {amount} coins successful.')
            return redirect('home') 
    else:
        form = WithdrawForm()

    return render(request, 'swapmarket/withdraw.html', {'form': form})

@login_required
def withdraw_admin(request):
    if request.user.is_staff:
        pending_withdraws = Coins.objects.filter(receiver=CustomUser.objects.get(username='admin'),is_confirmed=False)
        return render(request, 'swapmarket/withdraw_admin.html', {'pending_withdraws': pending_withdraws})
    else:
        return redirect('home')

@login_required
def approve_withdraw(request, withdraw_id):
    if request.user.is_staff:
        withdraw = Coins.objects.get(id=withdraw_id)
        if withdraw.is_confirmed:
            messages.error(request, 'This withdraw has already been confirmed.')
        elif withdraw.sender.coins_balance >= withdraw.amount:
            withdraw.is_confirmed = True
            withdraw.sender.coins_balance -= withdraw.amount
            withdraw.sender.save()
            withdraw.receiver.coins_balance += withdraw.amount
            withdraw.receiver.save()
            withdraw.save()
            messages.success(request, f'withdraw of {withdraw.amount} coins has been approved.')

        return redirect('withdraw_admin')
    
@login_required
def cart_user(request):
    pending_carts = Coins.objects.filter(sender=request.user, is_confirmed=False).exclude(receiver=CustomUser.objects.get(username='admin'))
    return render(request, 'swapmarket/cart_user.html', {'pending_carts': pending_carts})

@login_required
def approve_cart(request, cart_id):
    cart = Coins.objects.get(id=cart_id)
    if cart.is_confirmed:
        messages.error(request, 'This cart has already been confirmed.')
    elif cart.sender.coins_balance >= cart.amount:
        cart.is_confirmed = True
        admin_user = CustomUser.objects.get(username='admin')
        admin_user.coins_balance -= cart.amount
        admin_user.save()
        cart.receiver.coins_balance += cart.amount
        cart.receiver.save()
        cart.save()
        messages.success(request, f'cart of {cart.amount} coins has been approved.')

    return redirect('cart_user')

@login_required
def cancel_cart(request, cart_id):
    cart = Coins.objects.get(id=cart_id)
    if cart.is_confirmed:
        messages.error(request, 'This cart has already been confirmed.')
    else:
        admin_user = CustomUser.objects.get(username='admin')
        admin_user.coins_balance -= cart.amount
        admin_user.save()
        cart.sender.coins_balance += cart.amount
        
        cart.sender.save()
        cart.delete()
        messages.success(request, f'cart of {cart.amount} coins has been cancelled.')
        
    return redirect('cart_user')
