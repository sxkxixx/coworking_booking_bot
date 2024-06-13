import datetime

MONTH_GENITIVE_CASE = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря"
}


def extract_time_from_dt(dt: datetime.datetime) -> str:
    """
    Возвращает форматированную строку в формате ЧЧ:ММ
    :rtype: str
    """
    return dt.strftime("%H:%M")


def get_formatted_dt(dt: datetime.datetime) -> str:
    """
    Возвращает форматированную строку в формате "<Число> <Месяц>, ЧЧ:ММ"
    :param dt:
    :return: str
    """
    return f"{dt.day} {MONTH_GENITIVE_CASE[dt.month]}, {extract_time_from_dt(dt)}"
