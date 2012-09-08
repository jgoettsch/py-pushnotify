#!/usr/bin/env python
# vim: set fileencoding=utf-8


class PushNotifyError(Exception):
    """Base exception for all pushnotify errors.

    Args:
        args[0]: A string containing a message.
        args[1]: An integer containing an error.

    """

    def __init__(self, *args):

        self.args = [arg for arg in args]


class FormatError(PushNotifyError):
    """Raised when a request is not in the expected format.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class ApiKeyError(PushNotifyError):
    """Raised when a provided API key is invalid

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class RateLimitExceeded(PushNotifyError):
    """Raised when too many requests are submitted in too small a time
    frame.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class ServerError(PushNotifyError):
    """Raised when the notification server experiences an internal error.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class UnknownError(PushNotifyError):
    """Raised when the notification server returns an unknown error.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class UnrecognizedResponseError(PushNotifyError):
    """Raised when the notification server returns an unrecognized
    response.

    Args:
        args[0]: A string containing the response from the server.
        args[1]: -1.

    """

    pass


if __name__ == '__main__':
    pass
