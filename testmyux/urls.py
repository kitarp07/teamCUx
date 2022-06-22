"""testmyux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from optparse import AmbiguousOptionError
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from client.views import *
from pages.views import *
from Tester.views import *
urlpatterns = [
#    path('admin', auth_views.LoginView.as_view(template_name='adminpage/adminlogin.html'), name='admin'),
    path('admin/', admin.site.urls),
   path('client/register', client_reg_view, name="client-reg" ),
   path('', homepage, name="homepage" ),
   path('',include('Tester.urls')),
   path('client/login', client_login_view, name="client-login"),
   path('client/dashboard', client_dashoard, name='client-dash'),
   path('tester/login', tlogin, name='tlogin' ),
 
   path('client/create-test', create_test, name='create-test'),
   path('client/verify-email/<uidb64>/<token>', verify_email, name="verify"),
   path('tester/upload-video', tester_upload_video, name='upload-video'),
   path('client/email-verified', email_verified_page, name='email-verified' ),
   path('tester/email-verified', email_verified_page, name='tester-email-verified' ),
   path('tester/alltests', view_all_tests, name= "alltests"),
   path('client/sentbytester', sent_by_tester, name='sentbytester'),
   path('client/profile', client_profile, name='client-profile'),
   path('client/edit-profile/<int:pk>', edit_profile, name='client-edit-profile'),
   path('client/forgetpassword/enteremail', enter_email, name='enter-email'),
   path('client/forgetpassword/clicklink/<uidb64>/<token>', click_link, name="clicklink"),
   path('client/changepassword/<int:pk>', change_password, name="change-password"),
   path('tester/forgetpassword/enteremail', enter_email, name='tester-enter-email'),
   path('tester/forgetpassword/clicklink/<uidb64>/<token>', click_link, name="tester-clicklink"),
   path('tester/changepassword/<int:pk>', change_password, name="tester-change-password")


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
