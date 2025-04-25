from datetime import datetime
from subprocess import DEVNULL, STARTF_USESHOWWINDOW, STARTUPINFO, SW_HIDE, Popen
from time import sleep

from win10toast import ToastNotifier


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

def windows_notify(title: str = "Python", msg: str = "Notification") -> None:
    ToastNotifier().show_toast(title, msg, threaded=True)
    