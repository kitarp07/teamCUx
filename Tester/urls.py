from django.contrib import admin
from django.urls import path,include

from Tester import views
from pages.views import *
urlpatterns = [
    path('tregister',views.tester_reg_view,name='tregister'),
    path('tlogin/',views.tlogin, name="tlogin"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('afterlogin', views.afterlogin_view, name="afterlogin"),

     path('view-customer', views.view_customer, name='view-customer'),

]
