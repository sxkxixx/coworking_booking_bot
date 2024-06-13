import logging
import re
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.message_executors.password_msg_executor import PasswordMessageExecutor
from common.states import AuthState
from infrastructure.database import User, EmailAuthData
from infrastructure.settings import InfrastructureSettings
from storage.email_auth_repository.abstract_email_auth_repository import AbstractEmailAuthRepository
from storage.user_repository import AbstractUserRepository
from .abstract_message_handler import AbstractMessageHandler

logger = logging.getLogger(__name__)


class EmailMessage(AbstractMessageHandler):
    """Обработчик сообщения с электронной почтой от пользователя"""

    FILTERS = [AuthState.email]

    email_regex = re.compile(r'^[A-Za-z0-9]+[.-_]*[A-Za-z0-9]+@(?:urfu.me|urfu.ru)$')

    INVALID_EMAIL_MESSAGE: str = (
        """Ой... Вы ввели не валидную электронную почту...\n"""
        """Электронная почта должна иметь домен <b>urfu.me</b> / <b>urfu.ru</b>\n"""
        """Например, name.surname@urfu.ru\n"""
        """Повторите попытку с валидной почтой"""
    )

    USER_NOT_FOUND_MESSAGE: str = (
        """Здравствуйте! К сожалению, я Вас пока не знаю.\n"""
        """Если у вас уже есть аккаунт в сервисе бронирования """
        """коворкингов УрФУ, то обратитесь в техническую поддержку по адресу {tech_support}. """
        """Если еще нет, то вы можете зарегистрироваться в нашем """
        """<a href='{frontend_url}'>сервисе</a>"""
    )

    PASSWORD_SENT_MESSAGE = (
        """На указанную Вами почту (%s) выслано сообщение с одноразовым паролем.👨‍💻\n"""
        """Пожалуйста, пришлите его нашему телеграм-боту"""
    )

    def __init__(
            self,
            user_repository: AbstractUserRepository,
            email_auth_repository: AbstractEmailAuthRepository,
            email_executor: PasswordMessageExecutor,
            infrastructure_settings: InfrastructureSettings,
    ):
        self.user_repository = user_repository
        self.email_auth_repository = email_auth_repository
        self.email_executor = email_executor
        self.infrastructure_settings = infrastructure_settings

    async def process_message(self, message: Message, state: FSMContext) -> None:
        email: str = message.text
        if self.email_regex.match(email) is None:
            logger.error(f"Email = {email} not match pattern")
            await message.answer(self.INVALID_EMAIL_MESSAGE, parse_mode='html')
            return
        user: Optional[User] = await self.user_repository.get_user_by_email(email)
        if not user:
            logger.error(f"User with email={email} not found")
            await message.answer(
                self.USER_NOT_FOUND_MESSAGE.format(
                    tech_support=self.infrastructure_settings.TECHNICAL_SUPPORT_EMAIL,
                    frontend_url=self.infrastructure_settings.FRONTEND_HOST,
                ),
                parse_mode='html'
            )
            return
        auth_data: EmailAuthData = await self.email_auth_repository.create(user, message.chat.id)
        await self.email_executor.execute(receiver=user.email, password=auth_data.password)
        logger.info(f"Password is sent to user email={user.email}")
        await state.set_state(AuthState.one_time_password)
        await message.answer(self.PASSWORD_SENT_MESSAGE % email)
