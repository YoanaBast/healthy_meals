from django import template

register = template.Library()

@register.filter
def get(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None

@register.filter
def get_unit(measurements, unit):
    return measurements.filter(unit=unit).first()

@register.filter
def name_for_quantity(unit, quantity):
    return unit.name_for_quantity(quantity)

@register.filter
def smart_float(value):
    try:
        f = round(float(value), 2)
        return int(f) if f == int(f) else f
    except (ValueError, TypeError):
        return value

@register.filter
def split(value, delimiter=" "):
    return value.split(delimiter)