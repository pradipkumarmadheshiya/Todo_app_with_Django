from django.urls import path
from .views import RegisterView, LoginView, TodoView

urlpatterns=[
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("todos/", TodoView.as_view(), name="todos"),
    path("todos/<int:pk>/", TodoView.as_view(), name="todos_edit_delete")
]