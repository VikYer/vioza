from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Ad, Category, Subcategory
from .forms import AdAddForm, AdImageFormSet


class AdListView(ListView):
    model = Ad
    template_name = 'classified/ads_list.html'
    context_object_name = 'ads'
    paginate_by = 10

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.subcategory:
            context['title'] = f'{self.subcategory.title} in {self.category.title}'
        elif self.category:
            context['title'] = self.category.title
        else:
            context['title'] = 'All ads'

        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'classified/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        ad = self.object
        context['title'] = ad


class CreateAd(CreateView):
    model = Ad
    form_class = AdAddForm
    template_name = 'classified/create_ad_form.html'
    extra_context = {'title': 'Create Ad'}
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['images_formset'] = AdImageFormSet(
                self.request.POST,
                self.request.FILES
            )
        else:
            context['images_formset'] = AdImageFormSet()

        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        images_formset = context['images_formset']

        form.instance.author = self.request.user

        if images_formset.is_valid():
            self.object = form.save()

            images_formset.instance = self.object
            images = images_formset.save()

            main_index = self.request.POST.get('main_page')

            if main_index is not None:
                main_index = int(main_index)

                if 0 <= main_index < len(images):
                    self.object.main_page = images[main_index]
                    self.object.save(update_fields=['main_page'])

            return super().form_valid(form)

        return self.form_invalid(form)
