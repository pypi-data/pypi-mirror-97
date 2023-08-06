import csv
import json

from .models import Consignment, PreparedConsignment


class Session():
    """
    """

    def __init__(self):
        pass


    def __enter__(self):
        return self


    def __exit__(self, *args):
        self.close()


    def prepare_consignment(self, consign):
        """
        """
        p = PreparedConsignment()
        p.prepare(
            method=consign.method.upper(),
            data=consign.data,
            url=consign.url,
            delimiter=consign.delimiter
        )
        return p


    def consign(self, method, data, url,
            delimiter=None):
        """Constructs a :class:`Consign <Consign>`, prepares it and stores it.
        """

        # Creates the Consignment.
        csgn = Consignment(
            method=method.upper(),
            data=data,
            url=url,
            delimiter=delimiter
        )

        # Prepares the Consignment.
        luggage = self.prepare_consignment(csgn)

        # Stores the Luggage.
        resp = self.store(luggage)

        return resp


    def store(self, luggage):
        """Send a given PreparedConsignment.
        """


    def close(self):
        """Closes all adapters and as such the session"""
        # for v in self.adapters.values():
        #     v.close()
        pass
