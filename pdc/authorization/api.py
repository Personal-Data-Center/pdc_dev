from PIL import Image, ImageOps
from secrets import token_urlsafe
import os

from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from pdc.authorization import models

# TODO: require service api key, return the correct user info if user exists
class GetUser(APIView):

    def get(self, request):
        apiKey = request.GET.get('apiKey', False)
        sessionCookie = request.GET.get('sessionCookie', False)
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                session = Session.objects.get(session_key=sessionCookie)
                session_data = session.get_decoded()
                user = User.objects.get(id=session_data["_auth_user_id"])
                profilePic = models.ProfilePic.objects.get(username=user.username)
                profile = { "size4": profilePic.profilePicSize4,
                "size3": profilePic.profilePicSize3,
                "size2": profilePic.profilePicSize2,
                "size1": profilePic.profilePicSize1}
                content = {'Success': True,
                'username': user.username,
                'email': user.email,
                'admin' : user.is_superuser,
                'firstName' : user.first_name,
                'lastName' : user.last_name,
                'last_login' : user.last_login,
                'date_joined' : user.date_joined,
                'lastName' : user.last_name,
                'profilePic' : profile}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'bad apiKey', 'Success': False}
        return Response(content)

class CreateUser(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey', False)
        username = request.GET.get('username', False)
        password = request.GET.get('password', False)
        admin = request.GET.get('admin', False)
        email = request.GET.get('email', False)
        firstName = request.GET.get('firstName', False)
        lastName = request.GET.get('lastName', False)
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                #1 delete user on db
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
                if admin == "True":
                    user.is_superuser = True
                    user.is_staff = True
                user.save()
                try:
                    profilePic = models.ProfilePic(username=username)
                    profilePic.save()
                    content = {'Success': True}
                except Exception as e:
                    user = User.objects.get(username=username)
                    user.delete()
                    content = {'error' : str(e), 'Success': False}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)

class DeleteUser(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey', False)
        username = request.GET.get('username', False)
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                #1 delete user on db
                user = User.objects.get(username=username)
                user.delete()
                #2 delete profilePic
                ChangeProfilePic.deleteOldPic(self, username)
                profilePic = models.ProfilePic.objects.get(username=username)
                profilePic.delete()
                content = {'Success': True}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)

class changeUserPassword(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey', False)
        username = request.GET.get('username', False)
        password = request.GET.get('password', False)
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                content = {'Success': True}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)

class changeUserInfo(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey')
        username = request.GET.get('username')
        newUsername = request.GET.get('newUsername')
        lastName = request.GET.get('lastName')
        firstName = request.GET.get('firstName')
        email = request.GET.get('email')
        admin = request.GET.get('admin', 'False')
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                user = User.objects.get(username=username)
                user.username = newUsername
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                user.is_superuser = admin.lower() in [True]
                user.is_staff = admin.lower() in [True]
                user.save()
                content = {'Success': True}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)


class GetUsers(APIView):

    def get(self, request):
        apiKey = request.GET.get('apiKey', False)
        usersMain = []
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                users = User.objects.all()
                for user in users:
                    profilePic = models.ProfilePic.objects.get(username=user.username)
                    profile = { "size4": profilePic.profilePicSize4,
                    "size3": profilePic.profilePicSize3,
                    "size2": profilePic.profilePicSize2,
                    "size1": profilePic.profilePicSize1}
                    newUser = {
                    'username' : user.username,
                    'firstName': user.first_name,
                    'lastName' : user.last_name,
                    'email' : user.email,
                    'admin' : user.is_superuser,
                    'picture': profile,
                    }
                    usersMain.append(newUser)
                content = {'Success': True, 'users' : usersMain}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'systemKey missing or wrong', 'Success': False}
        return Response(content)

