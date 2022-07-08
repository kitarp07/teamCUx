
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from Tester.forms import FeedbackForm, TesterForm, UploadVideoForm, UserDeleteForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from client.models import CreateTests, UxClient
from Tester.utils import generatee_token
from django.core.mail import EmailMessage
from django.conf import settings
from Tester.models import FeedBack, UploadVideo, UxTester
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from testmyux.decoraters import tester_user_group


def send_activation_email_tester(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('Tester/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generatee_token.make_token(user)
    })
    customer = UxTester.objects.get(user=user.pk)
    email = EmailMessage(subject=email_subject, body=email_body,
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

            if User.objects.filter(username=name).exists() or User.objects.filter(email=email).exists():
                messages.success(request, "User already exists. Please choose different name and email")
            else:
                if name != "" and name !=  "" and name != "" and name != "":
                    if pw==cpw:
                        user = User.objects.create_user(name, email, pw)
                        
                        
                        try:   
                            group = Group.objects.get(name="tester")
                        except:
                            group = Group.objects.create(name="tester")
                            
                        user.groups.add(group)
                        user.save()
                        client = form.save(commit=False) # save info but dont commit change to database
                        client.user = user
                        client.save()
                        send_activation_email_tester(user,request)
                        messages.success(request, "Please check your email for email verification")
                        return redirect('tlogin')
                    else:
                        messages.success(request, "Passwords don't match")
                else:
                    messages.success(request, "Please fill all the fields")

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
            return redirect('testeralltests')
           
        else:
            messages.success(request, "Wrong Credentials. Please try again")

        # tlogin(request,user)  
        # messages.add_message(request, messages.SUCCESS)  

   
    return render(request, 'Tester/login.html')   


def send_activation_email(user,request):
    current_site=get_current_site(request)
    email_subject ='Activate your account'
    email_body= render_to_string('Tester/activate.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generatee_token.make_token(user)
    })
    customer=UxTester.objects.get(user=user.pk)
    email=EmailMessage(subject=email_subject,body=email_body,
                    from_email=settings.EMAIL_FROM_USER,
                    to=[customer.email]
    )
    
    email.send()

def activate_user(request, uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
        customer=UxTester.objects.get(user=user)


    except Exception as e:  
        user=None 

    if user and generatee_token.check_token(user,token):
        customer.is_email_verified=True
        customer.save()    

        messages.add_message(request,messages.SUCCESS,'eMAIL VERIFIED')   
        return redirect('tester-email-verified')


    return render(request,'Tester/activate-failed.html',{"user":user})    



def afterlogin_view(request):
    if request.user.is_superuser:
        return redirect('admintests')
    else:
        messages.error(request, "Invalid login credentials")
        return redirect('admin')  


# @login_required (login_required='admin')
def admin_dashoard(request):
    return render(request, 'adminpage/viewcustomer.html')    


def view_customer(request):
    users=UxTester.objects.all()
    return render(request,"adminpage/viewcustomer.html",{'users':users})    

def view_client(request):
    clients=UxClient.objects.all()
    return render(request,"adminpage/viewclient.html",{'clients':clients})


def tester_dashboard(request):
    tester= request.user.uxtester
    context={
        'tester':tester
    }
    return render(request, 'Tester/testerdash.html',context)    

 

def testerprofile(request):
    
    user=request.user
    if user is not None:
        if user.groups.all()[0].name == 'tester':
             
            customer = request.user.uxtester

            videos = UploadVideo.objects.filter( tester = customer.id)

            context ={
                 'customer':customer,
                 'videos': videos
             }
            return render(request,'Tester/tester-profile.html',context)


    
    else:
        messages.success(request, "Wrong Credentials. Please try again")
        return redirect('tlogin')
    


def edit_profile(request,pk):
    user =UxTester.objects.get(id=pk)
    userForm= TesterForm(instance=user)
    if request.method=='POST':
        userForm=TesterForm(request.POST,request.FILES, instance=user)
        if userForm.is_valid():
            userForm.save()
            
            return redirect('/')
    return render(request,'Tester/tester-edit-profile.html',{
        'userForm': userForm,
        'user':user
    })
    return render(request, 'Tester/testerdash.html')   


def tester_email_verified(request):
    return render(request, "EmailVerified/EmailVerified.html")


    
@login_required(login_url='tlogin')
def tester_upload_video(request):
    form = UploadVideoForm()
    if request.user.is_authenticated:
        customer = request.user.uxtester
        tests = CreateTests.objects.all()
        if request.method == 'POST':
            form = UploadVideoForm(request.POST)
            if form.is_valid():
                link = form.cleaned_data['video_link']
                test = form.cleaned_data['test']
                
                client = test.created_by
                tester = request.user.uxtester

                video = UploadVideo.objects.create(
                    video_link = link,
                    client = client, 
                    test = test, 
                    tester= tester,
                    paymentreceived =2,
                    )

            
        
        context = {
            'tests': tests
        }
    else:
        context = {
            
        }
        return HttpResponse("You are not logged in.")

       

    return render(request, "Tester/uploadvideo.html", context)

def view_all_tests(request):
    tests = CreateTests.objects.all()
    context = {"tests": tests}
    return render(request, "Tester/inside-dash/all-tests.html", context)

def send_forget_password_email_tester(request, user):
    subject = "Reset password link"
    if request.method == "POST":
        email = request.POST.get('email')
    current_site = get_current_site(request)
    email_body = render_to_string('Tester/forgetpassword/clicklink.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generatee_token.make_token(user),

    })
    email = EmailMessage(subject=subject, 
    body=email_body, 
    from_email= settings.EMAIL_FROM_USER,
    to=[user.email]
    )

    email.send()


