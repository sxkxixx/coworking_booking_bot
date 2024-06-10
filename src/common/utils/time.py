import datetime


def get_formatted_datetime(dt: datetime.datetime) -> str:
    """
    Возвращает форматированную строку в формате ЧЧ:ММ
    :rtype: str
    """
    return dt.strftime("%H:%M")
