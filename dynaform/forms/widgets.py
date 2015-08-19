# *-* coding:utf-8 *-*

from itertools import chain
from django.utils.encoding import force_text
from django.utils.html import format_html

import json
from django import forms
from django.forms.widgets import TextInput, FileInput, Select
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

#from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.encoding import force_unicode
from django.conf import settings


class FoundationCheckboxSelectMultipleWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        html = super(FoundationCheckboxSelectMultipleWidget, self).render(name, value, attrs, choices)
        return mark_safe(html.replace('<ul>', '<ul class="inline-list">'))

class FoundationRadioSelectWidget(forms.RadioSelect):
    def render(self, name, value, attrs=None, choices=()):
        html = super(FoundationRadioSelectWidget, self).render(name, value, attrs, choices)
        return mark_safe(html.replace('<ul>', '<ul class="inline-list">'))

class FoundationURLWidget(TextInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        html = """
            <div class="row collapse">
                <div class="large-2 two small-1 mobile-one columns">
                    <span class="prefix">URL</span>
                </div>
                <div class="large-10 ten small-3 mobile-three columns">
                    <input%s />
                </div>
            </div>
        """
        return mark_safe(html % flatatt(final_attrs))

class FoundationImageWidget(FileInput):
    html = """
        <div class="row">
            <div class="twelve columns">
                <span class="th"><img src="%(MEDIA_URL)s%(value)s" /></span>
            </div>
        </div>
        <div class="row">
            <div class="two columns">
                <input%(flat_attrs)s />
            </div>
        </div>
    """

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        final_attrs.update({
            'MEDIA_URL': settings.MEDIA_URL,
            'flat_attrs': flatatt(final_attrs),
        })

        return mark_safe(self.html % final_attrs)

class FoundationThumbnailWidget(FoundationImageWidget):
    html = """
        <div class="row">
            <div class="two mobile-six columns">
                <span class="th"><img src="%(MEDIA_URL)s%(value)s" /></span>
            </div>
            <div class="ten mobile-six columns">
                <input%(flat_attrs)s />
            </div>
        </div>
    """

class CheckOtherWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.CheckboxInput(),
                   forms.TextInput()]
        super(CheckOtherWidget, self).__init__(widgets, attrs)
 
    def decompress(self, value):
        if value:
            return json.loads(value)
        else:
            return ['', '']


class SelectSelectedDisableFirst(forms.widgets.Select):
    """
    Select con el primer elemento Selected y Disabled

    """

    def render_option(self, selected_choices, option_value, option_label, selected_disabled=False):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        elif selected_disabled:
            selected_html = ' selected="selected" disabled'
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            elif len(output) < 1:
                # Asume que el primer elemento no tiene valor y es Selected Disabled
                output.append(self.render_option(selected_choices, option_value, option_label, selected_disabled=True))
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)
