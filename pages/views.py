import imp
from django.shortcuts import redirect, render
from Tester.models import UxTester
from client.models import UxClient, CreateTests

# Create your views here.
def homepage(request):
    print(request)

    return render(request, 'homepage/Homepage.html')

def admintester(request):
    users = UxTester.objects.all()
    context ={'users': users}

    return render(request, 'adminpage/admintester.html', context)

def adminclient(request):

    users = UxClient.objects.all()
    context ={'users': users}

    return render(request, 'adminpage/adminclient.html', context)

def admintests(request):
    tests = CreateTests.objects.all()
    context ={'tests': tests}

    return render(request, 'adminpage/admintest.html', context)

def aboutus(request):
    return render(request, 'homepage/aboutus.html')

def contactus(request):
    return render(request, 'homepage/contactus.html')

def gotodashboard(request):
    try:
        if request.user.is_authenticated:
            if request.user.groups.all()[0].name == 'client':
                return redirect('client-dash')
            elif request.user.groups.all()[0].name == 'tester':
                return redirect('tester-dash')
    except:
            return redirect('admintests')
    else:
        return redirect('homepage')

def deleteTests(request, pk):
    test = CreateTests.objects.get(id=pk)   
    if request.method == 'POST':
        test.delete()
        return redirect('admintests')

def deleteTesters(request, pk):
    tester = UxTester.objects.get(id=pk)   
    if request.method == 'POST':
        tester.delete()
        return redirect('admintester')

def deleteClients(request, pk):
    uxclient = UxClient.objects.get(id=pk)   
    if request.method == 'POST':
        uxclient.delete()
        return redirect('adminclient')

