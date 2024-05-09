import enum


class BookingStatus(enum.Enum):
    NEW: str = 'new'
    AWAIT_CONFIRM: str = 'await_confirm'
    CONFIRMED: str = 'confirmed'
    CANCELLED: str = 'cancelled'
    PASSED: str = 'passed'
