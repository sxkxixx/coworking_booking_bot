from abc import ABC, abstractmethod
from typing import Callable


class AbstractTask(ABC):
    @abstractmethod
    def task(self) -> Callable:
        raise NotImplementedError()
