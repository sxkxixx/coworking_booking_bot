from typing import Optional

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.states import AuthState
from infrastructure.database.models import User
from storage.user_repository.abstract_user_repository import AbstractUserRepository
from .abstract_message_handler import AbstractMessageHandler


class StartCommandMessage(AbstractMessageHandler):
    FILTERS = [CommandStart()]

    NOT_AUTH_MESSAGE: str = (
        """Здравствуйте, приветствуем Вас в боте сервиса онлайн бронирования коворкингов УрФУ.\n"""
        """Пожалуйста, введите почту, под который Вы регистрировались в сервисе - это требуется """
        """для аутентификации Вас в системе 🔥"""
    )

    USER_AUTHORIZED_MESSAGE: str = (
        """Здравствуйте, %s, рады снова видеть вас в сервисе бронирования коворкингов УрФУ!\n"""
        """Вы уже авторизованы в нашем боте."""
    )

    def __init__(self, user_repository: AbstractUserRepository) -> None:
        self.user_repository = user_repository

    async def process_message(self, message: Message, state: FSMContext) -> None:
        user: Optional[User] = await self.user_repository.get_user_by_chat_id(message.chat.id)
        if not user:
            await state.set_state(AuthState.email)
            await message.answer(self.NOT_AUTH_MESSAGE)
            return
        await message.answer(self.USER_AUTHORIZED_MESSAGE % user.email)
