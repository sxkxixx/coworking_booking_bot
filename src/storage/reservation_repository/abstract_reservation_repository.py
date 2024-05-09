from abc import ABC, abstractmethod
from typing import List, Optional

from infrastructure.database import Reservation, BookingStatus


class AbstractReservationRepository(ABC):
    @abstractmethod
    async def select_new_reservation(self) -> List[Reservation]:
        raise NotImplementedError()

    @abstractmethod
    async def change_status(self, reservation: Reservation, status: BookingStatus) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_reservation(self, reservation_id) -> Optional[Reservation]:
        raise NotImplementedError()
