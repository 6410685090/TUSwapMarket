from django.shortcuts import render , redirect
from swapmarket.models import Item, Category
from swapmarket.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import os
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
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
    try:
        items = Item.objects.get(seller__username=username, itemname=itemname)
        return render(request, 'swapmarket/item.html' , {
                "item" : items
            })
    except:
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

