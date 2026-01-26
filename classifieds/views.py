from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView

from .models import Ad, Category, Subcategory
from .forms import AdAddForm


class AdListView(ListView):
    model = Ad
    template_name = 'classified/ads_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        queryset = Ad.published.select_related('category', 'subcategory')

        self.category = None
        self.subcategory = None

        category_slug = self.kwargs.get('category_slug')
        subcategory_slug = self.kwargs.get('subcategory_slug')

        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)

        if subcategory_slug:
            self.subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
            queryset = queryset.filter(subcategory=self.subcategory)

        return queryset.order_by('-publish')


class CreateAd(CreateView):
    form_class = AdAddForm
    template_name = 'classified/create_ad_form.html'
    extra_context = {'title': 'Create Ad'}
