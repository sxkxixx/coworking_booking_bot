import datetime
from typing import List, Optional

from peewee_async import Manager

from common.utils import get_yekaterinburg_dt
from infrastructure.database import BookingStatus, User, CoworkingSeat, Coworking
from infrastructure.database import Reservation
from .abstract_reservation_repository import AbstractReservationRepository


class ReservationRepository(AbstractReservationRepository):
    def __init__(self, manager: Manager):
        self.manager = manager

    async def change_status(self, reservation: Reservation, status: BookingStatus) -> None:
        reservation.status = status.value
        await self.manager.update(reservation)

    async def select_new_reservation(self) -> List[Reservation]:
        query = (
            Reservation.select()
            .where(Reservation.status == BookingStatus.NEW.value)
            # Подтверждение за 2 часа,
            # разность между текущим временем и стартом брони меньше либо равно 2-ум часам
            .where(
                # (Reservation.session_start - get_yekaterinburg_dt()) <= datetime.timedelta(
                # hours=2)
            )
            .join(User)
            .switch(Reservation)
            .join(CoworkingSeat).join(Coworking)
        )
        return await self.manager.execute(query)

    async def get_reservation(self, reservation_id) -> Optional[Reservation]:
        return await self.manager.get_or_none(Reservation, Reservation.id == reservation_id)
