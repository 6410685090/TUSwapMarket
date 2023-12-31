import os
import json
from PIL import Image
from django.test import TestCase, Client
from io import BytesIO
from swapmarket.models import Item
from .models import Room, Message
from user.models import CustomUser
from django.urls import reverse, resolve
from .views import signin, signup, profile, registered, edit_profile, changepassword, findroom, inbox
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import CustomUserEditForm 

class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.profile_url = reverse('user:profile')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword',
            phone='1234567890',
            firstname='John',
            lastname='Doe',
            userdescription='Test user description',
            userpicture='path/to/user/picture.jpg',
            coins_balance=100,
        )
        self.client.login(username='testuser', password='oldpassword')
    def test_url_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
    def test_templates_profile(self):
        self.assertEqual(resolve(self.profile_url).func, profile)
    def test_check_my_item(self):
        item1 = Item.objects.create(
                                itemname = '1',
                                seller = self.user,
                                nItem = 0,
                                price = 0,
                                itempicture = 'path/to/user/picture1.jpg',)
        item2 = Item.objects.create(
                                itemname = '2',
                                seller = self.user,
                                nItem = 0,
                                price = 0,
                                itempicture = 'path/to/user/picture2.jpg',)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        for i in range(0, len([subject for subject in Item.objects.filter(seller=self.user)])):
            self.assertEqual(
            response.context['myitem'][i],
            [subject for subject in Item.objects.filter(seller=self.user)][i]
            )


class signinTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com',
            phone='1234567890',
            displayname='Test Display Name',
            firstname='John',
            lastname='Doe',
            userdescription='Test user description',
            userpicture='path/to/user/picture.jpg',
            coins_balance=100,
        )
        self.signin = reverse('user:signin')
    def test_url_signup(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.signin)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signin.html')
    def test_templates_signin(self):
        self.assertEqual(resolve(self.signin).func, signin)
    def test_custom_user_fields(self):
        user = CustomUser.objects.get(id=1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.displayname, 'Test Display Name')
        self.assertEqual(user.firstname, 'John')
        self.assertEqual(user.lastname, 'Doe')
        self.assertEqual(user.userdescription, 'Test user description')
        self.assertEqual(user.userpicture, 'path/to/user/picture.jpg')
        self.assertEqual(user.coins_balance, 100)
    def test_Redirect(self):
        response = self.client.post(self.signin, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    def test_user_is_none(self):
        response = self.client.post(self.signin, {"username": "6410000200", "password": "007008ZA"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password. Please try again.')
    def test_signin_get_request(self):
        response = self.client.get(self.signin)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('message'))

class SignupTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.signup = reverse('user:signup')
    def test_url_signup(self):
        response = self.client.get(self.signup)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
    def test_templates_signup(self):
        self.assertEqual(resolve(self.signup).func, signup)
    def test_signup_sucessful(self):
        response = self.client.post(self.signup,
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass',
                'cpassword': 'testpass',
            }
        )
        self.assertEqual(response.url, '/registered')
        self.assertEqual(self.client.session['signup_username'], 'testuser')
        self.assertEqual(self.client.session['signup_email'], 'test@example.com')
        self.assertEqual(self.client.session['signup_password'], 'testpass')
    def test_signup_username_exists(self):
        CustomUser.objects.create(username='testuser', email='existing@example.com', password='testpass')
        response = self.client.post(self.signup,
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass',
                'cpassword': 'testpass',
            }
        )
        self.assertEqual(response.context['message'], "Username already exists.")
    def test_signup_email_exists(self):
        CustomUser.objects.create(username='testuser1', email='test@example.com', password='testpass')
        response = self.client.post(self.signup,
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass',
                'cpassword': 'testpass',
            }
        )
        self.assertEqual(response.context['message'], "Email already exists")
    def test_signup_password_not_match(self):    
        response = self.client.post(self.signup,
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass',
                'cpassword': 'testpass2',
            }
        )
        self.assertEqual(response.context['message'], "Passwords do not match")

class RegisteredTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.registered = reverse('user:registered')
    def test_url_registered(self):
        response = self.client.get(self.registered)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/registered.html')
    def test_templates_registered(self):
        self.assertEqual(resolve(self.registered).func, registered)
    def test_registered_successful(self):
        image_content = b'This is a test image.'
        image_file = SimpleUploadedFile('test_image.jpg', image_content, content_type='image/jpeg')
        s = self.client.session
        s.update({
            "signup_username": 'testuser',
            "signup_email": 'test@example.com',
            "signup_password": 'testpass',
        })
        s.save()
        signup_username = self.client.session.get('signup_username')
        signup_email = self.client.session.get('signup_email')
        signup_password = self.client.session.get('signup_password')
        response = self.client.post(self.registered, 
            { 
                'phone': '1234567890',
                'firstname': 'John',
                'lastname': 'Doe',
                'userdescription': 'Test user description',
                'userpicture': image_file,
                'username': signup_username,
                'email': signup_email,
                'password': signup_password,

            }
        )
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(self.client.session['_auth_user_id'])
    def test_registered_del_session(self):
        image_content = b'This is a test image.'
        image_file = SimpleUploadedFile('test_image.jpg', image_content, content_type='image/jpeg')
        s = self.client.session
        s.update({
            "signup_username": 'testuser',
            "signup_email": 'test@example.com',
            "signup_password": 'testpass',
        })
        s.save()
        signup_username = self.client.session.get('signup_username')
        signup_email = self.client.session.get('signup_email')
        signup_password = self.client.session.get('signup_password')
        response = self.client.post(self.registered, 
            { 
                'phone': '1234567890',
                'firstname': 'John',
                'lastname': 'Doe',
                'userdescription': 'Test user description',
                'userpicture': image_file,
                'username': signup_username,
                'email': signup_email,
                'password': signup_password,

            }
        )
        self.assertNotIn('signup_username', self.client.session)
        self.assertNotIn('signup_email', self.client.session)
        self.assertNotIn('signup_password', self.client.session)
    def test_registered_upload_profile(self):
        s = self.client.session
        s.update({
            "signup_username": 'testuser',
            "signup_email": 'test@example.com',
            "signup_password": 'testpass',
        })
        s.save()
        signup_username = self.client.session.get('signup_username')
        signup_email = self.client.session.get('signup_email')
        signup_password = self.client.session.get('signup_password')
        response = self.client.post(self.registered, 
            { 
                'phone': '1234567890',
                'firstname': 'John',
                'lastname': 'Doe',
                'userdescription': 'Test user description',
                'username': signup_username,
                'email': signup_email,
                'password': signup_password,
            }
        )
        self.assertEqual(response.context['message'], "Please upload you picture")
    def test_registered_email_exists(self):
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        CustomUser.objects.create(username='existinguser', email='test@example.com', password='testpass')
        s = self.client.session
        s.update({
            "signup_username": 'testuser',
            "signup_email": 'test@example.com',
            "signup_password": 'testpass',
        })
        s.save()
        signup_username = self.client.session.get('signup_username')
        signup_email = self.client.session.get('signup_email')
        signup_password = self.client.session.get('signup_password')        
        response = self.client.post(self.registered,
            {
                'phone': '1234567890',
                'firstname': 'John',
                'lastname': 'Doe',
                'userdescription': 'Test user description',
                'userpicture': image_file,
                'username': signup_username,
                'email': signup_email,
                'password': signup_password,
            }
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email already exists")

class EditProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            phone='1234567890',
            firstname='John',
            lastname='Doe',
            userdescription='Test user description',
            userpicture=image_file ,
            coins_balance=100,
        )
        self.client.login(username='testuser', password='testpass')
        self.edit_profile = reverse('user:edit_profile')
    def test_url_edit_profile(self):
        response = self.client.get(self.edit_profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/editprofile.html')
    def test_templates_edit_profile(self):
        self.assertEqual(resolve(self.edit_profile).func, edit_profile)
    def test_edit_profile_get_request(self):
        response = self.client.get(self.edit_profile)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserEditForm)
    def test_edit_profile_successful(self):
        response = self.client.post(self.edit_profile,
            {
                'phone': '9876543210',
                'firstname': 'UpdatedFirstName',
                'lastname': 'UpdatedLastName',
                'bank' : 'SCB',
                'bankid' : '12345678',
                'userdescription': 'Updated user description',
            }
        )
        self.assertRedirects(response, reverse('user:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '9876543210')
        self.assertEqual(self.user.firstname, 'UpdatedFirstName')
        self.assertEqual(self.user.lastname, 'UpdatedLastName')
        self.assertEqual(self.user.userdescription, 'Updated user description')
    def test_remove_old_picture(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'new_user_picture.jpg'
        file.seek(0)
        
        response = self.client.post(self.edit_profile,
            {
                'userpicture': file,
                'phone': '9876543210',
                'firstname': 'UpdatedFirstName',
                'lastname': 'UpdatedLastName',
                'bank' : 'SCB',
                'bankid' : '12345678',
                'userdescription': 'Updated user description',
            },
            format="multipart"
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '9876543210')
        self.assertEqual(self.user.userpicture.name, 'user_pictures/new_user_picture.jpg')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile')
        os.remove('media/user_pictures/new_user_picture.jpg')

class ChangePasswordViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword',
            phone='1234567890',
            firstname='John',
            lastname='Doe',
            userdescription='Test user description',
            userpicture='path/to/user/picture.jpg',
            coins_balance=100,
        )
        self.client.login(username='testuser', password='oldpassword')
        self.chpass = reverse('user:chpass')

    def test_url_changepassword(self):
        response = self.client.get(self.chpass)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/chpass.html')
    def test_templates_chpass(self):
        self.assertEqual(resolve(self.chpass).func, changepassword)
    def test_change_password_successful(self):
        response = self.client.post(self.chpass,
            {
                'newpass': 'newpassword',
                'cnewpass': 'newpassword',
            }
        )
        self.assertEqual(response.url, '/logout')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))
    def test_change_password_passwords_not_match(self):
        response = self.client.post(self.chpass,
            {
                'newpass': 'newpassword',
                'cnewpass': 'differentpassword',
            }
        )
        self.assertContains(response, 'Password not match.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpassword'))

class SendMessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.room = Room.objects.create(name='Test Room')
        self.send_url = reverse('user:send')

    def test_send_message(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'message': 'Hello, test message!',
            'username': 'testuser',
            'room_id': self.room.id,
        }
        response = self.client.post(self.send_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 1)
        created_message = Message.objects.first()
        self.assertEqual(created_message.value, 'Hello, test message!')
        self.assertEqual(created_message.user, 'testuser')
        self.assertEqual(created_message.room, str(self.room.id))

class FindRoomTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
    def test_existing_room(self):
        existing_room = Room.objects.create(name='existing_room')
        response = self.client.get('user:/chat/existing_room/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/room.html')
        self.assertEqual(response.context['room_details'], existing_room)
    def test_new_room(self):
        response = self.client.get('user:/chat/new_room/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/room.html')
        self.assertTrue(Room.objects.filter(name='new_room').exists())
        self.assertEqual(response.context['room_details'].name, 'new_room')

class GetMessagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    def test_get_messages(self):
        room = Room.objects.create(name='test_room')
        message1 = Message.objects.create(room=room, user=self.user, value='Hello')
        message2 = Message.objects.create(room=room, user=self.user, value='How are you?')
        response = self.client.get('user:/getMessages/test_room/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('messages', response_data)
        expected_messages = list(Message.objects.filter(room=room.id).values())
        self.assertEqual(response_data['messages'], expected_messages)

class InboxTest(TestCase):
    def setUp(self) :
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        self.client = Client()
        self.user = CustomUser.objects.create(username='TEST1', email = "1")
        self.user.set_password('Student331')
        self.user.userpicture = image_file
        self.user.save()
        self.inbox_url = reverse('user:inbox')
    def test_url_inbox(self):
        self.client.login(username='TEST1', password='Student331')
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/inbox.html')
        self.assertEqual(resolve(self.inbox_url).func, inbox) 
    def test_inbox_view(self):
        self.client.login(username='TEST1', password='Student331')
        room1 = Room.objects.create(name='testuser_room1')
        room2 = Room.objects.create(name='room2_testuser')
        room3 = Room.objects.create(name='testuser_room3_anotheruser')
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('allroom', response.context)
        self.assertIn('mychat', response.context)