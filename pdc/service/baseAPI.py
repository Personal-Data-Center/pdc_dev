from django.http import JsonResponse
from django.conf import settings

def getServiceInfo(request):
    icon = {
        'size4' : settings.MEDIA_URL + "serviceicon/size4.png",
        'size3' : settings.MEDIA_URL + "serviceicon/size3.png",
        'size2' : settings.MEDIA_URL + "serviceicon/size2.png",
        'size1' : settings.MEDIA_URL + "serviceicon/size1.png",
    }
    content = { 'Success' : 'True',
    'name' : settings.SERVICE_NAME,
    'version' : 'todo',
    'author' : 'todo',
    'description' : 'todo',
    'page' : 'todo',
    'contact' : 'todo',
    'icon' : icon,
    }
    return JsonResponse(content)
