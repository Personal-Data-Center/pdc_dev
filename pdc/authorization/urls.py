from django.urls import path, include
from . import api


urlpatterns = [
      path('getuser/', api.getUser.as_view(), name='getuser'),
      path('isauthenticated/', api.isAuthenticated.as_view(), name='isauthenticated')
 ]
