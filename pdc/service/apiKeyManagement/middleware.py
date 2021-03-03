from django.http import JsonResponse
from . import models

def keyCheck(get_response):

    def middleware(request):
        apiKey = request.GET.get('apiKey', False)
        if request.isApi:
            if models.ServiceKey.objects.filter(apiKey=apiKey).exists():
                if request.method == 'POST':
                    if models.ServiceKey.objects.get(apiKey=apiKey).canPost:
                        response = get_response(request)
                    else:
                        content = {'Sucess': False, 'error' : 'no permission to POST'}
                        response = JsonResponse(content)
                if request.method == 'GET':
                    if models.ServiceKey.objects.get(apiKey=apiKey).canGet:
                        response = get_response(request)
                    else:
                        content = {'Sucess': False, 'error' : 'no permission to GET'}
                        response = JsonResponse(content)
            else:
                content = {'Sucess': False, 'error' : 'no permission'}
                response = JsonResponse(content)
        else:
            response = get_response(request)
        return response


    return middleware
