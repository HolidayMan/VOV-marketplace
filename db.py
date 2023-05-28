import asyncio
from typing import Type

import aiomysql

from settings import DB_SETTINGS


class _AsyncCursorManager:
    """
    Context manager for aiomysql cursor.
    """
    def __init__(self, conn: aiomysql.Connection, cursor_type: Type[aiomysql.Cursor] = aiomysql.DictCursor):
        self._conn: aiomysql.Connection = conn
        self._cursor: aiomysql.Cursor | None = None
        self._cursor_type = cursor_type

    async def __aenter__(self) -> aiomysql.Cursor:
        self._cursor = await self._conn.cursor(self._cursor_type).__aenter__()
        return self._cursor

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._conn.rollback()
        await self._cursor.close()


class AsyncSession:
    """
    Context manager for aiomysql connection and cursor.
    Example of usage:
    async with AsyncSession(conn).cursor() as cursor:
        await cursor.execute('SELECT * FROM table')
        conn.commit()
    """
    def __init__(self, conn: aiomysql.Connection, cursor_type: Type[aiomysql.Cursor] = aiomysql.DictCursor,
                 auto_close: bool = True):
        self._conn: aiomysql.Connection = conn
        self._cursor: aiomysql.Cursor | None = None
        self._cursor_type = cursor_type
        self._auto_close = auto_close

    def cursor(self) -> _AsyncCursorManager:
        return _AsyncCursorManager(self._conn, self._cursor_type)

    async def commit(self):
        await self._conn.commit()

    async def rollback(self):
        await self._conn.rollback()

    def close(self):
        self._conn.close()

    def __del__(self):
        if self._auto_close:
            self.close()


def session_maker(loop: asyncio.AbstractEventLoop, host: str, port: int, user: str, password: str, db: str):
    """
    Creates a new sessionmaker object.
    """
    async def factory(cursor_type: Type[aiomysql.Cursor] = aiomysql.DictCursor, auto_close: bool = True) -> AsyncSession:
        """
        Creates a new session.
        """
        conn = await aiomysql.connect(host=host, port=port, user=user, password=password, db=db, loop=loop)
        return AsyncSession(conn, cursor_type, auto_close)
    return factory


DEFAULT_SESSION_FACTORY = session_maker(asyncio.get_running_loop(), **DB_SETTINGS)
