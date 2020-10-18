from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login.as_view(), name='cas_ng_login'),
]

