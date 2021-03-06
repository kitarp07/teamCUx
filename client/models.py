from django.db import models
from django.contrib.auth.models import User

# from Tester.models import UxTester

# Create your models here.
class UxClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200,blank=True, null=False)
    email = models.CharField(max_length=200,blank=True, null=False)
    phone = models.CharField(max_length=10,blank=True, null=False)
    password = models.CharField(max_length=30,blank=True, null=False)
    isEmailVerified = models.BooleanField(default=False)
    



    
class CreateTests(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    mention_tasks = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    additional_guidelines = models.TextField(null=True, blank=True) 
    created_by = models.ForeignKey(UxClient, on_delete=models.SET_NULL, null=True, blank=True)
    #paymentdetails
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    nameoncard = models.CharField(max_length=100, null=True, blank=True)
    cardnumber = models.FloatField(default = 0, null=True, blank=True)
    cvv = models.FloatField(default = 0, null=True, blank=True)
    expirydate = models.DateTimeField(auto_now_add=False,  null=True, blank=True)
    amountpaid = models.FloatField(default = 0, null=True, blank=True)
    isApproved = models.BooleanField(default=False)


   

    