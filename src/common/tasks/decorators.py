import asyncio
import logging
from functools import wraps
from typing import Callable, Optional

log = logging.getLogger(__name__)


def periodic_task_run(sleep: Optional[int] = None):
    """Декоратор, который запускает периодическую задачу"""

    def _periodic_task_run(coro: Callable):
        @wraps(coro)
        async def _wrapper(*args, **kwargs):
            async def run(*_args, **_kwargs) -> None:
                try:
                    log.info(f'Launch {coro.__name__} task')
                    await coro(*_args, **_kwargs)
                    log.info(f'{coro.__name__} successfully ends')
                except Exception as exc:
                    log.exception(f'{coro.__name__} exc = %s', exc)
            if not sleep:
                await run(*args, **kwargs)
                return

            log.info(f"Initialize a background task {coro.__name__}")
            while True:
                await run(*args, **kwargs)
                await asyncio.sleep(sleep)

        return _wrapper
    return _periodic_task_run
