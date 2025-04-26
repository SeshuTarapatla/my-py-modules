from datetime import datetime
from subprocess import DEVNULL, STARTF_USESHOWWINDOW, STARTUPINFO, SW_HIDE, Popen
from time import sleep

__all__ = ["wait_in_loop", "spawn_windows_process"]


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


def spawn_windows_process(
    cmd: str, title: str = "", minimized: bool = False
) -> Popen[bytes]:
    """Spawn the given windows process in a new shell.

    Args:
        cmd (str): command arguments in a string.
        title (str, optional): title of the console. Defaults to "".
        minimized (bool, optional): minimize the console window. Defaults to False.

    Returns:
        Popen[bytes]: subprocess.Popen object
    """
    startupinfo = STARTUPINFO()
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = SW_HIDE
    args = " ".join(["start", f'"{title}"', ("/min" if minimized else ""), cmd])
    process = Popen(
        args=args, shell=True, stdout=DEVNULL, stderr=DEVNULL, startupinfo=startupinfo
    )
    return process
