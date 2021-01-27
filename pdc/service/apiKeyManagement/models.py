from django.db import models

# Create your models here.
class ServiceKey(models.Model):
    serviceName = models.CharField(max_length=30, unique=True)
    apiKey = models.CharField(max_length=67, unique=True)
    canGet = models.BooleanField(default=False)
    canPost = models.BooleanField(default=False)

class GrantedKey(models.Model):
    serviceName = models.CharField(max_length=30, unique=True)
    servicePath = models.CharField(max_length=50, unique=True)
    apiKey = models.CharField(max_length=67, unique=True)
