from aiogram.fsm.state import StatesGroup, State


class AuthState(StatesGroup):
    """Класс для состояний при авторизации в боте"""
    email = State()
    one_time_password = State()
