from multiprocessing import context
from django.shortcuts import render
from client.forms import ClientForm
from django.contrib.auth.models import User
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
    context = {'form': form}

    return render(request, 'client/register.html', context)
    



