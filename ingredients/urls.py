from django.urls import path, include
from . import views

# urlpatterns = [
#     path('', views.manage_ingredients, name='manage_ingredients'),
#     path('more/', views.create_ingredient_more, name='create_ingredient_more'),
#     path('ingredients/add-popup/', views.add_ingredient_popup, name='add_ingredient_popup'),
#     path('<int:ingredient_id>delete/', views.delete_ingredient, name='delete_ingredient'),
#     path('<int:ingredient_id>/details/', views.ingredient_detail, name='ingredient_detail'),
#     path('<int:ingredient_id>/edit/', views.edit_ingredient, name='edit_ingredient'),
#     path('<int:ingredient_id>/delete/', views.delete_ingredient, name='delete_ingredient'),
#     path('<int:ingredient_id>/edit-popup/', views.edit_ingredient_popup, name='edit_ingredient_popup'),
#
# ]

ingredient_detail_patterns = [
    path('details/', views.ingredient_detail, name='ingredient_details'),
    path('edit/', views.edit_ingredient, name='edit_ingredient'),
    path('delete/', views.delete_ingredient, name='delete_ingredient'),
]

urlpatterns = [
    path('', views.manage_ingredients, name='manage_ingredients'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('<int:ingredient_id>/', include(ingredient_detail_patterns)),
]
