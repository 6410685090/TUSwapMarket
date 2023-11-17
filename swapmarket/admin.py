from django.contrib import admin
from .models import Coins, Category, Item

# Register your models here.

from django.contrib import admin
from .models import Coins, Category, Item

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('tag',)

class CoinsAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'amount', 'is_confirmed']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['itemname', 'seller', 'nItem', 'price']
    list_filter = ('itemtag',)
    search_fields = ('itemname', 'seller__username')
    filter_horizontal = ('itemtag',)



admin.site.register(Coins, CoinsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)