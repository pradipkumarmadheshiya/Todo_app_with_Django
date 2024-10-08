from django.urls import reverse, path
from django.http import JsonResponse
from .models import Profile
from rest_framework.response import Response
from rest_framework import status
import jwt

class JWTAuthmiddleware:

    def __init__(self, get_response):
        self.get_response=get_response
        self.excluded_paths=[reverse("register"), reverse("login"), reverse("resetPassword")]

    def __call__(self, request):
        # if request.path in self.excluded_paths or request.path.startswith("/admin/") or request.path.startswith("/todos/"):
        if any(request.path.startswith(path) for path in self.excluded_paths) or request.path.startswith("/admin/") or request.path.startswith("/todos/"):
            return self.get_response(request)

        token = request.COOKIES.get("jwt")
        payload=jwt.decode(token, "secret", algorithms=["HS256"])
        profile=Profile.objects.filter(user=payload["id"]).first()
        
        if profile.user_type!="admin" and request.method!="GET":
            # return Response({"message":"Unauthorised"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return JsonResponse({"message": "Unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)
                 
        request.admin=profile

        return self.get_response(request)