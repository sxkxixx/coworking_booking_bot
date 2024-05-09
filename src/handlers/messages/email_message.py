import re
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.message_executors.password_msg_executor import PasswordMessageExecutor
from common.states import AuthState
from infrastructure.database import User, EmailAuthData
from storage.email_auth_repository.abstract_email_auth_repository import AbstractEmailAuthRepository
from storage.user_repository import AbstractUserRepository
from .abstract_message_handler import AbstractMessageHandler


class EmailMessage(AbstractMessageHandler):
    FILTERS = [AuthState.email]

    email_regex = re.compile(r'^[A-Za-z0-9]+[.-_]*[A-Za-z0-9]+@(?:urfu.me|urfu.ru)$')

    INVALID_EMAIL_MESSAGE: str = (
        """Ой... Вы ввели не валидную электронную почту...\n"""
        """Электронная почта должна иметь домен <b>urfu.me</b> / <b>urfu.ru</b>\n"""
        """Например, name.surname@urfu.ru\n"""
        """Повторите попытку с валидной почтой"""
    )

    USER_NOT_FOUND_MESSAGE: str = (
        """Здравствуйте! Я вас пока не знаю. Если у вас уже есть аккаунт в сервисе бронирования """
        """коворкингов УРФУ, то обратитесь в техническую поддержку по адресу @Электронная почта@."""
        """Если еще нет, то вы можете зарегистрироваться по адресу: @Ссылка на сайт@"""
    )

    PASSWORD_SENT_MESSAGE = (
        """На указанную Вами почту (%s) выслано сообщение с одноразовым паролем.👨‍💻\n"""
        """Пожалуйста, пришлите его нашему телеграм-боту"""
    )

    def __init__(
            self,
            user_repository: AbstractUserRepository,
            email_auth_repository: AbstractEmailAuthRepository,
            email_executor: PasswordMessageExecutor
    ):
        self.user_repository = user_repository
        self.email_auth_repository = email_auth_repository
        self.email_executor = email_executor

    async def process_message(self, message: Message, state: FSMContext) -> None:
        email: str = message.text
        if self.email_regex.match(email) is None:
            await message.answer(self.INVALID_EMAIL_MESSAGE, parse_mode='html')
            return
        user: Optional[User] = await self.user_repository.get_user_by_email(email)
        if not user:
            await message.answer(self.USER_NOT_FOUND_MESSAGE, parse_mode='html')
            return
        auth_data: EmailAuthData = await self.email_auth_repository.create(user, message.chat.id)
        await self.email_executor.execute(receiver=user.email, password=auth_data.password)
        await state.set_state(AuthState.one_time_password)
        await message.answer(self.PASSWORD_SENT_MESSAGE % email)
