import logging


def configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s"
    )
