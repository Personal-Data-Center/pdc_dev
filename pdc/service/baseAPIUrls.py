from django.urls import path, include
from pdc.authorization import serviceAuthAPI
from . import baseAPI

urlpatterns = [
    path('getserviceinfo/', baseAPI.getServiceInfo, name='getserviceinfo'),
]
