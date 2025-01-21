from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

class JSONAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json' and request.body:
            import json
            try:
                data = json.loads(request.body)
                if 'auth' in data:
                    token_key = data['auth'].get('token')
                    if token_key:
                        token = Token.objects.filter(key=token_key).first()
                        if token:
                            request.user = token.user
            except json.JSONDecodeError:
                pass
        return self.get_response(request)
