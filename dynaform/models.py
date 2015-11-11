# *-* coding=utf-8 *-*

import StringIO
from django.db import models
from django import forms
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.defaultfilters import slugify 
from django.utils.encoding import force_unicode
#from djblog.common.models import MultiSiteBaseModel, GenericRelationModel
from dynaform.forms.widgets import DYNAFORM_FIELDS, DYNAFORM_WIDGETS

try:
    import json
except ImportError:
    from django.utils import simplejson as json

import logging
logger = logging.getLogger(__name__)

class JsonField(models.Field):
    """ 
    JSON Field 
    """
    __metaclass__ = models.SubfieldBase

    serialize_to_string = True

    def get_internal_type(self):
        return "TextField"

    def value_to_string(self, obj):
        return self.get_prep_value(self._get_val_from_obj(obj))

    def get_prep_value(self, value):
        if value:
            if isinstance(value, StringIO.StringIO):
                value = value.getvalue()
            stream = StringIO.StringIO()
            json.dump(value, stream, cls=DjangoJSONEncoder)
            value = stream.getvalue()
            stream.close()
            return value
        return None

    def to_python(self, value):
        if value == "":
            return None

        if isinstance(value, basestring):
            value = json.loads(value)
        elif isinstance(value, StringIO.StringIO):
            value = value.getvalue()
            value = json.load(value)
        return value


class MultiSiteBaseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        """
        Registros para el site actual o sin site 
        """
        qs = super(MultiSiteBaseManager, self).get_queryset(*args, **kwargs)
        qs = qs.filter(models.Q(site__id__in=[settings.SITE_ID,]) | models.Q(site__isnull=True))
        return qs

    def get_for_lang(self, *args, **kwargs):
        """
        Registros para el idioma actual o sin idioma
        """
        qs = self.get_queryset(*args, **kwargs)
        if 'django.middleware.locale.LocaleMiddleware' in getattr(settings, 'MIDDLEWARE_CLASSES', []):
            return qs.filter(models.Q(lang__iexact=translation.get_language()) | models.Q(lang__exact=''))
        else:
            logger.warning('NO get for lang %s', translation.get_language())
        return qs

    def get_for_site_or_none(self, *args, **kwargs):
        """
        Registros para el site actual 
        """
        qs = super(MultiSiteBaseManager, self).get_queryset(*args, **kwargs)
        return qs.filter(site__id__in=[settings.SITE_ID,])


class MultiSiteBaseManagerAdmin(models.Manager):
    pass


class MultiSiteBaseModel(models.Model):
    """
    Base para Multi Site y Lang
    """
    lang = models.CharField(max_length=20, blank=True, choices=settings.LANGUAGES) 
    site = models.ManyToManyField(Site, blank=True, null=True, related_name="%(app_label)s_%(class)s_related")

    # el primero es el que luego es llamado con _default_manager
    objects_for_admin = MultiSiteBaseManagerAdmin()
    objects = MultiSiteBaseManager()

    class Meta:
        abstract = True


