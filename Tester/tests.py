from urllib import response
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .utils import generate_token
from client.views import *
from client.models import UxClient
from Tester.models import UxTester

class TestViews(TestCase):
    def test_register(self):
        user = User.objects.create(username="user")
        user.set_password('password')
        user.save()
        client = Client()
        login = client.login(username="user", password = "password")
        url = reverse('tregister')
        response =  client.post(url, {
            'name': 'test name',
            'email': 'test email',
            'phone': 'phone',
            'password': 'password'
        })
        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "Tester/tregister.html")


    def test_tester_login(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()      
        client = Client()
        login = client.login(username="user", password = "password")
        customer = UxTester.objects.create(
            user= user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password = "password"
        )
        customer.refresh_from_db()
        url = reverse('tlogin')
        response = client.post(url, {
            'email': 'user@gmail.com',
            'password': 'password'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')   



    def test_email_verification(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()
        customer = UxTester.objects.create(
            user= user,
            name="testname",

            email="user@gmail.com",

            phone="9848044876",

            password = "password"
       )
        login = client.login(username="user", password = "password")
        token = generate_token.make_token(user)
        url = reverse('activate', args=[user.pk, token ])
        response = client.post(url)
        print(response.status_code)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tester/activate-failed.html')

    
    def test_adminlogin(self):
        my_admin=User.objects.create_superuser('myuser','myemail@test.com','password')
        my_admin.set_password('password')
        my_admin.save()

        client=Client()
        client.login(username="myuser",password="password")
        url=reverse('afterlogin')
        response = client.post(url, {
            'username': 'myuser',
            'password': 'password'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, 'admindash')     