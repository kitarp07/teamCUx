from urllib import response
from django.test import TestCase, Client
from django.urls import reverse, resolve
# Create your tests here.

from client.views import *
from client.models import UxClient


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

        print(response)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "client/register.html")
