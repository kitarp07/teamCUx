import imp
from django.shortcuts import render
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