from django.urls import path
from .views_ajax import subcategories_ajax

app_name= 'ajax'

urlpatterns = [
    path("subcategories/<int:category_id>/", subcategories_ajax, name="subcategories_ajax"),
]

