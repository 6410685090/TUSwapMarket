from django.db import models
from django.core.validators import MaxValueValidator
from user.models import CustomUser

# Create your models here.

class Category(models.Model):
    tag = models.CharField(max_length=64)
    def __str__(self):
        return self.tag

class Item(models.Model):
    itemname = models.CharField(max_length=64)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='items_for_sale', default=None, null=False)
    buyers = models.ManyToManyField(CustomUser, related_name='items_bought', blank=True)
    nItem = models.PositiveIntegerField(validators=[MaxValueValidator(99)])
    price =  models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    categories = models.ManyToManyField(Category, blank=True)
    itemdescription = models.CharField(max_length=500, blank=True, null=True, default='')
    itempicture = models.ImageField()

    def __str__(self):
        return self.itemname

class Coins(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_coins', default=None, null=False)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_coins', default=None, null=False)
    amount = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount} coins"
