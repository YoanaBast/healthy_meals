from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_ingredients, name='manage_ingredients'),
    path('more/', views.create_ingredient_more, name='create_ingredient_more'),

]
