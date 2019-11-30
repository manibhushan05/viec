from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    alt_mobile = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100, null=True)
    code = models.CharField(max_length=7)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='employee_deleted_by')
