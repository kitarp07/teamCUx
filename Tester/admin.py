from distutils.command.upload import upload
from django.contrib import admin
from .models import UploadVideo
# Register your models here.
admin.site.register(UploadVideo)