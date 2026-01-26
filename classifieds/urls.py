from django.urls import path

from .views import AdListView, CreateAd

app_name = 'classifieds'

urlpatterns = [
    path(
        'create/',
        CreateAd.as_view(),
        name='create_ad'
    ),
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
