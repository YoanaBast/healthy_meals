from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_recipes, name='manage_recipes'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),  # view single recipe
    path('add/', views.add_recipe, name='add_recipe'),
    path('<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),  # edit recipe
    path('<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),  # optional delete view
    path("<int:id>/toggle_fav/", views.toggle_favourite, name="toggle_favourite")

]
