from abc import ABC, abstractmethod
from typing import List, Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class AbstractMessageHandler(ABC):
    FILTERS: List[Any]

    @abstractmethod
    async def process_message(self, message: Message, state: FSMContext) -> None:
        raise NotImplementedError()
