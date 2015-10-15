# +-+ coding:utf-8 +-+

from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.http import HttpResponse
from models import DynaFormTracking, DynaFormField, DynaFormTemplate, DynaFormForm
from dummy_form import DummyTextInput


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
        app, module = ("dynaform", "dynaformtracking")
        try:
            fields = queryset.model._meta.get_fields()
        except:
            fields = modeladmin.model._meta.fields

        fields = ['sender', 'site', 'pub_date']
        fields.extend(queryset[0].get_data().keys())
        csv_data = "\t".join([u"%s" % f for f in fields]) + "\r\n"
        for data in queryset:
            csv_data = csv_data + "\t".join([u"%s" % f for f in \
                    [data.sender, data.site.name, data.pub_date.strftime("%d/%m/%Y"), "\t".join(data.get_data().values())] ]) + "\r\n"
        response = HttpResponse(csv_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = "attachment; filename=%s-%s.xls" % (app, module) 
        return response
    export_selected.short_description = u"Export Selected"



admin.site.register(DynaFormTracking, DynaFormTrackingAdmin)
admin.site.register(DynaFormForm, DynaFormFormAdmin)
admin.site.register(DynaFormTemplate, DynaFormTemplateAdmin)
