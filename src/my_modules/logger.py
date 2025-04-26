from typing import Any
from rich.console import Console

__all__ = ["console", "log"]


# common console for all rich priting
console = Console(highlight=False)


class log:
    """Logger methods"""
    @staticmethod
    def info(msg: Any) -> None:
        console.print(f" [[blue]INFO[/]] : {msg}")

    @staticmethod
    def warn(msg: Any) -> None:
        console.print(f" [[yellow]WARN[/]] : {msg}")

    @staticmethod
    def error(msg: Any) -> None:
        console.print(f"[[red]ERROR[/]] : {msg}")
