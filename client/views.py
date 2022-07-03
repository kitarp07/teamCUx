from http import client
from lib2to3.pgen2 import token
from tokenize import group
from unicodedata import name
import uuid

from django.shortcuts import redirect, render
from Tester.models import UploadVideo
from client.forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from client.models import UxClient
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from Tester.models import UxTester


def send_verification_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Verify your email'
    email_body = render_to_string('client/emailverify.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),

    })

    customer = UxClient.objects.get(user=user.pk)

    email = EmailMessage(subject=email_subject, 
    body=email_body, 
    from_email= settings.EMAIL_FROM_USER,
    to=[customer.email]
    )

    email.send()



def client_reg_view(request):
    form = ClientForm()
    if request.method == 'POST': 
        form = ClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            cpw = request.POST.get('cpassword')
            
            if User.objects.filter(username=name).exists() or User.objects.filter(email=email).exists():
                messages.success(request, "User already exists. Please choose different name and email")
            else:
                if name != "" and name !=  "" and name != "" and name != "":
                    if pw==cpw:
                        user = User.objects.create_user(name, email, pw)
                        
                        
                        try:   
                            group = Group.objects.get(name="client")
                        except:
                            group = Group.objects.create(name="client")
                            
                        user.groups.add(group)
                        user.save()

                    

                        client = form.save(commit=False) # save info but dont commit change to database
                        client.user = user
                        client.save()
                        send_verification_email(user, request)
                        messages.success(request, "Please check your email for email verification")
                        return redirect('client-login')
                    else:
                        messages.success(request, "Passwords don't match")
                else:
                    messages.success(request, "Please fill all the fields")


    context = {'form': form}

    return render(request, 'client/register.html', context)

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        customer = UxClient.objects.get(user=user)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        customer.isEmailVerified = True
        customer.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified')
        return redirect ('email-verified')

    return render(request, 'client/verification_failed.html', {"user": user })
    


def client_login_view(request):
   
    

    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        
        user = authenticate(request, username=email, password=passw)

        
        if user is None:
            messages.success(request, "Wrong Credentials. Please try again")
       
        elif user.groups.all()[0].name == 'client':
            login(request, user)
            return redirect('client-dash')
           
        else:
            messages.success(request, "Wrong Credentials. Please try again")
            


    return render(request, "client/login.html")

def client_dashoard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.groups.all()[0].name == 'client':
            customer = user.uxclient
            context ={
                    'customer':customer
                }
    else:
        messages.success(request, "Wrong Credentials. Please try again")
        return redirect('client-login')

    return render(request, 'client/clientdash.html', context)

def create_test(request):
    form = CreateTestForm()
    if request.user.is_authenticated:
        if request.user.uxclient:
            customer = request.user.uxclient
        else:
            messages.erorr(request, "Wrong Credentials. Please try again")
        if request.method=='POST':
            form = CreateTestForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                mention_tasks = form.cleaned_data['mention_tasks']
                requirements = form.cleaned_data['requirements']
                additional_guidelines = form.cleaned_data['additional_guidelines']
                cardname = form.cleaned_data['nameoncard']
                cardnum = form.cleaned_data['cardnumber']
                cvv = form.cleaned_data['cvv']
                expdate = form.cleaned_data['expirydate']


                CreateTests.objects.create(
                    title= title,
                    mention_tasks = mention_tasks,
                    requirements = requirements,
                    additional_guidelines = additional_guidelines,
                    created_by = customer,
                    nameoncard = cardname,
                    cardnumber = cardnum,
                    cvv = cvv,
                    expirydate =expdate,
                    amountpaid = 10

                )

    return render(request, "client/create-test.html")

def email_verified_page(request):
    return render(request, "client/EmailVerified.html")

def sent_by_tester(request):
    if request.user.is_authenticated:
        user = request.user.uxclient
        videos = UploadVideo.objects.filter(client=user.pk)
        
    else:
        videos = UploadVideo.objects.all()

    context = {
            'videos': videos
        }

    return render(request, "client/sentbytester.html", context)

def alltests(request):
    if request.user.is_authenticated:
        user = request.user.uxclient
        tests = CreateTests.objects.filter(created_by=user.pk)
        
    else:
        messages.success(request, "You are not logged in")
        return redirect('client-login')

   
        
    
    context = {
            'tests': tests
        }

    return render(request, "client/alltests.html", context)



def client_profile(request):
    user = request.user

    if user is not None:
        if user.groups.all()[0].name == 'client':
             
            customer = request.user.uxclient

            context ={
                 'customer':customer
             }
            return render(request, "client/clientprofile.html",context)


    
    else:
        messages.success(request, "Wrong Credentials. Please try again")
        return redirect('client-login')

def edit_profile(request, pk):
    uxclient = UxClient.objects.get(id=pk)
    form = ClientForm(request.POST)
    user = request.user
    if user is None:
            messages.success(request, "Wrong Credentials. Please try again")
       
    elif user.groups.all()[0].name == 'client':
        if request.method == "POST":
            uxclient.name = request.POST.get('name')
            uxclient.email = request.POST.get('email')
            uxclient.phone = request.POST.get('phone')
            user.username = request.POST.get('name')
            user.email = request.POST.get('email')
            user.save()
            uxclient.save()
            return redirect('client-profile')
           
    else:
        messages.success(request, "Wrong Credentials. Please try again")
   

    context = {'form': form, 'uxclient':uxclient}
    return render(request, 'client/edit-profile.html', context)

def send_forget_password_email(request, user):
    subject = "Reset password link"
    if request.method == "POST":
        email = request.POST.get('email')
    current_site = get_current_site(request)
    email_body = render_to_string('client/forgetpassword/clicklink.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),

    })
    email = EmailMessage(subject=subject, 
    body=email_body, 
    from_email= settings.EMAIL_FROM_USER,
    to=[user.email]
    )

    email.send()


#forget password
def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email):
            messages.success(request, 'User not registered')
        else:
            user = User.objects.get(email=email)
            print (user.username)
            send_forget_password_email(request, user)
    

    return render(request, 'client/forgetpassword/enteremail.html')

def click_link(request,  uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        customer = UxClient.objects.get(user=user)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        return redirect ('change-password', pk=user.id)

    return render(request, 'client/forgetpassword/clicklink.html')

def change_password(request, pk):
    user = User.objects.get(id=pk)
    customer = UxClient.objects.get(user=user)
    if request.method == "POST":
        password = request.POST.get("newpassword")
        cpassword = request.POST.get("confirmpassword")

        if password == cpassword:
            customer.password = password
            user.set_password(password)
            user.save()
            customer.save()
            return redirect('client-login')
    return render(request, "client/forgetpassword/changepassword.html")

def delete_account(request, pk):
    customer = UxClient.objects.get(id=pk)
    user = User.objects.get(email=customer.email)
    logout(request)
    customer.delete()
    user.delete()
    messages.success(request, "Your account has been deleted")
    return redirect('client-login')

    
def rating(request, pk):
    video = UploadVideo.objects.get(id=pk)
    if request.method == 'POST':
        video.rating = request.POST.get('rating')
        video.save()
        messages.success(request, "Your rating has been submitted")
    return redirect('sentbytester')


def approvetests(request, pk):
    test = CreateTests.objects.get(id=pk)
     
    if request.method == 'POST':
        test.isApproved = True
        test.save()
        return redirect('admintests')