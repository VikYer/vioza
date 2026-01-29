from django.urls import path
from django.views.decorators.cache import cache_page

from .views_ajax import subcategories_ajax, cities_ajax

app_name = 'ajax'

urlpatterns = [
    path(
        'subcategories/<int:category_id>/',
         cache_page(60 * 60)(subcategories_ajax),
         name='subcategories_ajax'
    ),
    path(
        'cities/<int:region_id>/',
        cache_page(60 * 60)(cities_ajax),
        name='cities_ajax'
    ),
]
