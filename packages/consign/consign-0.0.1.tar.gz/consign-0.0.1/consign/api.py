def consign(nature, data, location, **kwargs):
    """Constructs and sends a :class:`Request <Request>`.
    :param nature: nature for the new :class:`Request` object: ``CSV``, ``JSON``, ``SQL``.
    :param data: data for the new :class:`Request` object.
    :param location: path for the new :class:`Request` object.
    """
    pass


def csv(data, location, delimiter=",", **kwargs):
    r"""Stores a CSV file locally.

    :param data: data for the new :class:`Request` object.
    :param location: path for the new :class:`Request` object.
    """
    return consign("csv", data, location, **kwargs)


def json(data, location, **kwargs):
    r"""Stores a JSON file locally.

    :param data: data for the new :class:`Request` object.
    :param location: path for the new :class:`Request` object.
    """
    return consign("json", data, location, **kwargs)
