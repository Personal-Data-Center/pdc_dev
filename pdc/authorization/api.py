from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings
from secrets import token_urlsafe
from pdc.authorization import models


# TODO: require service api key, return the correct user info if user exists
class getUser(APIView):

    def get(self, request):
        token = request.GET.get('token', False)
        try:
            session = Session.objects.get(session_key=token)
            session_data = session.get_decoded()
            user = User.objects.get(id=session_data["_auth_user_id"])
            content = {'username': user.username, 'email': user.email, 'admin' : user.is_superuser}
        except Exception as e:
            content = {'user': 'None'}
        return Response(content)

# TODO: block brute force attacks
class CreateServiceKey(APIView):

    def post(self, request):
        systemKey = request.GET.get('systemKey', False)
        serviceID = request.GET.get('serviceID', False)
        content = serviceID
        if (systemKey == settings.SYSTEM_API_KEY):
            if serviceID :
                try:
                    apiKey = token_urlsafe(50)
                    dbKey = models.ServiceKey(serviceName = serviceID, apiKey = apiKey)
                    dbKey.save()
                    content = { 'apiKey': apiKey, 'Success': 'True'}
                except Exception as e:
                    content = {'error' : str(e), 'Success': 'False'}
            else:
                content = {'error' : 'serviceId invalid', 'Success': 'False'}
        else:
            content = {'error' : 'systemKey invalid', 'Success': 'False'}
        return Response(content)

# TODO: block brute force attacks
class GetServiceKey(APIView):

    def get(self, request):
        systemKey = request.GET.get('systemKey', False)
        serviceID = request.GET.get('serviceID', False)
        content = serviceID
        if (systemKey == settings.SYSTEM_API_KEY):
            if serviceID :
                try:
                    apiKey = models.ServiceKey.objects.get(serviceName=serviceID)
                    content = { 'apiKey': apiKey.apiKey, 'Success': 'True'}
                except Exception as e:
                    content = {'error' : str(e), 'Success': 'False'}
            else:
                content = {'error' : 'serviceId invalid', 'Success': 'False'}
        else:
            content = {'error' : 'systemKey invalid', 'Success': 'False'}
        return Response(content)



# TODO: block brute force attacks
class RemoveServiceKey(APIView):

    def post(self, request):
        systemKey = request.GET.get('systemKey', False)
        serviceID = request.GET.get('serviceID', False)
        content = serviceID
        if (systemKey == settings.SYSTEM_API_KEY):
            if serviceID :
                try:
                    apiKey = models.ServiceKey.objects.get(serviceName = serviceID)
                    apiKey.delete()
                    content = { 'Success': 'True'}
                except Exception as e:
                    content = {'error' : str(e), 'Success': 'False'}
            else:
                content = {'error' : 'serviceId invalid', 'Success': 'False'}
        else:
            content = {'error' : 'systemKey invalid', 'Success': 'False'}
        return Response(content)
