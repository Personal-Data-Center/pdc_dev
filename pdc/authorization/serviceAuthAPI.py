from django.http import JsonResponse

def GetUser(request):
        if request.method == 'GET':
            profile = { "size4": request.user.profilePicSize4,
            "size3": request.user.profilePicSize3,
            "size2": request.user.profilePicSize2,
            "size1": request.user.profilePicSize1}
            content = {'Success': 'True',
            'username': request.user.username,
            'email': request.user.email,
            'admin' : request.user.admin,
            'firstName' : request.user.firstName,
            'lastName' : request.user.lastName,
            'last_login' : request.user.lastLogin,
            'date_joined' : request.user.dateJoined,
            'profilePic' : profile}
        else:
            content = {'error': 'only GET allowed', 'Success': 'Fase'}
        return JsonResponse(content)
