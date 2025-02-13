from django import template

register = template.Library()

@register.filter(name='times')
def times(value):
    try:
        return range(value)
    except TypeError:
        return range(0)  # Return an empty range if the value is invalid
