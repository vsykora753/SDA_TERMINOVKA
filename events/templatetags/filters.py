from django import template

register = template.Library()


@register.filter
def truncate_without_ellipsis(value, length):
    """
    Truncates a string to the specified length without adding ellipsis.

    Args:
        value: Input text to be truncated.
        length: Maximum number of characters in the resulting string.

    Returns:
        The truncated string if the original length exceeds 'length';
        otherwise returns the original text.
"""

    if len(value) > length:
        return value[:length]
    return value


@register.filter
def m_2_km(value):
    """
    Converts meters to kilometers.

    Args:
        value: Value in meters (int | float).

    Returns:
        Value in kilometers (value / 1000). If the input is non-numeric, it
        returns it unchanged.
    """

    try:
        return value / 1000
    except (ValueError, TypeError):
        return value


@register.filter  # zobrazit formát času
def format_HHMM(value):
    """
    Formats a time to a string in HH:MM format.

    Args:
        value: A time value (datetime.time | datetime.datetime | None).

    Returns:
        A string in 'HH:MM' format, or 'No time provided', if the value is
        None.
    """

    if value is not None:
        return value.strftime('%H:%M')
    return 'No time provided'


@register.filter
def get_item(dictionary, key):
    """
    Returns a value from a dictionary based on the specified key.

    Args:
        dictionary: The dictionary to read from.
        key: The key to look up the value.

    Returns:
        The value corresponding to 'key', or None if the key does not exist.
    """

    return dictionary.get(key)


@register.filter
def to(value, arg):
    """
    Creates a range of numbers from value to arg-1.

    Args:
        value: The starting value (int) of the range.
        arg: The ending value (unincluded).

    Returns:
        A range(value, arg) object.
    """

    return range(value, arg)


@register.filter
def get_index(list_, index):
    """
    Returns the list item at the given index.

    Args:
        list_: The list to select from.
        index: The position of the item in the list.

    Returns:
        The element at position 'index', or None if the index does not
        exist.
    """

    try:
        return list_[index]
    except:
        return None
