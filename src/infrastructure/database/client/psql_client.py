from types import TracebackType
from typing import Optional, Type, Any

from infrastructure.settings import DatabaseSettings
from .abstract_client import AbstractDatabaseClient

try:
    import asyncpg
except ImportError:
    raise ImportError('Unable to import module "asyncpg", check dependencies')

from asyncpg import Connection, connect
from asyncpg.exceptions import ConnectionDoesNotExistError, NoActiveSQLTransactionError
from asyncpg.transaction import Transaction


class PostgresClient(AbstractDatabaseClient):
    def __init__(self, db_settings: DatabaseSettings) -> None:
        self.db_settings = db_settings

        self.__connection: Optional[Connection] = None
        self.__transaction: Optional[Transaction] = None

    async def __connect(self) -> Connection:
        return await connect(
            host=self.db_settings.DATABASE_HOST,
            port=self.db_settings.DATABASE_PORT,
            user=self.db_settings.DATABASE_USER,
            password=self.db_settings.DATABASE_PASSWORD,
            database=self.db_settings.DATABASE_NAME,
        )

    async def __aenter__(self) -> None:
        self.__connection = await self.__connect()
        self.__transaction = self.__connection.transaction()
        await self.__transaction.start()

    async def execute_query(self, query: str, *args, timeout: float = None) -> Any:
        if not self.__connection or self.__connection.is_closed():
            raise ConnectionDoesNotExistError()
        return await self.__connection.execute(query, *args, timeout)

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> None:
        self.__self_check_conn_state()
        await self.__transaction.rollback()
        await self.__transaction.rollback()

    def __self_check_conn_state(self) -> None:
        if not self.__connection or self.__connection.is_closed():
            raise ConnectionDoesNotExistError()
        if not self.__connection.is_in_transaction():
            raise NoActiveSQLTransactionError()

    async def commit(self) -> None:
        self.__self_check_conn_state()
        await self.__transaction.commit()

    async def rollback(self) -> None:
        self.__self_check_conn_state()
        await self.__transaction.rollback()
