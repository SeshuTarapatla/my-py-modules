from datetime import datetime
from time import sleep


def wait_in_loop(
    started_at: datetime,
    buffer: float = 1,
    wait_limit: float = 60,
    err_message: str = "",
) -> None:
    """Helper function used to wait in indefinite loops.

    Args:
        started_at (datetime): Loop started at.
        buffer (float, optional): Sleep buffer between iteration in seconds. Defaults to 1.
        wait_limit (float, optional): Wait max limit in seconds. Defaults to 60.
        err_message (str, optional): Timeout Exception message. Defaults to "".

    Raises:
        TimeoutError: If loop is stuck beyond max wait limit.
    """    
    sleep(buffer)
    if (datetime.now() - started_at).seconds >= wait_limit:
        raise TimeoutError(err_message)
