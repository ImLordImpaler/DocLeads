# myapp/middleware.py

from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.http import JsonResponse

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Check for Authorization header
            print(request.path)
            if request.path in ['/accounts/register','/accounts/login'] or request.path.startswith('/admin/'): 
                pass
            else:
                auth_header = request.headers.get('Authorization')
                if auth_header:
                    token_prefix = 'Bearer '
                    if auth_header.startswith(token_prefix):
                        token_key = auth_header.split(" ")[-1]
                        # token_key = auth_header[len(token_prefix):]  # Extract the token part
                        try:
                            token = Token.objects.get(key=token_key)
                            user = token.user  # Get the associated user
                            request.user_id = user  # Attach the user to the request
                        except Token.DoesNotExist:
                            raise AuthenticationFailed('Invalid token')
                    else:
                        raise AuthenticationFailed('Authorization header must start with Bearer')
                else:
                    raise AuthenticationFailed('Authorization header is missing')
            
            response = self.get_response(request)
            return response
        
        except AuthenticationFailed as E:
            return JsonResponse({'error':str(E)}, status=401)
