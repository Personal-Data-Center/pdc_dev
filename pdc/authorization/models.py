from django.db import models

class ServiceKey(models.Model):
    serviceName = models.CharField(max_length=30, unique=True)
    apiKey = models.CharField(max_length=67, unique=True)
