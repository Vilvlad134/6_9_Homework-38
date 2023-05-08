from errors import raise_http_error
from aiohttp import web
from models import ORM_MODEL, ORM_MODEL_CLS

from sqlalchemy.orm import Session


async def get_item(session: Session, model_cls: ORM_MODEL_CLS, item_id: int | str) -> ORM_MODEL:
    item = await session.get(model_cls, item_id)
    if item is None:
        raise raise_http_error(web.HTTPNotFound, f"{model_cls.__name__} not found")
    return item

