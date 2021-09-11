def get(obj, key, required_type=None):
    """Return the value with the specified key in obj if it exists, otherwise return None.

    If required_type is not None, a TypeError will be raised if the corresponding value
    is not an instance of required_type.
    """
    if key not in obj:
        return None
    if required_type is not None and not isinstance(obj[key], required_type):
        raise TypeError(f'{key} is not a {required_type}')
    return obj[key]


def require(obj, key, required_type=None):
    """Return the value with the specified key in obj if it exists, otherwise raise a KeyError.

    If required_type is not None, a TypeError will be raised if the corresponding value
    is not an instance of required_type.
    """
    if key not in obj:
        raise KeyError(f'{key} not found')
    if required_type is not None and not isinstance(obj[key], required_type):
        raise TypeError(f'{key} is not a {required_type}')
    return obj[key]
