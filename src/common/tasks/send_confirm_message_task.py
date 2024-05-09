import datetime
from typing import List

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.utils import get_formatted_datetime
from common.utils.messages import CONFIRM_RESERVATION_MESSAGE
from infrastructure.database import Reservation, User, CoworkingSeat, Coworking, BookingStatus
from storage.reservation_repository import AbstractReservationRepository
from .decorators import periodic_task_run
from ..callback_data import ConfirmCancelCallbackData, ConfirmCancelAction


@periodic_task_run(60)
async def send_confirm_message(
        bot: Bot,
        reservation_repository: AbstractReservationRepository,
) -> None:
    reservations: List[Reservation] = await reservation_repository.select_new_reservation()
    print(len(reservations))
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
                    reservation.session_start - datetime.timedelta(hours=2)
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
