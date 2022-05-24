from django.contrib import admin
from django.urls import path,include

from Tester import views
from pages.views import *
urlpatterns = [
    path('',views.tester_reg_view,name='tregister'),
    path('tlogin/',views.tlogin, name="tlogin"),

]
