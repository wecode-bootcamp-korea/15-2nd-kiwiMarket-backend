import json, bcrypt, jwt, re, random

from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        try:
            if access_token == None:
                request.user = None
            else:
                payload = jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
                user = User.objects.get(id=payload['user_id'])
                request.user = user
            
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
        
        return func(self, request, *args, **kwargs)
    return wrapper
