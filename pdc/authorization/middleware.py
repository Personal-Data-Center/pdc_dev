from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class PDCUser:

    def __init__(self):
        pass


class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.user.is_authenticated():
            return HttpResponseRedirect('/authorizator/login/')
