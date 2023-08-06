from . import sessions


def consign(nature, data, location, **kwargs):
    """Constructs and sends a :class:`Request <Request>`.
    :param nature: nature for the new :class:`Request` object: ``CSV``, ``JSON``, ``SQL``.
    :param data: data for the new :class:`Request` object.
    :param location: path for the new :class:`Request` object.
    """
    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    with sessions.Session() as session:
        return session.consign(nature=nature, data=data, location=location, **kwargs)


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
