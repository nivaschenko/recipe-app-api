import os

from django.core.cache import cache
from rest_framework.request import Request
from rest_framework.response import Response


def create_cache_key(request: Request, is_public: bool = False) -> str:
    """
    Generate key for cashing API requests.
    :param request:
    :param is_public:
    :return:
    """
    path = request.path
    params = request.query_params.dict()
    params_str = "&".join(f"{key}={value}" for key, value in params.items())

    if is_public:
        cache_key = f"_path:{path}_params:{params_str}"
    else:
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        cache_key = f"_user:{user_id}_path:{path}_params:{params_str}"

    return cache_key


def custom_cache(timeout=None, is_public: bool | None = False):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):

            key = create_cache_key(request, is_public=is_public)
            cached_data = cache.get(key)

            if cached_data is not None:
                return Response(cached_data)

            response = func(self, request, *args, **kwargs)

            if timeout is not None:
                cache.set(key, response.data, timeout)
            else:
                env_timeout = os.environ.get("DJANGO_CACHE_TIMEOUT", 3600)
                print(env_timeout)
                cache.set(key, response.data, timeout=env_timeout)

            return response
        return wrapper
    return decorator


def delete_cache(is_public: bool | None = False):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            key = create_cache_key(self.request, is_public = is_public)
            cache.delete(key)

            return func(self, *args, **kwargs)
        return wrapper
    return decorator
