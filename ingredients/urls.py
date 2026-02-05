from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_ingredients, name='manage_ingredients'),
    path('more/', views.create_ingredient_more, name='create_ingredient_more'),
    path('<int:ingredient_id>/details/', views.ingredient_detail, name='ingredient_detail'),
    path('<int:ingredient_id>/edit/', views.edit_ingredient, name='edit_ingredient'),
    path('<int:ingredient_id>/delete/', views.delete_ingredient, name='delete_ingredient'),
]

