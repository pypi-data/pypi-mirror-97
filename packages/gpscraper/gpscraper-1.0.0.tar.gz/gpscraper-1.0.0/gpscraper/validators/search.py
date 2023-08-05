def search(query, token, unknown_1, pagination_delay, lang):
    if not isinstance(query, str):
        raise TypeError('query must be of type str.')
    if not query:
        raise ValueError('query cannot be empty.')

    if not isinstance(token, str) and token is not None:
        raise TypeError("'token' must be either type str or None.")
    if isinstance(token, str) and not token:
        raise ValueError("'token' cannot be empty.")

    if not isinstance(unknown_1, str) and unknown_1 is not None:
        raise TypeError('unknown_1 must be either type str or None.')
    if isinstance(unknown_1, str) and not unknown_1:
        raise ValueError('unknown_1 cannot be empty.')

    if not isinstance(pagination_delay, (int, float)):
        raise TypeError("'pagination_delay' must be of type (int | float).")
    if pagination_delay < 0:
        raise ValueError("'pagination_delay' can not be negative.")

    if not isinstance(pagination_delay, (int, float)):
        raise TypeError("'pagination_delay' must be of type (int | float).")
    if pagination_delay < 0:
        raise ValueError("'pagination_delay' can not be negative.")

    if not isinstance(lang, str):
        raise TypeError("'lang' must be of type str.")
    if not lang:
        raise ValueError("'lang' cannot be empty.")
