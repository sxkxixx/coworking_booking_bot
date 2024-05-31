from abc import ABC, abstractmethod
from typing import Optional, List

from infrastructure.database.models import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user_by_chat_id(self, chat_id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def set_chat_id(self, user: User, chat_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_telegram_users(self) -> List[User]:
        raise NotImplementedError()
