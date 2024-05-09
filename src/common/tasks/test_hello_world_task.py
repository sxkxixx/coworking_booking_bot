from aiogram import Bot

from common.utils import get_yekaterinburg_dt
from storage.user_repository import AbstractUserRepository
from .decorators import periodic_task_run


@periodic_task_run(30)
async def send_hello_world_task(
        bot: Bot,
        user_repository: AbstractUserRepository
) -> None:
    """
    Тестовая таска для проверки работоспособности декоратора
    """
    """TODO: Убрать перед публикацией на прод!!!"""
    users = await user_repository.get_telegram_users()
    for user in users:
        await bot.send_message(
            chat_id=user.telegram_chat_id,
            text=f"Hello, World. {get_yekaterinburg_dt()}"
        )
