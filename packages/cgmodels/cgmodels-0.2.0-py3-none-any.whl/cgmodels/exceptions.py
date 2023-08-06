class ModelError(Exception):

    """
    Base exception for the package
    """

    def __init__(self, message: str):
        super(ModelError, self).__init__()
        self.message = message


class SampleSheetError(ModelError):
    """Raised when something is wrong with the orderform"""
