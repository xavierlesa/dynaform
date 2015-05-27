from django.conf.urls import patterns, include, url
from django.conf import settings
from dynaform.views import DynaformViewAJAX, DynaformChoicesRelatedFieldViewAJAX

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w\-\_\.]+)/(?P<pk>\d+)/?$', DynaformViewAJAX.as_view(), name='dynaform_action'),
    url(r'^(?P<field_pk>\d+)/(?P<related_field_pk>\d+)/(?P<pk>\d+)/?$', DynaformChoicesRelatedFieldViewAJAX.as_view(), name='dynaform_choices_related_queryset'),
)
