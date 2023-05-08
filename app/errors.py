from typing import Type
from aiohttp import web
import json

ERROR_TYPE = Type[web.HTTPUnauthorized] | Type[web.HTTPForbidden] | Type[web.HTTPNotFound]


def raise_http_error(error_class: ERROR_TYPE, message: str | dict):
    raise error_class(
        text=json.dumps({"status": "error", "description": message}),
        content_type="application/json",
    )
