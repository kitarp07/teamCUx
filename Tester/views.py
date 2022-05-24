from django.shortcuts import redirect, render
from Tester.forms import TesterForm
from django.contrib.auth.models import User

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
                return redirect('/homepage')
    context = {'form': form}
 
    return render(request, 'tester/tregister.html', context)