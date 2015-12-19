# -*- coding:utf8 -*-

import re

try:
    import json
except ImportError:
    from django.utils import simplejson as json

import datetime
from django.conf import settings
from django.template import Context
from django.http import HttpResponseRedirect, Http404, HttpResponse, \
        HttpResponseBadRequest
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db import models
from dynaform.models import DynaFormForm, DynaFormField, DynaFormTracking
from dynaform.forms.base import DynaFormClassForm

from django.contrib.auth.decorators import login_required

import logging
log = logging.getLogger(__name__)

DYNAFORM_SESSION_KEY = getattr(settings, 'DYNAFORM_SESSION_KEY', 'DYNAFORM')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class PermissionRequiredMixin(LoginRequiredMixin):
    pass


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content, content_type='application/json', 
                **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class DynaformMixin(object):

    disable_csrf = False

    def post(self, request, *args, **kwargs):
        object_form_pk = request.POST.get('_object_form_pk')
        url = request.POST.get('_object_form_success_url')

        if not object_form_pk and not url and getattr(request, 'session', False):
            DYNAFORM = request.session.get(DYNAFORM_SESSION_KEY, False)
            if DYNAFORM and DYNAFORM.has_key('pk'):
                object_form_pk = DYNAFORM['pk']
                url = DYNAFORM.get('success_url', False)

        context = Context()
        try:
            form_object = DynaFormForm.objects.get(pk=object_form_pk)
            form = DynaFormClassForm(
                    data=request.POST, 
                    files=request.FILES, 
                    request=request, 
                    context=context, 
                    object_form=form_object
                    )

            if form.is_valid():
                form.save()
                if url:
                    return HttpResponseRedirect(url)

            print 'post process', form.errors

        except DynaFormForm.DoesNotExist:
            raise Http404
                
        # Fallback resolution order: POST, GET, dispatch
        superClass = super(DynaformMixin, self)

        if hasattr(superClass, 'post'):
            return superClass.post(request, *args, **kwargs)

        if hasattr(superClass, 'get'):
            return superClass.get(request, *args, **kwargs)

        return superClass.dispatch(request, *args, **kwargs)

    #@ensure_csrf_cookie
    def dispatch(self, *args, **kwargs):
        original = super(DynaformMixin, self)
        if self.disable_csrf:
            response = csrf_exempt(original.dispatch)(*args, **kwargs)
        else:
            response = original.dispatch(*args, **kwargs)
        response['P3P'] = 'CP="Link b"'
        return response


class DynaformViewAJAX(SingleObjectMixin, View):
    """
    Vista generica para usar con dynaform, ajax o algo así
    """
    def get_queryset(self):
        # este metodo ya lo resuelve el MultiSiteBaseModel
        return DynaFormForm.objects.get_for_lang()

    def post(self, request, *args, **kwargs):
        context = Context()
        
        form_object = self.get_object()

        form = DynaFormClassForm(data=request.POST, files=request.FILES, \
                request=request, context=context, object_form=form_object)

        if form.is_valid():
            form.save()
            # si es por ajax devuelve OK
            return HttpResponse(json.dumps({
                    'status': 'ok', 
                    'dt': form.dt.pk,
                    'code':200 
                }), content_type='application/json')
  
        return HttpResponseBadRequest(json.dumps({
                    'status': 'error', 
                    'code': 400, 
                    'errors': form.errors
                }), content_type='application/json')




