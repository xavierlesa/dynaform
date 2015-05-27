# *-* coding=utf-8 *-*

from django import template
from django.conf import settings
from django.core import urlresolvers
from dynaform import forms as dynaforms

DYNAFORM_SESSION_KEY = getattr(settings, 'DYNAFORM_SESSION_KEY', 'DYNAFORM')
DYNAFORM_SUCCESS_REDIRECT_URL = getattr(settings, 'DYNAFORM_SUCCESS_REDIRECT_URL', '/')

register = template.Library()

################################################################################
# tags new style
################################################################################
from django.utils.safestring import mark_safe

from django.template import Template
from django.contrib.contenttypes.models import ContentType
from dynaform.models import DynaFormForm, DynaFormTemplate
from dynaform.forms.base import DynaFormClassForm

@register.assignment_tag(takes_context=True)
def dynaform_form(context, form_slug, success_url, form_template=None, *args, **kwargs):
    """
    Genera e instancia el formulario según el `slug`. Si no existe devuelve un 
    comentario `HTML` informando que no se encontró.
    Para determinar la dirección de éxito hay que pasar la url en el argumento
    `success_url` que es obligatorio.

    {% dynaform_form form_slug='contact' success_url='/contact/done/' as form %}

    Para que el formulario haga el render en un template especifico se puede pasar
    en el argumento `form_template` pero es una opción totan sabiendo que se 
    pueden cargar directamente desde dynaform/dynaformtemplate.

    Este `templatetag` también genera una variable `form_title` en el `context` 
    donde guarda el título del formulario, el que es cargado desde el admin.
    """

    try:
        object_form = DynaFormForm.objects.get_for_lang().get(slug=form_slug, is_active=True)
    except DynaFormForm.DoesNotExist:
        return {mark_safe('<!-- DynaFormForm %s DoesNotExist -->' % form_slug):[]}

    request = context['request']

    obj = context.get('object', None)
    if obj:
        ct = ContentType.objects.get_for_model(obj)

    # Si es POST y no valido el form, vuelve a hacer el render pero mostrando los errores
    if request.method == "POST":
        form = DynaFormClassForm(data=request.POST, files=request.FILES, request=request, object_form=object_form, context=context, success_url=success_url)
    else:
        form = DynaFormClassForm(request=request, object_form=object_form, context=context, success_url=success_url)

    form.action = object_form.get_absolute_url()
    form.title = object_form.form_title
    form.object = object_form

    if form_template:
        try:
            template = DynaFormTemplate.objects.get(id=form_template)
            template = Template(template.html)
        except DynaFormTemplate.DoesNotExist:
            return form

    elif object_form.form_template:
        template = Template(object_form.form_template.html)

    else:
        return form

    context.update({'form': form, 'form_title': object_form.form_title })
    html = template.render(context)
    return mark_safe(html)


@register.filter
def get_ct_pk(obj):
    """
    Devuelve el `content_type` de un objeto
    """
    try:
        ct = ContentType.objects.get_for_model(obj)
        ct = ct.pk
    except ContentType.DoesNotExist:
        ct = None
    return ct
