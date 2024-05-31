from abc import ABC, abstractmethod
from typing import Any, List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery


class CallbackQueryHandler(ABC):
    FILTER: List[Any]

    @abstractmethod
    async def handle_callback_query(
            self,
            query: CallbackQuery,
            callback_data: CallbackData
    ) -> None:
        """Callback для обработки CallbackQuery"""
        raise NotImplementedError()
