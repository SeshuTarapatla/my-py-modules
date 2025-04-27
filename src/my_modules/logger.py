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
        console.print(f" [[blue]INFO[/]] : {log._handle_new_lines(msg)}")

    @staticmethod
    def warn(msg: Any) -> None:
        """Log warning message."""
        console.print(f" [[yellow]WARN[/]] : {log._handle_new_lines(msg)}")

    @staticmethod
    def error(msg: Any) -> None:
        """Log error message."""
        console.print(f"[[red]ERROR[/]] : {log._handle_new_lines(msg)}")
    
    @staticmethod
    def _handle_new_lines(msg: Any) -> str:
        """Handle any starting newlines before logging. Ex: '\\nHello world'"""
        msg = str(msg)
        i = 0
        for i, newline in enumerate(msg):
            if newline == "\n":
                print(newline)
            else:
                break
        return msg[i:]
