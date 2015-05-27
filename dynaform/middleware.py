# *-* coding:utf-8 *-*

from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect

DYNAFORM_SESSION_KEY = getattr(settings, 'DYNAFORM_SESSION_KEY', 'DYNAFORM')

#############
#
# IMPORTANT !!!!!!!!!!!
#
# Dynaform Middleware became depracated since version 1.0.0b
# Use nebula.dynaform.views.DynaformMixin instead
#
#############

class DynaFormMiddleware(object):
    def process_response(self, request, response):
        if getattr(request, 'session', False) and request.session.get(DYNAFORM_SESSION_KEY, False):
            url = request.session.get(DYNAFORM_SESSION_KEY+"_SUCCESS_URL", '.')

            try:
                del request.session[DYNAFORM_SESSION_KEY]
                del request.session[DYNAFORM_SESSION_KEY+"_SUCCESS_URL"]
            except KeyError:
                pass

            if url:
                return HttpResponseRedirect(url)
        return response

class ContentLengthWriter(object):
    """A simple middleware that writes content-length
    """
    def process_response(self, request, response):
        if not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))
        return response
