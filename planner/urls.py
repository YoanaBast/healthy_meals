from django.urls import path

from planner import views

urlpatterns = [
    path('', views.manage_fridge, name='manage_fridge'),
    path('edit/<int:item_id>/', views.edit_fridge_item, name='edit_fridge_item'),
    path('add/', views.add_fridge_item, name='add_fridge_item'),
    path('<int:fridge_id>/delete/', views.delete_fridge_item, name='delete_fridge_item')
]
