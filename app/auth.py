import datetime
from config import TOKEN_TTL
from errors import raise_http_error
from models import Token
from aiohttp import web
from typing import Callable, Awaitable
from crud import get_item
import bcrypt


def hash_password(password: str):
    return (bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


@web.middleware
async def checkauth_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    token_id = request.headers.get("token")
    if not token_id:
        raise_http_error(web.HTTPForbidden, "incorrect token")
    try:
        token = await get_item(request["session"], Token, token_id)
    except web.HTTPNotFound:
        token = None
    if not token or token.creation_time + datetime.timedelta(seconds=TOKEN_TTL) <= datetime.datetime.now():
        raise_http_error(web.HTTPForbidden, "incorrect token")
    request["token"] = token
    return await handler(request)
