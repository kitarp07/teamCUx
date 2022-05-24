from django.shortcuts import redirect, render
from client.forms import ClientForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


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

            if pw==cpw:
                user = User.objects.create_user(name, email, pw)
                user.save()

                client = form.save(commit=False) # save info but dont commit change to database
                client.user = user
                client.save()
                return redirect('client-login')
    context = {'form': form}

    return render(request, 'client/register.html', context)
    


def client_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        

        user = authenticate(request, username=email, password=passw)

        if user is None:
            messages.success(request, "Wrong Credentials. Please try again")
        if user is not None:
            login(request, user)
            return redirect('client-dash')


    return render(request, "client/login.html")

def client_dashoard(request):
    return render(request, 'client/clientdash.html')