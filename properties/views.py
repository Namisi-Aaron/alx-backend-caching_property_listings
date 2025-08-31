from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from properties.models import Property

@cache_page(60 * 15)
def property_list(request):
    try:
        properties = Property.objects.all()
        return JsonResponse(data={"properties": list(properties.values())}, status=200)
    except Exception as e:
        return JsonResponse(data={"error": str(e)}, status=500)
