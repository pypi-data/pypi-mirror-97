# -*- coding: utf-8 -*-
import uuid
from threading import local

from django.utils.deprecation import MiddlewareMixin

from django_logger.models import Remote


class RequestThreadlocal(local):
    request = object()


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    RequestLoggingMiddleware enables better logging of Django requests.

    It assigns a unique ID to each request, using the Python uuid module, and
    keeps a threadlocal reference to the request that logging filters or
    adapters can use to access request attributes.

    It should be installed first in your MIDDLEWARE_CLASSES setting, so that
    the request information is available for logging as early as possible.
    """
    
    context = RequestThreadlocal()

    def process_request(self, request):
        request.uuid = uuid.uuid4().hex
        self.context.request = request

        Remote.objects.create(request="", uuid=request.uuid, user_agent=request.META.get("HTTP_USER_AGENT"))

    def process_response(self, request, response):
        obj, created = Remote.objects.get_or_create(uuid=request.uuid)
        obj.response = response
        obj.status_code = response.status_code
        obj.save()
        return response

