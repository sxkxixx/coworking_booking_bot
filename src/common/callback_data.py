from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ConfirmCancelAction(Enum):
    confirm = "confirm"
    cancel = "cancel"


class ConfirmCancelCallbackData(CallbackData, prefix=""):
    action: ConfirmCancelAction
    reservation_id: int
