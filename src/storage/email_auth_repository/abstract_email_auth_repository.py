from abc import ABC, abstractmethod
from typing import Optional

from infrastructure.database import EmailAuthData, User


class AbstractEmailAuthRepository(ABC):
    @abstractmethod
    async def create(self, user: User, chat_id: int) -> EmailAuthData:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, *filters) -> Optional[EmailAuthData]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_record(self, auth_data: EmailAuthData) -> None:
        raise NotImplementedError()
