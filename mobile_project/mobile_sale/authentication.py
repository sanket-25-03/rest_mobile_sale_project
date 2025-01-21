from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class JSONAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.method not in ('POST', 'PUT', 'DELETE'):  # Skip GET requests
            auth_data = request.data.get("auth")
            if not auth_data:
                raise AuthenticationFailed("Authentication credentials were not provided.")
            
            username = auth_data.get("username")
            token = auth_data.get("token")

            if not username or not token:
                raise AuthenticationFailed("Both username and token are required.")

            try:
                user = User.objects.get(username=username)
                user_token = Token.objects.get(user=user)

                if user_token.key != token:
                    raise AuthenticationFailed("Invalid token.")

                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed("User not found.")
            except Token.DoesNotExist:
                raise AuthenticationFailed("Token not found.")

        return None
