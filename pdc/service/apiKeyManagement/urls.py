from django.urls import path, include
from . import api

urlpatterns = [
    path('createkey/', api.createKey, name='createkey'),
    path('deletekey/', api.deleteKey, name='deletekey'),
]
