from typing import Optional

from aiogram.types import CallbackQuery

from common.callback_data import ConfirmCancelCallbackData, ConfirmCancelAction
from infrastructure.database import Reservation
from infrastructure.database.enum import BookingStatus
from storage.reservation_repository import AbstractReservationRepository
from .callback_query_handler import CallbackQueryHandler

__all__ = [
    'ConfirmCancelCallbackQueryHandler'
]


class ConfirmCancelCallbackQueryHandler(CallbackQueryHandler):
    CONFIRM_MESSAGE: str = (
        """Вы успешно подтвердили бронирование.\n"""
        """Ждем вас в {session_start}"""
    )
    CANCEL_MESSAGE: str = (
        """Бронирование на {session_start} отменено. Ждём Вас в следующий раз!❤"""
    )

    FILTER = [ConfirmCancelCallbackData.filter()]

    def __init__(
            self,
            reservation_repository: AbstractReservationRepository,
    ):
        self.reservation_repository = reservation_repository

    async def handle_callback_query(
            self,
            query: CallbackQuery,
            callback_data: ConfirmCancelCallbackData
    ) -> None:
        reservation: Optional[Reservation] = await self.reservation_repository.get_reservation(
            callback_data.reservation_id)
        if not reservation:
            raise Exception()
        assert reservation.status == BookingStatus.AWAIT_CONFIRM.value

        if callback_data.action == ConfirmCancelAction.confirm:
            await self.reservation_repository.change_status(reservation, BookingStatus.CONFIRMED)
            await query.message.answer(
                text=self.CONFIRM_MESSAGE.format(session_start=reservation.session_start)
            )
            return

        await self.reservation_repository.change_status(reservation, BookingStatus.CANCELLED)
        await query.message.answer(
            text=self.CANCEL_MESSAGE.format(session_start=reservation.session_start)
        )
        await query.message.delete()
