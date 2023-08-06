from typing import Dict

from bson import ObjectId

from pronto_commons.utils import get_jwt_token


def get_jwt_id(*, dictionary: Dict) -> ObjectId:
    """
    Function that retrieves the jwt_id from a dictionary that contains the jwt_token information
    decrypted.

    :param Dict dictionary: The dictionary that contains the key `jwt_token` decrypted.
    :return: ObjectId
        The ObjectId inside the jwt_token
    :raises:
        - InvalidId - If the _id inside the jwt_token is invalid
    """
    token_dict = get_jwt_token(dictionary=dictionary)
    user_id = token_dict.get("_id", "")
    return ObjectId(user_id)


def transform_location_to_geojson(*, latitude: float, longitude: float) -> Dict:
    """Function to conver a latitude and longitude into a geojson point
    :param float latitude: The latitude of the point
    :param float longitude: The longitude of the point
    :rtype: Dict
    :return: The GeoJSON point
    """
    return {"coordinates": [float(longitude), float(latitude)], "type": "Point"}
