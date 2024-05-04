import asyncio

from aiogram import Bot, Dispatcher

from handlers import auth_router
from infrastructure.settings import BotSettings


async def _run_polling() -> None:
    bot_settings = BotSettings()
    main_dp = Dispatcher()
    main_dp.include_routers(auth_router)
    bot = Bot(token=bot_settings.BOT_TOKEN)

    await main_dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(_run_polling())
