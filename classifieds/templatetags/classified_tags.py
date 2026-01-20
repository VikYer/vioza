from django import template
from django.core.cache import cache

from ..models import Category

register = template.Library()


@register.inclusion_tag('classified/includes/_category_list.html')
def display_category_list():
    categories = cache.get('categories_with_subcategories')
    if not categories:
        categories = (
            Category.objects
            .prefetch_related('subcategories')
            .order_by('title')
        )
        cache.set('categories_with_subcategories', categories, 60 * 60 * 24 * 30)
    return {'categories': categories}
