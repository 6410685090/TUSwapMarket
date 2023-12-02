from django import forms
from .models import CustomUser, Message

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['userpicture', 'displayname', 'firstname', 'lastname', 'phone' ,'bank' , 'bankid', 'userdescription' ]
    
    def clean_displayname(self):
        displayname = self.cleaned_data.get('displayname')
        return displayname or ''
    
    def clean_userdescription(self):
        userdescription = self.cleaned_data.get('userdescription')
        return userdescription or ''
