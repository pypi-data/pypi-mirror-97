import asyncio
import contextlib
import errno
import json as jsonmodule
import logging
import sqlite3
import sys
import time
from http.cookies import Morsel, SimpleCookie
from types import SimpleNamespace
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Sequence

import aiohttp
from aiohttp import WSMessage
from multidict import CIMultiDict
from yarl import URL

from .errors import (
    AuthenticationError,
    AuthorizationError,
    ClientError,
    IllegalArgumentError,
    ResourceNotFound,
    ServerNotAvailable,
)
from .tracing import gen_trace_id

if sys.version_info >= (3, 7):  # pragma: no cover
    from contextlib import asynccontextmanager
else:
    from async_generator import asynccontextmanager


log = logging.getLogger(__name__)

SESSION_COOKIE_MAXAGE = 5 * 60  # 5 min

SCHEMA = {
    "cookie_session": (
        "CREATE TABLE cookie_session "
        "(name TEXT, domain TEXT, path TEXT, cookie TEXT, timestamp REAL)"
    ),
    "cookie_session_index": (
        "CREATE UNIQUE INDEX cookie_session_index ON cookie_session " "(name)"
    ),
}
DROP = {
    "cookie_session_index": "DROP INDEX IF EXISTS cookie_session_index",
    "cookie_session": "DROP TABLE IF EXISTS cookie_session",
}


DEFAULT_TIMEOUT = aiohttp.ClientTimeout(None, None, 60, 60)


