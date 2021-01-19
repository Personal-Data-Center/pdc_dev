from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from pdc.authorization.PDCUser import PDCUser
import json
import requests


def PDCAuth(get_response):

    def middleware(request):
        sessionCookie = request.COOKIES.get('authorizator_session', False)
        if sessionCookie:
            url = "http://authorizator/authorizator/api/getuser/?apiKey=" + settings.AUTHORIZATOR_API_KEY + "&"
            authorizatorResponse = requests.get(url+"sessionCookie="+sessionCookie+"&").text
            authorizatorJson = json.loads(authorizatorResponse)
            if (authorizatorJson["Success"]=="True"):
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
                response = get_response(request)
            else:
                response = loginOrAPIResponse(request)
        else:
            response = loginOrAPIResponse(request)
        return response

    def loginOrAPIResponse(request):
        if "api" not in request.path:
            response = HttpResponseRedirect("/authorizator/login/?next=/" + settings.SERVICE_PATH)
        else:
            content = {'error' : 'not logged in', 'Success': 'False'}
            response = JsonResponse(content)
        return response

    return middleware
