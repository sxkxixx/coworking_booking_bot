import asyncio

from aiogram import Bot, Dispatcher
from jinja2 import Environment, FileSystemLoader

from common.message_executors.password_msg_executor import PasswordMessageExecutor
from common.middlewares import RequestElapsedMiddleware
from common.tasks import send_confirm_message, booking_cancel_task
from common.tasks.tasks import mark_reservations_as_passed
from handlers import StartCommandMessage, EmailMessage
from handlers.callback_query import ConfirmCancelCallbackQueryHandler
from handlers.messages.auth_message import AuthMessage
from handlers.messages.user_reservation_message import UserReservationMessage
from infrastructure.database import manager
from infrastructure.logger import configure_logging
from infrastructure.settings import BotSettings, SMTPSettings
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
    configure_logging(bot_settings.LOG_LEVEL)

    dp = Dispatcher()

    # Repositories
    user_repository = UserRepository(manager)
    email_auth_repository = EmailAuthRepository(manager)
    reservation_repository = ReservationRepository(manager)

    # Register handlers
    dp.message.register(
        StartCommandMessage(user_repository).process_message, *StartCommandMessage.FILTERS
    )
    dp.message.register(
        EmailMessage(
            user_repository,
            email_auth_repository,
            PasswordMessageExecutor(smtp_settings, get_jinja2_environment())
        ).process_message,
        *EmailMessage.FILTERS
    )
    dp.message.register(
        AuthMessage(email_auth_repository, user_repository).process_message,
        *AuthMessage.FILTERS
    )
    dp.message.register(
        UserReservationMessage(user_repository, reservation_repository).process_message,
        *UserReservationMessage.FILTERS
    )

    # Register callback query handlers
    dp.callback_query.register(
        ConfirmCancelCallbackQueryHandler(reservation_repository).handle_callback_query,
        *ConfirmCancelCallbackQueryHandler.FILTER
    )

    bot = Bot(token=bot_settings.BOT_TOKEN)

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
