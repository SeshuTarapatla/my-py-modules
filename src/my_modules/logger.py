from functools import wraps
from typing import Any, Callable

from rich.console import Console

__all__ = ["console", "log"]


# Common console for all rich printing
console = Console()


def status_decorator(message: str) -> Callable:
    """A status decorator that prints rich.status while a function is getting executed.

    Args:
        message (str): Status messsage.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with console.status(message):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


class log:
    """Log methods"""
    
    @staticmethod
    def info(message: str | Any) -> None:
        """Log info message."""
        console.print(f"[[blue]INFO[/]]  : {message}")

    @staticmethod
    def warn(message: str | Any) -> None:
        """Log warning message."""
        console.print(f"[[yellow]WARN[/]]  : {message}")

    @staticmethod
    def error(message: str | Any) -> None:
        """Log warning message."""
        console.print(f"[[red]Error[/]] : {message}")
