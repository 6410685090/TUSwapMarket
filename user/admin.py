from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , Room , Message

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'firstname', 'lastname', 'phone', 'userpicture', 'coins_balance','is_staff']

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['room' , 'user' ,'value']

admin.site.register(CustomUser, CustomUserAdmin)



    
admin.site.register(Room)
admin.site.register(Message, MessageAdmin)