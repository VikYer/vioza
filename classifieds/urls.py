from django.urls import path

from .views import AdListView, CreateAd, AdDetailView

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
    path(
        '<slug:ad_slug>-<int:ad_id>/',
        AdDetailView.as_view(),
        name='ad_detail'
    )
]
