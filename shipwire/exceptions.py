class TheGameCrafterError(Exception):
    """
    Base Exception thrown by the TheGameCrafter object when there is a
    general error interacting with the API.
    """
    pass


class ResponseError(TheGameCrafterError):
    """
    Exception raised when a response indicating failure is encountered
    """

    def __init__(self, response):
        try:
            error_code = str(response.json()['error']['code'])
        except:
            error_code = "Unknown Code"

        try:
            message = response.json()['error']['message']
        except:
            message = "Unknown Message"

        try:
            data = response.json()['error']['data']
        except:
            data = ""

        super(ResponseError, self).__init__(
            'Error Code (%s): %s %s' %
            (error_code, message, data))
        self.response = response


class TimeoutError(TheGameCrafterError):
    """
    Exception raised when a timeout occurs.
    """
    pass
