from email.message import EmailMessage

from jinja2 import Environment

from infrastructure.settings import SMTPSettings
from .abstract_executor import AbstractExecutor


class PasswordMessageExecutor(AbstractExecutor):
    template_name = "one_time_password.html"

    def __init__(
            self,
            settings: SMTPSettings,
            jinja_env: Environment,

    ):
        super().__init__(settings)
        self.jinja_env = jinja_env

    subject = "Авторизация. Сервис бронирования коворкингов УрФУ"

    async def execute(self, receiver: str, password: int) -> None:
        message = EmailMessage()
        message["From"] = self.settings.SMTP_EMAIL
        message["To"] = receiver
        message["Subject"] = self.subject
        message.set_content(await self.render_template(password=password), subtype="html")
        await self.send_message(message)

    async def render_template(self, **kwargs) -> str:
        template = self.jinja_env.get_template(self.template_name)
        return await template.render_async(**kwargs)
