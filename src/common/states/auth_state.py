from aiogram.fsm.state import StatesGroup, State


class AuthState(StatesGroup):
    email = State()
    one_time_password = State()
