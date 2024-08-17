from django.shortcuts import render
from .models import Profile, Todo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django_filters.filters import OrderingFilter

from .serializers import UserSerializer, TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
import jwt, datetime, django_filters

class RegisterView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            profile=Profile(user=user, user_type=request.data.get("user_type"))
            profile.save()
            return Response({"message":"Signup successful", "user_detail":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"Invalid credential", "error":serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

class LoginView(APIView):
    def post(self, request):
        username=request.data.get("username")
        password=request.data.get("password")
        user=User.objects.filter(username=username).first()
        if not user:
            return Response({"message":"User not registered, Please signup"}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({"message":"Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)
        payload={
            "id":user.id,
            "exp":datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=120),
            "iat":datetime.datetime.now(datetime.UTC)
        }
        token=jwt.encode(payload, "secret", algorithm="HS256")

        response=Response()
        response.data={"message":"login successful", "token":token}
        response.status=status.HTTP_200_OK
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=False,
            samesite=None,
            secure=None
        )
        return response
    
class TodoView(APIView):

    def get(self, request):
        todos=Todo.objects.all()
        serializer=TodoSerializer(todos, many=True)
        return Response({"message":"All todos are here-", "data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        
        request.data["user"]=request.admin.id
        
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data['user'] = request.admin
            serializer.save()
            return Response({"message":"Todo Added"}, status=status.HTTP_201_CREATED)
        return Response({"message":"something went wrong", "detail":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        
        todoId=kwargs.get("pk")
        todo=Todo.objects.get(id=todoId)
        serializer=TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Todo updated", "detail":serializer.data}, status=status.HTTP_200_OK)
        return Response({"message":"Something went wrong", "detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        
        todoId=kwargs.get("pk")
        todo=Todo.objects.get(id=todoId)
        todo.delete()
        return Response({"message":"Todo deleted", "todo":TodoSerializer(todo).data}, status=status.HTTP_200_OK)
    
class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000

class TodoListView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'status']
    # ordering_fields =["created_at"]
    pagination_class=CustomPagination