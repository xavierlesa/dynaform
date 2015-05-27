# *-* coding:utf-8 *-*
import json
from django import forms
from dynaform.forms import widgets as custom_widgets

# Try importing ReCaptchaField
try:
    import ReCaptchaField
except ImportError:
    print 'ReCaptchaField was not loaded'


class CheckOtherField(forms.fields.MultiValueField):
    widget = custom_widgets.CheckOtherWidget
 
    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.BooleanField(required=False),
                       forms.fields.CharField()]
        super(CheckOtherField, self).__init__(list_fields, *args, **kwargs)
 
    def compress(self, values):
        return json.dumps(values)



