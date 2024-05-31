import logging
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class RequestElapsedMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        start_time = time.time()
        result = await handler(event, data)
        logging.info(f"Event = {event.__class__.__name__}, elapsed = {time.time() - start_time}")
        return result
