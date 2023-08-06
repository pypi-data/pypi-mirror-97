def has_all(object, names):
    for name in names:
        exists = callable(getattr(object, name, None))
        if not exists:
            return False
    return True


def get_missing(object, names):
    missing = []
    for name in names:
        exists = callable(getattr(object, name, None))
        if not exists:
            missing.append(name)
    if missing:
        return missing
    return None
