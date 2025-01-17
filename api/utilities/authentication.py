import os
import bcrypt
from calendar import timegm
from datetime import datetime, timedelta
from fastapi import Cookie
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from typing import Annotated, Optional
from models.jwt import AccountJWTPayload, AccountJWTUserData
from queries.accounts_queries import AccountUserWithPassword

ALGORITHM = ALGORITHMS.HS256


SIGNING_KEY = os.environ.get("SIGNING_KEY")
if not SIGNING_KEY:
    ValueError("SIGNING_KEY environment variable not set")


async def decode_jwt(token: str) -> Optional[AccountJWTPayload]:
    try:
        payload = jwt.decode(token, SIGNING_KEY, algorithms=[ALGORITHM])
        return AccountJWTPayload(**payload)
    except (JWTError, AttributeError) as e:
        print(e)
    return None


async def try_get_jwt_user_data(fast_api_token: Annotated[str | None, Cookie()] = None) -> Optional[AccountJWTUserData]:
    if not fast_api_token:
        return
    payload = await decode_jwt(fast_api_token)
    if not payload:
        return

    return payload.user


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def hash_password(plain_password) -> str:
    return bcrypt.hashpw(
        plain_password.encode("utf-8"), bcrypt.gensalt()
    ).decode()


def generate_jwt(user: AccountUserWithPassword) -> str:
    exp = timegm((datetime.utcnow() + timedelta(hours=1)).utctimetuple())
    jwt_data = AccountJWTPayload(
        exp=exp,
        sub=user.username,
        user=AccountJWTUserData(username=user.username, id=user.id),
    )
    encoded_jwt = jwt.encode(
        jwt_data.model_dump(), SIGNING_KEY, algorithm=ALGORITHMS.HS256
    )
    return encoded_jwt
