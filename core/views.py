from django.shortcuts import render

# Create your views here.!

def homepage(request):
    return render(request, 'core/homepage.html')

def how_it_works(request):
    return render(request, 'core/how_it_works.html')