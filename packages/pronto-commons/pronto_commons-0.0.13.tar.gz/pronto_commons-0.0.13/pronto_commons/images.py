import base64
import io
from mimetypes import guess_extension, guess_type
from typing import Dict, Optional
from warnings import warn

try:
    from PIL import Image
except ImportError:
    warn(
        "PIL is not found and it is used in some methods inside this library",
        ImportWarning,
    )

from pronto_commons.utils import MB_BYTES


def return_extension_from_base64(*, base64_string: str) -> Optional[str]:
    """Function to return the extension from a base64 image
    :param str base64_string: The image represented as a base64 string
    :rtype: Optional[str]
    :return: The extension with a dot such as .png or None
    """
    guessed = guess_type(base64_string)
    if guessed[0] is None:
        return None

    jpg_list = ["image/jpg", "image/jpeg"]
    if guessed[0] in jpg_list:
        return ".jpg"
    return guess_extension(guessed[0])


def compress_image(
    *,
    image_bytes: io.BytesIO,
    extension: str,
    maximum_image_size_bytes: int = MB_BYTES,
) -> io.BytesIO:
    # The extension must be only the format such as jpeg, png, without a prefix-point
    extension = extension.lower()

    if extension == "jpg":
        # PIL IMAGE doesn't accept JPG
        extension = "jpeg"
    bytes_size = image_bytes.getbuffer().nbytes
    if bytes_size <= maximum_image_size_bytes:
        # We don't need to resize, is useless it's already below the limit
        return image_bytes
    else:
        quality_factor = 1 / (bytes_size / maximum_image_size_bytes)
        quality_factor = (
            quality_factor * 100
        )  # The quality factor must be  multiple of 10
        quality_factor = int(quality_factor)
        new_image_bytes = io.BytesIO()
        # Optimizing image
        image = Image.open(image_bytes)
        if extension == "jpeg" and image.mode != "RGB":
            # RGB is required to save as JPEG
            image = image.convert("RGB")
        new_width = int(image.width * (quality_factor / 100))
        new_heigth = int(image.height * (quality_factor / 100))

        image = image.resize((new_width, new_heigth), Image.ANTIALIAS)

        image.save(
            new_image_bytes,
            format=extension,
            optimize=True,
            quality=quality_factor,
        )

        new_image_bytes.seek(0)

        if new_image_bytes.getbuffer().nbytes > bytes_size:
            # If the image is too small there is a bug, which will give us a not optimized image
            image_bytes.seek(0)
            return image_bytes

        new_image_bytes.seek(0)
        return new_image_bytes


def convert_base64_to_image(*, base64_string: str) -> io.BytesIO:
    """Function to convert a base64 image into bytes
    :param str base64_string: The base64 image string
    :rtype: io.BytesIO
    :return: A bytes object, that represents the image
    """
    encoded_data = base64_string.split(",")[1]
    return io.BytesIO(base64.b64decode(encoded_data))
