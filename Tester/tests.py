

# Create your tests here.
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse, resolve
# Create your tests here.
from Tester.views import *
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
        self.assertTemplateUsed(response, "tester/tregister.html")