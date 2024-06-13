from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.settings import InfrastructureSettings
from .abstract_message_handler import AbstractMessageHandler
from ..mixins import HelpMenuMixin


class HelpMessage(AbstractMessageHandler, HelpMenuMixin):
    FILTERS = [Command("help")]

    HELP_MESSAGE: str = (
        """Бронирование коворкингов УрФУ\n\n"""
        """Контакты:\n"""
        """\tТехническая поддержка - <b>{tech_support}</b>\n"""
        """\tURL приложения - <a href="{frontend_link}"><b>Сервис бронирования</b></a>\n\n"""
        """Команды:\n"""
        """\t/help - Просмотр информации о Боте\n"""
        """\t/upcoming - Посмотреть ближайшее бронирование"""
    )

    def __init__(self, infrastructure_settings: InfrastructureSettings):
        self.infrastructure_settings = infrastructure_settings

    async def process_message(self, message: Message, state: FSMContext) -> None:
        return await message.answer(
            self.HELP_MESSAGE.format(
                tech_support=self.infrastructure_settings.TECHNICAL_SUPPORT_EMAIL,
                frontend_link=self.infrastructure_settings.FRONTEND_HOST,
            ),
            parse_mode="html"
        )

    @property
    def description(self) -> str:
        return "Помощь"

    @property
    def command(self) -> str:
        return "/help"
