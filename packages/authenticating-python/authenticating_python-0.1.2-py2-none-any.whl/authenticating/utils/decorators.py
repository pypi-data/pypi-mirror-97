from requests.exceptions import (
    HTTPError, 
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    URLRequired,
    TooManyRedirects,
    MissingSchema,
    InvalidHeader,
    InvalidURL,
    InvalidSchema,
    InvalidProxyURL,
    ChunkedEncodingError,
    ContentDecodingError,
    StreamConsumedError,
    RetryError,
    UnrewindableBodyError,
)
from functools import wraps


def requests_exception_handling(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (
            HTTPError, ConnectionError, ProxyError,
            SSLError, Timeout, URLRequired,
            TooManyRedirects, MissingSchema, InvalidHeader,
            InvalidURL, InvalidSchema, InvalidProxyURL,
            ChunkedEncodingError, ContentDecodingError, StreamConsumedError,
            RetryError, UnrewindableBodyError,
        ) as error:
            raise 'the following {error} has occured'.format(error=error)
    return wrapper_function

