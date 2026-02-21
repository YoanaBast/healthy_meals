from django.urls import path

from planner import views

urlpatterns = [
    path('', views.manage_fridge, name='manage_fridge'),
    path('edit/<int:item_id>/', views.edit_fridge_item, name='edit_fridge_item'),
    path('add/', views.add_fridge_item, name='add_fridge_item'),
    path('<int:fridge_id>/delete/', views.delete_fridge_item, name='delete_fridge_item'),
    path('suggestions/', views.get_meal_suggestions, name='meal_suggestions'),
    path('recipes/<int:id>/make/', views.make_recipe, name='make_recipe'),
    path('generate_grocery_list/', views.generate_grocery_list, name='generate_grocery_list'),
    path('grocery-list/', views.user_grocery_list, name='user_grocery_list'),
    path("grocery-list/delete/<int:item_id>/", views.delete_grocery_item, name="delete_grocery_item"),
    path("grocery-list/add-to-fridge/<int:item_id>/", views.add_grocery_to_fridge, name="add_grocery_to_fridge",),
    path("grocery-list/add-all-to-fridge/", views.add_all_grocery_to_fridge, name="add_all_grocery_to_fridge",),
]
