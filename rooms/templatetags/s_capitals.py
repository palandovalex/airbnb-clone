from django import template


register = template.Library()
@register.filter()
def s_capitals(value):
    return f"s_capitals+{value}"
