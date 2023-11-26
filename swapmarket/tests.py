from io import BytesIO
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Category, Item, Coins
from .views import home, about, sell_item, sbt, item_detail, delete_item, deposit_coins
from user.models import CustomUser
from .forms import ItemForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from PIL import Image

# Create your tests here.

class HomeTest(TestCase):
    
    # Set up for testing.
    def setUp(self) :
        
        # Create client.
        self.client = Client()
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")

        # Create user TEST1.
        self.user1 = CustomUser.objects.create_user(username='TEST1', email = "1")
        self.user1.set_password('Student331')
        self.user1.userpicture = image_file
        self.user1.save()
        
        # Create user TEST2.
        self.user2 = CustomUser.objects.create_user(username='TEST2', email = "2")
        self.user2.set_password('Student331')
        self.user2.userpicture = image_file
        self.user1.save()
        
        # Create staff user STAFF.
        self.staffUser = CustomUser.objects.create_user(username='STAFF',email = "3", is_staff=True)
        self.staffUser.set_password('Student331')
        self.staffUser.save()

    def test_url_profile_Staff(self):
        home_url = reverse('home')
        self.client.login(username='STAFF', password='Student331')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(home_url).func, home)

    def test_url_profile_Authenticate(self):
        home_url = reverse('home')
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/homepage.html')
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
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        
        # Create user TEST1.
        self.user1 = CustomUser.objects.create_user(username='TEST1', email = "1")
        self.user1.set_password('Student331')
        self.user1.userpicture = image_file
        self.user1.save()
        
        # Create user TEST2.
        self.user2 = CustomUser.objects.create_user(username='TEST2', email = "2")
        self.user2.set_password('Student331')
        self.user2.userpicture = image_file
        self.user2.save()
        
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
        self.client = Client()
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")

        self.user1 = CustomUser.objects.create_user(username='TEST1', email = "1")
        self.user1.set_password('Student331')
        self.user1.userpicture = image_file
        self.user1.save()

        self.user2 = CustomUser.objects.create_user(username='TEST2', email = "2")
        self.user2.set_password('Student331')
        self.user2.userpicture = image_file
        self.user2.save()

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
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.client = Client()

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.userpicture = image_file
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
        self.assertTemplateUsed(response, 'swapmarket/sbt.html')
        self.assertEqual(resolve(self.sbt_url).func, sbt)
    
class ItemDetailTest(TestCase):
        
    def setUp(self):
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.client = Client()

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.userpicture = image_file
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
                                   itempicture = image_file)
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
        
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.client = Client()

        self.user1 = CustomUser.objects.create(username='TEST1', email = "1")
        self.user1.userpicture = image_file
        self.user1.set_password('Student331')
        self.user1.save()
        
        # Create user TEST2.
        self.user2 = CustomUser.objects.create(username='TEST2', email = "2")
        self.user2.userpicture = image_file
        self.user2.set_password('Student331')
        self.user2.save()
        
        # Create example tag A
        self.category = Category.objects.create(tag = '1')
        
        # Create example item 1
        self.item = Item.objects.create(itemname = 'A',
                                   seller = self.user1,
                                   nItem = 0,
                                   price = 0,
                                   itempicture = image_file)
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
class DepositTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user.userpicture = image_file
        self.user.save()

        self.deposit_coins = reverse('deposit_coins')
    def test_templates(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.deposit_coins)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/deposit.html')
    def test_url_deposit_coins(self):
        self.assertEqual(resolve(self.deposit_coins).func, deposit_coins)
    # def test_deposit_coins_post(self):
    #     self.client.login(username='testuser', password='testpassword')
    #     form_data = {
    #         'amount' : 100,
    #     }
    #     response = self.client.post(self.deposit_coins, data=form_data)
        
    #     all_messages = [msg for msg in get_messages(response.wsgi_request)]
    #     self.assertEqual(all_messages[0].tags, "success")
    #     self.assertEqual(all_messages[0].message, f'Deposit of 100 coins successful.')
        
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('home'))
    # def test_deposit_coins_post(self):
    #     self.client.login(username='testuser', password='testpassword')
    #     form_data = {
    #         'amount' : 100,
    #     }
    #     response = self.client.post(self.deposit_coins, data=form_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, 'home')
    #     self.assertContains(response, f'Deposit of {amount} coins successful.')

