import logging
from typing import Optional

from aiogram.types import CallbackQuery

from common.callback_data import ConfirmCancelCallbackData, ConfirmCancelAction
from common.utils import get_formatted_dt
from infrastructure.database import Reservation
from infrastructure.database.enum import BookingStatus
from storage.reservation_repository import AbstractReservationRepository
from .callback_query_handler import CallbackQueryHandler

__all__ = [
    'ConfirmCancelCallbackQueryHandler'
]

logger = logging.getLogger(__name__)


class ConfirmCancelCallbackQueryHandler(CallbackQueryHandler):
    """Класс обработчик для кнопок подтвердить / отклонить бронирование"""

    CONFIRM_MESSAGE: str = (
        """Вы успешно подтвердили бронирование.\n"""
        """Ждем вас {session_start} ❤"""
    )
    CANCEL_MESSAGE: str = (
        """Бронирование на {session_start} отменено. Ждём Вас в следующий раз! 🌚"""
    )

    ALREADY_CONFIRMED: str = """Данное бронирование уже <b>подтверждено</b>."""
    ALREADY_CANCELLED: str = """Данное бронирование уже <b>отменено</b>."""
    ALREADY_PASSED: str = """Данное бронирование уже <b>прошло</b>."""

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
            callback_data.reservation_id
        )
        logger.info(f"Action at Reservation(id={reservation.id})")
        if not reservation:
            logger.info(f"Unexpected error, Reservation(id={callback_data.reservation_id}) is null")
            raise Exception()
        match reservation.status:
            case BookingStatus.CONFIRMED.value:
                logger.error("Reservation(id=%s) already confirmed", reservation.id)
                return await query.message.answer(self.ALREADY_CONFIRMED, parse_mode="html")
            case BookingStatus.CANCELLED.value:
                logger.error("Reservation(id=%s) already cancelled", reservation.id)
                return await query.message.answer(self.ALREADY_CANCELLED, parse_mode="html")
            case BookingStatus.PASSED.value:
                logger.error("Reservation(id=%s) already passed", reservation.id)
                return await query.message.answer(self.ALREADY_PASSED, parse_mode="html")

        assert reservation.status == BookingStatus.AWAIT_CONFIRM.value

        if callback_data.action == ConfirmCancelAction.confirm:
            await self.reservation_repository.change_status(reservation, BookingStatus.CONFIRMED)
            await query.message.answer(
                text=self.CONFIRM_MESSAGE.format(
                    session_start=get_formatted_dt(reservation.session_start)
                )
            )
            logger.info("User confirmed Reservation(id=%s)", reservation.id)
        else:
            await self.reservation_repository.change_status(reservation, BookingStatus.CANCELLED)
            await query.message.answer(
                text=self.CANCEL_MESSAGE.format(
                    session_start=get_formatted_dt(reservation.session_start)
                )
            )
            logger.info("User cancelled Reservation(id=%s)", reservation.id)
