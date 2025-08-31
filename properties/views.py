from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from properties.models import Property

@cache_page(60 * 15)
def property_list(request):
    try:
        properties = Property.objects.all()
        return JsonResponse({"properties": list(properties.values())})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
