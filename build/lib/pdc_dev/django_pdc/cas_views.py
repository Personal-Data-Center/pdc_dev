from datetime import timedelta
from importlib import import_module
from typing import Any
from urllib import parse as urllib_parse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django_cas_ng.models import ProxyGrantingTicket, SessionTicket
from django_cas_ng.signals import cas_user_logout
from django_cas_ng.utils import (
    get_cas_client,
    get_protocol,
    get_redirect_url,
    get_service_url,
    get_user_from_session,
)

from django_cas_ng import views as django_cas_ng_views

class login(django_cas_ng_views.LoginView):

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Forwards to CAS login URL or verifies CAS ticket
        :param request:
        :return:
        """
        next_page = django_cas_ng_views.clean_next_page(request, request.GET.get('next'))
        required = request.GET.get('required', False)

        service_url = get_service_url(request, next_page)
        client = get_cas_client(service_url=service_url, request=request)
        redirect_login_url = client.get_login_url()
        redirect_login_url = redirect_login_url.strip('http://authorizator/')
        redirect_login_url = "http://localhost/authorizator/cas/" + redirect_login_url

        if not next_page and settings.CAS_STORE_NEXT and 'CASNEXT' in request.session:
            next_page = request.session['CASNEXT']
            del request.session['CASNEXT']

        if not next_page:
            next_page = get_redirect_url(request)

        if request.user.is_authenticated:
            if settings.CAS_LOGGED_MSG is not None:
                message = settings.CAS_LOGGED_MSG % request.user.get_username()
                messages.success(request, message)
            return self.successful_login(request=request, next_page=next_page)

        ticket = request.GET.get('ticket')
        if not ticket:
            if settings.CAS_STORE_NEXT:
                request.session['CASNEXT'] = next_page
            return HttpResponseRedirect(redirect_login_url)

        user = authenticate(ticket=ticket,
                            service=service_url,
                            request=request)
        pgtiou = request.session.get("pgtiou")
        if user is not None:
            auth_login(request, user)
            if not request.session.exists(request.session.session_key):
                request.session.create()

            try:
                st = SessionTicket.objects.get(session_key=request.session.session_key)
                st.ticket = ticket
                st.save()
            except SessionTicket.DoesNotExist:
                SessionTicket.objects.create(
                    session_key=request.session.session_key,
                    ticket=ticket
                )

            if pgtiou and settings.CAS_PROXY_CALLBACK:
                # Delete old PGT
                ProxyGrantingTicket.objects.filter(
                    user=user,
                    session_key=request.session.session_key
                ).delete()
                # Set new PGT ticket
                try:
                    pgt = ProxyGrantingTicket.objects.get(pgtiou=pgtiou)
                    pgt.user = user
                    pgt.session_key = request.session.session_key
                    pgt.save()
                except ProxyGrantingTicket.DoesNotExist:
                    pass

            if settings.CAS_LOGIN_MSG is not None:
                name = user.get_username()
                message = settings.CAS_LOGIN_MSG % name
                messages.success(request, message)

            return self.successful_login(request=request, next_page=next_page)

        if settings.CAS_RETRY_LOGIN or required:
            return HttpResponseRedirect(redirect_login_url)

        raise PermissionDenied(_('Login failed.'))
