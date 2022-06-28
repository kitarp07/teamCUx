from django.contrib import admin
from django.urls import path,include

from Tester import views
from pages.views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('tregister',views.tester_reg_view,name='tregister'),
    path('tlogin/',views.tlogin, name="tlogin"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('afterlogin', views.afterlogin_view, name="afterlogin"),
    path('view-customer',views.view_customer,name='view-customer'),
    path('viewclient',views.view_client,name="viewclient"),
    path('admindash' ,views.admin_dashoard,name='admindash'),
    path('myprofile/<int:pk>', views.myprofile, name='myprofile'),
    path('editprofile/<int:pk>', views.editprofile, name= 'editprofile'),
    path('testerdashboard', views.tester_dashoard, name='tester-dash'),
    path('deletetester/<int:pk>', views.delete_tester,name="deletetester"),
    # path('sendfeedback',views.send_feedback,name='sendfeedback'),
    path('sendfeedback',views.send_feedbackform,name='sendfeedback'),



    #password reset
#      path('password_reset/',auth_views.PasswordResetView.as_view(
#              template_name='Tester/password_reset_form.html'),
#          name='password_reset'),

#     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='Tester/password_reset_done.html'),name='password_reset_done'),

#     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Tester/password_reset_confirm.html'),name='password_reset_confirm'),

#     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
#              template_name='Tester/password_reset_complete.html'),
#          name='password_reset_complete'),
# 
]
