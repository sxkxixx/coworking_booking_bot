import datetime
import logging
from typing import List

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.utils import extract_time_from_dt
from common.utils.messages import CONFIRM_RESERVATION_MESSAGE, CANCEL_RESERVATION_MESSAGE
from infrastructure.database import Reservation, User, CoworkingSeat, Coworking, BookingStatus
from storage.reservation_repository import AbstractReservationRepository
from .decorators import periodic_task_run
from ..callback_data import ConfirmCancelCallbackData, ConfirmCancelAction

logger = logging.getLogger(__name__)


@periodic_task_run(60)
async def send_confirm_message(
        bot: Bot,
        reservation_repository: AbstractReservationRepository,
) -> None:
    """
    Задача, которая посылает сообщение пользователю с целью подтвердить/отменить бронь
    :param bot: Бот
    :param reservation_repository: Репозиторий
    :return: None
    """
    reservations: List[Reservation] = await reservation_repository.select_reservations_to_confirm()
    logger.info(f"Not confirmed messages count = {len(reservations)}")
    for reservation in reservations:
        user: User = reservation.user
        seat: CoworkingSeat = reservation.seat
        coworking: Coworking = seat.coworking
        logger.info(
            f"Sending confirm message to Reservation(id=%s) to User(email=%s)",
            reservation.id, user.email
        )
        await bot.send_message(
            chat_id=user.telegram_chat_id,
            text=CONFIRM_RESERVATION_MESSAGE.format(
                name=coworking.title,
                session_start=extract_time_from_dt(reservation.session_start),
                confirm_deadline=extract_time_from_dt(
                    reservation.session_start - datetime.timedelta(minutes=30)),
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text="Подтвердить",
                        callback_data=ConfirmCancelCallbackData(
                            action=ConfirmCancelAction.confirm,
                            reservation_id=reservation.id
                        ).pack()
                    ),
                    InlineKeyboardButton(
                        text="Отменить",
                        callback_data=ConfirmCancelCallbackData(
                            action=ConfirmCancelAction.cancel,
                            reservation_id=reservation.id
                        ).pack()
                    )
                ]]
            )
        )
        # Обязательно, чтобы пользователь не получал сообщения каждую минуту
        await reservation_repository.change_status(reservation, BookingStatus.AWAIT_CONFIRM)
        logger.info(
            "Changing Reservation(id=%s) to status %s", reservation.id, BookingStatus.AWAIT_CONFIRM
        )


@periodic_task_run(60)
async def booking_cancel_task(
        bot: Bot,
        reservation_repository: AbstractReservationRepository,
) -> None:
    """
    Фоновая задача, которая уведомляет пользователя об отмене бронирования
    :param bot: Бот
    :param reservation_repository: Репозиторий
    :return: None
    """
    reservations: List[Reservation] = await reservation_repository.select_expired_to_confirm()
    logger.info("Canceling %s reservation", len(reservations))
    for reservation in reservations:
        user: User = reservation.user
        coworking: Coworking = reservation.seat.coworking
        await reservation_repository.change_status(reservation, BookingStatus.CANCELLED)
        logger.info(
            "Canceling Reservation(id=%s) of User(email=%s)", reservation.id, user.email
        )
        await bot.send_message(
            chat_id=user.telegram_chat_id,
            text=CANCEL_RESERVATION_MESSAGE.format(
                name=coworking.title,
                session_start=extract_time_from_dt(reservation.session_start),
            ),
        )


@periodic_task_run(120)
async def mark_reservations_as_passed(
        reservation_repository: AbstractReservationRepository
) -> None:
    """
    Фоновая задача, которая после завершения бронирования меняет статус задачи на passed
    :param reservation_repository: Репозиторий бронирования
    :return: None
    """
    reservations: List[Reservation] = await reservation_repository.select_passed()
    logger.info("Marking %s reservations as passed")
    for booking in reservations:
        # Если логика везде правильная, статус бронирования будет везде CONFIRMED
        if booking.status != BookingStatus.CONFIRMED.value:
            logger.error("Status of Reservation(id=%s) $ne Confirmed", booking.id)
        await reservation_repository.change_status(booking, BookingStatus.PASSED)
        logger.info("Reservation(id=%s) marked as Passed", booking.id)
