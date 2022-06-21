from django.shortcuts import render

# Create your views here.
def homepage(request):
    print(request)

    return render(request, 'homepage/Homepage.html')