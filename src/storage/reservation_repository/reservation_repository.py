import datetime
from typing import List, Optional

from peewee_async import Manager

from infrastructure.database import BookingStatus, User, CoworkingSeat, Coworking
from infrastructure.database import Reservation
from .abstract_reservation_repository import AbstractReservationRepository


class ReservationRepository(AbstractReservationRepository):
    def __init__(self, manager: Manager):
        self.manager = manager

        self.confirm_delta = datetime.timedelta(hours=2)
        self.cancel_delta = datetime.timedelta(minutes=30)

    async def change_status(self, reservation: Reservation, status: BookingStatus) -> None:
        reservation.status = status.value
        await self.manager.update(reservation)

    async def select_reservations_to_confirm(self) -> List[Reservation]:
        query = (
            Reservation.select()
            .where(Reservation.status == BookingStatus.NEW.value)
            # Подтверждение за 2 часа,
            # разность между текущим временем и стартом брони меньше либо равно 2-ум часам
            .where(
                (Reservation.session_start - datetime.datetime.now()) <= self.confirm_delta
            )
            .join(User)
            .switch(Reservation)
            .join(CoworkingSeat)
            .join(Coworking)
        )
        return await self.manager.execute(query)

    async def get_reservation(self, reservation_id) -> Optional[Reservation]:
        return await self.manager.get_or_none(Reservation, Reservation.id == reservation_id)

    async def select_expired_to_confirm(self) -> List[Reservation]:
        query = (
            Reservation.select()
            .where(Reservation.status == BookingStatus.AWAIT_CONFIRM.value)
            .where(
                (Reservation.session_start - datetime.datetime.now()) <= self.cancel_delta
            )
            .join(User)
            .switch(Reservation)
            .join(CoworkingSeat)
            .join(Coworking)
        )
        return await self.manager.execute(query)

    async def get_income_reservation(self, user: User) -> Optional[Reservation]:
        query = (
            Reservation.select()
            .where(Reservation.user == user)
            .where(Reservation.status != BookingStatus.CANCELLED.value)
            .where(datetime.datetime.now() <= Reservation.session_end)
            .join(User)
            .switch(Reservation)
            .join(CoworkingSeat)
            .join(Coworking)
            .order_by(Reservation.session_start.asc())
        )
        try:
            return await self.manager.get_or_none(query)
        except AttributeError:
            return None

    async def select_passed(self) -> List[Reservation]:
        query = (
            Reservation.select()
            .where(Reservation.status != BookingStatus.CANCELLED)
            .where(Reservation.session_end <= datetime.datetime.now())
        )
        return await self.manager.execute(query)
