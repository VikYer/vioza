from django.http import JsonResponse
from .models import Subcategory


def subcategories_ajax(request, category_id):
    subs = Subcategory.objects.filter(category_id=category_id)

    data = {
        "subcategories": [
            {
                "title": sub.title,
                "slug": sub.slug
            }
            for sub in subs
        ]
    }

    return JsonResponse(data)
