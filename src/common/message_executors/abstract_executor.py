import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage

from infrastructure.settings import SMTPSettings


class AbstractExecutor(ABC):
    def __init__(self, settings: SMTPSettings):
        self.settings = settings

    @abstractmethod
    async def execute(self, **kwargs) -> None:
        raise NotImplementedError()

    async def send_message(self, message: EmailMessage) -> None:
        with smtplib.SMTP_SSL(
                host=self.settings.SMTP_SERVER, port=self.settings.SMTP_PORT
        ) as connection:
            connection.login(
                user=self.settings.SMTP_EMAIL,
                password=self.settings.SMTP_PASSWORD
            )
            connection.send_message(message)
