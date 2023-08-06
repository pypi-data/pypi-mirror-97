from functools import wraps
from importlib import util as importlib_util
from re import split
from typing import Dict, Optional, Tuple

try:
    import jwt
except ImportError:
    pass

try:
    from bson import ObjectId
    from bson.errors import InvalidId
except ImportError:
    pass

from werkzeug.routing import BaseConverter, ValidationError

from flask import abort, json, make_response, request
from pronto_commons.exceptions import BusinessException

marshmallow_spec = importlib_util.find_spec("marshmallow")
mongoengine_spec = importlib_util.find_spec("mongoengine")


def build_validation_error_response(*, errors: Dict) -> Tuple[Dict, int]:
    """Function that builds the error response that the frontend expects
    when a validation error ocurrs while parsing the request arguments

    :param Dict errors: The errors thaat were thrown by marshmallow (or any other library),
        when doing a validation.
    :return: Tuple[str, int]
        - Dict[str, Dict] [0] - The errors passed as an argument, inside a dictionary with
            the key errors
        - int [1] - The number 422, which tells us the error we should return on flask is an HTTP 422 code.

    ============================
             Example
    ============================

    In[1]: errors = {"name": ["Name is not valid"]}
    In[2]: build_validation_error_response(errors=errors)
    Out[2]: ({"errors": {"name": ["Name is not valid"]}}, 422)
    """
    return {"errors": errors}, 422


def build_business_error_response(*, errors: Dict) -> Tuple[Dict, int]:
    """Function that builds the error response that the frontend expects
    when a business error ocurrs.

    :param Dict errors: The errors that were thrown by the business exception.
    :return: Tuple[str, int]
        - Dict[str, str] [0] - The errors passed as they are
        - int [1] - The number 409, which tells us the error we should return on flask is an HTTP 409 code.

    ============================
             Example
    ============================

    In[1]: errors = {"code": "code", "message": "message·}
    In[2]: build_business_error_response(errors=errors)
    Out[2]: ({"code": "code", "message": "message·}, 409)
    """
    return errors, 409


def parse_errors(func):
    """A decorator that wraps a flask view, and parses the exceptions that could happen
    returning or raising a correspondent value, depending on the exception.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if marshmallow_spec:
                from marshmallow import exceptions

                if isinstance(e, exceptions.ValidationError):
                    return build_validation_error_response(errors=e.messages)

            if mongoengine_spec:
                from bson.errors import InvalidId
                from mongoengine import DoesNotExist

                if isinstance(e, DoesNotExist):
                    abort(404)
                elif isinstance(e, InvalidId):
                    abort(400)

            if isinstance(e, BusinessException):
                return build_business_error_response(errors=e.serialize())

            raise e

    return wrapper


def _decode_jwt_from_headers(*, header_name: str, header_type: str):
    """Copied from https://github.com/vimalloc/flask-jwt-extended/blob/master/flask_jwt_extended/view_decorators.py#L173
    Copied so we don't depend on the library
    """

    # Verify we have the auth header
    auth_header = request.headers.get(header_name, None)
    if not auth_header:
        raise jwt.InvalidTokenError("Header not found on request")

    # Make sure the header is in a valid format that we are expecting, ie
    # <HeaderName>: <HeaderType(optional)> <JWT>
    jwt_header = None

    # Check if header is comma delimited, ie
    # <HeaderName>: <field> <value>, <field> <value>, etc...
    if header_type:
        field_values = split(r",\s*", auth_header)
        _jwt_header = [s for s in field_values if s.split()[0] == header_type]
        if len(_jwt_header) < 1 or len(_jwt_header[0].split()) != 2:
            msg = "Bad {} header. Expected value '{} <JWT>'".format(
                header_name, header_type
            )
            raise jwt.InvalidTokenError(msg)
        jwt_header = _jwt_header[0]
    else:
        jwt_header = auth_header

    if not jwt_header:
        raise jwt.InvalidTokenError("Header not found at all")
    parts = jwt_header.split()
    if not header_type:
        if len(parts) != 1:
            msg = "Bad {} header. Expected value '<JWT>'".format(header_name)
            raise jwt.InvalidTokenError(msg)
        encoded_token = parts[0]
    else:
        encoded_token = parts[1]

    return encoded_token, None


def requires_jwt_authentication(
    jwt_secret_key: str,
    verify_exp=False,
    validate_refresh_token=False,
    sub: Optional[str] = None,
    header_name: str = "Authorization",
    header_type: str = "Bearer",
):
    from pronto_commons.jwt import decode_jwt

    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                token, _ = _decode_jwt_from_headers(
                    header_name=header_name, header_type=header_type
                )
                decoded_token = decode_jwt(
                    jwt_token=token,
                    verify_exp=verify_exp,
                    jwt_secret_key=jwt_secret_key,
                )
            except (
                jwt.ExpiredSignatureError,
                jwt.DecodeError,
                jwt.InvalidTokenError,
            ) as e:

                abort(401)

            if validate_refresh_token:
                if (
                    decoded_token.get("typ") != "refresh"
                ):  # Validation on the typ claim, it has to be a refresh token
                    abort(401)

            if sub:
                if decoded_token.get("sub") != sub:
                    # We validate that the sub is supposed to be the one we want
                    abort(401)

            _kwargs = {**kwargs, "jwt_token": decoded_token}
            return func(*args, **_kwargs)

        return wrapper

    return wrap


def handle_exception(e: Exception):
    """Return JSON instead of HTML for HTTP errors."""
    try:
        raise e
    except:
        import traceback

        traceback.print_exc()
    data = json.dumps(
        {
            "code": "server_error",
            "message": repr(type(e).__name__),
        }
    )
    response = make_response(data, 500)
    response.content_type = "application/json"
    return response


class ObjectIdConverter(BaseConverter):
    def to_python(self, value: str) -> ObjectId:
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError()

    def to_url(self, value: ObjectId) -> str:
        return str(value)
