"""Define package errors."""


class SmartWeatherError(Exception):
    """Define a base error."""

    pass


class InvalidApiKey(SmartWeatherError):
    """Define an error related to invalid or missing API Key."""

    pass


class RequestError(SmartWeatherError):
    """Define an error related to invalid requests."""

    pass

class ResultError(SmartWeatherError):
    """Define an error related to the result returned from a request."""

    pass
