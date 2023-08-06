import csv
import json



class Session():
    """
    """

    def __init__(self):
    

    def prepare_consignment(self, consign):
        """
        """
        

    def consign(self, nature, data, location):
        """Constructs a :class:`Consign <Consign>`, prepares it and stores it.
        """

        # Creates the Consignment.
        csgn = Consignment(
            nature=nature.upper(),
            data=data,
            location=location
        )

        # Prepares the Consignment.
        luggage = self.prepare_consignment(csgn)

        # Stores the Luggage.
        resp = self.store(luggage)

        return resp
