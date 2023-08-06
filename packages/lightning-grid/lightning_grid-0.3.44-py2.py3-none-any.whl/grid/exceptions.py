class AuthenticationError(Exception):
    """Risen when the user is not authenticated."""
    pass


class TrainError(Exception):
    """
    Risen whenever we have an exception during a training
    operation.
    """
    pass
