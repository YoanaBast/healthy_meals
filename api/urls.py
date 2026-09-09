from django.urls import path
from . import views

urlpatterns = [
    # Ingredients
    path('ingredients/', views.ListCreateIngredientApiView.as_view(), name='api_ingredients_list_create'),
    path('ingredients/<int:pk>/', views.RetrieveUpdateDestroyIngredientApiView.as_view(), name='api_ingredients_detail'),
    path('ingredients/<int:pk>/units/', views.AddIngredientMeasurementUnitApiView.as_view(), name='api_ingredients_add_unit'),
    path('ingredients/<int:pk>/units/<int:unit_id>/', views.DeleteIngredientMeasurementUnitApiView.as_view(), name='api_ingredients_delete_unit'),

    # Ingredient categories
    path('ingredient-categories/', views.ListCreateIngredientCategoryApiView.as_view(), name='api_ingredient_categories_list_create'),
    path('ingredient-categories/<int:pk>/', views.RetrieveUpdateDestroyIngredientCategoryApiView.as_view(), name='api_ingredient_categories_detail'),

    # Dietary tags
    path('dietary-tags/', views.ListCreateIngredientDietaryTagApiView.as_view(), name='api_dietary_tags_list_create'),
    path('dietary-tags/<int:pk>/', views.RetrieveUpdateDestroyIngredientDietaryTagApiView.as_view(), name='api_dietary_tags_detail'),

    # Measurement units (global catalog)
    path('units/', views.ListCreateMeasurementUnitApiView.as_view(), name='api_units_list_create'),
    path('units/<int:pk>/', views.RetrieveUpdateDestroyMeasurementUnitApiView.as_view(), name='api_units_detail'),

    # Recipes
    path('recipes/', views.ListCreateRecipeApiView.as_view(), name='api_recipes_list_create'),
    path('recipes/<int:pk>/', views.RetrieveUpdateDestroyRecipeApiView.as_view(), name='api_recipes_detail'),

    # Recipe categories
    path('recipe-categories/', views.ListCreateRecipeCategoryApiView.as_view(), name='api_recipe_categories_list_create'),
    path('recipe-categories/<int:pk>/', views.RetrieveUpdateDestroyRecipeCategoryApiView.as_view(), name='api_recipe_categories_detail'),
]