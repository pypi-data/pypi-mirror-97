def details(app_id, lang):
    if not isinstance(app_id, str):
        raise TypeError("'app_id' must be of type str.")
    if not id:
        raise ValueError("'app_id' cannot be empty.")

    if not isinstance(lang, str):
        raise TypeError("'lang' must be of type str.")
    if not lang:
        raise ValueError("'lang' cannot be empty.")