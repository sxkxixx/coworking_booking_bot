import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from jinja2 import Environment, FileSystemLoader

from common.message_executors.password_msg_executor import PasswordMessageExecutor
from common.middlewares import RequestElapsedMiddleware
from common.tasks import send_confirm_message, booking_cancel_task
from common.tasks.tasks import mark_reservations_as_passed
from handlers import (
    StartCommandMessage,
    EmailMessage,
    AuthMessage,
    UserReservationMessage,
    HelpMessage
)
from handlers.callback_query import ConfirmCancelCallbackQueryHandler
from infrastructure.database import manager
from infrastructure.logger import configure_logging
from infrastructure.settings import BotSettings, SMTPSettings, InfrastructureSettings
from storage.email_auth_repository.auth_email_data_repository import EmailAuthRepository
from storage.reservation_repository import ReservationRepository
from storage.user_repository.user_repository import UserRepository


def get_jinja2_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader('/templates'),
        enable_async=True
    )
    return env


async def _main() -> None:
    # Settings
    bot_settings = BotSettings()
    smtp_settings = SMTPSettings()
    infrastructure_settings = InfrastructureSettings()
    configure_logging(bot_settings.LOG_LEVEL)

    dp = Dispatcher()

    # Repositories
    user_repository = UserRepository(manager)
    email_auth_repository = EmailAuthRepository(manager)
    reservation_repository = ReservationRepository(manager)

    # Message Executors
    password_message_executor = PasswordMessageExecutor(smtp_settings, get_jinja2_environment())

    # Handlers
    start_command = StartCommandMessage(user_repository)
    auth_pwd_message = AuthMessage(email_auth_repository, user_repository)
    email_message = EmailMessage(
        user_repository, email_auth_repository, password_message_executor, infrastructure_settings
    )
    user_reservation_message = UserReservationMessage(
        user_repository, reservation_repository, infrastructure_settings
    )
    help_message = HelpMessage(infrastructure_settings)

    # Callback queries
    confirm_cancel_handler = ConfirmCancelCallbackQueryHandler(reservation_repository)

    # Register handlers
    dp.message.register(start_command.process_message, *start_command.FILTERS)
    dp.message.register(email_message.process_message, *email_message.FILTERS)
    dp.message.register(auth_pwd_message.process_message, *auth_pwd_message.FILTERS)
    dp.message.register(user_reservation_message.process_message, *user_reservation_message.FILTERS)
    dp.message.register(help_message.process_message, *help_message.FILTERS)

    # Register callback query handlers
    dp.callback_query.register(
        confirm_cancel_handler.handle_callback_query,
        *confirm_cancel_handler.FILTER
    )

    menu_commands = [
        BotCommand(command=help_message.command, description=help_message.description),
        BotCommand(
            command=user_reservation_message.command,
            description=user_reservation_message.description
        )
    ]

    bot = Bot(token=bot_settings.BOT_TOKEN)

    await bot.set_my_commands(menu_commands)

    # background periodic tasks
    _tasks = [
        asyncio.create_task(booking_cancel_task(bot, reservation_repository)),
        asyncio.create_task(send_confirm_message(bot, reservation_repository)),
        asyncio.create_task(mark_reservations_as_passed(reservation_repository))
    ]

    elapsed_middleware = RequestElapsedMiddleware()
    dp.message.middleware(elapsed_middleware)
    dp.callback_query.middleware(elapsed_middleware)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(_main())
