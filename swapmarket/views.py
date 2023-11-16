from django.shortcuts import render , redirect
from .models import Item, Category
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

def sell_item(request):
    if request.method == 'POST':
        item_data = {
            'itemname': request.POST['itemname'],
            'nItem': int(request.POST['nItem']),
            'price': int(request.POST['price']),
            'itemdescription': request.POST.get('itemdescription', ''),
            'itempicture': request.FILES['itempicture'],
            'categories': request.POST.getlist('categories'),
        }

        user = request.user

        categories = [Category.objects.get_or_create(tag=category)[0] for category in item_data['categories']]

        item = Item.objects.create(
            seller=user,
            itemname=item_data['itemname'],
            nItem=item_data['nItem'],
            price=item_data['price'],
            itemdescription=item_data.get('itemdescription', ''),
            itempicture=item_data['itempicture']
        )
        item.categories.set(categories)
        return redirect('/profile')
    
    return render(request, 'swapmarket/sell_item.html')

def item_detail(request, username, itemname):
    try:
        items = Item.objects.get(seller__username=username, itemname=itemname)
        return render(request, 'swapmarket/item.html' , {
                "item" : items
            })
    except:
        return redirect('home')