# forget password
def tester_enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email):
            messages.success(request, 'User not registered')
        else:
            user = User.objects.get(email=email)
            print (user.username)
            send_forget_password_email_tester(request, user)
    

    return render(request, 'Tester/forgetpassword/enteremail.html')

def tester_click_link(request,  uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        customer = UxTester.objects.get(user=user)
    except Exception as e:
        user = None
    if user and generatee_token.check_token(user, token):
        return redirect ('change-password', pk=user.id)

    return render(request, 'Tester/forgetpassword/clicklink.html')

def tester_change_password(request, pk):
    user = User.objects.get(id=pk)
    customer = UxTester.objects.get(user=user)
    if request.method == "POST":
        password = request.POST.get("newpassword")
        cpassword = request.POST.get("confirmpassword")

        if password == cpassword:
            customer.password = password
            user.set_password(password)
            user.save()
            customer.save()
            return redirect('tlogin')
    return render(request, "Tester/forgetpassword/changepassword.html")
    
# @login_required
# def deleteuser(request):
#     if request.method=='POST':
#         delete_form= UserDeleteForm(request.POST, instance=request.user)
#         user=request.user
#         user.delete()
#         messages.info(request,'your account has been deleted.')
#         return redirect('homepage')

#     else:
#         delete_form =UserDeleteForm(instance=request.user)

#     context={
#         'delete_form': delete_form
#     }   
#     return render(request,'Tester/delete_account.html',context)     

@login_required
def delete_tester(request,pk):
    user=UxTester.objects.get(id=pk)
    user.delete()
    return redirect('homepage')  
     
def send_feedbackform(request):
    print(request.user.id)
    user = request.user
    if request.method=='POST':

        form=FeedbackForm(request.POST)
        
        if form.is_valid():
            feedback=form.cleaned_data['feedback']
            
            
            form.save()
        return render(request,'client/sendfeedback.html')
    else:
        form=FeedbackForm()    
    context={'form':form}
    return render(request, 'client/sendfeedback.html',context)


def tlogout(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'Sucessfully logged out') 
    return redirect('tlogin')
        


def logout_admin(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'Sucessfully logged out') 

    return redirect ('tlogin')

