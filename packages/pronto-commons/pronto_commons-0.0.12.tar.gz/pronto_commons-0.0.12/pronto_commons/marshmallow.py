from decimal import Decimal
from typing import Optional
from warnings import warn

try:
    from bson import ObjectId
except ImportError:
    warn("bson is not found and it's used for some classes inside this file")

try:
    import phonenumbers
except ImportError:
    warn("phonenumbers is not found and it's used for some classes inside this file")


from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate, validates
from pronto_commons.entities import PhoneNumber
from pronto_commons.images import convert_base64_to_image, return_extension_from_base64
from pronto_commons.utils import FileBytesExtension

not_empty = validate.Length(min=1)


class PaginationSchema(Schema):
    has_more = fields.Bool()
    has_previous = fields.Bool()
    page = fields.Int()
    total_items = fields.Int()
    total_pages = fields.Int()


class ValidatePaginationQueryParams(Schema):
    page = fields.Int(validate=validate.Range(min=1))

    class Meta:
        unknown = EXCLUDE


class LocationSchema(Schema):
    latitude = fields.Str()
    longitude = fields.Str()

    @validates("latitude")
    def validate_latitude(self, value):
        try:
            _value = Decimal(value)
            if _value == 0:
                raise ValidationError("Latitude can not be 0")
        except Exception as e:
            raise ValidationError("Latitude can not be 0")

    @validates("longitude")
    def validate_longitude(self, value):
        try:
            _value = Decimal(value)
            if _value == 0:
                raise ValidationError("Longitude can not be 0")
        except Exception as e:
            raise ValidationError("Longitude can not be 0")

    class Meta:
        unknown = EXCLUDE


class Base64ImageField(fields.Field):
    """Field to accept base64 images on json requests and decodes them to an io.Bytes"""

    def _deserialize(self, value, *args, **kwargs) -> FileBytesExtension:
        """Function to deserialize the field
        :return: A list being the first item on the list the bytes of the file,
            and the second the extension
        """
        try:
            profile_picture_extension = return_extension_from_base64(value)
            if not profile_picture_extension:
                raise ValidationError("No extension found on image")
            return FileBytesExtension(
                (convert_base64_to_image(value), profile_picture_extension)
            )
        except Exception as e:
            raise ValidationError(
                "The image must be a valid base64 string with an extension"
            ) from e


class PhoneField(fields.Field):
    """Field to validate a phone number format on a request"""

    def _deserialize(self, value, *args, **kwargs) -> PhoneNumber:
        try:
            phone_parsed = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_parsed):
                raise ValidationError("The format of the phone number is not valid")
            return PhoneNumber(
                country_code=str(phone_parsed.country_code),
                national_number=str(phone_parsed.national_number),
            )
        except Exception as e:
            raise ValidationError(
                "The phone number must follow an international format"
            ) from e


class ObjectIdField(fields.Field):
    """Field to validate an  ObjectId format on a request"""

    def _serialize(self, value, *args, **kwargs) -> Optional[str]:
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, *args, **kwargs) -> ObjectId:
        try:
            return ObjectId(value)
        except Exception as e:
            raise ValidationError("The field must be a valid ObjectId") from e
