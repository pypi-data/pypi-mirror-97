class In1Exceptions(Exception):
    """Base class for in1 API exceptions."""

    pass


class NoResult(In1Exceptions):
    """Exception class in case inference was not successful for reasons other than:

    * Authentication failed
    * Quota was exceeded
    * Sent image was too large
    * Inference result did not pass quality control
    """

    def __init__(self, msg: str = ""):
        super().__init__(msg)


class DownloadFailed(In1Exceptions):
    """Exception class for instances where an image failed to download from the server."""

    def __init__(self, msg: str = ""):
        super().__init__(msg)


class AuthenticationError(In1Exceptions):
    """Exception class for instances related to failure to authenticate with the given
    api-key.
    """

    def __init__(self, msg: str = ""):
        super().__init__(msg)


class IncorrectImageGeneration(In1Exceptions):
    """Exception class for instances when the input image was incorrectly produced,
    resulting in malformed or corrupted image.
    """

    def __init__(self, msg: str = ""):
        super().__init__(msg)


class UnsupportedImageFormat(In1Exceptions):
    """Exception class for instances when the input image does not conform to format
    requirements. Causes include image too large, incorrect order or number of
    dimensions.
    """

    def __init__(self, msg: str = ""):
        super().__init__(msg)


class ServerError(In1Exceptions):
    """Exception class for all issues on the server's side. These are out of the
    end-user's control. Please contact in1 for further assistance.
    """

    def __init__(self, msg: str = ""):
        super().__init__(msg)


class InsufficientCredits(In1Exceptions):
    """Exception class for instances related to insufficient credits in the current in1
    account. Please update credits to continue using in1.
    """

    def __init__(self, msg: str = ""):
        super().__init__(msg)
