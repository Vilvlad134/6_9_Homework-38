from auth import check_password, hash_password
from crud import get_item
from errors import raise_http_error
from models import Token, User, get_session_maker, Advertisments
from aiohttp import web
from typing import Callable, Awaitable
from sqlalchemy.future import select

Session = get_session_maker()


@web.middleware
async def session_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    async with Session() as session:
        request["session"] = session
        return await handler(request)


def check_owner(request: web.Request, user_id: int):
    if not request["token"] or request["token"].user.id != user_id:
        raise_http_error(web.HTTPForbidden, "only owner has access")


async def register(request: web.Request):
    user_data = await request.json()
    user_data["password"] = hash_password(user_data["password"])
    new_user = User(**user_data)
    request["session"].add(new_user)
    await request["session"].commit()
    return web.json_response({"id": new_user.id})


async def login(request: web.Request):
    login_data = await request.json()
    query = select(User).where(User.email == login_data["email"])
    result = await request["session"].execute(query)
    user = result.scalar()
    if not user or not check_password(login_data["password"], user.password):
        raise_http_error(web.HTTPUnauthorized, "incorrect login or password")

    token = Token(user=user)
    request["session"].add(token)
    await request["session"].commit()

    return web.json_response({"token": str(token.id)})


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info["user_id"])
        user = await get_item(self.request["session"], User, user_id)
        return web.json_response(
            {"id": user.id,
             "email": user.email}
        )

    async def patch(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user_data = await self.request.json()
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])

        user = await get_item(self.request["session"], User, user_id)
        for field, value in user_data.items():
            setattr(user, field, value)
        self.request["session"].add(user)
        await self.request["session"].commit()

        return web.json_response(
            {"id": user.id,
             "email": user.email}
        )

    async def delete(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user = await get_item(self.request["session"], User, user_id)
        await self.request["session"].delete(user)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})


async def create_adv(request: web.Request):
    if not request["token"]:
        raise_http_error(web.HTTPForbidden, "incorrect token")
    login_data = await request.json()
    login_data['owner'] = request["token"].user.id
    new_adv = Advertisments(**login_data)
    request["session"].add(new_adv)
    await request["session"].commit()
    return web.json_response({"id": new_adv.id})


class AdvertismentsView(web.View):
    async def get(self):
        adv_id = int(self.request.match_info["advertisments_id"])
        advertisment = await get_item(self.request["session"], Advertisments, adv_id)
        return web.json_response(
            {"id": advertisment.id,
             "email": advertisment.header}
        )

    async def patch(self):
        adv_id = int(self.request.match_info["advertisments_id"])
        adv = await get_item(self.request["session"], Advertisments, adv_id)
        check_owner(self.request, adv.owner)
        adv_data = await self.request.json()
        for field, value in adv_data.items():
            setattr(adv, field, value)
        self.request["session"].add(adv)
        await self.request["session"].commit()
        return web.json_response(
            {"id": adv.id,
             "header": adv.header}
        )

    async def delete(self):
        adv_id = int(self.request.match_info["advertisments_id"])
        adv = await get_item(self.request["session"], Advertisments, adv_id)
        check_owner(self.request, adv.owner)
        await self.request["session"].delete(adv)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})


