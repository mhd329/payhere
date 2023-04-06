from django import template


register = template.Library()


# 19글자 까지만 표시하고 뒤는 ...
@register.filter()
def long_slicer(value, arg: str):
    if len(arg) > 19:
        value = arg[:19] + "..."
    return value


# 4글자 까지만 표시하고 뒤는 ...
@register.filter()
def short_slicer(value, arg: str):
    if len(arg) > 4:
        value = arg[:4] + "..."
    return value
