"""
Wavelet WSGI application framework.
"""

from typing import Self, Any, Callable
from enum import IntEnum
from functools import singledispatch
from argparse import ArgumentParser
import sys
from dataclasses import dataclass

"""
This module contains HTTP status codes.
"""

def is_informational_status_code(code: int) -> bool:
    return 100 <= code <= 199


def is_success_status_code(code: int) -> bool:
    return 200 <= code <= 299


def is_redirect_status_code(code: int) -> bool:
    return 300 <= code <= 399


def is_client_error_status_code(code: int) -> bool:
    return 400 <= code <= 499


def is_server_error_status_code(code: int) -> bool:
    return 500 <= code <= 599


class Status(IntEnum):
    """
    The HTTP status titles and codes.
    """
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226
    MULTIPLE_CHOICES = 300 
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    RESERVED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    REQUEST_ENTITY_TOO_LARGE = 413
    REQUEST_URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    ION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    BANDWIDTH_LIMIT_EXCEEDED = 509
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


class Request:
    """
    Request encapsulates the client data send via HTTP protocol.
    """

    methods = (
        "GET", "POST", "PUT", "DELETE", "TRACE", "CONNECT", "OPTIONS"
    )

    def __init__(self, scheme: str, domain: str, encoding: str = "utf-8"):
        self._scheme = scheme
        self._domain = domain
        self._encoding = encoding

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def encoding(self) -> str:
        return self._encoding

    def accepts(self, media_type: str):
        ...

    def headers(self):
        ...

    def is_safe(self) -> bool:
        return self.scheme in ("https",)


# GetRequest
# PostRequest
# DeleteRequest


class Response:
    """
    Response encapsulates server data send via HTTP response.
    """

    def __init__(self, status_code: int, content: str) -> None:
        self._status_code = status_code
        self._content = content

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def content(self) -> str:
        return self._content

    def __eq__(self, that: object) -> bool:
        if that is None or not isinstance(that, type(self)):
            return False 

        return (self.status_code, self.content) == (that.status_code, that.content)

    def __hash__(self) -> int:
        return hash((type(self), self.status_code, self.content))




@dataclass(frozen=True, slots=True)
class Header:
    ...

@dataclass(frozen=True,  slots=True)
class RequestHeader(Header):
    ...
    

@dataclass(frozen=True,  slots=True)
class ResponseHeader(Header):
    ...


@dataclass(frozen=True)
class URL:
    host: str
    port: int



def cli(arguments):    
    parser = ArgumentParser()
    
    parser.add_argument("--version", action="store_true", help="Show version number.")
    parser.add_argument("-p", "--port", action="store_true", help="Port")


# ########################################################################## #
# Exceptions
# ########################################################################## #

class WaveletException(Exception):
    """A base class exception."""
    pass

# ########################################################################## #


class Controller:
    def __init__(self) -> None:
        ...

    def handle(request) -> Response:
        return Response(200, "OK")


class Middleware:
    def __init__(self):
        ...



class Wavelet:
    """
    The WSGI application. 
    """

    def __init__(self) -> None:
        self.routes = {
            "...": lambda x: x, # handler
        }

    def register_controler(self):
        ...

    def __call__(self, environment: dict[str, str], start_response: Callable):
        
        body = f"Request method: {environment['REQUEST_METHOD']}"

        environment_items = "\n".join([f"{k}, {v}" for k, v in sorted(environment.items())])
    
        # HTTP_*
        # SERVER_*
        # wsgi.*
        
        headers = [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ("Content-Length", str(len(body + environment_items))),
        ]
        status = "200 OK"
        start_response(status, headers)

        yield [body.encode(), environment_items.encode()]


if __name__ == "__main__":

    arguments = sys.argv

    from wsgiref.simple_server import make_server
    
    wavelet = Wavelet()

    with make_server(host='localhost', port=8051, app=wavelet) as server:
        print("Running on localhost:8051")
        server.serve_forever()
        