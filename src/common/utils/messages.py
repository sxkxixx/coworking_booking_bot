from enum import Enum


class StartMessages(Enum):
    NOT_AUTH_MESSAGE: str = (
        """Здравствуйте, приветствуем Вас в боте сервиса онлайн бронирования коворкингов УрФУ.\n"""
        """Пожалуйста, введите почту, под который Вы регистрировались в сервисе - это требуется """
        """для аутентификации Вас в системе 🔥"""
    )

    USER_AUTHORIZED_MESSAGE: str = (
        """Здравствуйте, %s, рады снова видеть вас в системе! Вы уже авторизованы в нашей боте."""
    )