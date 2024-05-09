import datetime


def get_yekaterinburg_dt() -> datetime:
    tz = datetime.timezone(offset=datetime.timedelta(hours=+5))  # Yekaterinburg Time Zone
    return datetime.datetime.now(tz)


def get_formatted_datetime(dt: datetime.datetime) -> str:
    """
    Возвращает форматированную строку в формате ЧЧ:ММ
    :rtype: str
    """
    return f'{dt.hour}:{dt.minute}'
