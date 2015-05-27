temlatetags

    {% load getdynaform %}

    {% with forms=object|get_extra_content_for_key:'dynaform' object=object %}
    {% for form in forms %}
    {% dynaform_form form_slug=form.name success_url=form.field as object_form %}{{ object_form }}
    {% endfor %}
    {% endwith %}


