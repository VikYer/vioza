from django import template

from ..models import Category

register = template.Library()

@register.inclusion_tag('classified/includes/_category_list.html')
def display_category_list():
    categories = (
        Category.objects
        .prefetch_related('subcategories')
        .order_by('title')
    )
    return {'categories': categories}