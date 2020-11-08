from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import resolve
from .views import index, account, causes, volunteer_opportunities, volunteer_signup
from django.contrib.auth.models import User
from django.test import Client
from .models import Cause, Transaction, Volunteer_Opp, Volunteer_Transaction
from django.utils import timezone
from django.conf import settings
from importlib import import_module

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
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()
        request = HttpRequest()
        request.user = user
        response = index(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Donation App</title>', html)

class AccountPageTest(TestCase):
    def test_account_page_returns_correct_html(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()
        request = HttpRequest()
        request.user = user
        response = account(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>My Account</title>', html)

class CausesPageTest(TestCase):
    def test_cause_page_returns_correct_html(self):
        request = HttpRequest()
        response = causes(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>View Causes</title>', html)

class VolunteeringPageTest(TestCase):
    def test_volunteering_page_returns_correct_html(self):
        request = HttpRequest()
        response = volunteer_opportunities(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>View Volunteer Opportunities</title>', html)

class VolunteerSignUpPageTest(TestCase):
    def test_signup_page_returns_correct_html(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()
        request = HttpRequest()
        request.user = user
        response = volunteer_signup(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Volunteer Sign Up</title>', html)

class CauseModelTests(TestCase):
    def test_negative_total(self):
        cause = Cause(name="test", description="testing causes", total_money=-100.00, goal=100)
        self.assertTrue(cause, False)

    def test_negative_goal(self):
        cause = Cause(name="test", description="testing causes", total_money=0, goal=-100.00)
        self.assertTrue(cause, False)

class TransactionModelTests(TestCase):
    def test_negative_amount(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()
        cause = Cause(name="test", description="testing causes", total_money=-100.00, goal=100)
        transaction = Transaction(cause=cause, user=user, amount=-100.00, date=timezone.now())
        self.assertTrue(transaction, False)

class VolunteerOpportunityModelTests(TestCase):
    def test_negative_total(self):
        cause = Volunteer_Opp(name="test", description="testing volunteer opportunities", total_people=-6, people_needed=6)
        self.assertTrue(cause, False)

    def test_negative_goal(self):
        cause = Volunteer_Opp(name="test", description="testing volunteer opportunities", total_people=6, people_needed=-6)
        self.assertTrue(cause, False)

    def test_invalid_date(self):
        cause = Volunteer_Opp(name="test", description="testing causes", total_people=-10, people_needed=15, date='120',
                              begin='11:00')

        self.assertTrue(cause, False)

    def test_invalid_time(self):
        cause = Volunteer_Opp(name="test", description="testing causes", total_people=-10, people_needed=15, date = '10/23/20',
                              begin='110')

        self.assertTrue(cause, False)

class VolunteerModelTransactionModelTests(TestCase):
    def test_acceptence_no_date(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()
        cause = Volunteer_Opp(name="test", description="testing causes", total_people=-10, people_needed=15)
        signup = Volunteer_Transaction(name=cause, user=user)
        self.assertTrue(signup, True)

    def test_acceptence_date(self):
        user = User.objects.create(username='donationAppCS3240@gmail.com')
        user.set_password('CS3240!!')
        user.save()
        cause = Volunteer_Opp(name="test", description="testing causes", total_people=-10, people_needed=15, date = '10/23/20', begin = '11:00')
        signup = Volunteer_Transaction(name=cause, user=user)
        self.assertTrue(signup, True)


