from urllib import response
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from Tester.utils import generatee_token
from client.views import *
from .views import *

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
        self.assertRedirects(response, '/testerdashboard')   



    # def test_email_verification(self):
    #     user = User.objects.create(username="user76", email="user123@gmail.com")
    #     user.set_password('password')
    #     user.save()
    #     client = Client()
    #     customer = UxTester.objects.create(
    #         user= user,
    #         name="testname",
    #          password = "password"
    #    )
    #     login = client.login(username="user", password = "password")
    #     token = generate_token.make_token(user)
    #     url = reverse('activate', args=[user.pk, token ])
    #     response = client.post(url)
    #     print(response.status_code)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'Tester/activate-failed.html')



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
        token = generatee_token.make_token(user)
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
        self.assertRedirects(response, '/')    

    def test_tester_profile(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        group = Group.objects.create(name='client')
        user.groups.add(group)

        login = client.login(username="user", password="password")

        customer = UxTester.objects.create(
            user=user,
            id=1,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )

        url = reverse('myprofile', args=[customer.id])

        response = client.post(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Tester/tester-profile.html')

    def test_edit_profile(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        group = Group.objects.create(name='client')
        user.groups.add(group)
        login = client.login(username="user", password="password")

        customer = UxTester.objects.create(
            user=user,
            id=1,
            name="testname",
            email="user@gmail.com",
            phone="9848044876",
            password="password"

        )
        customer.refresh_from_db()

        url = reverse('editprofile', args=[customer.id])

        response = client.post(url, {
            'user': user,
            'name': 'testname',
            'email': 'test email',
            'phone': 'phone',
            'password': 'password'
        })

        customer.refresh_from_db()

        self.assertEquals(customer.name, 'testname')
        self.assertEquals(response.status_code, 200)   

    def change_password(self):
        user = User.objects.create(username="user", email="user@gmail.com")
        user.set_password('password')
        user.save()
        client = Client()

        customer = UxTester.objects.create(
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
    
    
    # def test_logout(self):
    #     # Log in
    #     self.client.login(username='XXX', password="XXX")

    #     # Check response code
    #     response = self.client.get('/admin/')
    #     self.assertEquals(response.status_code, 302)

    #     # Check 'Log out' in response
    #     # self.assertTrue('Log out' in response.content)

    #     # Log out
    #     self.client.logout()

    #     # Check response code
    #     response = self.client.get('/admin/')
    #     self.assertEquals(response.status_code, 302)

    #     # Check 'Log in' in response
    #     self.assertTrue('Log in' in response.content)

class TestURL(SimpleTestCase):
    def test_login(self):
        url=reverse('tlogin')
        self.assertEquals(resolve(url).func,tlogin)

    def test_viewcustomer(self):
        url=reverse('view-customer') 
        self.assertEquals(resolve(url).func,view_customer) 

    def test_admindashboard(self):
        url=reverse('admindash')
        self.assertEquals(resolve(url).func,admin_dashoard)  

    def test_myprofile(self):
        url=reverse('myprofile',args=[1])
        self.assertEquals(resolve(url).func,myprofile) 
    
    def test_testerdashboard(self):
        url =reverse('tester-dash')
        self.assertEquals(resolve(url).func, tester_dashboard)

    def test_sendfeedback(self):
        url=reverse('sendfeedback')
        self.assertEquals(resolve(url).func, send_feedbackform)

    def test_tlogout(self):
        url=reverse('tlogout')
        self.assertEquals(resolve(url).func,tlogout)

    def logout_admin(self):
        url=reverse('logout_admin')
        self.assertEquals(resolve(url).func,logout_admin)    
    #     client=Client()
    #     client.login(username="myuser",password="password")
    #     url=reverse('afterlogin')
    #     response = client.post(url, {
    #         'username': 'myuser',
    #         'password': 'password'
    #     })
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, 'admindash')     
