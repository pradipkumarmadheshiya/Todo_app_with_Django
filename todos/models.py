from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLE=(
        ("reader", "Reader"),
        ("admin", "Admin")
    )
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_type=models.CharField(max_length=10, choices=USER_ROLE, default="reader")

    def __str__(self):
        return f"{self.user.username}-{self.user_type}"
    
class Todo(models.Model):
    name=models.CharField(max_length=50)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return f"{self.name}-{self.user}"