from django.urls import path, include
from . import views


recipe_detail_patterns = [
    # path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),

    path('<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),

    # path('<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('<int:pk>/delete/', views.DeleteRecipeView.as_view(), name='delete_recipe'),

    path('<int:pk>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('<int:pk>/toggle_fav/', views.toggle_favourite, name='toggle_favourite'),
]

recipe_category_patterns = [
    path('add/', views.add_recipe_category_ajax, name='add_recipe_category_ajax'),
    path('list/', views.list_categories_ajax, name='list_recipe_categories_ajax'),
    path('<int:pk>/edit/', views.edit_category_ajax, name='edit_recipe_category_ajax'),
    path('<int:pk>/delete/', views.delete_category_ajax, name='delete_recipe_category_ajax'),
]

urlpatterns = [
    # path('', views.manage_recipes, name='manage_recipes'),
    path('', views.ManageRecipesView.as_view(), name='manage_recipes'),

    # path('add/', views.add_recipe, name='add_recipe'),
    path('add/', views.AddRecipeView.as_view(), name='add_recipe'),

    path('ajax/recipe-categories/', include(recipe_category_patterns)),
    path('', include(recipe_detail_patterns)),
]