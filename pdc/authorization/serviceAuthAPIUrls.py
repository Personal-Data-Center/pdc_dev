from django.urls import path, include
from pdc.authorization import serviceAuthAPI

urlpatterns = [
    path('getuser/', serviceAuthAPI.getUser, name='getuser'),
    path('about/', serviceAuthAPI.about, name='about'),
]
