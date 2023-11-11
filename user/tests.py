
from django.test import TestCase, Client
# from django.contrib.auth.models import User
from user.models import CustomUser
from django.urls import reverse, resolve
from .views import signin, signup, profile, registered, edit_profile, changepassword
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here. 

class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.profile_url = reverse('user:profile')
    def test_url_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
    def test_templates_profile(self):
        self.assertEqual(resolve(self.profile_url).func, profile)

class signinTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create(
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
        
    def test_url_sigin(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.signin)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signin.html')
        self.assertEqual(resolve(self.signin).func, signin)
    def test_after_post(self):
        self.client.login(username="testuser", password= "testpass")
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
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.signin, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)
    def test_user_is_none(self):
        response = self.client.post(self.signin, {"username": "6410000200", "password": "007008ZA"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password. Please try again.')
    def test_signin_get_request(self):
        response = self.client.get(self.signin)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('message'))

class SigupTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.signup = reverse('user:signup')
    def test_url_sigup(self):
        response = self.client.get(self.signup)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertEqual(resolve(self.signup).func, signup)

    def test_sigup_sucessful(self):
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
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username already exists") 
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
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email already exists") 
    def test_signup_password_not_match(self):    
        response = self.client.post(self.signup,
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass',
                'cpassword': 'testpass2',
            }
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Passwords do not match")

class RegisteredTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.registered = reverse('user:registered')
    def test_url_registered(self):
        response = self.client.get(self.registered)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/registered.html')
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
    def test_registered_email_exists(self):
        image_content = b'This is a test image.'
        image_file = SimpleUploadedFile('test_image.jpg', image_content, content_type='image/jpeg')
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
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            phone='1234567890',
            firstname='John',
            lastname='Doe',
            userdescription='Test user description',
            userpicture='path/to/user/picture.jpg',
            coins_balance=100,
        )
        self.client.login(username='testuser', password='testpass')
        self.edit_profile = reverse('user:edit_profile')
    def test_url_edit_profile(self):
        response = self.client.get(self.edit_profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/editprofile.html')
        self.assertEqual(resolve(self.edit_profile).func, edit_profile)
    def test_edit_profile_successful(self):
        response = self.client.post(self.edit_profile,
            {
                'phone': '9876543210',
                'firstname': 'UpdatedFirstName',
                'lastname': 'UpdatedLastName',
                'userdescription': 'Updated user description',
            }
        )
        self.assertRedirects(response, reverse('user:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '9876543210')
        self.assertEqual(self.user.firstname, 'UpdatedFirstName')
        self.assertEqual(self.user.lastname, 'UpdatedLastName')
        self.assertEqual(self.user.userdescription, 'Updated user description')

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
