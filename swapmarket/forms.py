from django import forms
from .models import Item, Category

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemname', 'nItem', 'price', 'itemdescription', 'itempicture', 'itemtag', 'payment']

    itemtag = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  
        widget=forms.CheckboxSelectMultiple,
    )

    payment = forms.ChoiceField(
    choices=[
        ('coin', 'Coin'),
        ('other', 'Other'),
    ],
    widget=forms.RadioSelect,
    )
