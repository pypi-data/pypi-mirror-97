from enum import IntEnum

# NOTE:  These enums are unused right now.  They have been added in preparation for API redesign efforts.
from typing import Union, List, Any, Dict, Optional

from DKModules.DKLogger import DKLogger


class SuccessCode(IntEnum):
    OK = 200
    Created = 201
    Accepted = 202
    NoContent = 204


class RedirectCode(IntEnum):
    MultipleChoices = 300
    Moved = 301
    Found = 302
    SeeOther = 303
    NotModified = 304
    TempRedirect = 307
    Redirect = 308


class ErrorCode(IntEnum):
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    MethodNotAllowed = 405
    NotAcceptable = 406
    RequestTimeout = 408
    Conflict = 409
    Gone = 410
    PreconditionFailed = 412
    PayloadTooLarge = 413


class ServerErrorCode(IntEnum):
    InternalServerError = 500
    NotImplemented = 501
    BadGateway = 502
    ServiceUnavailable = 503
    GatewayTimeout = 504


# --- REST API Response Errors mapping to 4xx status codes --- #
class HttpResponseError(Exception):
    def __init__(
        self,
        message: str,
        code: Union[ErrorCode, ServerErrorCode],
        data: Optional[Union[List[str], Dict[str, Any]]] = None,
    ) -> None:
        self.data = data
        self.message = message
        self.code = code
        if self.data and not self.message:
            self.message = "A problem has been encountered while processing the request"
        try:
            DKLogger.error(f"{self.__class__.__name__} [{self.code}]: {self.message}\n{self.data}")
        except:
            pass
        super().__init__(self.message)


class InternalServerError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ServerErrorCode.InternalServerError, data=data)


class BadRequestError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.BadRequest, data=data)


class UnauthorizedError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.Unauthorized, data=data)


class ForbiddenError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.Forbidden, data=data)


class NotFoundError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.NotFound, data=data)


class MethodNotAllowedError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.MethodNotAllowed, data=data)


class NotAcceptableError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.NotAcceptable, data=data)


class RequestTimeoutError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.RequestTimeout, data=data)


class ConflictError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.Conflict, data=data)


class GoneError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.Gone, data=data)


class PreconditionFailedError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.PreconditionFailed, data=data)


class PayloadTooLargeError(HttpResponseError):
    def __init__(self, message: str, data: Optional[Union[List[str], Dict[str, Any]]] = None) -> None:
        super().__init__(message, code=ErrorCode.PayloadTooLarge, data=data)


# ------------------------------------------------------------ #


# --- Misc REST Utility Errors --- #
class RequestObjectError(BadRequestError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class QueryParamMissingError(RequestObjectError):
    def __init__(self, expected: str, actual: List[str]) -> None:
        super().__init__(f'Could not find query parameter "{expected}" in [{", ".join(actual)}]')


class RequestObjectMalformedError(RequestObjectError):
    def __init__(self, missing: str) -> None:
        super().__init__(f'"request" object malformed, missing "{missing}" property')


class RequestObjectMissingUserInfoError(RequestObjectError):
    def __init__(self, missing: Union[List[str], str]) -> None:
        if isinstance(missing, list):
            keys = '", "'.join(missing)
        else:
            keys = missing
        super().__init__(f'"request" object missing required user info key(s): "{keys}"')


# -------------------------------- #

# --- System Route Errors --- #
class FileFailedToCompileError(BadRequestError):
    def __init__(self, data: List[str]) -> None:
        msg = "The file failed to compile.  See 'error_details' for more info"
        super().__init__(message=msg, data=data)


# --------------------------- #


# --- Auth0 & Token Errors --- #
class Auth0Error(UnauthorizedError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TokenExpiredError(Auth0Error):
    def __init__(self) -> None:
        super().__init__("Token is expired")


class InvalidAudienceError(Auth0Error):
    def __init__(self) -> None:
        super().__init__("Invalid audience")


class InvalidTokenSignatureError(Auth0Error):
    def __init__(self) -> None:
        super().__init__("Token signature is invalid")


class InvalidIssuedAtError(Auth0Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TokenRefreshError(Auth0Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


# ---------------------------- #


# --- Access Control Errors --- #
class AccessControlError(UnauthorizedError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UserInformationMissingError(AccessControlError):
    def __init__(self) -> None:
        super().__init__("User profile information not found")


# -------------------------------- #
