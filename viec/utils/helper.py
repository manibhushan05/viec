import re

EXT_REGEX = re.compile(r'^.*\.([A-Za-z0-9]{0,4})$')
EXT_DEFAULT = 'jpg'


def get_ext(filename, default=EXT_DEFAULT):
    filename = None if not filename else filename.strip()
    if not filename:
        return default

    match = EXT_REGEX.match(filename)
    if not match:
        return default

    try:
        ext = match.groups()[0]
        ext = None if not ext else ext.strip()
    except IndexError:
        ext = None

    return ext or default


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except (model.DoesNotExist, ValueError) as err:
        return None
    except model.MultipleObjectsReturned:
        return model.objects.filter(**kwargs).last()
    except TypeError:
        return None
