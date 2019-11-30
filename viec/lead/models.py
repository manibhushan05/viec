from django.contrib.auth.models import User
from django.db import models

from utils.models import City


class Lead(models.Model):
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    RECOMMENDED_BY_CHOICES = (
        ('FR', "Friend"),
        ('PS', 'Previous Student'),
        ('WI', 'Walk-In'),
        ('SA', 'Sub Agent'),
        ('OB', 'Other Branch'),
    )
    VISA_TYPE_CHOICES = (
        ('SV', 'STUDENT VISA'),
        ('TV', 'TOURIST VISA')
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100, null=True)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    recommended_by = models.CharField(max_length=2, choices=RECOMMENDED_BY_CHOICES)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='leads_deleted_by')
