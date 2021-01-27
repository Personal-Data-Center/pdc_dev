from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from pdc.authorization.PDCUser import PDCUser
from pdc.service.apiKeyManagement.models import ServiceKey
from pdc.service.apiKeyManagement.models import GrantedKey
import json
import requests


def PDCAuth(get_response):

    def middleware(request):
        sessionCookie = request.COOKIES.get('authorizator_session', False)
        if sessionCookie:
                createUser(request, sessionCookie)
                response = get_response(request)
        else:
            response = loginOrAPIResponse(request)
        return response

    def loginOrAPIResponse(request):
        if "api" not in request.path:
            response = HttpResponseRedirect("/authorizator/login/?next=/" + settings.SERVICE_PATH)
        else:
            apiKey = request.GET.get('apiKey', False)
            if ServiceKey.objects.filter(apiKey=apiKey).exists():
                createAPIUser(request)
                response = get_response(request)
            else:
                content = {'error' : 'no permission', 'Success': False}
                response = JsonResponse(content)
        return response

    def createUser(request, sessionCookie):
        authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
        url = "http://authorizator/authorizator/api/getuser/?apiKey=" + authorizatorKey + "&"
        authorizatorResponse = requests.get(url+"sessionCookie="+sessionCookie+"&").text
        authorizatorJson = json.loads(authorizatorResponse)
        if (authorizatorJson["Success"]==True):
            request.user = PDCUser(
                username=authorizatorJson["username"],
                email=authorizatorJson["email"],
                admin=authorizatorJson["admin"],
                firstName=authorizatorJson["firstName"],
                lastName=authorizatorJson["lastName"],
                dateJoined=authorizatorJson["date_joined"],
                lastLogin=authorizatorJson["last_login"],
                profilePicSize4=authorizatorJson["profilePic"]["size4"],
                profilePicSize3=authorizatorJson["profilePic"]["size3"],
                profilePicSize2=authorizatorJson["profilePic"]["size2"],
                profilePicSize1=authorizatorJson["profilePic"]["size1"],
            )
            request.isApi = False
        else:
            response = loginOrAPIResponse(request)

    def createAPIUser(request):
        request.user = PDCUser(
            username='api',
            email='api@api.com',
            admin=False,
            firstName='api',
            lastName='api',
            dateJoined='api',
            lastLogin='api',
            profilePicSize4='/authorizator/media/profilePic/defaultProfile.svg',
            profilePicSize3='/authorizator/media/profilePic/defaultProfile.svg',
            profilePicSize2='/authorizator/media/profilePic/defaultProfile.svg',
            profilePicSize1='/authorizator/media/profilePic/defaultProfile.svg',
        )
        request.isApi = True

    return middleware
