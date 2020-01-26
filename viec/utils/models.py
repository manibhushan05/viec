from datetime import datetime

from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70)
    short_name = models.CharField(max_length=10, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dial_code = models.CharField(max_length=10,null=True)
    code = models.CharField(max_length=3, null=True, unique=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.deleted_on = datetime.now()
        super(Country, self).save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Countries'


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


# class City(models.Model):
#     name = models.CharField(max_length=100)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     deleted = models.BooleanField(default=False)
#     deleted_on = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name


class Address(models.Model):
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    pin = models.CharField(max_length=10, null=True)
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
