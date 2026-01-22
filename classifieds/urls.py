from django.urls import path

from .views import AdListView

app_name = 'classifieds'

urlpatterns = [
    path(
        '<slug:category_slug>/',
        AdListView.as_view(),
        name='ads_by_category'
    ),
    path(
        '<slug:category_slug>/<slug:subcategory_slug>/',
        AdListView.as_view(),
        name='ads_by_subcategory'
    ),
]