from django.contrib import admin
from django.urls import path,include

from Tester import views
from pages.views import *
urlpatterns = [
    path('tester/register',views.tester_reg_view,name='tregister')
]
