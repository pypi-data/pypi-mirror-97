import sqlite3
import ssl
import sys
from typing import AsyncIterator, Callable

import aiohttp
import certifi
import pytest
from aiohttp import web
from typing_extensions import AsyncContextManager
from yarl import URL

from neuro_sdk import IllegalArgumentError, ServerNotAvailable
from neuro_sdk.core import (
    _Core,
    _ensure_schema,
    _load_cookies,
    _make_cookie,
    _save_cookies,
)

from tests import _TestServerFactory

if sys.version_info >= (3, 7):
    from contextlib import asynccontextmanager
else:
    from async_generator import asynccontextmanager


_ApiFactory = Callable[[URL], AsyncContextManager[_Core]]


@pytest.fixture
async def api_factory() -> AsyncIterator[_ApiFactory]:
    @asynccontextmanager
    async def factory(url: URL) -> AsyncIterator[_Core]:
        ssl_context = ssl.SSLContext()
        ssl_context.load_verify_locations(capath=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        session = aiohttp.ClientSession(connector=connector)
        api = _Core(session, "bd7a977555f6b982")
        yield api
        await api.close()
        await session.close()

    yield factory


async def test_relative_url(
    aiohttp_server: _TestServerFactory, api_factory: _ApiFactory
) -> None:
    called = False

    async def handler(request: web.Request) -> web.Response:
        nonlocal called
        called = True
        raise web.HTTPOk()

    app = web.Application()
    app.router.add_get("/test", handler)
    srv = await aiohttp_server(app)

    async with api_factory(srv.make_url("/")) as api:
        relative_url = URL("test")
        with pytest.raises(AssertionError):
            async with api.request(method="GET", url=relative_url, auth="auth") as resp:
                resp
    assert not called


async def test_absolute_url(
    aiohttp_server: _TestServerFactory, api_factory: _ApiFactory
) -> None:
    async def handler(request: web.Request) -> web.Response:
        raise web.HTTPOk()

    app = web.Application()
    app.router.add_get("/test", handler)
    srv = await aiohttp_server(app)

    async with api_factory(srv.make_url("/")) as api:
        absolute_url = srv.make_url("test")
        async with api.request(method="GET", url=absolute_url, auth="auth") as resp:
            assert resp.status == 200


async def test_raise_for_status_no_error_message(
    aiohttp_server: _TestServerFactory, api_factory: _ApiFactory
) -> None:
    async def handler(request: web.Request) -> web.Response:
        raise web.HTTPBadRequest()

    app = web.Application()
    app.router.add_get("/test", handler)
    srv = await aiohttp_server(app)

    async with api_factory(srv.make_url("/")) as api:
        with pytest.raises(IllegalArgumentError, match="^400: Bad Request$"):
            async with api.request(method="GET", url=srv.make_url("test"), auth="auth"):
                pass


async def test_raise_for_status_contains_error_message(
    aiohttp_server: _TestServerFactory, api_factory: _ApiFactory
) -> None:
    ERROR_MSG = '{"error": "this is the error message"}'

    async def handler(request: web.Request) -> web.Response:
        raise web.HTTPBadRequest(text=ERROR_MSG)

    app = web.Application()
    app.router.add_get("/test", handler)
    srv = await aiohttp_server(app)

    async with api_factory(srv.make_url("/")) as api:
        with pytest.raises(IllegalArgumentError, match=f"^{ERROR_MSG}$"):
            async with api.request(method="GET", url=srv.make_url("test"), auth="auth"):
                pass


async def test_server_bad_gateway(
    aiohttp_server: _TestServerFactory, api_factory: _ApiFactory
) -> None:
    async def handler(request: web.Request) -> web.Response:
        raise web.HTTPBadGateway()

    app = web.Application()
    app.router.add_get("/test", handler)
    srv = await aiohttp_server(app)

    async with api_factory(srv.make_url("/")) as api:
        url = srv.make_url("test")
        with pytest.raises(ServerNotAvailable, match="^502: Bad Gateway$"):
            async with api.request(method="GET", url=url, auth="auth") as resp:
                assert resp.status == 200


# ### Cookies tests ###


def test_load_cookies_no_table() -> None:
    with sqlite3.connect(":memory:") as db:
        assert [] == _load_cookies(db)


def test_load_cookies_incorrect_schema() -> None:
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE cookie_session (a TEXT)")
        assert [] == _load_cookies(db)


def test_load_cookies_valid() -> None:
    now = 123456

    with sqlite3.connect(":memory:") as db:
        _ensure_schema(db, update=True)

        db.execute(
            """INSERT INTO cookie_session
        (name, domain, path, cookie, timestamp)
        VALUES (?, ?, ?, ?, ?)""",
            (
                "NEURO_STORAGEAPI_SESSION",
                "https://dev.neu.ro",
                "/",
                "cookie-value",
                now,
            ),
        )
        assert [
            _make_cookie(
                "NEURO_STORAGEAPI_SESSION",
                "cookie-value",
                "https://dev.neu.ro",
                "/",
            )
        ] == _load_cookies(db, now=now)


def test_save_load_multiple_cookies() -> None:
    now = 123456

    with sqlite3.connect(":memory:") as db:
        c1 = _make_cookie(
            "NEURO_STORAGEAPI_SESSION",
            "cookie-value",
            "https://dev.neu.ro",
            "/",
        )

        c2 = _make_cookie(
            "NEURO_REGISTRYAPI_SESSION",
            "cookie-value",
            "https://dev.neu.ro",
            "/",
        )

        _save_cookies(db, [c1, c2], now=now)

        assert [c2, c1] == _load_cookies(db, now=now)


def test_save_load_multiple_cookies_last_stamps() -> None:
    now = 123456

    with sqlite3.connect(":memory:") as db:
        c1 = _make_cookie(
            "NEURO_STORAGEAPI_SESSION",
            "cookie-value",
            "https://dev.neu.ro",
            "/",
        )

        c2 = _make_cookie(
            "NEURO_REGISTRYAPI_SESSION",
            "cookie-value",
            "https://dev.neu.ro",
            "/",
        )

        _save_cookies(db, [c1, c2], now=now)

        c3 = _make_cookie(
            "NEURO_REGISTRYAPI_SESSION",
            "cookie-value2",
            "https://dev.neu.ro",
            "/",
        )

        _save_cookies(db, [c3], now=now + 1)

        assert [c3, c1] == _load_cookies(db, now=now + 1)
