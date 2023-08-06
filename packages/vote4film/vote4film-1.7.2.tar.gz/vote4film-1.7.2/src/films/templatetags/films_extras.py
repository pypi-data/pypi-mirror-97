from django import template

register = template.Library()


@register.filter("duration_format")
def duration_format(value):
    value = int(value)
    hours = value // 60
    minutes = value % 60
    h = "hr" if hours == 1 else "hrs"
    m = "min" if minutes == 1 else "mins"
    return f"{hours} {h}, {minutes} {m}"


@register.simple_tag
def define(val=None):
    return val
