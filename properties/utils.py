from django.core.cache import cache
from properties.models import Property

def get_all_properties():
    '''
    Retrieve all properties from Redis cache or db
    caches for 1 hour if not found in cache.
    '''
    try:
        properties = cache.get("all_properties")
        if properties is None:
            properties = list(Property.objects.all().values())
            cache.set("all_properties", properties, 3600)
        return properties, 200
    except Exception as e:
        return {"error": str(e)}, 500
