import datetime
import io
import math
from decimal import Decimal
from typing import Dict, List, NewType, Optional, Tuple, TypeVar
from urllib.parse import urlparse

TWOPLACES = Decimal(10) ** -2
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
T = TypeVar("T")
MB_BYTES = 1024 * 1024
FileBytesExtension = NewType("FileBytesExtension", Tuple[io.BytesIO, str])


def get_jwt_token(*, dictionary: Dict) -> Dict:
    """Returns the JWT token from a dictionary that has a key `jwt_token` which contains
        the information about a JWT token, decrypted.

    :param Dict dictionary: The dictionary that contains the information
    :rtype: Dict
    :return:
        The dictionary containging the information, in case it doesn't exist, an empty dict is returned
    """
    return dictionary.get("jwt_token", {})


def get_url_path(*, url: str) -> str:
    """Function to retrieve the path from a URL
    :param str url: The whole url
    :rtype: str
    :return: The path of the url
    """
    path = urlparse(url).path
    return path


def generate_pagination(*, page: int, total_items: int, items_per_page: int) -> Dict:
    """Function to generate a pagination dictionary based on the parameters
    :param int page: The page in which the pagination currently is
    :param int total_items: The number of items which are in the pagination
    :param int items_per_page: How many items are shown on every page
    :rtype: Dict
    :return: The dictionary returning the info about the pagination
    """
    skip = page * items_per_page
    total_pages = math.ceil(total_items / items_per_page)
    pagination = {
        "has_previous": False if total_items == 0 else page > 1,
        "has_more": skip < total_items,
        "page": page,
        "total_items": total_items,
        "total_pages": total_pages,
    }
    return pagination


def can_change_matrix(*, old_value: T, new_value: T, matrix: Dict[T, List[T]]) -> bool:
    """Function to see if one value can change into another, based on a matrix
    :param T old_value: The old value, already assigned
    :param T new_value: The new value to be assigned
    :param Dict[T, List[T]] matrix: Which values are allowed to change, to what values
    :rtype: bool
    :return: If the old value can be replaced by the new value
    """
    if old_value == new_value:
        return True

    return new_value in matrix[old_value]


def remove_whitespaces_from_string(*, string: str) -> str:
    """Function to remove all the whitespaces from a string,
    including tabs and line breaks.
    examples: Victor \n Castillo -> Victor Castillo
              Victor \t Castillo -> Victor Castillo
    :param str string: The string which weill have no whitespaces
    :rtype: str
    :return: The new string without whitespaces
    """

    string_list = string.split()
    return " ".join(string_list)
