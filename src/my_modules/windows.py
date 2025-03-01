from winsound import Beep as WinBeep


def Beep(frequency: int = 1000, duration: float = 1) -> None:
    """A wrapper around Windows Beep API.

    Args:
        frequency (int): Frequency of sound in hertz. Must be in range 37 through 32,767. Defaults to 1000 hertz.
        duration (float): How long the sound should play, in seconds. Defaults to 1 seconds.
    """
    duration_in_ms = int(duration * 1_000)
    WinBeep(frequency, duration_in_ms)
