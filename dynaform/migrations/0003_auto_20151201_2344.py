# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynaform', '0002_auto_20150527_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynaformfield',
            name='field_widget',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'Simple', ((b'TextInput', b'TextInput'), (b'PasswordInput', b'PasswordInput'), (b'HiddenInput', b'HiddenInput'), (b'DateInput', b'DateInput'), (b'DateTimeInput', b'DateTimeInput'), (b'TimeInput', b'TimeInput'), (b'Textarea', b'Textarea'))), (b'Multiples', ((b'CheckboxInput', b'CheckboxInput'), (b'Select', b'Select'), (b'SelectSelectedDisableFirst', b'SelectSelectedDisableFirst'), (b'NullBooleanSelect', b'NullBooleanSelect'), (b'SelectMultiple', b'SelectMultiple'), (b'RadioSelect', b'RadioSelect'), (b'CheckboxSelectMultiple', b'CheckboxSelectMultiple'))), (b'Fechas', ((b'SplitDateTimeWidget', b'SplitDateTimeWidget'), (b'SelectDateWidget', b'SelectDateWidget'), (b'HTML5DateWidget', b'HTML5DateWidget'), (b'HTML5TimeWidget', b'HTML5TimeWidget'))), (b'Archivos/Imagenes', ((b'FileInput', b'FileInput'), (b'ClearableFileInput', b'ClearableFileInput'))), (b'Foundation', ((b'FoundationRadioSelectWidget', b'FoundationRadioSelectWidget'), (b'FoundationCheckboxSelectMultipleWidget', b'FoundationCheckboxSelectMultipleWidget'), (b'FoundationURLWidget', b'FoundationURLWidget'), (b'FoundationImageWidget', b'FoundationImageWidget'), (b'FoundationThumbnailWidget', b'FoundationThumbnailWidget')))]),
        ),
    ]