class DepositAdminTest(TestCase):
    def setUp(self):
        # Create a regular user
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user.userpicture = image_file
        self.user.save()

        self.admin_user = CustomUser.objects.create_user(username='admin', email = 'admin@gmail.com' ,password='adminpassword', is_staff=True)
        self.client.login(username='testuser', password='testpassword')

    def test_deposit_admin_authenticated(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('deposit_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/deposit_admin.html')
        self.assertIn('pending_deposits', response.context)

    def test_deposit_admin_not_authenticated(self):
        self.client.logout()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('deposit_admin'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

# class ApproveDepositTest(TestCase):
#     def setUp(self):
#         self.client = Client()

#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
#         image = Image.new('RGB', (100, 100), 'white')
#         image_io = BytesIO()
#         image.save(image_io, format='JPEG')
#         image_io.seek(0)

#         # Create a SimpleUploadedFile from the image content
#         image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
#         self.user.userpicture = image_file
#         self.user.save()

#         self.admin_user = CustomUser.objects.create_user(username='admin', email = 'admin@gmail.com', password='adminpassword', is_staff=True)
#         self.client.login(username='admin', password='adminpassword')
#         self.deposit = Coins.objects.create(sender=self.user, receiver=self.admin_user, amount=50, is_confirmed=False)

#     def test_approve_deposit_staff_member(self):
#         # Make a POST request to the approve_deposit view
#         # response = self.client.post(reverse('approve_deposit', args=[self.deposit.id]))
#         response = self.client.post(f'deposit/admin/{self.deposit.id}/')

#         # Check that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)

#         # Check that the deposit is confirmed and the balances are updated
#         self.deposit.refresh_from_db()
#         # self.assertTrue(self.deposit.is_confirmed)
#         self.assertEqual(self.user.coins_balance, 50)
#         self.assertEqual(self.admin_user.coins_balance, 0)

#         # Check the success message
#         messages = [m.message for m in response.context['messages']]
#         self.assertIn('Deposit of 50 coins has been approved.', messages)

#         # Check that the user is redirected to the deposit_admin page
#         self.assertRedirects(response, reverse('deposit_admin'))

#     def test_approve_deposit_not_staff_member(self):
#         # Log out the admin user
#         self.client.logout()
#         self.client.login(username='testuser', password='testpassword')

#         # Make a POST request to the approve_deposit view
#         # response = self.client.post(reverse('approve_deposit', args=[self.deposit.id]))
#         response = self.client.post(f'deposit/admin/{self.deposit.id}/')
        

#         # Check that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)

#         # Check that the user is redirected to the home page
#         self.assertRedirects(response, reverse('home'))

#         # Check that the deposit is not confirmed and the balances are not updated
#         self.deposit.refresh_from_db()
#         self.assertFalse(self.deposit.is_confirmed)
#         self.assertEqual(self.user.coins_balance, 0)
#         self.assertEqual(self.admin_user.coins_balance, 0)

class WithdrawCoinsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user.userpicture = image_file
        self.user.save()

        # Create an admin user
        self.admin_user = CustomUser.objects.create_user(username='admin', email ='admin@gmail.com', password='adminpassword', is_staff=True)

        # Log in as the regular user
        self.client.login(username='testuser', password='testpassword')

    def test_successful_withdrawal(self):
        form_data = {
            'amount': 50,
        }
        response = self.client.post(reverse('withdraw_coins'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Coins.objects.filter(sender=self.user, receiver=self.admin_user, amount=50, is_confirmed=False).exists())
        self.assertRedirects(response, reverse('home'))

    def test_invalid_withdrawal(self):
        form_data = {
            'amount': -50,
        }
        response = self.client.post(reverse('withdraw_coins'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Coins.objects.filter(sender=self.user, receiver=self.admin_user, amount=-50, is_confirmed=False).exists())

class WithdrawAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user.userpicture = image_file
        self.user.save()

        self.admin_user = CustomUser.objects.create_user(username='admin',email = 'admin@gmail.com', password='adminpassword', is_staff=True)
        self.client.login(username='admin', password='adminpassword')
        self.withdrawal = Coins.objects.create(sender=self.user, receiver=self.admin_user, amount=50, is_confirmed=False)

    def test_withdraw_admin_authenticated(self):
        response = self.client.get(reverse('withdraw_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/withdraw_admin.html')
        self.assertIn('pending_withdraws', response.context)

    def test_withdraw_admin_not_authenticated(self):
        self.client.logout()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('withdraw_admin'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

class CartOfUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image content
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user.userpicture = image_file
        self.user.save()
        self.admin_user = CustomUser.objects.create_user(username='admin', email = 'admin@gmail.com', password='adminpassword', is_staff=True)
        self.client.login(username='testuser', password='testpassword')
        self.cart_user_url = reverse('cart_user')

    def test_cart_user_authenticated(self):
        response = self.client.get(self.cart_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swapmarket/cart_user.html')
        self.assertIn('pending_carts', response.context)

class ApproveDepositTest(TestCase):
    def setUp(self):
        # Create user's image.
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        
        # Create user testuser.
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.userpicture = image_file
        self.user.save()

        # Create staff user and login to website.
        self.admin_user = CustomUser.objects.create_user(username='admin',email = 'admin@gmail.com', password='adminpassword', is_staff=True)
        self.admin_user.coins_balance = 500
        self.admin_user.save()
        self.client.login(username='admin', password='adminpassword')
        
        # Create deposit.
        self.deposit = Coins.objects.create(sender=self.admin_user, receiver=self.user, amount=50, is_confirmed=False)
    
    def test_approve_deposit_normal(self):
        url = reverse('approve_deposit', args=[self.deposit.pk])
        self.assertEqual(url, f'/deposit/admin/{self.deposit.pk}/')
        
        response = self.client.get(url, kwargs={'deposit_id': self.deposit.pk})
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, f'Deposit of {self.deposit.amount} coins has been approved.')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('deposit_admin'))
        
    def test_approve_deposit_already_confirmed(self):
        self.deposit.is_confirmed = True
        self.deposit.save()
        
        url = reverse('approve_deposit', args=[self.deposit.pk])
        self.assertEqual(url, f'/deposit/admin/{self.deposit.pk}/')
        
        response = self.client.get(url, kwargs={'deposit_id': self.deposit.pk})
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "This deposit has already been confirmed.")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('deposit_admin'))
       
class ApproveWithdrawTest(TestCase):
    def setUp(self):
        # Create user's image.
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        
        # Create user testuser.
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.userpicture = image_file
        self.user.coins_balance = 500
        self.user.save()

        # Create staff user and login to website.
        self.admin_user = CustomUser.objects.create_user(username='admin',email = 'admin@gmail.com', password='adminpassword', is_staff=True)
        self.client.login(username='admin', password='adminpassword')
        
        # Create withdrawal.
        self.withdrawal = Coins.objects.create(sender=self.user, receiver=self.admin_user, amount=50, is_confirmed=False)
        
    def test_approve_withdraw_normal(self):
        url = reverse('approve_withdraw', args=[self.withdrawal.pk])
        self.assertEqual(url, f'/withdraw/admin/{self.withdrawal.pk}/')
        
        response = self.client.get(url, kwargs={'withdraw_id': self.withdrawal.pk})
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, f'withdraw of {self.withdrawal.amount} coins has been approved.')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('withdraw_admin'))
    
    def test_approve_withdraw_already_confirmed(self):
        self.withdrawal.is_confirmed = True
        self.withdrawal.save()
        
        url = reverse('approve_withdraw', args=[self.withdrawal.pk])
        self.assertEqual(url, f'/withdraw/admin/{self.withdrawal.pk}/')
        
        response = self.client.get(url, kwargs={'withdraw_id': self.withdrawal.pk})
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "This withdraw has already been confirmed.")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('withdraw_admin'))

