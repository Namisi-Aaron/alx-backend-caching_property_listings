from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    '''
    Retrieves a list of all properties
    '''
    try:
        properties, status = get_all_properties()
        return JsonResponse({"data": properties}, status=status)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
