import logging
from typing import Literal, Text, cast

from rich.console import Console, ConsoleRenderable
from rich.logging import RichHandler
from rich.traceback import install

__all__ = ["log", "console", "get_rich_logger"]


class CustomRichHandler(RichHandler):
    def render_message(self, record: logging.LogRecord, message: Text) -> ConsoleRenderable:
        renderable_message = cast(ConsoleRenderable, message)
        return renderable_message

def get_rich_logger(
    name: str | None = None,
    level: Literal["debug", "info", "warning", "error", "critical"] = "debug",
    console: Console | None = None,
    rich_tracebacks: bool = True,
    show_locals: bool = True,
) -> logging.Logger:
    """Create a rich logger instance."""
    if rich_tracebacks:
        install(show_locals=show_locals, console=console)
    match level:
        case "debug":
            log_level = logging.DEBUG
        case "info":
            log_level = logging.INFO
        case "warning":
            log_level = logging.WARNING
        case "error":
            log_level = logging.ERROR
        case "critical":
            log_level = logging.CRITICAL
        case _:
            raise AttributeError(
                f"Invalid log level. Choices: [debug, info, warning, error, critical]. Passed: {level}"
            )
    # logger init
    logger: logging.Logger = logging.getLogger(name=name)
    logger.setLevel(level=log_level)
    # rich handler
    rich_handler: RichHandler = CustomRichHandler(
        console=console, show_time=False, markup=True
    )
    # inject handler
    rich_handler.setLevel(level=log_level)
    logger.addHandler(rich_handler)
    # return logger
    return logger


# default logger
console = Console()
log = get_rich_logger(console=console)


if __name__ == "__main__":
    # sample log messages
    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.critical("This is a critical message.")
