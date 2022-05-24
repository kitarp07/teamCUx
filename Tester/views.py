from django.shortcuts import redirect, render
from Tester.forms import TesterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
                user.save()
 
                client = form.save(commit=False) # save info but dont commit change to database
                client.user = user
                client.save()
    context = {'form': form}
 
    return render(request, 'tester/tregister.html', context)

def tlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')  

        user=authenticate(request,email=email,password=password)

        if user is not None:
            tlogin(request,email)
            print('email')
        return redirect('tester-dash')

    else:
        return render(request, 'tester/login.html')   

def tester_dashoard(request):
    return render(request, 'Tester/testerdash.html')