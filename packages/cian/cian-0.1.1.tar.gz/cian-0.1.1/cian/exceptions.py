class CianException(Exception):
    """Base class for exceptions"""


class CianStatusException(CianException):
    """Incorrect status in response from cian server"""

    def __init__(self, status):
        super().__init__(f"Status in response from cian is not 'ok'. Status: {status}")
