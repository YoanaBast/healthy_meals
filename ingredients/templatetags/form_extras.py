from django import template

register = template.Library()

@register.filter
def get_item(form, field_name):
    return form[field_name]

@register.filter
def get_field(form, field_name):
    return form[field_name]

@register.filter
def get_label(form, field_name):
    return form[field_name].label_tag()
