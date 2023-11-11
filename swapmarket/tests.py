from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from .models import Category, Item, Coins
from .views import home, about
from user.models import CustomUser

# Create your tests here.

class Testing(TestCase):
    
    # Set up for testing.
    def setUp(self) :
        
        # Create client.
        self.client = Client()
        
        # Create user TEST1.
        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.set_password('Student331')
        self.user1.save()
        
        # Create user TEST2.
        self.user2 = CustomUser.objects.create(username='TEST2', email = "2")
        self.user1.set_password('Student331')
        self.user1.save()
        
        # Create staff user STAFF.
        self.staffUser = CustomUser.objects.create_user(username='STAFF',email = "3", is_staff=True)
        self.staffUser.set_password('Student331')
        self.staffUser.save()
    
    # Check str() function for class Category. True if str() = Category.tag.  
    def test_call_category(self) :
        category = Category.objects.create(tag = 'A')
        self.assertEqual(str(category), category.tag)
    
    # Check str() function for class Item. True if str() = Item.itemname.
    def test_call_item(self) :
        item = Item.objects.create(itemname = '1',
                                   seller = self.user1,
                                   nItem = 0,
                                   price = 0,)
        self.assertEqual(str(item), item.itemname)
    
    # Check str() function for class Coins. True if str() = "{Coins.sender} -> {Coins.receiver}: {Coins.amount} coins".
    def test_call_coins(self) :
        coins = Coins.objects.create(sender = self.user1,
                                     receiver = self.user2,
                                     amount = '0',
                                     is_confirmed = False)
        self.assertEqual(str(coins), f"{coins.sender} -> {coins.receiver}: {coins.amount} coins")
    
    # Check that non-authenticated user will go to swapmarket/homepage.html.
    def test_url_profile_notAuthenticate(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/homepage.html')
        self.assertEqual(resolve(home_url).func, home)
    
    # Check that non-authenticated user will go to swapmarket/about.html.
    def test_url_about_notAuthenticate(self):
        about_url = reverse('about')
        response = self.client.get(about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/about.html')
        self.assertEqual(resolve(about_url).func, about)
    
    # Check that authenticated user will go to user/homepage.html.
    def test_url_profile_Authenticate(self):
        home_url = reverse('home')
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/homepage.html')
        self.assertEqual(resolve(home_url).func, home)
    
    # Check that authenticated user will go to user/about.html.
    def test_url_about_Authenticate(self):
        about_url = reverse('about')
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/about.html')
        self.assertEqual(resolve(about_url).func, about)
    
    # Check that staff user will go to admin site.
    def test_url_profile_Staff(self):
        home_url = reverse('home')
        self.client.login(username='STAFF', password='Student331')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(home_url).func, home)