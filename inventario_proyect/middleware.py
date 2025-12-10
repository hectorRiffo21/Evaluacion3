from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:
    """
    Middleware que fuerza a TODAS las respuestas a no guardarse en caché.
    Evita que el navegador muestre páginas protegidas al presionar 'Atrás'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response
