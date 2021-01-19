from django.db import models

class ServiceKey(models.Model):
    serviceName = models.CharField(max_length=30, unique=True)
    apiKey = models.CharField(max_length=67, unique=True)

class ProfilePic(models.Model):
    username = models.CharField(max_length=30, unique=True)
    profilePicSize4 = models.CharField(max_length=150, blank=False, default='/authorizator/media/profilePic/defaultProfile.svg')
    profilePicSize3 = models.CharField(max_length=150, blank=False, default='/authorizator/media/profilePic/defaultProfile.svg')
    profilePicSize2 = models.CharField(max_length=150, blank=False, default='/authorizator/media/profilePic/defaultProfile.svg')
    profilePicSize1 = models.CharField(max_length=150, blank=False, default='/authorizator/media/profilePic/defaultProfile.svg')
