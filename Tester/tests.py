from urllib import response
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from Tester.models import UxTester

class TestViews(TestCase):
    def test_upload_video(self):
        user = User.objects.create(username="user")
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

        url = reverse('upload-video')

        customer.refresh_from_db()

        response = client.post(url, {
            'video_link': 'test link'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tester/uploadvideo.html')