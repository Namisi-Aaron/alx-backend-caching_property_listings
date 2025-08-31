import logging
from django.core.cache import cache
from properties.models import Property

logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    '''
    Connects to Redis via django_redis.
    Get keyspace_hits and keyspace_misses from INFO.
    Calculate hit ratio (hits / (hits + misses)).
    Log metrics and return a dictionary.
    '''
    try:
        cache_info = cache.client.info()
        hits = cache_info.get("keyspace_hits", 0)
        misses = cache_info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0
        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": hit_ratio
        }
        logger.info("Redis cache metrics: %s", metrics)
        return metrics, 200
    
    except Exception as e:
        logger.error("Error retrieving Redis cache metrics: %s", e)
        return {"Details": str(e)}, 500
