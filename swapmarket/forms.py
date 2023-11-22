from django import forms
from .models import Item, Category, Coins

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

class DepositForm(forms.ModelForm):
    class Meta:
        model = Coins
        fields = ['amount']

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Coins
        fields = ['amount']