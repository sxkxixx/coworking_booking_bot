from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ConfirmCancelAction(Enum):
    """Enum для действий по подтверждению и отклонению брони"""
    confirm = "confirm"
    cancel = "cancel"


class ConfirmCancelCallbackData(CallbackData, prefix=""):
    """Класс callback_data для кнопок подтверждения/отмены брони"""
    action: ConfirmCancelAction
    reservation_id: int
