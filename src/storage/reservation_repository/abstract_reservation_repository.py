from abc import ABC, abstractmethod
from typing import List, Optional

from infrastructure.database import Reservation, BookingStatus, User


class AbstractReservationRepository(ABC):
    @abstractmethod
    async def select_reservations_to_confirm(self) -> List[Reservation]:
        raise NotImplementedError()

    @abstractmethod
    async def change_status(self, reservation: Reservation, status: BookingStatus) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_reservation(self, reservation_id) -> Optional[Reservation]:
        raise NotImplementedError()

    @abstractmethod
    async def select_expired_to_confirm(self) -> List[Reservation]:
        raise NotImplementedError()

    @abstractmethod
    async def get_income_reservation(self, user: User) -> Optional[Reservation]:
        raise NotImplementedError()
