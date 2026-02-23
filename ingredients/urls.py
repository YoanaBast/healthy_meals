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
#
# ingredient_detail_patterns = [
#     path('details/', views.ingredient_detail, name='ingredient_details'),
#     path('edit/', views.edit_ingredient, name='edit_ingredient'),
#     path('delete/', views.delete_ingredient, name='delete_ingredient'),
# ]
#
# urlpatterns = [
#     path('', views.manage_ingredients, name='manage_ingredients'),
#     path('add/', views.add_ingredient, name='add_ingredient'),
#     path('<int:ingredient_id>/', include(ingredient_detail_patterns)),
#     path('ajax/add-category/', views.add_category_ajax, name='add_category_ajax'),
#     path('ajax/add-dietary-tag/', views.add_dietary_tag_ajax, name='add_dietary_tag_ajax'),
#     path('ajax/add-measurement-unit/', views.add_measurement_unit_ajax, name='add_measurement_unit_ajax'),
#     path('<int:ingredient_id>/add-unit/', views.add_measurement_unit, name='add_measurement_unit'),
#     path('delete-unit/<int:imu_id>/', views.delete_measurement_unit, name='delete_measurement_unit'),
#     path("category/edit/<int:pk>/", views.edit_category_ajax, name="edit_category_ajax"),
#     path("category/delete/<int:pk>/", views.delete_category_ajax, name="delete_category_ajax"),
#     path("dietary_tag/edit/<int:pk>/", views.edit_dietary_tag_ajax, name="edit_dietary_tag_ajax"),
#     path("dietary_tag/delete/<int:pk>/", views.delete_dietary_tag_ajax, name="delete_dietary_tag_ajax"),
# ]

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
]

urlpatterns = [
    path('', views.manage_ingredients, name='manage_ingredients'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('<int:ingredient_id>/', include(ingredient_detail_patterns)),
    path('ajax/', include(ajax_patterns)),
path('<int:ingredient_id>/units/<int:imu_id>/edit/', views.edit_measurement_unit_conversion, name='edit_measurement_unit_conversion'),
]