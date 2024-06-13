from abc import ABC, abstractmethod


class HelpMenuMixin(ABC):
    @property
    @abstractmethod
    def command(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError()
