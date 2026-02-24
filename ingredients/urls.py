from django.urls import path, include
from . import views

ajax_category_patterns = [
    path('', views.list_categories_ajax, name='list_categories_ajax'),
    path('add/', views.add_category_ajax, name='add_category_ajax'),
    path('<int:pk>/edit/', views.edit_category_ajax, name='edit_category_ajax'),
    path('<int:pk>/delete/', views.delete_category_ajax, name='delete_category_ajax'),
]


ajax_dietary_tag_patterns = [
    path('', views.list_dietary_tags_ajax, name='list_dietary_tags_ajax'),
    path('add/', views.add_dietary_tag_ajax, name='add_dietary_tag_ajax'),
    path('fragment/', views.dietary_tags_fragment, name='dietary_tags_fragment'),
    path('<int:pk>/edit/', views.edit_dietary_tag_ajax, name='edit_dietary_tag_ajax'),
    path('<int:pk>/delete/', views.delete_dietary_tag_ajax, name='delete_dietary_tag_ajax'),
]


ajax_unit_patterns = [
    path('add/', views.add_measurement_unit_ajax, name='add_measurement_unit_ajax'),
    path('', views.list_measurement_units_ajax, name='list_measurement_units_ajax'),
    path('<int:pk>/edit/', views.edit_measurement_unit_ajax, name='edit_measurement_unit_ajax'),
    path('<int:pk>/delete/', views.delete_measurement_unit_ajax, name='delete_measurement_unit_ajax'),
]


ajax_patterns = [
    path('category/', include(ajax_category_patterns)),
    path('dietary-tag/', include(ajax_dietary_tag_patterns)),
    path('unit/', include(ajax_unit_patterns)),
]


ingredient_unit_patterns = [
    path('add/', views.add_measurement_unit, name='add_measurement_unit'),
    path('<int:imu_id>/delete/', views.delete_measurement_unit, name='delete_measurement_unit'),
]


ingredient_detail_patterns = [
    path('', views.ingredient_detail, name='ingredient_detail'),
    path('edit/', views.edit_ingredient, name='edit_ingredient'),
    path('delete/', views.delete_ingredient, name='delete_ingredient'),
    path('unit/', include(ingredient_unit_patterns)),
    path('units/<int:imu_id>/edit/', views.edit_measurement_unit_conversion, name='edit_measurement_unit_conversion'),

]


urlpatterns = [
    path('', views.manage_ingredients, name='manage_ingredients'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('<int:ingredient_id>/', include(ingredient_detail_patterns)),
    path('ajax/', include(ajax_patterns)),
]