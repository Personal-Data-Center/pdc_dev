from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings
from secrets import token_urlsafe
from pdc.authorization import models
from django.conf import settings
from PIL import Image, ImageOps
from secrets import token_urlsafe
import os

# TODO: require service api key, return the correct user info if user exists
class GetUser(APIView):

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

class CreateUser(APIView):

    def post(self, request):
        pass

class DeleteUser(APIView):

    def post(self, request):
        pass

class DeleteProfilePic(APIView):

    def post(self, request):
        systemKey = request.GET.get('systemKey', False)
        username = request.GET.get('username', False)
        if (systemKey == settings.SYSTEM_API_KEY):
            try:
                ChangeProfilePic.deleteOldPic(self, username)
                content = {'Success': 'True'}
            except Exception as e:
                content = {'error' : str(e), 'Success': 'False'}
        else:
            content = {'error' : 'systemKey missing', 'Success': 'False'}
        return Response(content)

# TODO: delete older image create model after image uploaded, delete all generated files on exception
class ChangeProfilePic(APIView):

    size4= (512,512)
    size3= (256,256)
    size2= (128,128)
    size1= (64,64)

    def post(self, request):
        systemKey = request.GET.get('systemKey', False)
        username = request.GET.get('username', False)
        picture = request.FILES['filename']
        user = User.objects.get(username = username)
        #generate a random name so it wont interfere with other uploads
        randomName = settings.MEDIA_ROOT + "/profilePic/" + token_urlsafe(16) + picture.name
        savePath = settings.MEDIA_ROOT + "/profilePic/"
        if (systemKey == settings.SYSTEM_API_KEY):
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
                content = { 'profilePic': sizes , 'Success': 'True'}
            except Exception as e:
                content = {'error' : str(e), 'Success': 'False'}
        else:
            content = {'error' : 'systemKey missing', 'Success': 'False'}
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
                content = {'error' : 'serviceId missing', 'Success': 'False'}
        else:
            content = {'error' : 'systemKey missing', 'Success': 'False'}
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
                content = {'error' : 'serviceId missing', 'Success': 'False'}
        else:
            content = {'error' : 'systemKey missing', 'Success': 'False'}
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
                content = {'error' : 'serviceId missing', 'Success': 'False'}
        else:
            content = {'error' : 'systemKey missing', 'Success': 'False'}
        return Response(content)
