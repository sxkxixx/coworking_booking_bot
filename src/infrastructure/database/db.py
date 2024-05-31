import peewee_async

from infrastructure.settings import DatabaseSettings

db_settings = DatabaseSettings()

database = peewee_async.PostgresqlDatabase(
    database=db_settings.DATABASE_NAME,
    user=db_settings.DATABASE_USER,
    password=db_settings.DATABASE_PASSWORD,
    host=db_settings.DATABASE_HOST,
    port=db_settings.DATABASE_PORT
)
manager = peewee_async.Manager(database)
