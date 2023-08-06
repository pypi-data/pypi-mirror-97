import copy
import datetime
from functools import wraps
from typing import Dict, Optional, Tuple

import jwt


def encode_jwt(
    *, data: Dict, expiration_time_days: int, jwt_secret_key: str
) -> Tuple[str, int]:
    data_copy = copy.deepcopy(data)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
        days=expiration_time_days
    )
    data_copy.update({"exp": expiration_time})
    data_copy.update({"iat": datetime.datetime.utcnow()})
    token = jwt.encode(data_copy, jwt_secret_key, algorithm="HS256")
    return token, int(expiration_time.timestamp())


def decode_jwt(
    *, jwt_token: str, jwt_secret_key: str, verify_exp: bool = False
) -> Dict:
    data = jwt.decode(
        jwt_token,
        jwt_secret_key,
        algorithms=["HS256"],
        options={"verify_exp": verify_exp},
    )
    return data
