from re import S
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse, resolve
# Create your tests here.

from client.views import *
from client.models import UxClient
from client.utils import generate_token


class TestViews(TestCase):
    def test_register(self):
        user = User.objects.create(username="user")
        user.set_password('password')
        user.save()
        client = Client()

        login = client.login(username="user", password = "password")

       

        url = reverse('client-reg')

        response =  client.post(url, {
            'name': 'test name',
            'email': 'test email',
            'phone': 'phone',
            'password': 'password'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "client/register.html")
    

    def test_client_login(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        
        client = Client()

        login = client.login(username="user", password = "password")


        customer = UxClient.objects.create(
            user= user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password = "password"

        )

        customer.refresh_from_db()

        url = reverse('client-login')

        response = client.post(url, {
            'email': 'user@gmail.com',
            'password': 'password'
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/client/dashboard')
    
    def test_create_tests(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        login = client.login(username="user", password = "password")

        customer = UxClient.objects.create(
            user= user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password = "password"

        )

        url = reverse('create-test')

        response =  client.post(url, {
            'title': 'test name',
            'mention_tasks': 'tasks',
            'requirements': 'requirements',
            'additional_guidelines': 'additional',
            
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/create-test.html')


    def test_email_verification(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        customer = UxClient.objects.create(
            user= user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password = "password"

        )

        login = client.login(username="user", password = "password")

        token = generate_token.make_token(user)

        url = reverse('verify', args=[user.pk, token ])

        response = client.post(url)
        print(response.status_code)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/verification_failed.html')