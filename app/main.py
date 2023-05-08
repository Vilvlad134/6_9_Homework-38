from views import UserView, login, register, session_middleware, create_adv, AdvertismentsView
from aiohttp import web
from models import get_engine, get_session_maker, Base
from auth import checkauth_middleware


async def app_context(app: web.Application):
    print("START")
    async with get_engine().begin() as conn:
        bb = get_session_maker()
        async with bb() as session:
            await session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            await session.commit()
        await conn.run_sync(Base.metadata.create_all)
    yield
    await get_engine().dispose()
    print("FINISH")


async def get_app():
    app = web.Application(middlewares=[session_middleware])
    app_auth_required = web.Application(middlewares=[session_middleware, checkauth_middleware])

    app.cleanup_ctx.append(app_context)
    app.add_routes(
        [
            web.post("/login/", login),
            web.post("/users/", register),
            web.get("/users/{user_id:\d+}", UserView),
            web.get("/users/advertisments/{advertisments_id:\d+}", AdvertismentsView)
        ]
    )

    app_auth_required.add_routes(
        [
            web.patch("/{user_id:\d+}", UserView),
            web.delete("/{user_id:\d+}", UserView),
            web.post("/advertisments/", create_adv),
            web.patch("/advertisments/{advertisments_id:\d+}", AdvertismentsView),
            web.delete("/advertisments/{advertisments_id:\d+}", AdvertismentsView)
        ]
    )

    app.add_subapp(prefix="/users/", subapp=app_auth_required)
    return app

web.run_app(get_app())
