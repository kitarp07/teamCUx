from distutils.command.upload import upload
from pydoc import cli
from re import S
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse, resolve
from requests import request
# Create your tests here.

from client.views import *
from client.models import UxClient
from client.utils import generate_token
from Tester.models import UxTester


class TestViews(TestCase):
    def test_register(self):
        user = User.objects.create(username="user")
        user.set_password('password')
        user.save()
        client = Client()

        login = client.login(username="user", password="password")

        url = reverse('client-reg')

        response = client.post(url, {
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

        group = Group.objects.create(name='client')
        user.groups.add(group)
        login = client.login(username="user", password="password")

        customer = UxClient.objects.create(
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

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

        login = client.login(username="user", password="password")

        customer = UxClient.objects.create(
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )

        url = reverse('create-test')

        response = client.post(url, {
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
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )

        login = client.login(username="user", password="password")

        token = generate_token.make_token(user)

        url = reverse('verify', args=[user.pk, token])

        response = client.post(url)
        print(response.status_code)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/verification_failed.html')

    def test_client_profile(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        group = Group.objects.create(name='client')
        user.groups.add(group)

        login = client.login(username="user", password="password")

        customer = UxClient.objects.create(
            user=user,
            id=1,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )

        url = reverse('client-profile')

        response = client.post(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientprofile.html')

    def test_edit_profile(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        group = Group.objects.create(name='client')
        user.groups.add(group)
        login = client.login(username="user", password="password")

        customer = UxClient.objects.create(
            user=user,
            id=1,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )
        customer.refresh_from_db()

        url = reverse('client-edit-profile', args=[customer.id])

        response = client.post(url, {
            'user': user,
            'name': 'edit name',
            'email': 'test email',
            'phone': 'phone',
            'password': 'password'
        })

        customer.refresh_from_db()

        self.assertEquals(customer.name, 'edit name')
        self.assertEquals(response.status_code, 302)
    
    # def test_forget_email(self):
    #     user = User.objects.create(username="user", email="user@gmail.com")
    #     user.set_password('password')
    #     user.save()
    #     client = Client()

    #     customer = UxClient.objects.create(
    #         user=user,
    #         name="testname",
    #         email="user@gmail.com",
    #         phone="9848044876",
    #         password="password"

    #     )

    #     customer.refresh_from_db()

    #     login = client.login(username="user", password="password")

    #     token = generate_token.make_token(user)

    #     url = reverse('clicklink', args=[user.id, token])

    #     response = client.post(url)
    #     print(response.status_code)

    #     self.assertEquals(response.status_code, 200)
    
    def change_password(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        customer = UxClient.objects.create(
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )

        url = reverse('change-password', args=[customer.id])

        response = client.post(url,
        {
            'newpassword': 'newp',
            'cpassword': 'newp'
        })

        customer.refresh_from_db()

        customer.refresh_from_db()

        self.assertEquals(customer.password, 'newpassword')
        self.assertEquals(response.status_code, 302)
    
    def sent_by_tester(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        customer = UxClient.objects.create(
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )
        url = reverse('sent-by-tester')

        response = client.post(url)

        customer.refresh_from_db()

        self.assertEquals(response.status_code, 302)

    def test_deleteaccount(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        customer = UxClient.objects.create(
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )
        url = reverse('delete-account', args=[customer.id])
        
        response = client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/client/login')
    
    def test_rating(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user1 = User.objects.create(username="user1", email="user1@gmail.com")
        user1.set_password('password1')
        user.save()
        client = Client()
        login = client.login(username="user", password="password")
        customer = UxTester.objects.create( user=user1,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password" )
        customer1 = UxClient.objects.create(
            user=user,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )
        test = CreateTests.objects.create(
           id = 1,
           title = 'test name',
           mention_tasks = 'tasks',
           requirements = 'requirements',
           additional_guidelines = 'additional',
        )
        video = UploadVideo.objects.create(
            id = 100,
            video_link = 'videolink',
            client = customer1,
            test = test,
            tester = customer

        )
        rate_url = reverse('rating', args=[video.id])
        response_rate = client.post(rate_url)
        client.post(rate_url)
        self.assertEquals(response_rate.status_code, 302)
        self.assertRedirects(response_rate, '/client/sentbytester')


        

        




    