from datetime import datetime
from typing import Optional

import peewee

from .db import database


class User(peewee.Model):
    id: str = peewee.CharField(max_length=64, primary_key=True)
    email: str = peewee.CharField(max_length=64, unique=True)
    # Unused
    # hashed_password: str = peewee.CharField(max_length=256, null=False)
    last_name: str = peewee.CharField(max_length=32, null=False)
    first_name: str = peewee.CharField(max_length=32, null=False)
    patronymic: Optional[str] = peewee.CharField(max_length=32, null=True)
    is_student: bool = peewee.BooleanField()
    telegram_chat_id = peewee.BigIntegerField(null=True)
    avatar_filename: Optional[str] = peewee.CharField(max_length=128, null=True)

    class Meta:
        table_name = 'users'
        database = database


class EmailAuthData(peewee.Model):
    id: int = peewee.BigAutoField(primary_key=True)
    user: User = peewee.ForeignKeyField(User, backref='bot_auths')
    chat_id: int = peewee.BigIntegerField()
    password: int = peewee.IntegerField()
    created_at: datetime = peewee.DateTimeField(default=datetime.utcnow)

    class Meta:
        table_name = 'email_auth_data'
        database = database


class Coworking(peewee.Model):
    id: str = peewee.CharField(max_length=32, primary_key=True)
    avatar: str = peewee.CharField(max_length=64)
    title = peewee.CharField(max_length=128, null=False)
    institute: str = peewee.CharField(max_length=128, null=False)
    description: str = peewee.CharField(max_length=1024, null=False)
    address: str = peewee.CharField(max_length=128, null=False)

    class Meta:
        table_name = 'coworking_places'
        database = database


class CoworkingSeat(peewee.Model):
    id: int = peewee.IntegerField(primary_key=True)
    coworking: Coworking = peewee.ForeignKeyField(Coworking, backref='seats')
    label: Optional[str] = peewee.CharField(max_length=64, null=True)
    description: str = peewee.CharField(max_length=1024, null=False)
    place_type: str = peewee.CharField(max_length=32, null=False)
    seats_count: int = peewee.SmallIntegerField()

    class Meta:
        table_name = 'coworking_seats'
        database = database


class Reservation(peewee.Model):
    id = peewee.BigIntegerField(primary_key=True)
    user: User = peewee.ForeignKeyField(User, backref='user_bookings')
    seat: CoworkingSeat = peewee.ForeignKeyField(CoworkingSeat, backref='seat_booking')
    session_start = peewee.DateTimeField(null=False)
    session_end = peewee.DateTimeField(null=False)
    status: str = peewee.CharField(null=False)
    created_at: datetime = peewee.DateTimeField(default=datetime.utcnow)

    class Meta:
        table_name = 'seats_reservations'
        database = database
