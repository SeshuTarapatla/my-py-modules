from datetime import datetime
from time import sleep

__all__ = ["wait_in_loop"]


def wait_in_loop(
    started_at: datetime,
    wait: float = 10,
    buffer: float = 1,
    err_msg: str = "Loop timeout",
) -> None:
    """Helper function to wait in a synchronous loop.

    Args:
        started_at (datetime): loop started at.
        wait (float, optional): wait till, in seconds. Defaults to 10.
        buffer (float, optional): sleep between next check, in seconds. Defaults to 1.
        err_msg (str, optional): timeout error message. Defaults to "Loop timeout".

    Raises:
        TimeoutError: _description_
    """
    if (datetime.now() - started_at).seconds >= wait:
        raise TimeoutError(err_msg)
    sleep(buffer)
