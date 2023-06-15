from django.test import TestCase
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from channels.testing import HttpCommunicator
from .consumers import ChatConsumer
from .views import sendUserChatRequest
#UserDatabase TestCases
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(fullname="abc xyz",username="test1",email="abcxyz@gmail.com",phone='8500076565',gender='Male',country="India")
        User.objects.create(fullname="xyz abc",username="test2",email="xyzabc@gmail.com",phone='8512376565',gender='Male',country="India")

    def test_user_can_connect(self):
        tst1 = User.objects.get(username="test1")
        tst2 =  User.objects.get(username="test2")
        self.assertEqual(tst1.email, 'abcxyz@gmail.com')
        self.assertEqual(tst1.username, 'test1')
        self.assertEqual(tst1.gender, 'Male')
        self.assertEqual(tst2.username, 'test2')
        self.assertEqual(tst2.phone, '8512376565')
        self.assertEqual(tst2.email, 'xyzabc@gmail.com')


class LoginTestCase(TestCase):
    def setUp(self):
        self.user =  User.objects.create(fullname="abc xyz",username="Andrew",email="abcxyz@gmail.com",phone='8500076565',gender='Male',country="India")
        self.user.make_password('hello@123')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(self,username="abcxyz@gmail.com", password='hello@123')
        self.assertTrue((user is not None) and user.is_authenticated)
    
    def test_wrong_username(self):
        user = authenticate(self,username="xyzabc@gmail.com", password='hello@123')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(self,username="abcxyz@gmail.com", password='123')
        self.assertFalse((user is not None) and user.is_authenticated)
    
    def test_login_page_url(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='base/login_register.html')


class RegistrationPageTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.phone = '8787954987'
        self.password = make_password('password')
        self.gender ='Male'
        self.country = 'India'
    
    def test_signup_page_url(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='base/login_register.html')
    
    def test_signup_form(self):
        url = reverse('register')
        response = self.client.post(url, data={
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'password': make_password(self.password),
            'gender': self.gender,
            'country':self.country,
        })
        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
    
    def test_signup_page_view_name(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='base/login_register.html')
    
        
    
    
