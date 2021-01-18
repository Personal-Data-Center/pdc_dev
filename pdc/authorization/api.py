from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


class getUser(APIView):

    def get(self, request):
        token = request.GET.get('token', False)
        try:
            session = Session.objects.get(session_key=token)
            session_data = session.get_decoded()
            user = User.objects.get(id=session_data["_auth_user_id"])
            content = {'username': user.username, 'email': user.email, 'admin' : user.is_superuser}
        except Exception as e:
            content = {'error': str(e)}
        return Response(content)

class isAuthenticated(APIView):

    def get(self, request):
        token = request.GET.get('token', False)
        if token != False:
            try:
                session = Session.objects.get(session_key=token)
                session_data = session.get_decoded()
                content = {'authenticated': 'true'}
            except:
                content = {'authenticated': 'error'}
        else:
            content = {'authenticated': 'false'}
        return Response(content)
