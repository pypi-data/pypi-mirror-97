from logging import Formatter, StreamHandler, getLogger, Logger, INFO


_handler = StreamHandler()


class LogLevel:
    _log_level: int = INFO

    @classmethod
    def set(cls, level: int):
        cls._log_level = level

    @classmethod
    def get(cls) -> int:
        return cls._log_level


class LogFormatter:
    _formatter: Formatter = Formatter("%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s")

    @classmethod
    def set(cls, formatter: Formatter):
        cls._formatter = formatter

    @classmethod
    def get(cls) -> Formatter:
        return cls._formatter


def create_logger(name: str) -> Logger:
    global _handler

    _handler.setFormatter(LogFormatter.get())
    logger = getLogger(name)
    logger.addHandler(_handler)
    logger.setLevel(LogLevel.get())

    return logger
