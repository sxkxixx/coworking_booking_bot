from abc import ABC, abstractmethod
from typing import Any


class AbstractDatabaseClient(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def execute_query(self, query: str, *args, timeout: float = None) -> Any:
        raise NotImplementedError()
