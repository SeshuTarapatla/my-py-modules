from datetime import datetime

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)

from my_modules.logger import console

__all__ = ["now", "progress_bar"]


def now() -> datetime:
    """Alias function for datetime now without microseconds"""
    return datetime.now().replace(microsecond=0)

def progress_bar() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed:.0f}/{task.total:.0f}"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    )