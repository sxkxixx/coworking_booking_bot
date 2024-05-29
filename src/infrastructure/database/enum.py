import enum


class BookingStatus(enum.Enum):
    NEW: str = 'new'
    AWAIT_CONFIRM: str = 'await_confirm'
    CONFIRMED: str = 'confirmed'
    CANCELLED: str = 'cancelled'
    PASSED: str = 'passed'


class PlaceType(enum.Enum):
    """Enum для определения типа места для бронирования"""

    MEETING_ROOM: str = 'meeting_room'
    """Комната для переговоров"""

    TABLE: str = 'table'
    """Стол"""
