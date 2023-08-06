"""All functions functions must be common in all files."""
def list_get(data, pos, default=None):
    "Access multidimensional list returning default if an exception is raised."
    for p in pos:
        try:
            data = data[p]
        except:
            data = default
            break
    return data