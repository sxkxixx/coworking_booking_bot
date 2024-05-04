from abc import ABC
from typing import Optional


class BaseDataModel(ABC):
    __table_name__: str

    def __init__(self, *args, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)


class UserModel(BaseDataModel):
    __table_name__ = 'users'

    id: str
    email: str
    last_name: str
    first_name: str
    patronymic: str
    is_student: bool

    telegram_info: Optional['UserTelegramInfoModel']


class UserTelegramInfoModel(BaseDataModel):
    __table_name__ = 'users_telegram_info'

    username: str
    chat_id: int
