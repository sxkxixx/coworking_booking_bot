import datetime
from typing import List

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.utils import get_formatted_datetime, get_yekaterinburg_dt
from common.utils.messages import CONFIRM_RESERVATION_MESSAGE, CANCEL_RESERVATION_MESSAGE
from infrastructure.database import Reservation, User, CoworkingSeat, Coworking, BookingStatus
from storage.reservation_repository import AbstractReservationRepository
from storage.user_repository import AbstractUserRepository
from .decorators import periodic_task_run
from ..callback_data import ConfirmCancelCallbackData, ConfirmCancelAction


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
    for reservation in reservations:
        user: User = reservation.user
        seat: CoworkingSeat = reservation.seat
        coworking: Coworking = seat.coworking
        await bot.send_message(
            chat_id=user.telegram_chat_id,
            text=CONFIRM_RESERVATION_MESSAGE.format(
                name=coworking.title,
                session_start=get_formatted_datetime(reservation.session_start),
                confirm_deadline=get_formatted_datetime(
                    reservation.session_start - datetime.timedelta(minutes=30)
                ),
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
    for reservation in reservations:
        user: User = reservation.user
        coworking: Coworking = reservation.seat.coworking
        await reservation_repository.change_status(reservation, BookingStatus.CANCELLED)
        await bot.send_message(
            chat_id=user.telegram_chat_id,
            text=CANCEL_RESERVATION_MESSAGE.format(
                name=coworking.title,
                session_start=get_formatted_datetime(reservation.session_start),
            ),
        )


@periodic_task_run(30)
async def send_hello_world_task(bot: Bot, user_repository: AbstractUserRepository) -> None:
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
