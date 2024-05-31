import random
from typing import Optional

import peewee_async

from infrastructure.database import EmailAuthData, User
from .abstract_email_auth_repository import AbstractEmailAuthRepository


class EmailAuthRepository(AbstractEmailAuthRepository):
    def __init__(self, manager: peewee_async.Manager):
        self.manager = manager

    async def create(self, user: User, chat_id: int) -> EmailAuthData:
        random_passwd = random.randrange(10000, 100000)
        auth_data: EmailAuthData = await self.manager.create(
            EmailAuthData,
            user=user,
            password=random_passwd,
            chat_id=chat_id
        )
        return auth_data

    async def get(self, *filters) -> Optional[EmailAuthData]:
        return await self.manager.get_or_none(EmailAuthData, *filters)

    async def delete_record(self, auth_data: EmailAuthData) -> None:
        await self.manager.delete(auth_data)
