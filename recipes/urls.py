from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_recipes, name='manage_recipes'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path("<int:id>/toggle_fav/", views.toggle_favourite, name="toggle_favourite"),
    path('<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('ajax/add-recipe-category/', views.add_recipe_category_ajax, name='add_recipe_category_ajax'),


]
