from . import sessions


def consign(method, data, url, **kwargs):
    """Constructs and sends a :class:`Request <Request>`.
    :param method: method for the new :class:`Request` object: ``CSV``, ``JSON``, ``SQL``.
    :param data: data for the new :class:`Request` object.
    :param url: path for the new :class:`Request` object.
    :param delimiter: delimiter used to separate elements in a CSV row.
    """
    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    with sessions.Session() as session:
        return session.consign(method=method, data=data, url=url, **kwargs)


def csv(data, url, **kwargs):
    r"""Stores a CSV file locally.

    :param data: data for the new :class:`Request` object.
    :param url: path for the new :class:`Request` object.
    """
    return consign("csv", data, url, **kwargs)


def json(data, url, **kwargs):
    r"""Stores a JSON file locally.

    :param data: data for the new :class:`Request` object.
    :param url: path for the new :class:`Request` object.
    """
    return consign("json", data, url, **kwargs)
