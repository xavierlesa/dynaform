# +-+ coding:utf-8 +-+

from django import forms
from django.forms.widgets import TextInput, Textarea 
from django.utils.safestring import mark_safe

class DummyTextInput(Textarea):
    def __init__(self,attrs=None, *args, **kwargs):
        super(DummyTextInput,self).__init__(attrs, *args, **kwargs)
    
    def decompress(self,value):
        if value:
            return value.keys()
        return [None,None]
        
    def render(self, name, value, attrs=None, *args, **kwargs):
        f = '<div style="overflow:hidden;margin:10px 0"><div style="float:left; width:100px"><b>%s</b></div><div style="float:left">%s</div></div>'
        ret = ''
        if isinstance(value, dict):
            for key,val in zip(value.keys(), value.values()):
                ret = ret + mark_safe(f % (key, val))
        elif isinstance(value, (list, tuple)):
             for key,val in zip(range(len(value)), value):
                ret = ret + mark_safe(f % (key, val))

        return mark_safe( super(DummyTextInput, self).render(name, value, attrs=attrs)  + '<div style="">%s</div>' % ret)


""" Dummy Field """
class DummyField(forms.MultiValueField):
    widget = DummyTextInput
