class TransitionError(Exception):
    """Raised when there's a state transition that's not
    allowed.

    Attributes:
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, message):
        self.message = message
