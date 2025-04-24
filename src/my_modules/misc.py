from datetime import datetime


def now() -> datetime:
    """Alias function for datetime now without microseconds"""
    return datetime.now().replace(microsecond=0)
