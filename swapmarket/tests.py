import os
from io import BytesIO
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Category, Item, Coins
from .views import home, about, sell_item, sbt, item_detail, delete_item
from user.models import CustomUser
from .forms import ItemForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

# Create your tests here.

class HomeTest(TestCase):
    
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

    def test_url_profile_Staff(self):
        home_url = reverse('home')
        self.client.login(username='STAFF', password='Student331')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(home_url).func, home)

    def test_url_profile_Authenticate(self):
        home_url = reverse('home')
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/homepage.html')
        self.assertEqual(resolve(home_url).func, home)


    def test_url_profile_notAuthenticate(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/homepage.html')
        self.assertEqual(resolve(home_url).func, home)
class AboutTest(TestCase):
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

    def test_url_about_Authenticate(self):
        about_url = reverse('about')
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/about.html')
        self.assertEqual(resolve(about_url).func, about)

    def test_url_about_notAuthenticate(self):
        about_url = reverse('about')
        response = self.client.get(about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/about.html')
        self.assertEqual(resolve(about_url).func, about)

class ModelTest(TestCase):
    def setUp(self) :

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user2 = CustomUser.objects.create(username='TEST2', email = "2")
    def test_call_category(self) :
        category = Category.objects.create(tag = 'A')
        self.assertEqual(str(category), category.tag)
    
    def test_call_item(self) :
        item = Item.objects.create(itemname = '1',
                                   seller = self.user1,
                                   nItem = 0,
                                   price = 0,)
        self.assertEqual(str(item), item.itemname)
    
    def test_call_coins(self) :
        coins = Coins.objects.create(sender = self.user1,
                                     receiver = self.user2,
                                     amount = '0',
                                     is_confirmed = False)
        self.assertEqual(str(coins), f"{coins.sender} -> {coins.receiver}: {coins.amount} coins")

class SellItemTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image_io.seek(0)

        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.userpicture = image_file
        self.user.save()
        self.sell_item = reverse('sell_item')
        self.category1 = Category.objects.create(tag='Category 1')
        self.category2 = Category.objects.create(tag='Category 2')
    def test_templates(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.sell_item)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/sell_item.html')
    def test_sell_item_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        data = {
            'itemname': 'Test Item',
            'nItem': 1,
            'price': 10,
            'itemdescription': 'This is a test item.',
            'itempicture': image_file,
            'itemtag': [self.category1.id, self.category2.id],
            'payment': 'coin',
        }
        response = self.client.post(self.sell_item, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile')

        self.assertTrue(Item.objects.filter(itemname='Test Item'))
    def test_url_sell_item(self):
        self.assertEqual(resolve(self.sell_item).func, sell_item)
    def test_item_form_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        data = {
            'itemname': 'Test Item',
            'nItem': 1,
            'price': 10,
            'itemdescription': 'This is a test item.',
            'itempicture': image_file,
            'itemtag': [self.category1.id, self.category2.id],
            'payment': 'coin'
        }
        response = self.client.post(self.sell_item, data)
        self.assertTrue(Item.objects.filter(itemname='Test Item').exists())

    def test_is_not_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.sell_item)
        self.assertEqual(response.status_code, 200)
    def test_item_form_invalid_data(self):
        self.client.login(username='testuser', password='testpassword')

        # Create a POST request with invalid data
        form_data = {
        }
        form = ItemForm(data=form_data)  # 200 is the statusd code for a successful GET request (rendering the form page)
        self.assertFalse(form.is_valid())
        self.assertIn('nItem', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('itempicture', form.errors)
        self.assertIn('itemtag', form.errors)
        self.assertIn('payment', form.errors)
class SbtTest(TestCase):

    def setUp(self):
        img1 = Image.new(mode="RGB", size=(200, 200))
        img1.save("media/user_pictures/test_image.jpg")
        self.client = Client()

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.userpicture = 'user_pictures/test_user.jpg'
        self.user1.set_password('Student331')
        self.user1.save()

        self.sbt_url = reverse('sbt')
        
    def test_url_sbt_notAuthenticate(self):
        response = self.client.get(self.sbt_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/sbt.html')
        self.assertEqual(resolve(self.sbt_url).func, sbt)
    
    # Check that authenticated user will go to user/sbtl.html.
    def test_url_sbt_Authenticate(self):
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(self.sbt_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/sbt.html')
        self.assertEqual(resolve(self.sbt_url).func, sbt)
    
class ItemDetailTest(TestCase):
        
    def setUp(self):
        img1 = Image.new(mode="RGB", size=(200, 200))
        img1.save("media/user_pictures/test_image.jpg")
        img2 = Image.new(mode="RGB", size=(200, 200))
        img2.save("media/user_pictures/test_user.jpg")
        self.client = Client()

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.userpicture = 'user_pictures/test_user.jpg'
        self.user1.set_password('Student331')
        self.user1.save()
        self.user2 = CustomUser.objects.create(username='TEST2', email = "2")
        self.user2.set_password('Student331')
        self.user2.save()
        self.category = Category.objects.create(tag = '1')
        
        # Create example item 1
        self.item = Item.objects.create(itemname = 'A',
                                   seller = self.user1,
                                   nItem = 0,
                                   price = 0,
                                   itempicture = 'user_pictures/test_image.jpg')
        self.item.itemtag.add(self.category)

    def test_item_required_pass(self):
        item_detail_url = reverse('item_detail', args=['TEST1', 'A'])
        self.client.login(username='TEST1', password='Student331')
        self.assertEqual(item_detail_url, '/TEST1/A/')
        response = self.client.get(item_detail_url)
        self.assertTemplateUsed(response, 'swapmarket/item.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], self.item)
        self.assertEqual(resolve(item_detail_url).func, item_detail)
   
    # Test when look at item detail with error.
    def test_item_required_except(self):
        item_detail_url = reverse('item_detail', args=['TEST1', 'B'])
        self.client.login(username='TEST1', password='Student331')
        self.assertEqual(item_detail_url, '/TEST1/B/')
        response = self.client.get(item_detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertEqual(resolve(item_detail_url).func, item_detail)

class DeleteItemTest(TestCase):
    def setUp(self):
        
        img1 = Image.new(mode="RGB", size=(200, 200))
        img1.save("media/user_pictures/test_image.jpg")
        
        img2 = Image.new(mode="RGB", size=(200, 200))
        img2.save("media/user_pictures/test_user.jpg")
        self.client = Client()

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.userpicture = 'user_pictures/test_user.jpg'
        self.user1.set_password('Student331')
        self.user1.save()
        
        # Create user TEST2.
        self.user2 = CustomUser.objects.create(username='TEST2', email = "2")
        self.user2.set_password('Student331')
        self.user2.save()
        
        # Create example tag A
        self.category = Category.objects.create(tag = '1')
        
        # Create example item 1
        self.item = Item.objects.create(itemname = 'A',
                                   seller = self.user1,
                                   nItem = 0,
                                   price = 0,
                                   itempicture = 'user_pictures/test_image.jpg')
        self.item.itemtag.add(self.category)

    # Test when delete your own item.
    def test_delete_item_ownItems(self):
        delete_item_url = reverse('delete_item', kwargs={'username': self.user1.username, 'itemname': self.item})
        self.client.login(username='TEST1', password='Student331')
        self.assertEqual(delete_item_url, '/TEST1/A/delete/')
        response = self.client.get(delete_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile')
        self.assertEqual(resolve(delete_item_url).func, delete_item)
    
    # Test when trying to delete someone else's item.
    def test_delete_item_notYourOwnItems(self):
        delete_item_url = reverse('delete_item', kwargs={'username': self.user1.username, 'itemname': self.item})
        self.client.login(username='TEST2', password='Student331')
        self.assertEqual(delete_item_url, '/TEST1/A/delete/')
        response = self.client.get(delete_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertEqual(resolve(delete_item_url).func, delete_item)
