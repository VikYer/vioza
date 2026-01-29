from django.http import JsonResponse
from .models import Subcategory, City


def subcategories_ajax(request, category_id):
    subs = Subcategory.objects.filter(category_id=category_id).order_by('title')

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

def cities_ajax(request, region_id):
    cities = City.objects.filter(region_id=region_id)

    data = {
        "cities": [
            {
                "id": city.id,
                "name": city.name,
            }
            for city in cities
        ]
    }

    return JsonResponse(data)
