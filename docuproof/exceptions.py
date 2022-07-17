from sanic.exceptions import SanicException


class Http404(SanicException):
    status_code = 404
    message = "Not found"
    quiet = True


class HttpBadRequest(SanicException):
    status_code = 400
    message = "Bad request"
    quiet = True


class HttpInternalServerError(SanicException):
    status_code = 500
    message = "Internal server error"