class ApproveCartTest(TestCase):
    def setUp(self):
        # Create user's image.
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        
        # Create user testuser1.
        self.user1 = CustomUser.objects.create_user(username='testuser1',email = "1@gmail.com", password='testpassword')
        self.user1.userpicture = image_file
        self.user1.coins_balance = 500
        self.user1.save()
        
        # Create user testuser2.
        self.user2 = CustomUser.objects.create_user(username='testuser2',email = "2@gmail.com", password='testpassword')
        self.user2.userpicture = image_file
        self.user2.save()

        # Create staff user and login to website.
        self.admin_user = CustomUser.objects.create_user(username='admin',email = 'admin@gmail.com', password='adminpassword', is_staff=True)
        self.admin_user.coins_balance = 500
        self.admin_user.save()
        self.client.login(username='admin', password='adminpassword')
        
        # Create cart.
        self.cart = Coins.objects.create(sender=self.user1, receiver=self.user2, amount=50, is_confirmed=False)
        
    def test_approve_cart_normal(self):
        url = reverse('approve_cart', args=[self.cart.pk])
        self.assertEqual(url, f'/cart/{self.cart.pk}/')
        
        response = self.client.get(url, kwargs={'cart_id': self.cart.pk})
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, f'cart of {self.cart.amount} coins has been approved.')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_user'))
    
    def test_approve_cart_already_confirmed(self):
        self.cart.is_confirmed = True
        self.cart.save()
        
        url = reverse('approve_cart', args=[self.cart.pk])
        self.assertEqual(url, f'/cart/{self.cart.pk}/')
        
        response = self.client.get(url, kwargs={'cart_id': self.cart.pk})
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "This cart has already been confirmed.")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_user'))
