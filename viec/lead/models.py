from django.contrib.auth.models import User
from django.db import models

from utils.models import Address, Country


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
    TYPE_OF_LEAD_CHOICES = (
        ('C', 'Cold'),
        ('W', 'Warm'),
        ('H', 'Hot')
    )
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, null=True)
    mobile = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    recommended_by = models.CharField(max_length=2, choices=RECOMMENDED_BY_CHOICES, null=True)
    visa_type = models.CharField(max_length=2, choices=VISA_TYPE_CHOICES, null=True)
    country_interested = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    type_of_lead = models.CharField(max_length=1, choices=TYPE_OF_LEAD_CHOICES, null=True)
    month_intake = models.DateField(null=True)
    remarks = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