class DynaformChoicesRelatedFieldViewAJAX(JSONResponseMixin, View):

    TOKEN_FORMAT = re.compile('%\((?P<field>[a-z0-9\.\_\-]+)\)s', re.U|re.I)

    def label_from_instance(self, obj, label_format):
        key_fields = self.TOKEN_FORMAT.findall(label_format)
        ret = {}
        for key in key_fields:
            parts = key.split('__')
            val = obj
            for part in parts:
                val = getattr(val, part, '')
                ret.update({key: val})

        return label_format % ret

    def get(self, request, *args, **kwargs):
        field_pk = kwargs.get('field_pk', None)
        related_field_pk = kwargs.get('related_field_pk', None)
        pk = kwargs.get('pk', None)
        
        try:
            field = DynaFormField.objects.get(pk=field_pk)
        except DynaFormField.DoesNotExist:
            return self.render_to_response({
                    'status': 'error', 
                    'code': 400, 
                    'errors': 'Field DoesNotExist'
                })

        try:
            related_field = DynaFormField.objects.get(pk=related_field_pk)
        except DynaFormField.DoesNotExist:
            return self.render_to_response({
                    'status': 'error', 
                    'code': 400, 
                    'errors': 'Related Field DoesNotExist'
                })

        field = field.choices_queryset_queryset()
        related_field_qs = related_field.choices_queryset_queryset()

        try:
            field = field.get(pk=pk)
        except:
            return self.render_to_response({
                    'status': 'error', 
                    'code': 400, 
                    'errors': 'Choices DoesNotExist'
                })


        qs_args = {}
        for f in related_field_qs.model._meta.fields:
            if f.rel and f.rel.to and isinstance(field, f.rel.to):
                qs_args.update({ f.name: field })


        qs = related_field_qs.filter(**qs_args)

        return self.render_to_response({
            'status': 'ok',
            'code': 200,
            'data': [
            (
                obj.id, 
                related_field.choices_queryset_label 
                and self.label_from_instance(obj, 
                    related_field.choices_queryset_label) or '%s' % obj
            ) for obj in qs ]
        })


class DynaformReportListView(PermissionRequiredMixin, ListView):
    template_name = 'dynaform/report_list.html'
    model = DynaFormTracking

    def get_queryset(self, *args, **kwargs):
        qs = super(DynaformReportListView, self).get_queryset(*args, **kwargs)
        date_from = datetime.date.today() - datetime.timedelta(30)
        date_to = datetime.date.today()

        options = self.request.GET

        if options.get('date_from'):
            date_from = datetime.datetime.strptime(options['date_from'], '%Y-%m-%d').date()

        if options.get('date_to'):
            date_to = datetime.datetime.strptime(options['date_to'], '%Y-%m-%d').date()

        date_from_ant = date_from - datetime.timedelta(30)
        date_to_ant = date_to - datetime.timedelta(30)

        return qs.values('sender', 'object_form', 'object_form_id').annotate(
                    conversiones=models.Count(models.Case(models.When(pub_date__range=[date_from, date_to], then='object_form'))),
                    conversiones_anterior=models.Count(models.Case(models.When(pub_date__range=[date_from_ant, date_to_ant], then='object_form')))
                )



class DynaformReportDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'dynaform/report_detail.html'
    model = DynaFormForm

    def get_context_data(self, *args, **kwargs):
        context = super(DynaformReportDetailView, self).get_context_data(*args, **kwargs)

        object = self.get_object()
        log.debug("Obtiene el form %s", object.name)

        date_from = datetime.date.today() - datetime.timedelta(30)
        date_to = datetime.date.today()

        options = self.request.GET

        if options.get('date_from'):
            date_from = datetime.datetime.strptime(options['date_from'], '%Y-%m-%d').date()

        if options.get('date_to'):
            date_to = datetime.datetime.strptime(options['date_to'], '%Y-%m-%d').date()

        date_from_ant = date_from - datetime.timedelta(30)
        date_to_ant = date_to - datetime.timedelta(30)

        qs = DynaFormTracking.objects.filter(object_form=object).extra({
            'year': 'extract(year from pub_date)', 
            'month': 'extract(month from pub_date)'
            })\
                    .values('year', 'month')\
                    .annotate(conversiones=models.Count('id'))\
                    .order_by('year', 'month')
        

        context['object_list'] = qs
        return context
