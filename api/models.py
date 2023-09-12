from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Advocate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
