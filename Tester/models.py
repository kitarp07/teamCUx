from django.db import models

# Create your models here.
from client.models import CreateTests, UxClient

from django.contrib.auth.models import User
# Create your models here.
class UxTester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200,blank=True, null=False)
    email = models.CharField(max_length=200,blank=True, null=False)
    phone = models.CharField(max_length=10,blank=True, null=False)
    password = models.CharField(max_length=30,blank=True, null=False)
    is_email_verified =models.BooleanField(default=False)
    rating = models.FloatField(default = 0, null=True, blank=True)



class UploadVideo(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    video_link = models.CharField(max_length=255, blank=True, null=False)
    client = models.ForeignKey(UxClient, on_delete=models.SET_NULL, null=True, blank=True)
    test = models.ForeignKey(CreateTests, on_delete=models.SET_NULL, null=True, blank=True)
    tester = models.ForeignKey(UxTester, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.FloatField(default = 0, null=True, blank=True)


class FeedBack(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True)
    feedback=models.CharField(max_length=255,blank=True)
    tester=models.ForeignKey(UxTester,on_delete=models.SET_NULL,null=True,blank=True)
    client=models.ForeignKey(UxClient,on_delete=models.SET_NULL,null=True,blank=True)
    
