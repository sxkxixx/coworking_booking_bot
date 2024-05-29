from typing import Optional

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.utils import get_formatted_datetime
from infrastructure.database import User, Reservation, PlaceType
from storage.reservation_repository import AbstractReservationRepository
from storage.user_repository import AbstractUserRepository
from .abstract_message_handler import AbstractMessageHandler


class UserReservationMessage(AbstractMessageHandler):
    FILTERS = [Command("upcoming")]

    UNAUTHORIZED_MESSAGE: str = (
        """Для просмотра списка бронирований требуется авторизоваться в боте"""
    )

    RESERVATION_PATTERN: str = (
        """Найдено предстоящее бронирование!"""
        """Коворкинг: {coworking_name}\n"""
        """Адрес: {address}\n"""
        """Время бронирования: {session_start} - {session_end}\n"""
        """Тип места: {place_type}"""
    )

    NO_INCOMING_BOOKING_MESSAGE: str = (
        """Предстоящих бронирований не найдено 🚫\n"""
        """В сервисе бронирования можно подобрать подходящий коворкинг """
        """и зарезервировать на удобное время"""
    )

    def __init__(
            self,
            user_repository: AbstractUserRepository,
            reservation_repository: AbstractReservationRepository
    ):
        self.user_repository = user_repository
        self.reservation_repository = reservation_repository

    async def process_message(self, message: Message, state: FSMContext) -> None:
        user: Optional[User] = await self.user_repository.get_user_by_chat_id(message.chat.id)
        if not user:
            await message.answer(self.UNAUTHORIZED_MESSAGE)
            return
        booking: Reservation | None = await self.reservation_repository.get_income_reservation(user)
        if not booking:
            await message.answer(self.NO_INCOMING_BOOKING_MESSAGE)
            return
        await message.answer(
            self.RESERVATION_PATTERN.format(
                coworking_name=booking.seat.coworking.title,
                address=booking.seat.coworking.address,
                session_start=get_formatted_datetime(booking.session_start),
                session_end=get_formatted_datetime(booking.session_end),
                place_type=self.__place_type_ru(booking.seat.place_type),
            ),
        )

    @staticmethod
    def __place_type_ru(place_type: str) -> str:
        return {
            PlaceType.MEETING_ROOM.value: "Переговорная комната",
            PlaceType.TABLE.value: "Стол"
        }[place_type]