class _Core:
    """Transport provider for public API client.

    Internal class.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        trace_id: Optional[str],
        trace_sampled: Optional[bool] = None,
    ) -> None:
        self._session = session
        self._trace_id = trace_id
        self._trace_sampled = trace_sampled
        self._exception_map = {
            400: IllegalArgumentError,
            401: AuthenticationError,
            403: AuthorizationError,
            404: ResourceNotFound,
            405: ClientError,
            502: ServerNotAvailable,
        }
        self._prev_cookie: Optional[Morsel[str]] = None

    def _post_init(
        self,
        db: sqlite3.Connection,
    ) -> None:
        for cookie in _load_cookies(db):
            self._session.cookie_jar.update_cookies({cookie.key: cookie})

    def _save_cookies(self, db: sqlite3.Connection) -> None:
        to_save = []
        for cookie in self._session.cookie_jar:
            name = cookie.key
            if name.startswith("NEURO_") and name.endswith("_SESSION"):
                to_save.append(cookie)
        _save_cookies(db, to_save)

    @property
    def timeout(self) -> aiohttp.ClientTimeout:
        # TODO: implement ClientSession.timeout public property for session
        return self._session._timeout

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def close(self) -> None:
        pass

    @asynccontextmanager
    async def request(
        self,
        method: str,
        url: URL,
        *,
        auth: str,
        params: Optional[Mapping[str, str]] = None,
        data: Any = None,
        json: Any = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[aiohttp.ClientTimeout] = None,
    ) -> AsyncIterator[aiohttp.ClientResponse]:
        assert url.is_absolute()
        log.debug("Fetch [%s] %s", method, url)
        if headers is not None:
            real_headers: CIMultiDict[str] = CIMultiDict(headers)
        else:
            real_headers = CIMultiDict()
        real_headers["Authorization"] = auth
        if "Content-Type" not in real_headers:
            if json is not None:
                real_headers["Content-Type"] = "application/json"
        trace_request_ctx = SimpleNamespace()
        trace_id = self._trace_id
        if trace_id is None:
            trace_id = gen_trace_id()
        trace_request_ctx.trace_id = trace_id
        trace_request_ctx.trace_sampled = self._trace_sampled
        if params:
            url = url.with_query(params)
        async with self._session.request(
            method,
            url,
            headers=real_headers,
            json=json,
            data=data,
            timeout=timeout,
            trace_request_ctx=trace_request_ctx,
            # Use 4mb buffer as sometimes single job response can be huge.
            read_bufsize=2 ** 22,
        ) as resp:
            if 400 <= resp.status:
                err_text = await resp.text()
                if resp.content_type.lower() == "application/json":
                    try:
                        payload = jsonmodule.loads(err_text)
                    except ValueError:
                        # One example would be a HEAD request for application/json
                        payload = {}
                    if "error" in payload:
                        err_text = payload["error"]
                else:
                    payload = {}
                if resp.status == 400 and "errno" in payload:
                    os_errno: Any = payload["errno"]
                    os_errno = errno.__dict__.get(os_errno, os_errno)
                    raise OSError(os_errno, err_text)
                err_cls = self._exception_map.get(resp.status, IllegalArgumentError)
                raise err_cls(err_text)
            else:
                try:
                    yield resp
                except GeneratorExit:
                    # There is a bug in CPython and/or aiohttp,
                    # if GeneratorExit is reraised @asynccontextmanager
                    # reports this as an error
                    # Need to investigate and fix.
                    raise asyncio.CancelledError

    async def ws_connect(
        self, abs_url: URL, auth: str, *, headers: Optional[Dict[str, str]] = None
    ) -> AsyncIterator[WSMessage]:
        # TODO: timeout
        assert abs_url.is_absolute(), abs_url
        log.debug("Fetch web socket: %s", abs_url)

        if headers is not None:
            real_headers: CIMultiDict[str] = CIMultiDict(headers)
        else:
            real_headers = CIMultiDict()
        real_headers["Authorization"] = auth

        async with self._session.ws_connect(abs_url, headers=real_headers) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    yield msg


def _ensure_schema(db: sqlite3.Connection, *, update: bool) -> bool:
    cur = db.cursor()
    ok = True
    found = set()
    cur.execute("SELECT type, name, sql from sqlite_master")
    for type, name, sql in cur:
        if type not in ("table", "index"):
            continue
        if name in SCHEMA:
            if SCHEMA[name] != sql:
                ok = False
                break
            else:
                found.add(name)

    if not ok or found < SCHEMA.keys():
        for sql in reversed(list(DROP.values())):
            cur.execute(sql)
        for sql in SCHEMA.values():
            cur.execute(sql)
        return True
    return False


def _save_cookies(
    db: sqlite3.Connection,
    cookies: Sequence["Morsel[str]"],
    *,
    now: Optional[float] = None,
) -> None:
    if now is None:
        now = time.time()
    _ensure_schema(db, update=True)
    cur = db.cursor()
    for cookie in cookies:
        cur.execute(
            """\
                INSERT OR REPLACE INTO cookie_session
                (name, domain, path, cookie, timestamp)
                VALUES (?, ?, ?, ?, ?)""",
            (cookie.key, cookie["domain"], cookie["path"], cookie.value, now),
        )
    cur.execute(
        "DELETE FROM cookie_session WHERE timestamp < ?", (now - SESSION_COOKIE_MAXAGE,)
    )
    with contextlib.suppress(sqlite3.OperationalError):
        db.commit()


def _load_cookies(
    db: sqlite3.Connection, *, now: Optional[float] = None
) -> List["Morsel[str]"]:
    if now is None:
        now = time.time()
    if _ensure_schema(db, update=False):
        return []
    cur = db.execute(
        """\
            SELECT name, domain, path, cookie, timestamp FROM cookie_session
            WHERE timestamp >= ?
            ORDER BY name
        """,
        (now - SESSION_COOKIE_MAXAGE,),
    )
    ret: List[Morsel[str]] = []
    for name, domain, path, value, timestamp in cur:
        ret.append(_make_cookie(name, value, domain, path))
    return ret


def _make_cookie(name: str, value: str, domain: str, path: str) -> "Morsel[str]":
    tmp = SimpleCookie()  # type: ignore
    tmp[name] = value
    cookie = tmp[name]
    cookie["domain"] = domain
    cookie["path"] = path
    cookie["max-age"] = str(SESSION_COOKIE_MAXAGE)
    return cookie
