# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def attach_sender_to_tracking(apps, schema_editor):
    """
    Busca todos los trakings disponibles y los asocia a un posible sender 
    via sender
    """

    DynaFormForm = apps.get_model("dynaform", "DynaFormForm")
    DynaFormTracking = apps.get_model("dynaform", "DynaFormTracking")

    for dynaform in DynaFormForm.objects.all():
        DynaFormTracking.objects.filter(sender=dynaform.name[:200]).update(object_form=dynaform)


class Migration(migrations.Migration):

    dependencies = [
        ('dynaform', '0003_auto_20151201_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynaformtracking',
            name='object_form',
            field=models.ForeignKey(blank=True, to='dynaform.DynaFormForm', null=True),
        ),
        migrations.AddField(
            model_name='dynaformtracking',
            name='utm_campaign',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dynaformtracking',
            name='utm_medium',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dynaformtracking',
            name='utm_source',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),

        migrations.RunPython(attach_sender_to_tracking),
    ]
