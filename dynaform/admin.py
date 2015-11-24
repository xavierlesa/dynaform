# +-+ coding:utf-8 +-+

import csv
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.http import HttpResponse
from models import DynaFormTracking, DynaFormField, DynaFormTemplate, DynaFormForm
from dummy_form import DummyTextInput

class JSON2CSV(object):

    def safe_replace(sefl, val):
        if isinstance(val, basestring):
            return val.replace('"', '').encode('utf-8')
        return val

    def to_flat_json(self, row):
        csv_header = []
        flat_json = {}
        for key, val in row.iteritems():
            if isinstance(val, (dict,)):
                for k,v in val.iteritems():
                    flat_json.update({u"{0}_{1}".format(key, k): self.safe_replace(v)})

            elif isinstance(val, (list,tuple)):
                flat_json.update({unicode(key): ",".join([self.safe_replace(v) for v in val])})

            else:
                flat_json.update({unicode(key): self.safe_replace(val)})

        csv_header = set(csv_header).union(flat_json.keys())
        return flat_json, csv_header


    def json2csv(self, qs):
        csv = {'data': [], 'header': []}
        for row in qs:
            data, header = self.to_flat_json(row)
            csv['data'].append(data)
            csv['header'] = set(csv['header']).union(header)

        return csv


class DynaFormFieldInline(GenericStackedInline):
    model = DynaFormField
    ct_field = 'content_type'
    ct_fk_field = 'object_pk'
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                ('field_name', 'field_label'), 
                ('field_type', 'field_widget'), 
                ('field_help', 'is_required', 'is_hidden'), 
                ('default_value'), #'choices_delimiter'), 'choices'
                'field_order',
            ),
        }),

        ('Choices Manual', {
            'fields': (
                ('choices_delimiter', 'choices'),
            ),
            'classes': ('collapse',)
        }),

        ('Choices Modelo de Datos', {
            'fields': (
                ('choices_queryset', 'choices_queryset_empty_label',),
                ('choices_queryset_filter', 'choices_queryset_label'),
                ('choices_related_field',),
            ),
            'classes': ('collapse',)
        }),
    )


class DynaFormTemplateAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(DynaFormTemplateAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'html':
            attrs = formfield.widget.attrs
            attrs.update({'rows':100, 'style': 'font-family:courier;font-size:16px;color:green;height:450px'})
            formfield.widget = forms.Textarea(attrs=attrs)
        return formfield

    class Meta:
        model = DynaFormTemplate


class DynaFormFormAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'id')
    inlines = [DynaFormFieldInline, ]
    prepopulated_fields = {'slug': ('name',), 'form_title': ('name',)}
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'slug',), 
                ('error_class', 'required_css_class'),
                ('form_title', 'form_template'),
                'is_active',
            )
        }),

        ('Advanced setting', {
            'fields': (
                'lang', 
                'site',
            ),
            'classes': ('collapse',),
        }),

        ('Send Email', {
            'fields': (
                ('send_email', 'from_email'), 
                'recipient_list',
                ('subject_template', 'body_template',),
            ),
            'classes': ('collapse',)
        }),


        ('Autorespond Email', {
            'fields': (
                ('autorespond', 'autorespond_email_field'),
                ('autorespond_subject_template', 'autorespond_body_template',),
            ),
            'classes': ('collapse',)
        }),
    )
    actions = ['clone_form',]

    class Meta:
        model = DynaFormForm

    def clone_form(self, request, queryset):
        for obj in queryset:
            obj.clone()
    clone_form.short_description = "Clonar formulario"


class DynaFormTrackingForm(forms.ModelForm):
    data = forms.CharField(widget=DummyTextInput, required=False)
    
    class Meta:
        model = DynaFormTracking
        fields = [
                'site', 
                'lang', 
                'sender',
                'data'
                ]


class DynaFormTrackingAdmin(admin.ModelAdmin):
    list_display = ('sender', 'site', 'pub_date')
    list_filter = ('sender', 'site')
    date_hierarchy = 'pub_date'
    actions = ['export_selected']
    form = DynaFormTrackingForm

    def export_selected(modeladmin, request, queryset):
        qs = [
                dict(sender=obj.sender, site=obj.site, pub_date=obj.pub_date, data=obj.data)
                for obj in queryset
            ]

        json2csv = JSON2CSV()
        csv_data = json2csv.json2csv(qs)

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export_dynaformtracking.csv"'
        
        writer = csv.DictWriter(response, fieldnames=csv_data['header'])
        writer.writeheader()
        writer.writerows(csv_data['data'])

        return response
    export_selected.short_description = u"Export Selected"



admin.site.register(DynaFormTracking, DynaFormTrackingAdmin)
admin.site.register(DynaFormForm, DynaFormFormAdmin)
admin.site.register(DynaFormTemplate, DynaFormTemplateAdmin)
