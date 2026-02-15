from django import template

register = template.Library()

@register.filter
def nice_name(value):
    """
    Convert 'vitamin_b6' → 'Vitamin B6'
    """
    return value.replace("_", " ").title()
