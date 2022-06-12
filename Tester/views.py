
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from Tester.forms import TesterForm, UploadVideoForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from client.models import CreateTests, UxClient
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from Tester.models import UploadVideo, UxTester
from django.contrib.auth.decorators import login_required
from testmyux.decoraters import tester_user_group

def send_activation_email(user,request):
    current_site=get_current_site(request)
    email_subject ='Activate your account'
    email_body= render_to_string('Tester/activate.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    customer=UxTester.objects.get(user=user.pk)
    email=EmailMessage(subject=email_subject,body=email_body,
                    from_email=settings.EMAIL_FROM_USER,
                    to=[customer.email]
    )
    
    email.send()
    





def tester_reg_view(request):
    form = TesterForm()
    if request.method == 'POST': 
        form = TesterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            cpw = request.POST.get('cpassword')
            
 
            if pw==cpw:
                user = User.objects.create_user(name, email, pw)
                group = Group.objects.get(name='tester')
                user.groups.add(group)
                user.save()
 
                client = form.save(commit=False) # save info but dont commit change to database
                client.user = user
                client.save()
                send_activation_email(user,request)
                return redirect('tlogin')
    context = {'form': form}

 
    return render(request, 'Tester/tregister.html', context)


def tlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')  

        user=authenticate(request,username=email,password=password)

        # if not user.is_email_verified:
        #     messages.add_message(request, messages.ERROR,
        #     'Email is not verified, please check your email inbox')
        #     return render(request, 'tester/login.html', context)

        if user is None:
            messages.success(request, "Wrong Credentials. Please try again")

        elif user.groups.all()[0].name == 'tester':
            login(request, user)
            return redirect('tester-dash')
           
        
            
        else:
            messages.success(request, "Wrong Credentials. Please try again")

        # tlogin(request,user)  
        # messages.add_message(request, messages.SUCCESS)  

   
    return render(request, 'Tester/login.html')   


def activate_user(request, uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
        customer=UxTester.objects.get(user=user)


    except Exception as e:  
        user=None 

    if user and generate_token.check_token(user,token):
        customer.is_email_verified=True
        customer.save()    

        messages.add_message(request,messages.SUCCESS,'eMAIL VERIFIED')   
        return redirect(reverse('tester-email-verified'))


    return render(request,'Tester/activate-failed.html',{"user":user})    


@login_required
def afterlogin_view(request):
    if request.user.is_superuser:
        return redirect('homepage')
    else:
        messages.error(request, "Invalid login credentials")
        return redirect('admin')    



def view_customer(request):
    users=UxTester.objects.all()
    return render(request,"adminpage/viewcustomer.html",{'users':users})   

    

def view_client(request):
    clients=UxClient.objects.all()
    return render(request,"adminpage/viewclient.html",{'clients':clients})

def tester_dashoard(request):
    return render(request, 'Tester/testerdash.html')    

def tester_email_verified(request):
    return render(request, "EmailVerified/EmailVerified.html")

def tester_upload_video(request):
    form = UploadVideoForm()
    if request.user.is_authenticated:
        customer = request.user.uxtester
        if request.method == 'POST':
            form = UploadVideoForm(request.POST)
            if form.is_valid():
                link = form.cleaned_data['video_link']

            form.save()
    else:
        return HttpResponse("You are not logged in.")

    return render(request, "Tester/uploadvideo.html")

def view_all_tests(request):
    tests = CreateTests.objects.all()
    context = {"tests": tests}
    return render(request, "Tester/inside-dash/all-tests.html", context)