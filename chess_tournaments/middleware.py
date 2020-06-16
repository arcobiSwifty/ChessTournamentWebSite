from django.conf import settings
from django.shortcuts import redirect

from user.models import Player 

EXEMPT_URLS = [settings.LOGIN_URL]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += settings.LOGIN_EXEMPT_URLS

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        if not request.user.is_authenticated:
            path = request.path_info
            if path not in EXEMPT_URLS:
                return redirect(settings.LOGIN_URL)
        return None