class DeleteProfilePic(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey', False)
        username = request.GET.get('username', False)
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            try:
                ChangeProfilePic.deleteOldPic(self, username)
                content = {'Success': True}
            except Exception as e:
                content = {'error' : str(e), 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)

# TODO: delete older image create model after image uploaded, delete all generated files on exception
class ChangeProfilePic(APIView):

    size4= (512,512)
    size3= (256,256)
    size2= (128,128)
    size1= (64,64)

    def post(self, request):
        try:
            apiKey = request.GET.get('apiKey', False)
            username = request.GET.get('username', False)
            picture = request.FILES['profilePic']
            user = User.objects.get(username = username)
            #generate a random name so it wont interfere with other uploads
            randomName = settings.MEDIA_ROOT + "/profilePic/" + token_urlsafe(16) + picture.name
            savePath = settings.MEDIA_ROOT + "/profilePic/"
            if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
                try:
                    #check if there is an old picture and delete it
                    self.deleteOldPic(username)
                    #save original file
                    destination = open(randomName, 'wb+')
                    for chunk in picture.chunks():
                        destination.write(chunk)
                    destination.close()
                    #reduce image size and save it
                    path4 = self.generateProfilePic(self.size4, randomName, savePath)
                    path3 = self.generateProfilePic(self.size3, randomName, savePath)
                    path2 = self.generateProfilePic(self.size2, randomName, savePath)
                    path1 = self.generateProfilePic(self.size1, randomName, savePath)
                    #change profilePic paths on db
                    profilePicdb = models.ProfilePic.objects.get(username=username)
                    profilePicdb.profilePicSize4 = path4
                    profilePicdb.profilePicSize3 = path3
                    profilePicdb.profilePicSize2 = path2
                    profilePicdb.profilePicSize1 = path1
                    profilePicdb.save()
                    #delete original Image
                    os.remove(randomName)
                    sizes = {'size4': path4,'size3': path3,'size2': path2,'size1': path1}
                    content = { 'profilePic': sizes , 'Success': True}
                except Exception as e:
                    content = {'error' : str(e), 'Success': False}
            else:
                content = {'error' : 'systemKey missing', 'Success': False}
        except Exception as e:
            content = {'error' : str(e), 'Success': False}
        return Response(content)

    def generateProfilePic(self, size, filename, savePath):
        thumbPicture = Image.open(filename)
        #generate random name
        randomName = token_urlsafe(16)
        #generate saved image path
        imagePath= savePath + randomName + '.jpg'
        thumbPictureRGB = thumbPicture.convert('RGB')
        cropped = ImageOps.fit(thumbPictureRGB, size, Image.ANTIALIAS)
        cropped.save(imagePath)
        return imagePath

    def deleteOldPic(self, username):
        profilePic = models.ProfilePic.objects.get(username=username)
        #check if pic is the default
        if "defaultProfile" not in profilePic.profilePicSize4:
            os.remove(profilePic.profilePicSize4)
            profilePic.profilePicSize4 = "/authorizator/media/profilePic/defaultProfile.svg"
            os.remove(profilePic.profilePicSize3)
            profilePic.profilePicSize3 = "/authorizator/media/profilePic/defaultProfile.svg"
            os.remove(profilePic.profilePicSize2)
            profilePic.profilePicSize2 = "/authorizator/media/profilePic/defaultProfile.svg"
            os.remove(profilePic.profilePicSize1)
            profilePic.profilePicSize1 = "/authorizator/media/profilePic/defaultProfile.svg"
            profilePic.save()

# TODO: block brute force attacks
class CreateServiceKey(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey', False)
        serviceID = request.GET.get('serviceID', False)
        content = serviceID
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            if serviceID :
                try:
                    apiKey = token_urlsafe(50)
                    dbKey = models.ServiceKey(serviceName = serviceID, apiKey = apiKey)
                    dbKey.save()
                    content = { 'apiKey': apiKey, 'Success': True}
                except Exception as e:
                    content = {'error' : str(e), 'Success': False}
            else:
                content = {'error' : 'serviceId missing', 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)

# TODO: block brute force attacks
class GetServiceKey(APIView):

    def get(self, request):
        apiKey = request.GET.get('apiKey', False)
        serviceID = request.GET.get('serviceID', False)
        content = serviceID
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            if serviceID :
                try:
                    apiKey = models.ServiceKey.objects.get(serviceName=serviceID)
                    content = { 'apiKey': apiKey.apiKey, 'Success': True}
                except Exception as e:
                    content = {'error' : str(e), 'Success': False}
            else:
                content = {'error' : 'serviceId missing', 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)



# TODO: block brute force attacks
class RemoveServiceKey(APIView):

    def post(self, request):
        apiKey = request.GET.get('apiKey', False)
        serviceID = request.GET.get('serviceID', False)
        content = serviceID
        if (models.ServiceKey.objects.filter(apiKey=apiKey).exists()):
            if serviceID :
                try:
                    apiKey = models.ServiceKey.objects.get(serviceName = serviceID)
                    apiKey.delete()
                    content = { 'Success': True}
                except Exception as e:
                    content = {'error' : str(e), 'Success': False}
            else:
                content = {'error' : 'serviceId missing', 'Success': False}
        else:
            content = {'error' : 'systemKey missing', 'Success': False}
        return Response(content)
