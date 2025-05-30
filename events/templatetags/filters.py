from django import template

register = template.Library()

@register.filter
def truncate_without_ellipsis(value, length):
    """Zkrátí text bez přidání tří teček"""
    if len(value) > length:
        return value[:length]
    return value
    
@register.filter
def m_2_km(value):
    try:
        return value / 1000
    except (ValueError, TypeError):
        return value

@register.filter   # zobrazit formát času
def format_HHMM(value):   
    if value is not None:
        return value.strftime('%H:%M')
    return 'No time provided'

