from typing import Any

from rich.console import Console

__all__ = ["console", "log"]


# common console for all rich printing
console: Console = Console(highlight=False)


class log:
    """Logger methods."""

    @staticmethod
    def info(msg: Any) -> None:
        """Log info message."""
        console.print(f" [[blue]INFO[/]] : {msg}")

    @staticmethod
    def warn(msg: Any) -> None:
        """Log warning message."""
        console.print(f" [[yellow]WARN[/]] : {msg}")

    @staticmethod
    def error(msg: Any) -> None:
        """Log error message."""
        console.print(f"[[red]ERROR[/]] : {msg}")
