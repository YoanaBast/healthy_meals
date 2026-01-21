from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_recipes, name='manage_recipes'),

]
