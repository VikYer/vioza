from django.urls import path
from django.views.decorators.cache import cache_page

from .views_ajax import subcategories_ajax

app_name = 'ajax'

urlpatterns = [
    path("subcategories/<int:category_id>/", cache_page(60 * 60 * 24 * 30)(subcategories_ajax),
         name="subcategories_ajax"),
]
