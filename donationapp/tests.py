from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import index
from .views import account
from django.contrib.auth.models import User
from django.test import Client

# Create your tests here.
class Login_Test_Cases(TestCase):
    def setUp(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()

    def test_login(self):
        client = Client()

        self.assertTrue(client.login(username='donationAppCS3240@gmail.com', password='CS3240!!'), 'Login Failed')

class Login_Test_Case_Boundary(TestCase):
    def setUp(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()

    def test_login_wrong_password(self):
        client = Client()
        self.assertFalse(client.login(username='donationAppCS3240@gmail.com', password='cs3240!!'), 'Login Failed')

class Login_Test_Case_Capitalization(TestCase):
    def setUp(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()

    def test_login_wrong_password(self):
        client = Client()
        self.assertTrue(client.login(username='DONATIONAPPCS3240@gmail.com', password='CS3240!!'), 'Login Failed')


#These just tell whether loads to the right page
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Donation App</title>', html)

class AccountPageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = account(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>My Account</title>', html)