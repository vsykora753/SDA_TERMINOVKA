from django import template

register = template.Library()

@register.filter
def truncate_without_ellipsis(value, length):
    """Zkrátí text bez přidání tří teček"""
    if len(value) > length:
        return value[:length]
    return value
