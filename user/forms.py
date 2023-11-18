from django import forms
from .models import CustomUser, Message

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['userpicture', 'displayname', 'firstname', 'lastname', 'phone', 'userdescription']
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
