from datetime import datetime
from adbutils import adb
from adbutils._device import AdbDevice  # type: ignore
from uiautomator2 import Device as _Device

from my_modules.process import wait_in_loop


class Device(_Device):
    """Class that extends uiautomator2 Device class functionality."""

    def __init__(self, serial: str = ""):
        """Init ADB device with serial.

        Args:
            serial (str, optional): ADB Device serial. Defaults to "".
        """        
        self.serial = serial
        self.adb: AdbDevice = adb.device(serial)
    
    def init(self) -> None:
        """Lazy init to handle emulator boot up."""
        started_at = datetime.now()
        while not (self.adb.getprop("sys.boot_completed") == "1" and self.adb.getprop("init.svc.bootanim") == "stopped"):
            wait_in_loop(started_at, err_message="Emulator not booted")
        super().__init__(self.serial)
        
