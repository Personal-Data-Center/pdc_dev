#todo create and delete api keys (only if has auth to input granted key), add and remove granted keys(only if has auth to input granted key)
from django.http import JsonResponse
from django.conf import settings
import secrets
from . import models


# key management
def createKey(request):
    serviceName = request.GET.get('serviceName')
    canGet = request.GET.get('canGet', False)
    canPost = request.GET.get('canPost', False)
    if request.method == 'POST':
        try:
            generatedKey = secrets.token_urlsafe(50)
            newKeyModel = models.ServiceKey(serviceName=serviceName, canGet=canGet, canPost=canPost, apiKey=generatedKey)
            newKeyModel.save()
            content = {'Success' : True, 'key' : generatedKey}
        except Exception as e:
            content = {'Success' : False, 'Error' : str(e)}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def deleteKey(request):
    serviceName = request.GET.get('serviceName', False)
    if request.method == 'POST':
        try:
            serviceKey = models.ServiceKey.objects.get(serviceName=serviceName)
            serviceKey.delete()
            content = {'Success' : True}
        except Exception as e:
            content = {'Success' : False, 'Error' : str(e)}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

# granted key management

def addGrantedKey(request):
    grantedApiKey = request.GET.get('grantedApiKey', False)
    serviceName = request.GET.get('serviceName', False)
    servicePath = request.GET.get('servicePath', False)
    if request.method == 'POST':
        try:
            grantedKey = models.GrantedKey.objects(apiKey=grantedApiKey, servicePath=servicePath, serviceName=serviceName)
            grantedKey.save()
            content = {'Success' : True}
        except Exception as e:
            content = {'Success' : False, 'Error' : str(e)}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def deleteGrantedKey(request):
    serviceName = request.GET.get('serviceName', False)
    if request.method == 'POST':
        try:
            grantedKey = models.GrantedKey.objects.get(serviceName=serviceName)
            grantedKey.delete()
            content = {'Success' : True}
        except Exception as e:
            content = {'Success' : False, 'Error' : str(e)}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)
