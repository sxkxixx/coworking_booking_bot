from typing import Optional, List

import peewee_async

from infrastructure.database import User
from .abstract_user_repository import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, manager: peewee_async.Manager):
        self.manager = manager

    async def get_user_by_chat_id(self, chat_id: int) -> Optional[User]:
        try:
            return await self.manager.get_or_none(User, User.telegram_chat_id == chat_id)
        except AttributeError:
            return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            return await self.manager.get_or_none(User, User.email == email)
        except AttributeError:
            return None

    async def set_chat_id(self, user: User, chat_id: int) -> User:
        user.telegram_chat_id = chat_id
        await self.manager.update(user)
        return user

    async def get_telegram_users(self) -> List[User]:
        query = (
            User.select()
            .where(User.telegram_chat_id.is_null(False))
        )
        return await self.manager.execute(query)
