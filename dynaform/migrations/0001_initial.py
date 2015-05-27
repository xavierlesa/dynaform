# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dynaform.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynaFormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.PositiveIntegerField(null=True, verbose_name='object PK', blank=True)),
                ('field_name', models.SlugField(help_text='nombre del campo solo letras min\xfasculas, guinobajo y numeros ', max_length=200, verbose_name='Identificador del Campo')),
                ('field_label', models.CharField(help_text='nombre visible del campo', max_length=200, verbose_name='Etiqueta del Campo')),
                ('field_type', models.CharField(max_length=100, choices=[(b'BooleanField', b'BooleanField'), (b'CharField', b'CharField'), (b'ChoiceField', b'ChoiceField'), (b'DateField', b'DateField'), (b'DateTimeField', b'DateTimeField'), (b'DecimalField', b'DecimalField'), (b'EmailField', b'EmailField'), (b'FileField', b'FileField'), (b'FloatField', b'FloatField'), (b'ImageField', b'ImageField'), (b'IntegerField', b'IntegerField'), (b'RegexField', b'RegexField'), (b'SlugField', b'SlugField'), (b'TimeField', b'TimeField'), (b'URLField', b'URLField'), (b'NullBooleanField', b'NullBooleanField'), (b'MultipleChoiceField', b'MultipleChoiceField'), (b'ModelChoiceField', b'ModelChoiceField'), (b'ModelMultipleChoiceField', b'ModelMultipleChoiceField'), (b'ReCaptchaField', b'ReCaptchaField')])),
                ('field_widget', models.CharField(blank=True, max_length=100, null=True, choices=[(b'Simple', ((b'TextInput', b'TextInput'), (b'PasswordInput', b'PasswordInput'), (b'HiddenInput', b'HiddenInput'), (b'DateInput', b'DateInput'), (b'DateTimeInput', b'DateTimeInput'), (b'TimeInput', b'TimeInput'), (b'Textarea', b'Textarea'))), (b'Multiples', ((b'CheckboxInput', b'CheckboxInput'), (b'Select', b'Select'), (b'NullBooleanSelect', b'NullBooleanSelect'), (b'SelectMultiple', b'SelectMultiple'), (b'RadioSelect', b'RadioSelect'), (b'CheckboxSelectMultiple', b'CheckboxSelectMultiple'))), (b'Fechas', ((b'SplitDateTimeWidget', b'SplitDateTimeWidget'), (b'SelectDateWidget', b'SelectDateWidget'))), (b'Archivos/Imagenes', ((b'FileInput', b'FileInput'), (b'ClearableFileInput', b'ClearableFileInput'))), (b'Foundation', ((b'FoundationRadioSelectWidget', b'FoundationRadioSelectWidget'), (b'FoundationCheckboxSelectMultipleWidget', b'FoundationCheckboxSelectMultipleWidget'), (b'FoundationURLWidget', b'FoundationURLWidget'), (b'FoundationImageWidget', b'FoundationImageWidget'), (b'FoundationThumbnailWidget', b'FoundationThumbnailWidget')))])),
                ('field_help', models.CharField(max_length=200, verbose_name='Texto descripci\xf3n', blank=True)),
                ('is_required', models.BooleanField(default=True, verbose_name='Requerido')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Oculto')),
                ('default_value', models.CharField(help_text='Se pueden usar variables del contexto {{ object }}, {{ sites }}, etc', max_length=200, verbose_name='Valor por defecto', blank=True)),
                ('choices', models.TextField(help_text='Lista de "valor", "t\xedtulo" separada por el delimitador y por l\xednea', verbose_name='Lista de valores', blank=True)),
                ('choices_delimiter', models.CharField(default=b'|', max_length=1, verbose_name='Delimitador de valores por defecto es |', blank=True)),
                ('choices_queryset_filter', models.CharField(max_length=200, verbose_name='Filtros', blank=True)),
                ('choices_queryset_empty_label', models.CharField(default=b'------', max_length=100, verbose_name='Valor por defecto', blank=True)),
                ('choices_queryset_label', models.CharField(help_text='puede ser cualquier campo del modelo en formato, "%(nombre)s, %(apellido)s"', max_length=100, verbose_name='Formato', blank=True)),
                ('choices_queryset', models.ForeignKey(verbose_name='Modelo de Datos', blank=True, to='contenttypes.ContentType', null=True)),
                ('choices_related_field', models.ForeignKey(blank=True, to='dynaform.DynaFormField', null=True)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_dynaformfield', verbose_name='content type', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DynaFormForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(blank=True, max_length=20, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del form')),
                ('slug', models.SlugField(max_length=100)),
                ('is_active', models.BooleanField(default=True, help_text='activa para usar en el frontend', verbose_name='Es activo')),
                ('form_title', models.CharField(max_length=200, verbose_name='T\xedtulo del form')),
                ('send_email', models.BooleanField(default=True, verbose_name='Enviar mail')),
                ('from_email', models.CharField(default=b'webmaster@localhost', max_length=100, blank=True)),
                ('recipient_list', models.TextField(default=(), help_text='ej: lista separada por l\xedneas y coma.<br>Juan P\xe9rez, juanperez@dominio.com<br>Maria Gomez, mariagomez@dominio.com', verbose_name='Lista de destinatarios', blank=True)),
                ('error_class', models.CharField(default=b'error', max_length=40, verbose_name='Clase CSS para error')),
                ('required_css_class', models.CharField(default=b'required', max_length=40, verbose_name='Clase CSS para requerido')),
                ('autorespond', models.BooleanField(default=False, verbose_name='Autoresponder')),
                ('autorespond_email_field', models.CharField(default=b'email', max_length=40, verbose_name='Campo de email')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DynaFormTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(blank=True, max_length=20, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('name', models.CharField(help_text='ej: Subject Contacto', max_length=100, verbose_name='Nombre del template')),
                ('slug', models.SlugField(max_length=100)),
                ('html', models.TextField(help_text='parsea del contexto, y templatetags', verbose_name='HTML del Template')),
                ('is_plain', models.BooleanField(default=True)),
                ('site', models.ManyToManyField(related_name='dynaform_dynaformtemplate_related', null=True, to='sites.Site', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DynaFormTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de creaci\xf3n')),
                ('lang', models.CharField(default=b'en-us', max_length=20, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('sender', models.CharField(max_length=200)),
                ('data', dynaform.models.JsonField()),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
        ),
        migrations.AddField(
            model_name='dynaformform',
            name='autorespond_body_template',
            field=models.ForeignKey(related_name='dynaform_autorespond_body_template_related', blank=True, to='dynaform.DynaFormTemplate', null=True),
        ),
        migrations.AddField(
            model_name='dynaformform',
            name='autorespond_subject_template',
            field=models.ForeignKey(related_name='dynaform_autorespond_subject_template_related', blank=True, to='dynaform.DynaFormTemplate', null=True),
        ),
        migrations.AddField(
            model_name='dynaformform',
            name='body_template',
            field=models.ForeignKey(related_name='dynaform_body_template_related', blank=True, to='dynaform.DynaFormTemplate', null=True),
        ),
        migrations.AddField(
            model_name='dynaformform',
            name='form_template',
            field=models.ForeignKey(related_name='dynaform_form_template_related', blank=True, to='dynaform.DynaFormTemplate', null=True),
        ),
        migrations.AddField(
            model_name='dynaformform',
            name='site',
            field=models.ManyToManyField(related_name='dynaform_dynaformform_related', null=True, to='sites.Site', blank=True),
        ),
        migrations.AddField(
            model_name='dynaformform',
            name='subject_template',
            field=models.ForeignKey(related_name='dynaform_subject_template_related', blank=True, to='dynaform.DynaFormTemplate', null=True),
        ),
    ]