class GenericRelationManager(models.Manager):
    def for_model(self, model):
        """
        Para el modelo en particular y/o su instancia o clase 
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs

class GenericRelationModel(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_pk = models.PositiveIntegerField(_('object PK'), blank=True, null=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    objects = GenericRelationManager()

    def __unicode__(self):
        return u"%s" % self.content_object

    class Meta:
        abstract = True


class DynaFormTracking(models.Model):
    pub_date = models.DateTimeField(auto_now=True, verbose_name=_(u"Fecha de creación"))
    site = models.ForeignKey(Site)
    lang = models.CharField(max_length=20, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE.lower())
    sender = models.CharField(max_length=200)
    data = JsonField()

    def __unicode__(self, *args, **kwargs):
        return u"%s %s" % (self.pub_date, self.sender)

    def save(self, *args, **kwargs):
        super(DynaFormTracking, self).save(*args, **kwargs)

    def get_data(self):
        if isinstance(self.data, dict):
            return self.data
        elif isinstance(self.data, (list, tuple)):
            return dict(zip(xrange(len(self.data)),self.data))


#from south.modelsinspector import add_introspection_rules
#add_introspection_rules([], ["^nebula\.dynaform\.models\.JsonField"])

################################################################################
# Base Model DynaForm
################################################################################

class DynaFormField(GenericRelationModel):
    field_name = models.SlugField(_(u"Identificador del Campo"), max_length=200, help_text=_(u"nombre del campo solo letras minúsculas, guinobajo y numeros "))
    field_label = models.CharField(_(u"Etiqueta del Campo"), max_length=200, help_text=_(u"nombre visible del campo"))
    field_type = models.CharField(max_length=100, choices=DYNAFORM_FIELDS)
    field_widget = models.CharField(max_length=100, choices=DYNAFORM_WIDGETS, blank=True, null=True)
    field_help = models.CharField(_(u"Texto descripción"), max_length=200, blank=True)

    is_required = models.BooleanField(_(u"Requerido"), default=True)
    is_hidden = models.BooleanField(_(u"Oculto"), default=False)

    default_value = models.CharField(_(u"Valor por defecto"), max_length=200, blank=True, help_text=_(u"Se pueden usar variables del contexto {{ object }}, {{ sites }}, etc"))

    choices = models.TextField(_(u"Lista de valores"), blank=True, help_text=_(u"Lista de \"valor\", \"título\" separada por el delimitador y por línea"))
    choices_delimiter = models.CharField(_(u"Delimitador de valores por defecto es |"), max_length=1, blank=True, default='|')

    ##########################################################################
    # Choices por Modelo
    ##########################################################################
    choices_queryset = models.ForeignKey(ContentType, verbose_name=_(u"Modelo de Datos"), blank=True, null=True)
    choices_queryset_filter = models.CharField(_(u"Filtros"), max_length=200, blank=True)
    choices_queryset_empty_label = models.CharField(_(u"Valor por defecto"), max_length=100, blank=True, default="------")
    choices_queryset_label = models.CharField(_(u"Formato"), max_length=100, blank=True, help_text=_(u"puede ser cualquier campo del modelo en formato, \"%(nombre)s, %(apellido)s\""))

    choices_related_field = models.ForeignKey('self', blank=True, null=True)

    field_order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['field_order', ]

    def __unicode__(self):
        return unicode(self.field_name)

    def choices_queryset_queryset(self, *args, **kwargs):
        """
        Resuelve el modelo y genera el queryset para luego filtrar
        """
        import re
        and_split = re.compile('(?:\s+AND\s+)')
        qs = []
        if self.choices_queryset and self.field_type in \
                ("ModelChoiceField","ModelMultipleChoiceField"):
            qs = self.choices_queryset.get_all_objects_for_this_type()

            if self.choices_queryset_filter:
                filter_args = dict([f.split('=') for f in self.choices_queryset_filter.split(',')])

                # testing AND y OR
                # and_split.split("name__in=[1,2,4,5, 'AND', ' AND THEN...'] AND id__gt=2")
                # ["name__in=[1,2,4,5, 'AND ']", ' AND ', 'id__gt=2]
                # print and_split.split(self.choices_queryset_filter)
                # filter_args = dict([f.split('=') for f in and_split.split(self.choices_queryset_filter)])

                if filter_args:
                    qs = qs.filter(**filter_args)
        return qs



class DynaFormTemplate(MultiSiteBaseModel):
    """
    Templates for dinamic forms for subject, body and form itself
    """
    multisite_unique_together = ('slug',)

    name = models.CharField(_(u"Nombre del template"), max_length=100, help_text=_(u"ej: Subject Contacto"))
    slug = models.SlugField(max_length=100)
    html = models.TextField(_(u"HTML del Template"), help_text=_(u"parsea del contexto, y templatetags"))
    is_plain = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(DynaFormTemplate, self).save(*args, **kwargs)


class DynaFormForm(MultiSiteBaseModel):
    """
    Create dinamic forms from database
    """
    multisite_unique_together = ('slug',)

    name = models.CharField(_(u"Nombre del form"), max_length=100)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(_(u"Es activo"), default=True, help_text=_(u"activa para usar en el frontend"))

    form_title = models.CharField(_(u"Título del form"), max_length=200)
    form_template = models.ForeignKey(DynaFormTemplate, related_name="dynaform_form_template_related", blank=True, null=True)

    ##########################################################################
    # Enviar mail al guardar
    ##########################################################################
    send_email = models.BooleanField(_("Enviar mail"), default=True)
    from_email = models.CharField(max_length=100, default=settings.DEFAULT_FROM_EMAIL, blank=True)
    recipient_list = models.TextField(_(u"Lista de destinatarios"), default=settings.MANAGERS, blank=True,
            help_text=_(u"ej: lista separada por líneas y coma.<br>Juan Pérez, juanperez@dominio.com<br>Maria Gomez, mariagomez@dominio.com"))

    subject_template = models.ForeignKey(DynaFormTemplate, blank=True, null=True, related_name="dynaform_subject_template_related")
    body_template = models.ForeignKey(DynaFormTemplate, blank=True, null=True, related_name="dynaform_body_template_related")
    error_class = models.CharField(_(u"Clase CSS para error"), max_length=40, default="error")
    required_css_class = models.CharField(_(u"Clase CSS para requerido"), max_length=40, default="required")

    ##########################################################################
    # nuevo autorespondedor
    ##########################################################################
    autorespond = models.BooleanField(_(u"Autoresponder"), default=False)
    autorespond_subject_template = models.ForeignKey(DynaFormTemplate, blank=True, null=True, related_name="dynaform_autorespond_subject_template_related")
    autorespond_body_template = models.ForeignKey(DynaFormTemplate, blank=True, null=True, related_name="dynaform_autorespond_body_template_related")
    autorespond_email_field = models.CharField(_("Campo de email"), default='email', max_length=40)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(DynaFormForm, self).save(*args, **kwargs)

    def get_fields(self):
        return DynaFormField.objects.for_model(self)

    @models.permalink
    def get_absolute_url(self):
        return ('dynaform_action', (), {'slug': self.slug, 'pk': self.pk})

    def clone(self):
        """
        Hace un clon de la instania actual

        """
        
        # recrea la instancia del form
        form_clone = DynaFormForm(
                lang = self.lang,
                name = "clon de %s" % self.name,
                is_active = self.is_active,
                form_title = self.form_title,
                form_template = self.form_template,
                send_email = self.send_email,
                from_email = self.from_email,
                recipient_list = self.recipient_list,
                subject_template = self.subject_template,
                body_template = self.body_template,
                error_class = self.error_class,
                required_css_class = self.required_css_class,
                autorespond = self.autorespond,
                autorespond_subject_template = self.autorespond_subject_template,
                autorespond_body_template = self.autorespond_body_template,
                autorespond_email_field = self.autorespond_email_field
                )

        form_clone.save()

        content_type = ContentType.objects.get_for_model(form_clone)

        # recrea todos los fields
        for field in self.get_fields():

            field_clone = DynaFormField(
                    content_type = content_type,
                    object_pk = form_clone.pk,
                    field_name = field.field_name,
                    field_label = field.field_label,
                    field_type = field.field_type,
                    field_widget = field.field_widget,
                    field_help = field.field_help,
                    is_required = field.is_required,
                    is_hidden = field.is_hidden,
                    default_value = field.default_value,
                    choices = field.choices,
                    choices_delimiter = field.choices_delimiter,
                    choices_queryset = field.choices_queryset,
                    choices_queryset_filter = field.choices_queryset_filter,
                    choices_queryset_empty_label = field.choices_queryset_empty_label,
                    choices_queryset_label = field.choices_queryset_label,
                    choices_related_field = field.choices_related_field,
                    field_order = field.field_order
                    )

            field_clone.save()
