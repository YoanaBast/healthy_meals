from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.!

# def homepage(request):
#     return render(request, 'core/homepage.html')

# def how_it_works(request):
#     return render(request, 'core/how_it_works.html')

class HomepageView(TemplateView):
    template_name = 'core/homepage.html'

class HowItWorksView(TemplateView):
    template_name = 'core/how_it_works.html'