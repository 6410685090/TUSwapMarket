from django import forms
from .models import CustomUser

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['userpicture', 'displayname', 'firstname', 'lastname', 'phone', 'userdescription']