from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    alternate_phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=6, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['user']
        verbose_name = 'user'
        verbose_name_plural = 'Profile'


class Employee(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    alt_mobile = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100, null=True)
    code = models.CharField(max_length=7)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
