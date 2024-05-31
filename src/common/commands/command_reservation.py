from typing import Optional

from aiogram import Bot
from aiogram.filters import Command, CommandObject
from aiogram.utils.magic_filter import MagicFilter


class ReservationCommand(Command):
    def __init__(
            self,
            ignore_case: bool = False,
            ignore_mention: bool = False,
            magic: Optional[MagicFilter] = None,
    ):
        super().__init__(
            "reservation",
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
            magic=magic,
        )

    def __str__(self) -> str:
        return self._signature_to_string(
            ignore_case=self.ignore_case,
            ignore_mention=self.ignore_mention,
            magic=self.magic,
        )

    async def parse_command(self, text: str, bot: Bot) -> CommandObject:
        """
        Extract command from the text and validate

        :param text:
        :param bot:
        :return:
        """
        command = self.extract_command(text)
        self.validate_prefix(command=command)
        await self.validate_mention(bot=bot, command=command)
        command = self.validate_command(command)
        command = self.do_magic(command=command)
        return command  # noqa: RET504
