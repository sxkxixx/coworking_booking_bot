from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.states import AuthState
from infrastructure.database import EmailAuthData
from storage.email_auth_repository.abstract_email_auth_repository import AbstractEmailAuthRepository
from storage.user_repository import AbstractUserRepository
from .abstract_message_handler import AbstractMessageHandler


class AuthMessage(AbstractMessageHandler):
    INCORRECT_PASSWORD_MESSAGE = (
        """Введён неверный пароль, повторите попытку.\n"""
        """Если письмо не пришло на почту, проверьте, что Вы правильно ввели электронную почту """
        """или обратитесь в тех. поддержку"""
    )
    SUCCESS_AUTH_MESSAGE = (
        """Поздравляем с успешной авторизацией в телеграм-боте."""
        """Теперь я смогу отправлять вам сообщения о подтверждении бронирования и информацию о """
        """неожиданных изменениях в расписании работы коворкингов."""
    )

    FILTERS = [AuthState.one_time_password]

    def __init__(
            self,
            email_auth_repository: AbstractEmailAuthRepository,
            user_repository: AbstractUserRepository,
    ):
        self.email_auth_repository = email_auth_repository
        self.user_repository = user_repository

    async def process_message(self, message: Message, state: FSMContext) -> None:
        try:
            pwd = int(message.text)
        except ValueError:
            await message.answer(self.INCORRECT_PASSWORD_MESSAGE)
            return
        auth_data: Optional[EmailAuthData] = await self.email_auth_repository.get(
            EmailAuthData.chat_id == message.chat.id,
            EmailAuthData.password == pwd
        )
        if not auth_data:
            await message.answer(self.INCORRECT_PASSWORD_MESSAGE)
            return
        await self.user_repository.set_chat_id(auth_data.user, message.chat.id)
        await self.email_auth_repository.delete_record(auth_data)
        await state.clear()
        await message.answer(self.SUCCESS_AUTH_MESSAGE)
