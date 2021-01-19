from django.urls import path, include
from . import api


urlpatterns = [
      path('createuser/', api.CreateUser.as_view(), name='createuser'),
      path('deleteuser/', api.DeleteUser.as_view(), name='deleteuser'),
      path('getuser/', api.GetUser.as_view(), name='getuser'),
      path('changeprofilepic/', api.ChangeProfilePic.as_view(), name='changeprofilepic'),
      path('deleteprofilepic/', api.DeleteProfilePic.as_view(), name='deleteprofilepic'),
      path('createservicekey/', api.CreateServiceKey.as_view(), name='createservicekey'),
      path('getservicekey/', api.GetServiceKey.as_view(), name='getservicekey'),
      path('removeservicekey/', api.RemoveServiceKey.as_view(), name='removeservicekey'),
 ]
