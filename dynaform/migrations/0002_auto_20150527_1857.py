# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynaform', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dynaformfield',
            options={'ordering': ['field_order']},
        ),
        migrations.AddField(
            model_name='dynaformfield',
            name='field_order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
